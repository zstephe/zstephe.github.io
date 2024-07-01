from functions import *
from deep_translator import GoogleTranslator
f = open("languageDividedRules/FrenchRules.txt","r")
frenchRules = f.read().splitlines()
f.close()

#print(frenchRules[12302])
f = open("languageDividedRules/FrenchRulesTranslated.txt","a")
for sent in frenchRules[12302:]:
    print(sent)
    f.write((GoogleTranslator(source='fr',target='en').translate(sent))+"\n")

f.close()