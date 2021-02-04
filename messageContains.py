import re
import dice

def findQuotedText(text:str):
    return re.findall(r'\"([^\"]+?)\"', text)

def textSpaceReplace(text:str,replaceWith:str='[- ]?'):
    return text.replace(" ",replaceWith)

def search(text:str,phrase:str,wordsOnSide:int=2):
    '''Searches for text, and retrieves n words either side of the text, which are retuned seperatly'''
    between0AndNWords = '{' + f',{wordsOnSide}' + '}'
    phraseSpaceReplace = textSpaceReplace(phrase,'[- ]?')
    return re.findall(r"(?:[a-z']+\s){}{}(?:\s[a-z']+){}".format(between0AndNWords,phraseSpaceReplace,between0AndNWords), text, re.IGNORECASE)

def markSpokenPhrase(msg:str,,phrase:str,diceN:int=20):
    s = ''
    for quote in findQuotedText(msg):
        for ref in search(quote,phrase,4):
            s = f'{s}\n({dice.nSidedDie(diceN)}/{diceN}) :: {ref}'
    return s
