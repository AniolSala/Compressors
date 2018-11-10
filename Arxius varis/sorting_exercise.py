import matplotlib.pyplot as plt
import numpy as np

# In[1]

# Files:
file1 = open('C:/Users/Aniol/WPy-3661/Arxius py/Exercicis/sometext.txt')
file2 = open('C:/Users/Aniol/WPy-3661/Arxius py/Exercicis/LICENSE.txt')
file3 = open('C:/Users/Aniol/WPy-3661/Arxius py/Exercicis/ipsum_text.txt')
file4 = open(
    'C:/Users/Aniol/WPy-3661/Arxius py/Exercicis/Bible_King_James_Version.txt')
file5 = open('C:/Users/Aniol/WPy-3661/Arxius py/Exercicis/Quijote_1.txt')


def countWords(*files):
    '''We will create the dictionary with the keys being the
    characters in the text and the values being the number
    that each craracter appears. We will return de sorted
    dictionary'''
    strfile = ''
    for file in files:
        strfile += file.read().replace(' ', '').replace('\n', '')

    dict = {}
    for char in strfile:
        if char in dict:
            dict[char] += 1
        else:
            dict[char] = 1
        i += 1
    # Sorting from hight to low:
    sval = np.sort(np.array([val for val in dict.values()]))[::-1]
    sortDict = {}
    for val in sval:
        for key in dict:
            if dict[key] == val:
                sortDict[key] = val

    return sortDict


parsing = countWords(file5)
klist = [key for key in parsing]
vlist = np.array([val for val in parsing.values()])

fig = plt.figure(figsize=(15, 5))
plt.plot(klist, vlist / np.sum(vlist), 'o-')
plt.title('Character probability distribution of the holy bible')
plt.xlabel('Characters')
plt.ylabel('Probability of character appearence')
plt.show()


# In[2]


# In[3]


def compareDicts(dict1, dict2):
    '''Given dict1, we will sort the keys for dict2 to be in the
    same order as dict1.'''

    sortDict2 = {}
    # We sort now the common keys.
    for key in dict1:
        if key in dict2:
            sortDict2[key] = dict2[key]
    # We put the non-common keys.
    for key in dict2:
        if key not in dict1:
            sortDict2[key] = dict2[key]
    return sortDict2
