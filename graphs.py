#!python3
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

#Set up the words as x and its count as y
def wordFrequencyGraph(wordList, noSubmissions):
    x = []
    y = []
    for words in wordList:
        x.append(words['Word'])
        y.append(words['Count'])
    makeGraph(x, y, 'Number of Uses', 'Most Used Words in ' + str(noSubmissions) + ' Submissions', 'wordFrequency.png')

#Subreddit Name = x, Activity Count = y
def mostActiveChart(subredditList):
    finalList = []
    x = []
    y = []
    subredditList = sorted(subredditList, key=itemgetter('Count'), reverse=True)
    try:
        for i in range(0, 9):
            finalList.append({'Subreddit Name': subredditList[i]['Subreddit Name'].display_name, 'Count': subredditList[i]['Count']})
        z = 0
        for i in range(9, len(subredditList)):
            z += subredditList[i]['Count']
        finalList.append({'Subreddit Name': 'Other', 'Count': z})
        finalList = sorted(finalList, key=itemgetter('Count'), reverse=True)
    except IndexError:
        finalList = subredditList
    for items in finalList:
        x.append(items['Subreddit Name'])
        y.append(items['Count'])
    makeGraph(x, y, 'Amount of Submissions', 'Activity Graph', 'mostActive.png')


def makeGraph(x, y, label, title, saveAs):
        fig, ax = plt.subplots()
        y_pos = np.arange(len(y))
        ax.barh(y_pos, y)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(x)
        ax.invert_yaxis()
        ax.set_xlabel(label)
        ax.set_title(title)
        plt.tight_layout()
        plt.savefig(saveAs)
