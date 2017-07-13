#!python3
import praw, re, graphs, requests, config, os, time
from operator import itemgetter
from imgurpython import ImgurClient

#Functions to get karma by subreddit for comments and posts separately and then combine them
def addToSubredditList(subredditList, thing):
    '''
    If the subreddit exists in the list, increment the count by one.
    If the subreddit doesn't exist in the list, add the subreddit and set the count as 1.
    '''
    for subreddits in subredditList:
        if subreddits['Subreddit Name'] == thing.subreddit:
            subreddits['Count'] += 1
            break
    else:
        subredditList.append({'Subreddit Name': thing.subreddit, 'Count': 1})
    return subredditList

def mergeSubredditLists(comment, submission):
    '''
    Merge the two lists:
    If a subreddit in the second list already exists in the first list, the count of that subreddit is added to its counterpart in the first list.
    If a subreddit does not exist, it along with its count is added to the end of the list.
    Return the new list
    '''
    subredditList = comment
    for subreddit in submission:
        for subs in subredditList:
            if subreddit['Subreddit Name'] == subs['Subreddit Name']:
                subs['Count'] += subreddit['Count']
                break
        else:
            subredditList.append(subreddit)
    return subredditList

#Functions for retrieving data
def getCommentData(redditor):
    '''
    Iterate through every available comment posted by the user and store each comment's text.
    Then pass the comment to addToSubredditList() to increment the counter for each subreddit's activity.
    Return both the list of comments and the subredditList.
    '''
    commentList = []
    subredditList = []
    for comments in redditor.comments.new(limit=None):
        commentList.append(comments.body)
        subredditList = addToSubredditList(subredditList, comments)
    return commentList, subredditList

def getSubmissionData(redditor):
    '''
    Analyze every submission made by the redditor in descending order of karma. Add the text of each selfpost to the end of the list.
    Also count the number of links submitted.
    Call addToSubredditList() to increment or set up the counter.
    Return both the list of selfposts and the subredditList
    '''
    subredditList = []
    submissionList = []
    noLinks = 0
    for submissions in redditor.submissions.top('all'):
        if submissions.selftext:
            submissionList.append(submissions.selftext)
        else:
            noLinks += 1
        subredditList = addToSubredditList(subredditList, submissions)
    return subredditList, submissionList, noLinks

#Word frequency analysis and graph creation functions
def getWordFrequencyList(commentList):
    '''
    Create a regex expression to consider only alphanumeric characters I.E. remove special characters.
    For every comment made by the user split the comment into a list of individual words separated by spaces.
    For every word in the list, convert it to lower case and check if it is in the common word list. if yes, ignore it.
    If it isn't a common word, confirm that it has actual alphabets or numbers and add it to the list.
    Check if the word exists in the frequencyList, if yes increment its count.
    If it isn't in the list, add it to the list and give it a count of 1.
    Return the list after sorting in descending order.
    '''
    wordFile = open('commonWords.txt', 'r')
    commonWordsList = wordFile.read()
    wordFile.close()
    stripChars = re.compile(r'[a-zA-z0-9]+')
    frequencyList = []
    for comments in commentList:
        wordsList = comments.split(' ')
        for words in wordsList:
            words = words.lower()
            if words in commonWordsList:
                continue
            if(stripChars.search(words)):
                for existingWords in frequencyList:
                    if existingWords['Word'] == words:
                        existingWords['Count'] += 1
                        break
                else:
                    frequencyList.append({'Word': words.lower(), 'Count': 1})
    return sorted(frequencyList, key=itemgetter('Count'), reverse=True)

#Driver functions
def imgurBot():
    client = ImgurClient(config.imgurId, config.imgurSecret)
    frequencyLink = (client.upload_from_path('wordFrequency.png', config=None, anon=True))['link']
    activityLink = (client.upload_from_path('mostActive.png', config=None, anon=True))['link']
    return frequencyLink, activityLink

def executeOrder66(username):
    r = reddit.redditor(username)
    commentList, subredditListForComments = getCommentData(r)
    subredditListForSubmissions, submissionList, noLinks = getSubmissionData(r)
    subredditList = mergeSubredditLists(subredditListForComments, subredditListForSubmissions)
    noComments = len(commentList)
    noPosts = len(submissionList)
    frequencyList = getWordFrequencyList(commentList) + getWordFrequencyList(submissionList)
    graphs.wordFrequencyGraph(frequencyList[:10], noPosts + noComments)
    graphs.mostActiveChart(subredditList)
    frequencyLink, activityLink = imgurBot()
    message = ('''Hi **/u/%s**! Thanks for calling me. Here's what I've got for you:
\nI've found about **%s** comments and **%s** posts, **%s** of which were links. This makes for a total of **%s** submissions. Great job!
\nI've also taken the liberty of analysing your frequently used words and made a handy chart! [Click here to check it out.](%s)\nAnd since I like making charts, I even made one to show where you spend the majority of your time! [Click here to check out that chart.](%s)
\n\n---
[^(Message my Master)](https://www.reddit.com/message/compose?to=DarkeKnight) ^| [^(Source Code)](https://github.com/akashsara/reddit-comment-analysis-bot)
    ''' %(username, noComments, noPosts, noLinks, noComments + noPosts, frequencyLink, activityLink))
    return message

def runBot(reddit):
    subredditList = ['lansbot', 'india']
    keyWords = ['!!AnalyseMe', '!!AnalyzeMe', '!!analyseme', '!!ANALYSEME', '!!analyzeme', '!!ANALYZEME']
    for subreddit in subredditList:
        print(subreddit)
        for comment in reddit.subreddit(subreddit).comments(limit=None):
            if comment.saved:
                continue
            for keyWord in keyWords:
                if (keyWord in comment.body) and (comment.author != reddit.user.me()):
                    print('Found a post ' + comment.id ' by ' + comment.author)
                    message = executeOrder66(str(comment.author))
                    comment.reply(message)
                    comment.save()
                    print('Replied to post!')

reddit = praw.Reddit('Reddit Bot', user_agent = 'Desktop:(by github.com/akashsara):Reddit Comment Analyzer Bot')

while True:
    runBot(reddit)
    #time.sleep(300)
