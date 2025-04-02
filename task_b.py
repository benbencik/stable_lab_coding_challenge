import json
import os

# Configuration
SNAPSHOT_API = "https://hub.snapshot.org/graphql"
AAVE_SPACE = "aave.eth"
STABLELAB_ADDRESS = "0xECC2a9240268BC7a26386ecB49E1Befca2706AC9"
WHALE_ADDRESS = "0x8b37a5Af68D315cf5A64097D96621F64b5502a22"
DATA_DIR = "data"


def load_from_file(filename):
    """Load data from a JSON file."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r") as f:
        return json.load(f)


def subtask2(proposals):
    print("SUBTASK 2", "-" * 50)
    print("In following proposals StableLab votes are opposing to whale account:")
    for proposal in proposals:
        proposal_id = proposal["id"]
        choices = proposal["choices"]

        votes = load_from_file(f"{proposal_id}.json")["votes"]

        stablelab_choice = None
        whale_choice = None

        for vote in votes:
            voter = vote["voter"]
            if voter == STABLELAB_ADDRESS:
                stablelab_choice = vote["choice"]
            elif voter == WHALE_ADDRESS:
                whale_choice = vote["choice"]

        if (
            stablelab_choice != None
            and whale_choice != None
            and (stablelab_choice != whale_choice)
            and type(stablelab_choice) == int
            and choices[stablelab_choice - 1].lower() != "abstain"
            and choices[whale_choice - 1].lower() != "abstain"
        ):
            print(f"{proposal['title']} (ID: {proposal_id})")


def subtask3(proposals):
    print("\nSUBTASK 3", "-" * 50)
    print("In following proposals StableLab voted against majority:")

    for proposal in proposals:
        proposal_id = proposal["id"]
        scores = proposal["scores"]
        choices = [i.lower() for i in proposal["choices"]]
        majority_choice = max(range(len(scores)), key=lambda i: scores[i])

        votes = load_from_file(f"{proposal_id}.json")["votes"]
        stablelab_choice = None

        for vote in votes:
            voter = vote["voter"]
            if voter == STABLELAB_ADDRESS:
                stablelab_choice = vote["choice"]
                break

        if (
            stablelab_choice
            and type(stablelab_choice) == int
            and choices[stablelab_choice - 1].lower() != "abstain"
            and stablelab_choice - 1 != majority_choice
        ):
            print(f"{proposal['title']} (ID: {proposal_id})")


def main():
    proposals = load_from_file("proposals.json")
    subtask2(proposals)
    subtask3(proposals)


if __name__ == "__main__":
    main()
