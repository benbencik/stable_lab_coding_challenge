# Task C

In sandwitch attack a user places order right befre you and then one right after you. So the change in price that you create is exploited.

But how can the Jared know what order you want to make? Since the ledger is completely transparent, Jared can see pending orders and can identify your account. By doing this he influnces the price. If Jared manages to make an order before you be can drive the price up, so you buy more expensive and then he sells making a profit. If Jared sells a lot of the asset he can make it less valueable as you bought it.

The code for this task can be found in `task_c.py`

## Task C.1

I found the address on Etherscan and downloaded the transactions into a CSV file `jareds_transactions.csv`. We observe that the transactions are paired they are ordered so that within each pair, the first is the buy and the next is the sell. To calculate the profit for each sandwich, we take the difference in the effective prices of the buy and sell and then subtract the transaction fees. This can be expressed by formula:

`(sell price * selling amount) − (buy price * buying amount) − total fees`

For some reason I get negative profit in `task_c.py` after substracting the fees. But that would not make sense for Jared, so I am clearly missing something.

## Task C.2

Calculating the overall profit is just sum of the individual revenues and likewise the most profitable opportunity can be picked by finding max. 


## Task C.3

An attacker benefits only when the profit exceeds the gas fees. If only a small amount is traded, the price impact is minimal, and the potential profit is negligible compared to the cost of gas fees. That is why the attacker must target transactions with enough volume to cause significant price changes. The reason that Jared might be outcompeting others might simply be because of hard-ware. It is possible that Jared has really fast access and can see the pending orders faster than his competitors.