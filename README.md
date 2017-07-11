# Reddit Comment Analysis Bot

## What is it?

It's a bot that analyses the entire* comment history of a reddit user and replies with its findings.

\* - _Some comments may be unavailable due to how the reddit API works._

## Features:

* Analyses all the comments and posts made by the redditor.
* Finds the most commonly used words and creates a chart.
* Show a graph of user's most active subreddits.
* Displays some general information about the number of comments and posts.

## Usage:

![Usage](https://i.imgur.com/2ltlb4p.png)

![Chart 1](https://i.imgur.com/7N2Besa.png)

![Chart 2](https://i.imgur.com/l99rgFT.png)

## Setup:

Create `praw.ini` with the following details

```
[Reddit Bot]
client_id = id
client_secret = secret
username = reddit_username
password = reddit_password

```
