from functions import *
from GlotScript import sp
import os.path


folderPath = "vocab/"
langRuleFolderPath = "languageDividedRules/"
langs = ["English","German","French","Spanish","Italian","Russian","Japanese","Arabic"]
latinLangs = langs[:5]

data = pd.read_csv("csv_files/cleanedData.csv",index_col=False)
col = data['Description']


# makes the vocab.txt file from splitting all the rules if it hasn't been made
if os.path.isfile(folderPath+"vocab.txt"):
    f = open(folderPath+"vocab.txt","r")
    vocabList = f.read().splitlines()
    f.close()
else:
    vocabList = makeVocabList(col)
    vocabList.sort()
    f = open(folderPath+"vocab.txt", "w")
    f.write("\n".join(vocabList))
    f.close()

print("Vocab List length: "+ str(len(vocabList)))





#BELOW IS FOR MAKING VOCAB LISTS FROM TOTAL WORD LIST

for lang in latinLangs:
    # if the lists have not been made
    if(not os.path.isfile(folderPath+"this"+lang+".txt")):
        # opens the file of all vocab for the language
        f = open(folderPath+"wordlist-"+lang.lower()+".txt", "r")
        words = f.read().lower().splitlines()
        f.close()
        # goes through all vocab words and checks if in language
        myVocab = []
        for word in vocabList:
            if word in words:
                myVocab.append(word)
        # writes the vocab to an output file
        f=open(folderPath+"this"+lang+".txt","w")
        for word in myVocab:
            f.write(word+"\n")
        f.close()

# saves all the vocab lists in a single list to reference
allLatinVocabs = []
for lang in latinLangs:
    f = open(folderPath+"this"+lang+".txt", "r")
    allLatinVocabs.append(f.read().splitlines())
    f.close()

# prints the vocabs
print("Lang vocabs made:")
for vocab in allLatinVocabs:
    print(vocab[:10])



# Dividing the rules into different languages
langRules = []
for lang in langs:
    langRules.append([])
# goes through every rule
for rule in col:
    rule = str(rule)
    alpha = sp(rule)[0]
    # dividing out those that use different alphabets
    if alpha == 'Cyrl':
        langRules[langs.index("Russian")].append(rule)
    elif alpha == 'Arab':
        langRules[langs.index("Arabic")].append(rule)
    elif alpha in ['Hani', 'Hira', 'Kana', 'Hang']:
        langRules[langs.index("Japanese")].append(rule)
    # getting the latin alphabet rules
    elif alpha == 'Latn':
        # list to count number of words in the rule in each latin lang vocab list
        langCounts = [0]*len(latinLangs)
        for word in rule.split():
            # checks if the word is in each vocab list
            for i in range(len(allLatinVocabs)):
                if word in allLatinVocabs[i]:
                    langCounts[i]+=1

        # calculates the max number of words in the rule that fit one language
        maxi = max(*langCounts)
        # preferentially assigns the rule (in order: english, german, french, spanish, italian)
        for i in range(len(langCounts)):
            if langCounts[i]==maxi:
                langRules[i].append(rule)
                break

# writes the rules for each language into a file
for i in range(len(langs)):
    f=open(langRuleFolderPath+langs[i]+"Rules.txt","w")
    f.write("\n".join(langRules[i]))
    f.close()

