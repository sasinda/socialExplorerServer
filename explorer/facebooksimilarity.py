__author__ = 'pangjac'

import facebook
import requests
import numpy as np
import pandas as pd
from datetime import datetime

from collections import Counter
import urllib2, cookielib
import json


#define global app configurations
api_version = 'v2.5'
app_id = '1026357457425742'
app_secret = '62c89e23affe41bc9fab74b3485ad070'
app_token = '1026357457425742|3ivOpHQj1Hx0Hn66pCU0LtOy_c8'

#sas facebook token #expired
#user_token_dev2 ='CAAOld3eplU4BABZBrPxHqzjZC2aXxGgZA7ZBIZBCOiZBredw1oVCjXyb2dqz8KSG9qbN4FBnEBm5jqw9pjJDMruLlmLZBdj1kiCfy3H34smlD2TallE5UR9kbZBBOqEjBxomB3oux4HRb3P9ZC7ge5gLx0ePaEAOyoCwDIQoc46ZABLSx1VKZC8eGUGRNMgdiucerm60ZAcHcC3AmwZDZD'
#pangjac facebook token
user_token_dev ='CAACEdEose0cBAP4blWxOdXAA28y49vJpF1KRDZBWiLMHGR4AD907s4AwRUKb5nuJIZAcu5PFfJ2pkbXbcxFvNl8UXUkfOdtHxESZAROfyxZAWSoZBFzZCYVmswOacgONUOVkVmvGgByZC0zdEFijI4UOCpL4W2w0b5cMc24RCNtOlhMyj8LqM6xXPLPa1KpEBB5TUqBMKjurfiEqICTGHWj'
graph = facebook.GraphAPI(access_token=user_token_dev)

def getmyinfo(connections, user_token):
    '''
    This function is to get user own informaiton, given the targets, find the corresponding user own information
    :param connections: a list of targets, or a string if there is only one target
    :return: user information given the target(s)
    '''
    graph = facebook.GraphAPI(access_token=user_token)
    returnConnection = {}

    if len(connections) == 0:
        print "Not given expected return targets"
        return

    if len(connections)>1:

        for connection in connections:
            profile = graph.get_object(id = 'me')
            connectionObj = graph.get_connections(id = 'me', connection_name = connection)
            returnConnection.update({connection:connectionObj})
        return returnConnection

    elif (len(connections)==1):
        profile = graph.get_object(id = 'me')
        connectionObj = graph.get_connections(id = 'me', connection_name = connections[0])
        returnConnection.update({connections[0]:connectionObj})
        return returnConnection

#print getmyinfo(['friends'],user_token_dev)


def getfriends(usrid, userToken):
    '''
    This function is to get user friends
    :param connections: one single string for target ; usrid : either "me" or user id #; userToken: corresponding to userid
    :return: user friends list
    '''

    connections = 'friends'
    id = usrid

    graph = facebook.GraphAPI(access_token=userToken)
    returnConnection = {}

    profile = graph.get_object(id = id)
    connectionObj = graph.get_connections(id = id, connection_name = connections)
    returnConnection.update({connections:connectionObj})

    return returnConnection

#print getfriends('me', user_token_dev)


def getUserID(userToken):
    '''
    This function is to get user friends
    :param connections: one single string for target ; usrid : either "me" or user id #; userToken: corresponding to userid
    :return: user friends list
    '''
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    ACCESSTOKEN = userToken
    r = opener.open('https://graph.facebook.com/me?access_token=' + ACCESSTOKEN)
    content = r.read()
    id_info = json.loads(content)["id"]

    return id_info
#print getUserID(user_token_dev)


