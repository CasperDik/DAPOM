# solution 4.5
# author: Nick Szirbik
# date: 17 Sept 2020
"""
A veery limited English to Hungarian and
a Hungarian to Romanian dictionaries are created,
using the Python dictionary type dict.
Then the dictionary is used, briefly.
"""
def makeEnglishHungarianDictionary():
    hungarian = dict()
    hungarian['hello'] = ['szia', 'szervusz', 'helló']
    hungarian['yes'] = 'igen'
    hungarian['one'] = 'egy'
    hungarian['two'] = 'kettö'
    hungarian['three'] = 'három'
    hungarian['red'] = 'piros'
    hungarian['yellow'] = 'sárga'
    hungarian['green'] = 'zöld'
    hungarian['blue'] = 'kék'
    return hungarian

def makeHungarianRomanianDictionary():
    romanian = dict()
    romanian['szervusz'] = ['salut', 'hei', 'alo']
    romanian['igen'] = 'da'
    romanian['egy'] = 'unu'
    romanian['kettö'] = 'doi'
    romanian['three'] = 'trei'
    romanian['piros'] = 'roșu'
    romanian['sárga'] = 'galben'
    romanian['zöld'] = 'verde'
    romanian['kék'] = 'albastru'
    return romanian

def main():
    eng2hunDict = makeEnglishHungarianDictionary()
    countingTo3 = ['one', 'two', 'three']
    print("count in Hungarian to three:")
    for englishNo in countingTo3:
        print(eng2hunDict[englishNo])
# add new words
    eng2hunDict['four'] = 'négy'
    eng2hunDict['five'] = 'öt'

    countingTo5 = countingTo3 + ['four', 'five']

    print("count in Hungarian to five:")
    for englishNo in countingTo5:
        print(eng2hunDict[englishNo])

    hun2roDict = makeHungarianRomanianDictionary()
    romanianFlagColors = ['red', 'yellow', 'blue']
    print('RO flag colors - in Romanian:')
    for culoare in romanianFlagColors:
        print(hun2roDict[eng2hunDict[culoare]])


main()
