import os
import nltk
import re
from nltk import WordNetLemmatizer, word_tokenize
nltk.download('punkt')
nltk.download('wordnet')

dirPath = "corpus"  #directory that corpus is in

# Get all words from corpus and put them in a list
def splitCorpus():
    splcor = []         #final list to be returned

    #for loop to count files in corpus
    for x in os.listdir(dirPath):
        if x.endswith(".txt"):
            file = f"{dirPath}\{x}"
            f = open(file, "r", encoding="utf8")
            splcor += word_tokenize(f.read())

    return splcor

lem = WordNetLemmatizer()

#Normalize the corpus
def normalizeCorpus(splcor):
    norcor = []     #normalized corpus
    punc = r'[:?.,!"”“\$()]'
    for x in splcor:
        if not re.search(punc, x):  #trims out punctuation
            norcor.append(lem.lemmatize(x.lower()))

    return norcor

#build the positional index
def buildIndex(norcor):
    invIndex = []   #inverted index
    postingList = [] #posting list
    ind = 0 #counting index

    #loop through words in dictionary
    for word in norcor:
        if word not in invIndex:
            invIndex.append([word, [] ])
            print("indexing term: " + str(word))
        #loop through documents
        for x in os.listdir(dirPath):
            if x.endswith(".txt"):
                file = f"{dirPath}\{x}"
                f = open(file, "r", encoding="utf8")
                #search document for terms
                for l in word_tokenize(f.read()):
                    if lem.lemmatize(l.lower()) == word:
                        postingList.append(int(x.removesuffix(".txt"))) #add doc id to posting list
                        break   #word found, move on to next document
        invIndex[ind][1] = postingList  #assign posting list to term
        postingList = [] #wipe temporary posting list
        ind += 1

    print("indexing complete!")
    return invIndex

#prints inverted index
def printInvertedIndex(index):
    for x in range(len(index)):
        print(index[x][0] + ": " + str(index[x][1]))

#intersection algorithm
#where index is the inverted index
#       q1 is the first term
#       q2 is the second term
#returns posting list that has both q1 and q2
def intersectLists(index, q1, q2):
    answer = []

    #get postings list of queries
    for x in range(len(index)):
        if q1 == index[x][0]:
            i1 = x
        if q2 == index[x][0]:
            i2 = x

    #start at first document
    #p1 = index[i1][1][0]
    #p2 = index[i2][1][0]
    p1 = 0
    p2 = 0

    while p1 < len(index[i1][1]) and p2 < len(index[i2][1]):    #3d arrays make me sad
        #get doc ID
        x1 = index[i1][1][p1]
        x2 = index[i2][1][p2]

        #if doc id's match, add it and move both, else move the lesser one
        if x1 == x2:
            answer.append(x1)
            p1 += 1
            p2 += 1
        elif x1 < x2:
            p1 += 1
        else:
            p2 += 1

    return answer

#main program
#prompts user for two queries and gives back an intersected postings list
def runInterface():
    cor = splitCorpus()
    nor = normalizeCorpus(cor)
    index = buildIndex(nor)

    print("Hi! Welcome to the search engine! \n")
    q1 = input("Please input the first term to search\n")
    q2 = input("Please input the second term to search\n")

    #make sure queries are strings and non-empty
    #the try/except is in case a word isn't found in the index
    try:
        if q1 and q2 and isinstance(q1, str) and isinstance(q2, str):
            ans = intersectLists(index, q1, q2)
            if not ans: #if list is empty
                print("Sorry! No documents had both of your terms. Have a good day!")
            else:
                print("List: " + str(ans))
                print("Have a good day!")
        else:
            print("Hey! One of your queries isn't right. Only words are accepted. Please run the program again.")
    except:
        print("Sorry! No documents were found with one of your queries. Have a good day!")

runInterface()
