import sys
import numpy as np

def find_interval(interval, vector):
    no_in_int = int(np.ceil(len(vector) * (1 - interval) / 2))

    sorted_v = sort(vector)

    LB = sorted_v[no_in_int - 1]
    UB = sorted_v[-no_in_int]

    return LB, UB

def sort(vector):
    """
    a quick sort function to sort elements in a vector so that intervals can
    be found on them
    """

    vector = [num for num in vector]

    pivot = vector[0]

    low_list = []
    high_list = []
    
    for i in vector[1:]:
        if i <= pivot:
            low_list.append(i)
        
        else:
            high_list.append(i)


    if low_list != []:
        low_list = sort(low_list)

    if high_list != []:
        high_list = sort(high_list)

    new_list = low_list + [pivot] + high_list

    return new_list
    
sys.setrecursionlimit(200000)
#print(sort(np.array([np.random.random() for i in range(20)])))

if __name__ == "__main__":


    print(find_interval(0.99, np.arange(1, 10000)))
