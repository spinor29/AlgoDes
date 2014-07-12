# Mergesort algorithm

def mergesort(numbers):
    n = len(numbers)
    m1 = n/2
    m2 = n - m1
    
    if len(numbers) == 1:
        return numbers
    else: # divide into two parts
        numbers1 = mergesort(numbers[:m1])
        numbers2 = mergesort(numbers[m1:n])
    numbers_new = []

    i = 0
    j = 0
    
    while i < len(numbers1):
        while j < len(numbers2):
            if i != len(numbers1):
                if (numbers1[i] < numbers2[j]):
                    numbers_new.append(numbers1[i])
                    i += 1
                else:
                    numbers_new.append(numbers2[j])
                    j += 1
            else:
                numbers_new.append(numbers2[j])
                j += 1
        if i != len(numbers1):
            numbers_new.append(numbers1[i])
            i += 1
                               
    return(numbers_new)
    

def solve_it(input_data):
    lines = input_data.split('\n')
    lines.remove("")
    num_count = len(lines)
    integers = []
    # Store input integers in a list
    for i in range(num_count):
        integers.append(int(lines[i]))
 
    new_integers = mergesort(integers)
    print new_integers

import sys
#sys.setrecursionlimit(200000)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print 'Solving:', file_location
        solve_it(input_data)
    else:
        print 'This test requires an input file.'


