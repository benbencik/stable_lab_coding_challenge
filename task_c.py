import pandas as pd


def calculate_pair_profit(pair_df):
    sorted_pair = pair_df.sort_values("CurrentValue @ $1873.33355417794/Eth")
    buy = sorted_pair.iloc[0]
    sell = sorted_pair.iloc[1]

    buy_val = buy["Value_IN(ETH)"]
    sell_val = sell["Value_OUT(ETH)"]
    buy_price = buy["CurrentValue @ $1873.33355417794/Eth"]
    sell_price = sell["CurrentValue @ $1873.33355417794/Eth"]

    profit = (
        buy_val*buy_price  - sell_val*sell_price 
    )  #- buy["TxnFee(ETH)"] - sell["TxnFee(ETH)"]
    return profit, buy, sell


def main():
    csv_file = "jareds_transactions.csv"
    df = pd.read_csv(csv_file)

    df["Value_IN(ETH)"] = pd.to_numeric(df["Value_IN(ETH)"])
    df["Value_OUT(ETH)"] = pd.to_numeric(df["Value_OUT(ETH)"])
    df["CurrentValue @ $1873.33355417794/Eth"] = pd.to_numeric(
        df["CurrentValue @ $1873.33355417794/Eth"],
    )
    df["TxnFee(ETH)"] = pd.to_numeric(df["TxnFee(ETH)"])

    # Group by Blockno (each block should contain 2 transactions for a sandwich attack)
    groups = df.groupby("Blockno")

    pair_profits = []
    pair_details = []

    for block, group in groups:
        if len(group) != 2:
            continue

        profit, buy, sell = calculate_pair_profit(group)
        pair_profits.append(profit)
        pair_details.append(
            {
                "Profit(ETH)": profit,
                "Total Gas Fee (ETH)": buy["TxnFee(ETH)"] + sell["TxnFee(ETH)"],
            }
        )

    overall_profit = sum(pair_profits)
    max_idx = pair_profits.index(max(pair_profits))
    best_pair = pair_details[max_idx]

    print(f"Overall profit from all sandwiches (ETH): {overall_profit:.10f}\n")
    print("Pair with the highest single profit:")
    for key, value in best_pair.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
