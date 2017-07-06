#!python3
'''
TO DO:
Get frequency of words
Set it up to run all the time
Make sure it replies only once
Make a table for karma breakdown
Make a chart of graph or something for word frequency
Keep a list of common words and ignore those words in frequency chart
'''

import praw, datetime, time, re
from operator import itemgetter

def getComments(redditor):
    commentCount = 0
    downvoteList = []
    upvoteList = []
    commentList = []
    #Iterate through every available comment posted by the user
    #Add the text of each comment to the commentList
    #If the comment has negative karma, add it's karma and message to the downvoteList
    #If it has positive karma, do the same for the upvoteList
    for comments in redditor.comments.new(limit=None):
        commentList.append(comments.body)
        if(comments.score < 0):
            downvoteList.append({'Karma': comments.score, 'Message': comments.body})
        if(comments.score > 0):
            upvoteList.append({'Karma': comments.score, 'Message': comments.body})

    #Sort the upvoteList and downvoteList according to their karma and return all 3 lists
    downvoteList = sorted(downvoteList, key=itemgetter('Karma'))
    upvoteList = sorted(upvoteList, key=itemgetter('Karma'), reverse=True)
    return downvoteList, upvoteList, commentList

def printComments(commentList):
    for comments in commentList:
        for keys, values in comments.items():
            print(keys + ':' + str(values) + '.')#[:80] + '...')
        print('------------------------')

def getSubmissionBreakdownBySubreddit(redditor):
    #Initialize list of subreddits and total karma gained
    subredditList = []
    totalKarma = 0
    #Analze every submission made by the redditor in descending order of karma
    for submissions in redditor.submissions.top('all'):
        #If the subreddit exists in the list, just add the karma from this submission to it
        for subreddits in subredditList:
            if subreddits['Subreddit Name'] == submissions.subreddit:
                subreddits['Karma'] += submissions.score
                break
        #If it does not exist in the list, add the subreddit and the submission's karma
        else:
            subredditList.append({'Subreddit Name': submissions.subreddit, 'Karma': submissions.score})
        #Increment total karma regardless of the subreddit list
        totalKarma += submissions.score
    #Sort and return the list along with the total karma gained
    subredditList = sorted(subredditList, key=itemgetter('Karma'), reverse=True)
    return subredditList, totalKarma

def getWordFrequencyList(commentList):
    #Regex expression to consider only alphanumeric characters.
    stripChars = re.compile(r'[a-zA-z0-9]*')
    #Initializing list of words to count
    frequencyList = []
    #For every comment made by the user
    for comments in commentList:
        #Split the comment into individual words based on spaces
        wordsList = comments.split(' ')
        #For every word in the list
        for words in wordsList:
            #remove any special characters and convert the word to lower case
            words = stripChars.search(words).group()
            words = words.lower()
            #Ignore words that are less than 5 letters long
            if len(words) < 5:
                continue
            #Find the word in the frequencyList. If it exists, increment it's count
            for existingWords in frequencyList:
                if existingWords['Word'] == words:
                    existingWords['Count'] += 1
                    break
            #If it isn't in the list, add it to the list and give it  acount of 1
            else:
                frequencyList.append({'Word': words.lower(), 'Count': 1})
    #Return the list after sorting in descending order
    return sorted(frequencyList, key=itemgetter('Count'), reverse=True)

def startBot(reddit):
    #Get username and retrieve details from reddit
    username = input('Enter your username: ')
    redditor = reddit.redditor(username)
    return redditor

def runBot(redditor):
    downvoteList, upvoteList, commentList = getComments(redditor)
    '''
    print('------------------------')
    print('List of comments with negative karma:')
    print('------------------------')
    printComments(downvoteList)

    print('Most popular comments:')
    print('------------------------')
    printComments(upvoteList[:10])

    #Print the number of comments checked and the number of downvoted comments
    if(len(downvoteList) == 0):
        print('Good job! You haven\'t hit negative karma at all in your past %s comments!' % len(commentList))
    else:
        print('Analysed %s comments and found %s comments with negative karma!' % (len(commentList), len(downvoteList)))

    subredditList, karma = getSubmissionBreakdownBySubreddit(redditor)
    '''
    frequencyList = getWordFrequencyList(commentList)
    printComments(frequencyList[:20])

reddit = praw.Reddit('Lan\'s Reddit Bot', user_agent = 'Desktop:(by github.com/akashsara):Reddit Karma Analyzer Bot')

redditor = startBot(reddit)
runBot(redditor)
