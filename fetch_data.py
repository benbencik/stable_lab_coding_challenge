import json
import os
import requests
import argparse
import time

# Configuration
SNAPSHOT_API = "https://hub.snapshot.org/graphql"
AAVE_SPACE = "aave.eth"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

query_proposals = """
query Proposals($space: String!, $first: Int!, $skip: Int!) {
  proposals(first: $first, skip: $skip, where: { space: $space, state: "closed" }) {
    id
    title
    choices
    scores
  }
}
"""

query_votes = """
query Votes($proposal: String!) {
  votes(first: 1000, where: { proposal: $proposal }) {
    voter
    choice
  }
}
"""


def check_response(response):
    """Check if the API response is valid."""
    if response.status_code != 200:
        print("Error fetching data from API.")
        print("API response:", response.text)
        exit()
    return response.json()


def fetch_proposals(first, skip=0):
    """Fetch proposals from the Snapshot API."""
    response = requests.post(
        SNAPSHOT_API,
        json={
            "query": query_proposals,
            "variables": {"space": AAVE_SPACE, "first": first, "skip": skip},
        },
    )
    data = check_response(response)
    return data["data"]["proposals"]


def fetch_votes(proposal_id):
    """Fetch votes for a specific proposal."""
    response = requests.post(
        SNAPSHOT_API,
        json={"query": query_votes, "variables": {"proposal": proposal_id}},
    )
    data = check_response(response)
    return data["data"]["votes"]


def save_to_file(filename, data):
    """Save data to a JSON file."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filepath}")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Fetch proposals and votes from Snapshot API."
    )
    parser.add_argument(
        "--first",
        type=int,
        default=1000,
        help="Number of proposals to fetch (default: 100)",
    )
    parser.add_argument(
        "--skip", type=int, default=0, help="Number of proposals to skip (default: 0)"
    )
    args = parser.parse_args()

    # Fetch proposals
    proposals = fetch_proposals(first=args.first, skip=args.skip)
    save_to_file("proposals.json", proposals)

    # Fetch votes for each proposal
    for proposal in proposals:
        proposal_id = proposal["id"]
        votes = fetch_votes(proposal_id)

        proposal = {
            "proposal_id": proposal_id,
            "title": proposal["title"],
            "choices": proposal["choices"],
            "scores": proposal["scores"],
            "votes": votes,
        }

        save_to_file(f"{proposal_id}.json", proposal)

        # Add a delay to respect API rate limits
        time.sleep(0.5)


if __name__ == "__main__":
    main()
