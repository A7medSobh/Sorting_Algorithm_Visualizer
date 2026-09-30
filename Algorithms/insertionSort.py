import time as t

#-----------------------------
#Insertion Sort Algorithm
#-----------------------------
def insertion_sort(arr):
    insertion_comparisons = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0:
            insertion_comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j = j - 1
            else:
                break
        arr[j + 1] = key
    return arr, insertion_comparisons


def isSorted(anArray):
    # Check if the array is sorted in ascending order
    for i in range(1, len(anArray)):
        if anArray[i - 1] > anArray[i]:
            return False

    return True



#-----------------------------
#Reading data from a txt file
#-----------------------------
def read_data(filename):
    with open(filename, 'r') as file:
        data =[int(num) for line in file for num in line.split()]
    return data


#"data/rand1000.txt"
#"data/rand10000.txt"
#"data/rand100000.txt"
#"data/rand1000000.txt"
#"data/rand250000.txt"
#"data/500000.txt"

fileNames= ["rand1000.txt", "rand10000.txt"]

for name in fileNames:
    data = read_data("data/" + name)
    #Insertion Sort
    insertion_data = data.copy()
    start_time = t.time()
    insertion_data, insertion_comparisons = insertion_sort(insertion_data)
    end_time = t.time()
    insertion_time = end_time - start_time


    #Results
    print("\nFile:", name)
    print("Insertion Sort:")
    print("Time: ", insertion_time)
    print("Comparisons:", insertion_comparisons)
    print("Sorted:", isSorted(insertion_data))