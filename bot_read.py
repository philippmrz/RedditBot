#!/usr/bin/env python3
import praw
import pdb 
import re 
import os 
import csv
#from http://pythonforengineers.com/build-a-reddit-bot-part-2-reply-to-posts

#Read specific subreddit and bot values from csv
#Csv Model:
#[[praw-botname],[subredditname],[reddit-username], [first string to search for, string to reply],[second"""", ""],[third"""", ""]]
with open('stuff.csv', 'r') as f:
    reader = csv.reader(f)
    stuff = list(reader)

reddit = praw.Reddit(stuff[0][0])
subreddit = reddit.subreddit(stuff[1][0])
commentsList = []

#https://stackoverflow.com/questions/36366388/get-all-comments-from-a-specific-reddit-thread-in-python
def getSubComments(comment, allComments):
    allComments.append(comment)
    if not hasattr(comment, "replies"):
        replies = comment.comments()
    else:
        replies = comment.replies
    for child in replies:
        getSubComments(child, allComments)

#Create empty post_replied to if it doesnt exist yet, read existing file if it does
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

#Get 5 newest post submissions comments recursively and add them to commentsList
for submission in subreddit.new(limit=5):
        for comment in submission.comments:
            getSubComments(comment, commentsList)

#Check if each comment contains string and reply accordingly, add replied comment to post_replied_to
for comment in commentsList:
    if not comment.id in posts_replied_to and not comment.author.name == stuff[2][0]:
        posts_replied_to.append(comment.id)
        print(comment.id + '\n' + comment.body)
        if stuff[3][0] in comment.body:
            comment.reply(stuff[3][1])
        elif stuff[4][0] in comment.body:
            comment.reply(stuff[4][1])
        elif stuff[5][0] in comment.body or stuff[5][1] in comment.body:
            comment.reply(stuff[5][1])

#save replied post in .txt file
with open('posts_replied_to.txt', 'w') as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
