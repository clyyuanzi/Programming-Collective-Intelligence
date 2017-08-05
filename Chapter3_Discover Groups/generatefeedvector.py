import feedparser
import re


def getwords(html):
    #去除所有HTML标记
    txt = re.compile(r'<[^>]+>').sub('',html)
    
    #利用所有非字母字符拆分出单词
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    
    #转化成小写形式
    return [word.lower() for word in words if word!='']

def getwordcounts(url):
    d = feedparser.parse(url)
    wc ={}

    
    #循环所有文章条目 d.entries
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else: 
            summary = e.description
        
        #提取单词列表
        words = getwords(e.title+' '+summary) 
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
    print d.feed.title
    return d.feed.title,wc    
    

apcount={}
wordcounts={}
feedlist = [line for line in file('feedlist.txt')]
for feedurl in feedlist:
    title,wc = getwordcounts(feedurl)
    wordcounts[title]=wc
    for word,count in wc.items():
        apcount.setdefault(word,0)
        if count>1:
            apcount[word]+=1
    

wordlist=[]
for w,bc in apcount.items():
    frac = float(bc)/len(feedlist)
    if frac>0.1 and frac<0.5:
        wordlist.append(w)
        
        
out = file('blogdata.txt','w')
out.write('Blog')

for word in wordlist:
    out.write('\t%s' % word)
out.write('\n')

for blog,wc in wordcounts.items():
    out.write(blog.encode('utf-8'))
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')
    


    
    
    
     