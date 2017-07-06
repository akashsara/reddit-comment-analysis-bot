#!python3
'''
TO DO:
Set it up to run all the time
Make sure it replies only once
Make a table for karma breakdown
Make a chart of graph or something for word frequency
Most active subreddits
Karma/Comment
Karma/Submission
karma breakdown for comments by subreddit
Note: Might not match the karma shown on profiles because for some reason it seems to be ignoring some older self posts. So I'm assuming that it
does not consider self-post karma before the update that let selfposts give karma
'''

import praw, datetime, time, re
from operator import itemgetter

def getCommentData(redditor):
    #Iterate through every available comment posted by the user
    #Add the karma from each comment to the total
    #Add the text of each comment to the commentList
    #If the comment has negative karma, add it's karma and message to the downvoteList
    #If it has positive karma, do the same for the upvoteList
    #Sort the upvoteList and downvoteList according to their karma and return all 3 lists
    commentCount = 0
    totalKarma = 0
    downvoteList = []
    upvoteList = []
    commentList = []
    subredditList = []
    for comments in redditor.comments.new(limit=None):
        totalKarma += (comments.score - 1)
        commentList.append(comments.body)
        subredditList = getKarmaBreakdownBySubreddit(subredditList, comments)
        if(comments.score < 0):
            downvoteList.append({'Karma': comments.score, 'Message': comments.body})
        if(comments.score > 0):
            upvoteList.append({'Karma': comments.score, 'Message': comments.body})
    downvoteList = sorted(downvoteList, key=itemgetter('Karma'))
    upvoteList = sorted(upvoteList, key=itemgetter('Karma'), reverse=True)
    return downvoteList, upvoteList, commentList, subredditList, totalKarma

def getSubmissionData(redditor):
    #Analze every submission made by the redditor in descending order of karma
    #Add the submission's score to the total karma
    #Add the text of each selfpost to the list
    #Call a function to modify the subredditList
    #Sort and return the list along with the total karma gained
    subredditList = []
    submissionList = []
    totalKarma = 0
    for submissions in redditor.submissions.top('all'):
        totalKarma += (submissions.score - 1)
        submissionList.append(submissions.selftext)
        subredditList = getKarmaBreakdownBySubreddit(subredditList, submissions)
    subredditList = sorted(subredditList, key=itemgetter('Karma'), reverse=True)
    return subredditList, submissionList, totalKarma

def printComments(commentList):
    print('------------------------')
    for comments in commentList:
        for keys, values in comments.items():
            print(keys + ': ' + str(values))#[:80] + '...')
        print('------------------------')

def getKarmaBreakdownBySubreddit(subredditList, thing):
    #If the subreddit exists in the list, just add the karma from this submission/comment to it
    #If it does not exist in the list, add the subreddit and the submission/comment's karma
    for subreddits in subredditList:
        if subreddits['Subreddit Name'] == thing.subreddit:
            subreddits['Karma'] += (thing.score - 1)
            break
    else:
        subredditList.append({'Subreddit Name': thing.subreddit, 'Karma': thing.score - 1})
    return subredditList

def getWordFrequencyList(commentList):
    #Create a regex expression to consider only alphanumeric characters.
    #For every comment made by the user split the comment into a list of individual words based on spaces
    #For every word in the list remove any special characters and convert the word to lower case
    #Ignore words that are less than 5 letters long and ignore the https found in some links
    #Check if the word exists in the frequencyList exists, increment it's count
    #If it isn't in the list, add it to the list and give it a count of 1
    #Return the list after sorting in descending order
    stripChars = re.compile(r'[a-zA-z0-9]*')
    frequencyList = []
    for comments in commentList:
        wordsList = comments.split(' ')
        for words in wordsList:
            words = stripChars.search(words).group()
            words = words.lower()
            if len(words) < 5 or words == 'https':
                continue
            for existingWords in frequencyList:
                if existingWords['Word'] == words:
                    existingWords['Count'] += 1
                    break
            else:
                frequencyList.append({'Word': words.lower(), 'Count': 1})
    return sorted(frequencyList, key=itemgetter('Count'), reverse=True)

def startBot(reddit):
    #Get username and retrieve details from reddit
    username = input('Enter your username: ')
    redditor = reddit.redditor(username)
    return redditor

def combineSubredditBreakdowns(comment, submission):
    #Copy comment list to the new list
    #For every entry in the submission list, check if the subreddit exists in the new list
    #If it does, add the karma from that to the new list
    #Else add the entry to the list
    #Sort and return the new list
    subredditList = comment
    for subreddit in submission:
        for subs in subredditList:
            if subreddit['Subreddit Name'] == subs['Subreddit Name']:
                subs['Karma'] += subreddit['Karma']
                break
        else:
            subredditList.append(subreddit)
    return sorted(subredditList, key=itemgetter('Karma'), reverse=True)

def runBot(redditor):
    downvoteList, upvoteList, commentList, subredditListForComments, commentKarma = getCommentData(redditor)
    subredditListForSubmissions, submissionList, submissionKarma = getSubmissionData(redditor)
    subredditList = combineSubredditBreakdowns(subredditListForComments, subredditListForSubmissions)
    totalKarma = commentKarma + submissionKarma
    printComments(subredditList[:20])
    print('Total Karma: %s' % totalKarma)
    print('Comment Karma: %s' %commentKarma)
    print('Post Karma: %s' %submissionKarma)
    print('Analysed %s comments and %s posts.' % (len(commentList), len(submissionList)))
    #frequencyList = getWordFrequencyList(commentList)
    #frequencyList += getWordFrequencyList(submissionList)
    #printComments(frequencyList[:20])

reddit = praw.Reddit('Reddit Bot', user_agent = 'Desktop:(by github.com/akashsara):Reddit Karma Analyzer Bot')

redditor = startBot(reddit)
runBot(redditor)
