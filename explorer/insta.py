__author__ = 'pangjac'

from time import sleep
from instagram.client import InstagramAPI
from collections import Counter
import urllib2, cookielib
import json
import re, math

access_token = "2726686297.490d633.b0b820fdb43646898ee466eb96c36796"
client_secret = "a0f93d27a810423bbea873039698fd23"

#url to query for specific hashtag pictures
#hashtag = "trump"
#nextUrl = "https://api.instagram.com/v1/tags/"+hashtag+"/media/recent?access_token="+ACCESSTOKEN


def parseIns(access_token):
    '''
    This fuction is to find user instagram all picture actuall jpg url
    The assumption is to have a valid user "access_token"
    :param access_token:
    :return:
    A list, with every element is user ins jpg url
    '''

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    #ACCESSTOKEN = "2726686297.490d633.b0b820fdb43646898ee466eb96c36796"
    ACCESSTOKEN = access_token
    r = opener.open('https://api.instagram.com/v1/users/self/media/recent/?access_token=' + ACCESSTOKEN)
    content = r.read() #return meta data
    content_data = json.loads(content)["data"] # return "data " part from meta data

    userName = content_data[0]["user"]["username"].encode('utf-8')

    user_insPictureList = []
    for ele in content_data :
        elejpg_url = ele["images"]["low_resolution"]["url"].encode('utf-8').partition("?")[0]
        user_insPictureList.append(elejpg_url)

    result=user_insPictureList
    #result.append(userName)
    return result

#print parseIns(access_token)

#start to call AI API for picture classification

def pictureClassfication(pictureURL):
    '''
    This fuction is to give picture classification list and corresponding class probability
    :param ins jpg url
    :return:
    A List, which is a list of the highest 6 possible classification for this picture.
    '''

    opener = urllib2.build_opener()
    opener.addheaders = [('Authorization', 'Bearer TpI8gnjjYprxoTydQSoC41aW32suWv')]
    #r2 = opener.open('https://api.clarifai.com/v1/tag/?model=general-v1.3&url=https://scontent-yyz1-1.cdninstagram.com/t51.2885-15/e35/12822489_1573146096310514_580506399_n.jpg')
    r2 = opener.open('https://api.clarifai.com/v1/tag/?model=general-v1.3&url='+str(pictureURL))
    content_2 = r2.read()
    content2_data = json.loads(content_2)

    jpgClasses_ = content2_data['results'][0]['result']['tag']['classes']
    jpgClasses = [x.encode('UTF8') for x in jpgClasses_]
    jpgProbs= content2_data['results'][0]['result']['tag']['probs']

    if len(jpgClasses)>=10:
        return jpgClasses[:10]
    else:
        return jpgClasses

#print pictureClassfication("https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/12822489_1573146096310514_580506399_n.jpg")

def getInsPicClasses(insPictureList):
    '''
    This fuction is to take list of jpg url, get each jpg classification and combine all classification together with counting
    each classification, then return Counter of label&labelCounts
    The list of classifications would be used as a bag of words for following classifcation comparisons.
    :param ins picture url list
    :return: Counter of label&labelCounts
    '''
    insClassesList = []
    for url in insPictureList:
        #print url
        thisjpgClasses = pictureClassfication(url)
        #print thisjpgClasses
        insClassesList += thisjpgClasses

    countsIns = Counter(insClassesList)

    return countsIns


#inputList = parseIns(access_token)
#[('no person', 3), ('wood', 2), ('business', 2), ('nature', 2), ('summer', 1), ('love', 1), ('bouquet', 1), ('petal', 1), ('indoors', 1), ('flower', 1)]
#print getInsPicClasses(inputList)

def data_prepare(useraccessCode):
    '''
    This function is just used to encapsulation processing url procesedures
    The purpose is to make it more clear. That's all, nothing moew
    :param user access Token
    :return:
    A List, Every element in the List is a tuple like this ('label', labelCount)
    '''
    user_ins_jpg_List = parseIns(access_token)
    print user_ins_jpg_List
    user_label_vector = getInsPicClasses(user_ins_jpg_List)
    print user_label_vector

    return user_label_vector


def similarity(user1accessCode, user2accessCode):
    '''
    This fuction is to take two list of jpg labels (which from two users) (returned from etInsPicClasses(insPictureList)) and calculate their cosine similarity.
    This simple cosine function does not consider weight of the words by tf-idf,
    since tfidf needs a huge corpus to estimate, where instagram sandbox authentication won't allowed so.
    :param user access Token from two different users
    :return:
    cosine similarity values, type of float
    '''

    user1_labelvec= data_prepare(user1accessCode)
    user2_labelvec = data_prepare(user2accessCode)

    vectors_intersection = set(user1_labelvec.keys()) & set(user2_labelvec.keys())

    numerator = sum([user1_labelvec[_x] * user2_labelvec[_x] for _x in vectors_intersection])

    sum1 = sum([user1_labelvec[_x]**2 for _x in user1_labelvec.keys()])
    sum2 = sum([user2_labelvec[_x]**2 for _x in user2_labelvec.keys()])

    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# print similarity(access_token, access_token)




