def bubble_sort(array):
    length = len(array)
    if length < 2:
        return array
    else:
        for i in range(length - 1):
            for j in range(length - 1 - i):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
        return array


def quick_sort(array):
    length = len(array)
    if length < 2:
        return array
    else:
        base_value = array[0]
        small, equal, big = [], [base_value], []
        for i in array[1:]:
            if i > base_value:
                big.append(i)
            elif i < base_value:
                small.append(i)
            else:
                equal.append(i)
        return quick_sort(small) + equal + quick_sort(big)


def search_sort(array):
    length = len(array)
    if length < 2:
        return array
    else:
        for i in range(length):
            base_index = i
            for j in range(i, length):
                if array[j] < array[base_index]:
                    base_index = j
            if base_index != i:
                array[base_index], array[i] = array[i], array[base_index]
        return array


def insert_sort(array):
    length = len(array)
    if length < 2:
        return array
    else:
        for i in range(length):
            for j in range(i, 0, -1):
                if array[j] < array[j - 1]:
                    array[j], array[j - 1] = array[j - 1], array[j]
        return array


if __name__ == '__main__':
    list_a = [1, 5, 9, 6, 4, 5, 10]
    print(list_a)
    list_b = insert_sort(list_a)
    print(list_b)
