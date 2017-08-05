# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:35:53 2016

@author: bjchenliyuan
"""

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt 
def sim_distance(prefs,person1,person2):
    # shared-items 列表    
    si ={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
            
    #如果两人没有共同的物品，返回0
    if(len(si)==0):
        return 0
    
    #计算share-items的差值的平方和
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                        for item in si])
    
    return 1/(1+sqrt(sum_of_squares))
    
    
def sim_pearson(prefs,p1,p2):
     # shared-items 列表    
    si ={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
            
    #如果两人没有共同的物品，返回0
    if(len(si)==0):
        return 1
        
    sum1 = sum([prefs[p1][item] for item in si])
    sum2 = sum([prefs[p2][item] for item in si])

    sum1Sq = sum([pow(prefs[p1][item],2) for item in si])
    sum2Sq = sum([pow(prefs[p2][item],2) for item in si])
    
    pSum = sum([prefs[p1][item]*prefs[p2][item] for item in si])
    
    n = len(si)
    numerator = pSum-sum1*sum2/n
    denominator = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if denominator == 0:
        return 0
    
    pearson = numerator / denominator 
    
    return pearson
    
    
def topNMatches(prefs,person,n=5,similarity=sim_pearson):
    scores = [(similarity(prefs,person,other),other) 
                for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]
    
    
    
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        if other==person: 
            continue
        sim = similarity(prefs,person,other)
        
        # 忽略相似度小于0的情况
        if sim<=0:
            continue
        
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                #相似度*评价值之和
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                
                #相似度之和
                simSums.setdefault(item,0)
                simSums[item]+=sim
                
    #建立一个归一化的列表
    rankings =[(total/simSums[item],item)  for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings
    

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs,n=10):
    result = {}
    
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c+=1
        if c%100==0:
            print "%d / %d" % (c,len(itemPrefs))
        
        #寻找最相近的物品
        scores = topNMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores
    return result
    

def getRecommendationItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}
    
    for (item,rating) in userRatings.items():
        for (similarity,item2) in itemMatch[item]:
            if item2 in userRatings:
                continue
            
            #评价值与相似度的加权和
            scores.setdefault(item2,0)
            scores[item2] += similarity*rating
            
            #相似度的加权和
            totalSim.setdefault(item2,0)
            totalSim[item2] += similarity
    
    rankings = [(score/totalSim[item],item) for item,score in scores.items()]
            
    rankings.sort()
    rankings.reverse()
    return rankings
        
        
        
def loadMovieLens(path='D:\Work Space\python\Programming Collective Intelligence\Chapter2_Make Recommendations\ml-100k'):
    
    #获取影片标题
    movies = {}
    for line in open(path+'/u.item'):
        (id,title) = line.split('|')[0:2]
        movies[id]=title
        
    #加载数据
    prefs={}
    for line in open(path+'/u.data'):
        (user,movieid,rating,ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs
    