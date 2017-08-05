# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 18:05:08 2016

@author: bjchenliyuan
"""

def readfile(filename):
    lines = [line for line in file(filename)]
    
    #第一行是列标题
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data =[]
    for line in lines[1:]:
        p=line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return colnames,rownames[0:len(data)-1],data[0:len(data)-1]


from math import sqrt
def pearson(v1,v2):
    sum1 = sum(v1)
    sum2 = sum(v2)
    
    sum1Sq = sum([pow(v,2) for v in v1])
    sum2Sq = sum([pow(v,2) for v in v2])
    
    length = len(v1) if len(v1)<len(v2)  else len(v2)
    pSum = sum([v1[i]*v2[i] for i in range(length)])
    
    numerator = pSum-sum1*sum2/len(v1)
    denominator = sqrt(sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1))
    if denominator==0:
        return 0

    return 1-numerator/denominator


def tanimoto(v1,v2):
    c1,c2,share=0,0,0
    
    for i in range(len(v1)):
        if v1[i]!=0:
            c1+=1
        if v2[i]!=0:
            c2+=1
        if v1[i]!=0 and v2[i]!=0:
            share+=1
    return 1-float(share)/(c1+c2-share)




class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

    
def hcluster(rows,distance=pearson):
    distances={}
    currentclusterid=-1
    
    
    #最开始的聚类
    clust=[bicluster(rows[i],id=i) for i in range(len(rows))]
    
    while len(clust)>1:
        #初始化
        lowestpair = (0,1)
        closest = distance(clust[0].vec,clust[1].vec)
        
        #遍历每一个配对，寻找最小距离
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                #用distances来缓存距离的计算值
                if(clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id)]  = distance(clust[i].vec,clust[j].vec)
                
                d=distances[(clust[i].id,clust[j].id)]
                if d<closest:
                    closest = d
                    lowestpair=(i,j)
        
        
        #计算两个聚类的平均值
        mergevec = [(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 
                        for i in range(len(clust[0].vec))]
        
        #建立新的聚类
        newcluster = bicluster(mergevec,left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]],distance=d,id=currentclusterid)
                
        currentclusterid-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
    
    return clust[0]


def printclust(clust,labels=None,n=0):
    #利用缩进来建立层级布局
    for i in range(n):
        print '  !',
    #负数标记代表这是一个分支
    #正数标记代表这是一个叶节点
    if clust.id<0:
        print'-' 
    else:
        if labels == None:
            print clust.id
        else: 
            print labels[clust.id]
                                                                                                                                                                         
    #现在开始打印右侧分支和左侧分支
    if clust.left!=None:
        printclust(clust.left,labels=labels,n=n+1)
    if clust.right!=None:
        printclust(clust.right,labels=labels,n=n+1)
        

def getheight(clust):
    if clust.left==None and clust.right==None:
        return 1
    return getheight(clust.left)+getheight(clust.right)
        
        
def getdepth(clust):
    if clust.left==None and clust.right==None:
        return 0
    
    return max(getdepth(clust.left),getdepth(clust.right))+clust.distance
    

from PIL import Image,ImageDraw
def drawnode(draw,clust,x,y,scaling,labels):
    if clust.id<0:
        h1=getheight(clust.left)*20
        h2=getheight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2
        
        #线的长度
        l1=clust.distance*scaling
        #聚类到其子节点的垂直线
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))
        #连接左节点的水平线
        draw.line((x,top+h1/2,x+l1,top+h1/2),fill=(255,0,0))
        #连接右节点的水平线
        draw.line((x,bottom-h2/2,x+l1,bottom-h2/2),fill=(255,0,0))
        
       #调用函数绘制左右节点
        drawnode(draw,clust.left,x+l1,top+h1/2,scaling,labels)
        drawnode(draw,clust.right,x+l1,bottom-h2/2,scaling,labels)
    else:
        draw.text((x,y),labels[clust.id],(0,0,0))


def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
    h=getheight(clust)*20
    w=1200
    depth=getdepth(clust)
    
    scaling=float(w-150)/depth
    
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)
    
    draw.line((0,h/2,10,h/2),fill=(255,0,0))
    
    #画第一个节点
    drawnode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')


def rotatematrix(data):
    newdata=[]
    for i in range(len(data[0])):
        newrow= [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


def rotate(data):
    result=[]
    for i in range(len(data[0])):
        for j in range(len(data)):
            result.setdefault(0,0)
            result[j][i]=data[i][j]
    return result



import random
def kcluster(rows,distance=pearson,k=4):
    #确定每个点的最小值和最大值
    ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0]))]
    
    #随机产生k个中心点s
    clusters = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]
    
    
    lastmatches=None
    for t in range(100):
        print 'Iteration %d' % t
        bestmatches =[[] for i in range(k)]
        
        #在每一行中寻找距离最近的中心点
        for j in range(len(rows)):
            row=rows[j]
            bestmatch=0
            for i in range(k):
                d=distance(clusters[i],row)
                if d<distance(clusters[bestmatch],row):
                    bestmatch=i
            bestmatches[bestmatch].append(j)
        
        if bestmatches==lastmatches:
            break
        lastmatches=bestmatches
        
        
        #把中心点移到所有成员的平均位置处
        for i in range(k):
            avgs=[0.0]*len(rows[0])
            if len(bestmatches[i])>0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m]+=rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                clusters[i]=avgs
        
    return bestmatches




def scaledown(data,distance=pearson,rate=0.01):
    n=len(data)
    
    #每一对数据项之间的真实距离
    realdist=[[distance(data[i],data[j]) for i in range(n)] for j in range(n)]
    
    outersum=0
    
    #随机初始化节点在二维空间中的起始位置
    loc = [[random.random(),random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]
    
    lasterror = None
    for m in range(0,1000):
        #寻找投影后的距离
        for i in range(n):
            for j in range(n):
                fakedist[i][j]=sqrt(sum([pow(loc[i][col]-loc[j][col],2) for col in range(len(loc[i]))]))
                
        #移动节点
        grad=[[0.0,0.0] for i in range(n)]
        
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k:
                    continue
                #误差值等于目标距离与当前距离之间差值的百分比
                errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]
                
                #每一个节点根据误差的多少，按比例移动离开或者靠近其它节点
                grad[k][0]+=((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm   
                grad[k][1]+=((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm   


                #记录总的误差值
                totalerror+=abs(errorterm)
        print totalerror

        if lasterror and totalerror > lasterror:
            break
        
        lasterror = totalerror
        
        print grad
        for k in range(n):
            loc[k][0]-=rate*grad[k][0]
            loc[k][1]-=rate*grad[k][1]
            
    return loc


def draw2d(data,labels,jpeg='mds2d.jpg'):
    img=Image.new('RGB',(2000,2000),(255,255,255))
    draw=ImageDraw.Draw(img)
    for i in range(len(data)):
        x=(data[i][0]+0.5)*1000
        y=(data[i][1]+0.5)*1000
        draw.text((x,y),labels[i],(0,0,0))
    img.save(jpeg,'JPEG')




