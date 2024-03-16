import csv
import time
import json
import pandas as pd


column_names= ['tconst', 'primaryTitle', 'originalTitle', 'startYear',
               'runtimeMinutes', 'genres', 'averageRating', 'numVotes', 'ordering',
               'category', 'job', 'seasonNumber', 'episodeNumber', 'primaryName', 'birthYear',
               'deathYear', 'primaryProfession']


#############################################################################################################
# Data Filtering
#############################################################################################################
def data_filtering(filelocation, num):
        
    df = pd.read_csv(filelocation, skipinitialspace=True)
    if(num==1):
        #NEED TO CODE
        df_year = df[(df['startYear'] >= 1941) & (df['startYear'] <= 1955)] 
        df_year.reset_index(drop=True).to_csv("imdb_years_df.csv", index=False)

    if(num==2):
        #NEED TO CODE
        df_genres = df[(df['genres'] == 'Adventure') | (df['genres'] == 'Drama')]
        df_genres.reset_index(drop=True).to_csv("imdb_genres_df.csv", index=False)

    if(num==3):
        #NEED TO CODE
        profession_list = ['assistant_director', 'casting_director', 'art_director', 'cinematographer']
        df_professions = df[df["primaryProfession"].str.contains("|".join(profession_list))]
        df_professions.reset_index(drop=True).to_csv("imdb_professions_df.csv", index=False)

    if(num==4):
        #NEED TO CODE
        vowels = ["A", "E", "I", "O", "U"]
        df_vowels = df[df["primaryName"].str[0].str.upper().isin(vowels)] 
        df_vowels.reset_index(drop=True).to_csv("imdb_vowel_names_df.csv", index=False)

#############################################################################################################
#Quick Sort
#############################################################################################################
def pivot_element(arr):
    pivot=None
    if len(arr) >1:
        pivot = arr[len(arr)//2]
    return pivot 

def quicksort(arr, columns):
    # If the array has only one element or is empty, it is already sorted
    if len(arr) <= 1:
        return arr

    pivot = pivot_element(arr)
    l = []
    m = []
    r = []

    for a in arr:
        for i in range(len(columns)):
            if a[columns[i]] < pivot[columns[i]]:
                l.append(a)
                break
            elif a[columns[i]] > pivot[columns[i]]:
                r.append(a)
                break
            else:
                if i == len(columns) - 1:
                    m.append(a)
                    break
            

    return quicksort(l, columns) + m + quicksort(r, columns)

#############################################################################################################
#Selection Sort
#############################################################################################################
def selection_sort(arr, columns):
    size = len(arr) 
    for i in range(size-1): 
        minimum = i 
        for j in range(i+1, size): 
            is_smaller = False 
            for col in columns:
                if arr[j][col] < arr[minimum][col]: 
                    is_smaller = True 
                    break 
                elif arr[j][col] > arr[minimum][col]: 
                    break 
            if is_smaller:
                minimum = j 
        if minimum != i: 
            arr[i], arr[minimum] = arr[minimum], arr[i] 
    return arr

#############################################################################################################
#Heap Sort
#############################################################################################################
def check_columns(arr, columns, idx, largest):
    for c in columns:
        if arr[idx][c] < arr[largest][c]:
            return False
        elif arr[idx][c] > arr[largest][c]:
            return True
    return False


def max_heapify(arr, n, i, columns):

    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and check_columns(arr, columns, left, largest):
        largest = left

    if right < n and check_columns(arr, columns, right, largest):
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, n, largest, columns)


def build_max_heap(arr, n, columns):
    # Start from the last non-leaf node and heapify all nodes in reverse order
    for i in range(n // 2 - 1, -1, -1):
        # Heapify the current node
        max_heapify(arr, n, i, columns)

def heap_sort(arr, columns):

    n = len(arr)

    build_max_heap(arr, n, columns)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]

        max_heapify(arr, i, 0, columns)

    # Return the sorted array
    return arr

#############################################################################################################
#Shell Sort
#############################################################################################################
def is_less(a, b, columns):
    for i in columns:
        if a[i] > b[i]:
            break
        elif a[i] < b[i]:
            return True
    return False


def shell_sort(arr, columns):
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and is_less(temp, arr[j - gap], columns):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        # Decrease the diff size
        gap //= 2

    # Return the sorted array
    return arr


#############################################################################################################
#Merge Sort
#############################################################################################################
def merge(left, right, columns):
    result = []
    l, r = 0,0
    while l < len(left) and r < len(right):
        left_index = left[l]
        right_index = right[r]
        flag = 0
        for i in columns:
            if left_index[i] < right_index[i]:
                flag = -1
                break
            elif left_index[i] > right_index[i]:
                flag = 1
                break
        if flag <= 0:
            result.append(left_index)
            l += 1
        else:
            result.append(right_index)
            r += 1
    result += left[l:]
    result += right[r:]

    return result

def merge_sort(data, columns):

    if len(data) <= 1:
        return data
    m = len(data) // 2
    left_arr = data[:m]
    right_arr = data[m:]
    left_sorted = merge_sort(left_arr, columns)
    right_sorted = merge_sort(right_arr, columns) 
    return merge(left_sorted, right_sorted, columns)


#############################################################################################################
#Insertion Sort
#############################################################################################################
def insertion_sort(arr, columns):
    n = len(arr)

    for i in range(1, n):
        p = arr[i]
        p_val = [p[c] for c in columns]

        j = i - 1
        while j >= 0:
            j_indx = [arr[j][c] for c in columns]
            if j_indx > p_val:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break

        arr[j + 1] = p
    return arr

#############################################################################################################
# Sorting Algorithms Function Calls
#############################################################################################################
def sorting_algorithms(file_path, columns, select):
        

    df = pd.read_csv(file_path, skipinitialspace=True)
    
    column_vals = [column_names.index(i) for i in columns]
    
    data = df.values.tolist()

#############################################################################################################
# Donot Modify Below Code
#############################################################################################################
    if(select==1):
        start_time = time.time()
        output_list = insertion_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    if(select==2):
        start_time = time.time()
        output_list = selection_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    if(select==3):
        start_time = time.time()
        output_list = quicksort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    if(select==4):
        start_time = time.time()
        output_list = heap_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    if(select==5):
        start_time = time.time()
        output_list = shell_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    if(select==6):
        start_time = time.time()
        output_list = merge_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    
