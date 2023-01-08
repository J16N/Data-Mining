from itertools import count
from collections import Counter
from collections.abc import Generator, Iterable

def cartesian_product(items: Iterable[str], n_set: int) \
        -> Generator[str, None, None]:
    """
    This function returns the cartesian product
    of the items with itself. The n_set is used 
    to determine the total length of each element
    in the resulting set.

    ----------
    Parameters
    ----------
    items: List of items
    n_set: A positive integer

    -------
    Returns
    -------
    This is a generator function that yields each
    element for the resulting set.
    """
    
    for i in range(len(items) - 1):
        item_group: str = items[i]

        for j in range(i + 1, len(items)):
            s: set = set(item_group).union(items[j])

            if (len(s) == n_set):
                yield ''.join(sorted(s))


def get_freq(items: Iterable[str], transactions: list[set[str]], 
             frequencies: Counter) -> None:
    for transaction in transactions:
        for item_group in items:
            # if all the item in the item group is in 
            # the transaction
            if (all(item in transaction for item in item_group)):
                frequencies[item_group] += 1


def apriori(items: Iterable[str], transactions: list[set[str]], 
            min_support: float) -> dict:
    L: dict = {}
    frequencies: Counter = Counter()

    for n_set in count(start=1):
        get_freq(items, transactions, frequencies)
        support: dict = {
            item_group: frequencies[item_group] / len(transactions)  
            for item_group in items
        }
        # Get items whose value is greater than or 
        # equal to the minimum support
        L_temp: dict = {
            item_group: support[item_group] 
            for item_group in support 
            if support[item_group] >= min_support
        }
        # Clear the `frequencies` to save memory
        frequencies.clear()
        # If `L_temp` is empty, break out of the loop
        if (not L_temp):
            break

        L: dict = {**L, **L_temp}
        items: set = set(cartesian_product(tuple(L_temp.keys()), n_set + 1))

    return L


def get_rules(itemsets: dict, conf_lvl: float) \
        -> list[tuple[str, str, float]]:
    rules = []
    item_groups = tuple(itemsets.keys())
    N = len(item_groups)

    for i in range(N - 1):
        X: str = item_groups[i]
        
        for j in range(i, N):
            Y: str = item_groups[j]
            if (len(set(X) & set(Y)) != 0): continue
            item_group: str = ''.join(sorted(set(X) | set(Y)))
            if (itemsets.get(item_group) is None): continue

            conf_x_y: float = itemsets[item_group] / itemsets[X]
            conf_y_x: float = itemsets[item_group] / itemsets[Y]

            if (conf_x_y >= conf_lvl): rules.append((X, Y, conf_x_y))
            if (conf_y_x >= conf_lvl): rules.append((Y, X, conf_y_x))

    return rules


if __name__ == "__main__":
    transactions = [
        {'A', 'C', 'E'},        # Transaction 1
        {'C', 'E', 'F'},        # Transaction 2
        {'A', 'B', 'G'},        # Transaction 3
        {'A', 'D'},             # Transaction 4
        {'C', 'E', 'F', 'G'}    # Transaction 5
    ]
    min_support = 0.3
    frequencies = Counter()
    items = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    result = apriori(items, transactions, min_support)

    for k, v in result.items():
        print(f"{k} = {v}")