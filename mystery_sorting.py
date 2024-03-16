import pandas as pd
import os
import sys


column_names= ['tconst', 'primaryTitle', 'originalTitle', 'startYear',
               'runtimeMinutes', 'genres', 'averageRating', 'numVotes', 'ordering',
               'category', 'job', 'seasonNumber', 'episodeNumber', 'primaryName', 'birthYear',
               'deathYear', 'primaryProfession']

    
####################################################################################
# Donot Modify this Code
####################################################################################
class FixedSizeList(list):
    def __init__(self, size):
        self.max_size = size

    def append(self, item):
        if len(self) >= self.max_size:
            raise Exception("Cannot add item. List is full.")
        else:
            super().append(item)

###############################################################
#Merge Sort
################################################################
def compare(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a < b
    else:
        return str(a).strip() < str(b).strip()
    
def merge(left, right, columns):
   
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        c_res = compare(left[i][columns[1]], right[j][columns[1]])
        if c_res:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def merge_sort(data, columns):
    
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = data[:mid]
    right = data[mid:]

    left = merge_sort(left, columns)
    right = merge_sort(right, columns)
    return merge(left, right, columns)


####################################################################################
# Mystery_Function
####################################################################################
def Mystery_Function(file_path, memory_limitation, columns):
    #Load the 2000 chunck of data every time into Data Structure called List of Sublists which is named as "chuncks_2000"
    data_chunck = FixedSizeList(memory_limitation)

    output_dir = "Final"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)    

    datafile = pd.read_csv("imdb_dataset.csv", header=None, low_memory=False)
    datafile = datafile.applymap(lambda x: x.title())
    datafile = datafile.values.tolist()
    columns = ['tconst'] + columns
    vals = [column_names.index(col) for col in columns]
    datafile = merge_sort(datafile, vals)
    output_file = os.path.join(file_path, "test.csv")
    datafile = pd.DataFrame(datafile, columns=column_names)
    datafile.to_csv(output_file, index=False)

    rows = sum(1 for line in open(output_file, encoding='utf-8'))
    for i in range(0, rows, memory_limitation):
        data_chunck = pd.read_csv(file_path+"/test.csv", skiprows=i, nrows=memory_limitation, header=None)
        data = data_chunck.values.tolist()
        sorted_chunk = merge_sort(data, vals)
        sorted_datafile = pd.DataFrame(sorted_chunk, columns=column_names)
        output_file = os.path.join(output_dir, "Sorted_" + str(i // memory_limitation + 1)+ ".csv")
        if i == 0:
            sorted_datafile.to_csv(output_file, header = True, index=False)
        else:
            sorted_datafile.to_csv(output_file, header = False, index=False)
        
    temp = os.path.join(file_path, "test.csv")  
    os.remove(temp)

####################################################################################
# Data Chuncks
####################################################################################

def data_chuncks(file_path, columns, memory_limitation):

        data_chunck=FixedSizeList(memory_limitation)

        output_dir = "Individual"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        rows = sum(1 for line in open(file_path, encoding='utf-8'))
        columns = ['tconst'] + columns
        vals = [column_names.index(col) for col in columns]
        
        for i in range(0, rows, memory_limitation):
            data_chunck = pd.read_csv(file_path, skiprows=i, nrows=memory_limitation, header=None)
            data = data_chunck.values.tolist()
            sorted_chunck = merge_sort(data, vals)
            sorted_datafile = pd.DataFrame(sorted_chunck, columns=column_names)
            output_file = os.path.join(output_dir, "Sorted_" + str(i // memory_limitation + 1)+ ".csv")
            sorted_datafile.to_csv(output_file, index=False)


#Enable only one Function each from data_chuncks and Mystery_Function at a time

#Test Case 13
#data_chuncks('imdb_dataset.csv', ['startYear'], 2000)

#Test Case 14
#data_chuncks('imdb_dataset.csv', ['primaryTitle'], 2000)

#Test Case 15
data_chuncks('imdb_dataset.csv', ['startYear','runtimeMinutes' ,'primaryTitle'], 2000)


#Test Case 13
#Mystery_Function("Individual", 2000, ['startYear'])

#Test Case 14
#Mystery_Function("Individual", 2000, ['primaryTitle'])

#Test Case 15
Mystery_Function("Individual", 2000, ['startYear','runtimeMinutes' ,'primaryTitle'])
