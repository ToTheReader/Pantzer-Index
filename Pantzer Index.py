# Parsing OCR'd text of Pantzer Index into a Python dictionary (and performing some clean up; see Jupyter Notebooks for more clean up)

import re
import os
import pprint

pantzer = {}



# define source file

with open('testocr.txt','r') as file:
    text = file.read()


# replace the low quotation mark error with '.,' (and any other global changes)

text = text.replace('„', '.,')



# split the whole file down double line breaks to create a list of printer blocks

text_split_by_printer = text.split('\n\n')



# go into each printer block and create a list divided by the date markers, e.g. '1603:'

for i in text_split_by_printer:
    printerblock_split = re.findall(r"[\w\W]+?(?=1[4|5|6]\d\d[\/\d\d]*:|\Z)", i)

    # if the result isn't empty, assign the resulting list to the dict, under the key of its name (the first line of the first item)
    
    if len(printerblock_split) > 0:
        name = re.search(r'^.+?(?=\n|\Z)', printerblock_split[0]) #this r might not be necessary
        pantzer[name.group()] = printerblock_split


# for each item, create an inner dict with 'headnote' as key and the cleaned headnote text item as the value

for k, v in pantzer.items():
    inner_dict = {}
    headnote = v[0].replace('\n', ' ')
    headnote = headnote.strip()
    inner_dict['headnote'] = headnote
    
    
#     split the other items down the colon to separate the date from the STC numbers
    
    for i in range(1, len(v)):
        dates_split = v[i].split(':')
        

#         make a list from the numbers, split down commas
        
        numbers = dates_split[1].replace('\n', ' ') # makes sure 'comma new line' is 'comma space'
        numbers = numbers.split(', ') # then split numbers by the comma
        

#       clean each value in list
        numbers = [n.replace('\t', ' ') for n in numbers]
        numbers = [n.strip() for n in numbers]
        numbers = [n.rstrip('.') for n in numbers]
        numbers = [n.rstrip(',') for n in numbers]
        


#       replace abbreviation dashes with the numbers they represent

        numbers = [n.replace('—,', '—.') for n in numbers] #standardize dashes

        for i in range(0, len(numbers)):
            if '—.' in numbers[i]:

                root_number = re.search('\d+\.', numbers[i-1]) # look in the previous list item for the root number with regex
                root_number = root_number.group() # get string
                numbers[i] = numbers[i].replace('—.', root_number) #replace dash with string        
        
        
#       assign to inner dict with the year as key
        inner_dict[dates_split[0]] = numbers
        
#   replace the current name's value with this inner dict
        
    pantzer[k] = inner_dict
