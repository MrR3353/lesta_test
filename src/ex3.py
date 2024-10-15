# +: быстро работает с маленьким диапазоном чисел и большим массивом
# -: требует много памяти для больших диапазонов и снижается скорость работы
# -: все еще медленее чем стандартная сортировка Timsort
def counting_sort(lst):
    mn = min(lst)
    mx = max(lst)
    a = [0] * (mx - mn + 1)
    for i in lst:
        a[i - mn] += 1
    result = []
    for i in range(len(a)):
        for j in range(a[i]):
            result.append(i + mn)
    return result


def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = abs(arr[i]) // exp % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = abs(arr[i]) // exp % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]


# +: быстрее чем counting_sort работает на больших диапазонах чисел
# -: все еще медленее чем стандартная сортировка Timsort
def radix_sort(arr):
    arr = arr.copy()
    negatives = [-num for num in arr if num < 0]
    positives = [num for num in arr if num >= 0]

    if positives:
        max_val = max(positives)
    else:
        max_val = 0

    if negatives:
        max_neg_val = max(negatives)
    else:
        max_neg_val = 0

    exp = 1
    while max_val // exp > 0:
        counting_sort_for_radix(positives, exp)
        exp *= 10

    exp = 1
    while max_neg_val // exp > 0:
        counting_sort_for_radix(negatives, exp)
        exp *= 10

    negatives = [-num for num in reversed(negatives)]
    arr[:] = negatives + positives
    return arr

