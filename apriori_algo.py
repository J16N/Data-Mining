from itertools import count
from collections import Counter

def cartesian_product(items, n_set):
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
        item_group = items[i]

        for j in range(i + 1, len(items)):
            s = set(item_group).union(items[j])

            if len(s) == n_set:
                yield ''.join(s)



transactions = [
    {'A', 'B', 'D'},        # Transaction 1
    {'A', 'B'},             # Transaction 2
    {'B', 'C', 'D'},        # Transaction 3
    {'B', 'E'},             # Transaction 4
    {'B'},                  # Transaction 5
    {'A', 'C', 'D', 'E'},   # Transaction 6
    {'A', 'C', 'D', 'E'}    # Transaction 7
]
L = set()
min_support = 0.3
frequencies = Counter()
items = ('A', 'B', 'C', 'D', 'E')


for n_set in count(start=1):
    for transaction in transactions:
        for item_group in items:
            # if all the item in the item group is in the transaction
            if (all(item in transaction for item in item_group)):
                frequencies[item_group] += 1

    support = {item_group: frequencies[item_group] / len(transactions)  for item_group in items}
    # Get items whose value is greater than or equal to the minimum support
    L_temp = tuple(item_group for item_group in support if support[item_group] >= min_support)
    frequencies.clear()    # Clear the `frequencies` to save memory

    if (not L_temp):       # If `L_temp` is empty, break out of the loop
        break

    L = L.union(L_temp)
    items = tuple(cartesian_product(L_temp, n_set + 1))


print(*L, sep='\n')