def getPosts(usrid, userToken, limit = 1):
    '''
    This function is to get user posts and posts creation time
    :param usrid : either "me" or user id #; userToken: corresponding to userid ; limit is how far we fetch the facebook posts
    :return: tuple, the first para is all text information, the second para is text and creation time
    '''

    connections = 'posts'
    id = usrid
    graph = facebook.GraphAPI(access_token=userToken)
    profile = graph.get_object(id = id)

    all_posts = []

    all_post_time = []
    all_post_context = []
    all_post_likes = []

    countPost = 0
    # start to parse post
    posts = graph.get_connections(id = id, connection_name = connections)

    while posts['paging']['next'] and (countPost < limit):
        try:
            for post in posts["data"]: #every post #every post's all information
                #get post information and attached it to post List
                all_posts.append(post)

               #format post create_time
                dts=all_posts[-1].get('created_time');
                date_object_tmp = datetime.strptime(dts, "%Y-%m-%dT%H:%M:%S+0000")
                date_object = unicode(date_object_tmp.replace(microsecond=0)).encode('ascii','ignore')
                all_posts[-1]['created_time']=date_object

                
               # for this post id, get like info:
                #'https://graph.facebook.com/v2.5/100000112788297_1152773018069780/likes?summary=true&access_token=yourusertoken'
                this_postid = all_posts[-1].get('id')
                args = {'summary' : 'true' }
                likesObj=graph.get_connections(id=this_postid , connection_name='likes', **args)
                likes = likesObj["summary"]["total_count"]

                #update this post with post likes
                all_posts[-1].update({"likes": likes})

                this_creatTime =  all_posts[-1].get('created_time')
                this_message = all_posts[-1].get('message')
                this_likes =  all_posts[-1].get('likes')


                all_post_time.append(this_creatTime)
                all_post_context.append(this_message)
                all_post_likes.append(this_likes)

            #move to next Page posts
            posts=requests.get(posts['paging']['next']).json()
            countPost +=1;

        except KeyError:
        # When there are no more pages (['paging']['next']), break from the loop and end the script.
            break

    return json.dumps([{"x": all_post_time, "y": all_post_likes , "type": "bar"}])
    #return json.dumps({"time": all_post_time, "context": all_post_context, "likes": all_post_likes})

def postProcess(postList):
    from operator import itemgetter
    result = sorted(postList, key = itemgetter("likes"))
    return result

def findLikeinDay(timeList):
    likeDict = {}
    for i in range(0, len(timeList)-1):
        likeIndex = []
        currdate = timeList[i].split(" ",1)[0].encode('ascii','ignore')
        nextdate = timeList[i+1].split(" ",1)[0].encode('ascii','ignore')

        print currdate
        print nextdate

        print currdate == nextdate

        if currdate != nextdate:
            likeDict.update({currdate:["i"]})

            i = i + 1

        else:
            currdate = nextdate
            i = i + 2
            likeIndex = [i] + [i+1]

        likeDict.update({currdate : likeIndex})


    return likeDict

# postList = getPosts('me', user_token_dev, limit =10)

#timeList = [u'2016-03-16 06:20:39', u'2016-02-07 16:06:38', u'2016-02-07 15:41:32', u'2016-02-07 14:29:21', u'2016-02-06 22:07:42', u'2016-02-06 18:29:25', u'2016-02-05 01:27:59', u'2016-02-04 12:48:27', u'2016-01-31 15:49:30', u'2016-01-31 12:19:50', u'2016-01-29 15:01:13', u'2016-01-29 13:45:53', u'2016-01-29 13:38:58', u'2016-01-28 02:46:21', u'2016-01-25 08:48:15', u'2016-01-25 08:30:21', u'2016-01-19 05:22:53', u'2015-12-17 08:55:34', u'2015-12-09 03:21:43', u'2015-12-09 03:20:31', u'2015-12-08 04:43:27', u'2015-12-06 22:00:15', u'2015-12-04 20:57:10', u'2015-11-26 23:32:12']


#print postList

#print postProcess(postList)

def findindex (lst):

    #lst = [1,2,2,2,3,3,5,6]
    this_lst_dict = {}

    for i in range(0, len(lst)):

        if lst[i] not in this_lst_dict.keys():
            this_lst_dict.update({lst[i]:[i]})

        else:
            this_lst_dict.get(lst[i], None).append(i)

    return this_lst_dict




