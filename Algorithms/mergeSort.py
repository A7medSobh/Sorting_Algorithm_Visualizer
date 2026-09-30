import time as t


def merge_sort_visual(arr):
    yield from merge_sort(arr, 0, len(arr) - 1)


def merge_sort(arr, start, end):

    if start >= end:
        return

    mid = (start + end) // 2

    yield from merge_sort(arr, start, mid)
    yield from merge_sort(arr, mid + 1, end)

    yield from merge(arr, start, mid, end)


def merge(arr, start, mid, end):

    left = arr[start:mid + 1]
    right = arr[mid + 1:end + 1]

    i = 0
    j = 0
    k = start

    while i < len(left) and j < len(right):

        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1

        k += 1

        # Send the current array to Pygame
        yield arr.copy()

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
        yield arr.copy()

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
        yield arr.copy()