# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 14:34:18 2016

@author: bjchenliyuan
"""

import re
import math


def sampletrain(c1):
    c1.train('Nobody owns the water.','good')
    c1.train('the quick rabbit jumps fences','good')
    c1.train('make quick money at the online casino','bad')
    c1.train('the quick brown for jumps','good')


def getwords(doc):
    splitter=re.compile(r'\W*')
    words=[s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]
    return dict([(w,1) for w in words])


class classifier:
    def __init__(self,getfeatures,filename=None):
        #统计特征/分类组合的数量
        self.fc={}
        #统计每个分类中的文档数量
        self.cc={}
        self.getfeatures=getfeatures
    
    #增加对特征/分类组合的计数值
    def incf(self,f,cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat]+=1
        
    #增加对某一分类的计数值
    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1
    
    #某一特征出现于某一分类中的次数
    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0
    
    #属于某一分类的内容项数量
    def catcount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0.0
    
    #所有内容项的数量
    def totalcount(self):
        return sum(self.cc.values())
    
    #所有分类的列表
    def categories(self):
        return self.cc.keys()


    def train(self,item,cat):
        features=self.getfeatures(item)
        #针对该分类为每个特征增加计数值
        for f in features:
            self.incf(f,cat)
    
        #增加对该分类的计数值
        self.incc(cat)

            
    #计算概率
    def fprob(self,f,cat):
        if self.catcount(cat)==0:
            return 0
        return self.fcount(f,cat)/self.catcount(cat)
        
    
    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        #计算当前的概率
        basicprob=prf(f,cat)
        
        #统计特征在所有分类中出现的次数
        totals= sum([self.fcount(f,c)  for c in self.categories()])
        
        #计算加权平均
        bp=(weight*ap+totals*basicprob)/(totals+weight)
        return bp
    
    
class naivebayes(classifier):
    def docprob(self,item,cat):
        features=self.getfeatures(item)
        #将所有特征的概率相乘
        result=1
        for f in features.keys():
            result*=self.weightedprob(f,cat,self.fprob)
        return result
        
    def prob(self,item,cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item,cat)
        return docprob*catprob
 we        

    
        
            