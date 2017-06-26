
import numpy as np
import pandas as pd
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import roc_auc_score, make_scorer
from sklearn.model_selection import train_test_split


#working with string Data in DataFrame
#df['dow'] = df['dow'].str.split(',') # for all

df.to_pickle("train_data.pkl")
df = pd.read_pickle("train_data.pkl");
df.drop([u'time'],inplace=True,axis=1)
for x in df.genres:
     for i in x :
             genres.add(re.sub(ur'\:\d+',ur'',string=i));

#access time for each dow class
for x in df.dow:
...     for i in x:
...             c=re.sub(ur'\:\d+',ur'',i);
...             d=re.sub(ur'\d\:',ur'',i)
...             df[c]=d;
...

d = re.sub(one+ur'\:',ur'',string=l[0])

dow=set()

df['dow_list']=df['dow'].str.split(',');
for x in df['dow_list']:
     for i in x:
             dow.add(re.sub(ur'\:\d+',ur'',string=i));
dow=list(dow);
#could also be done using for loop
df[one]=[x.replace(re.sub(one+ur'\:\d+',ur'',string=x),"")for x in df['dow']]
df[three]=[re.findall(three+ur'\:\d+',string=x)for x in df['dow']]
#stage2 ends

#genres list
df['genres_list']=df['genres'].str.split(',');
genres=set();
for x in df['genres_list']:
     for i in x:
            genres.add(re.sub(ur'\:\d+',ur'',string=i))
g=list(genres);
#creating columns for all genres
for x in g:
    df[x]=[re.findall(x+ur'\:\d+',string=i) for i in df['genres']]
#stage2.2  ends

#stage3
#df['delete']=df[u'Cricket'].map(get_number);
def get_number(p):
        if(len(p)==0):
                return 0;
        else:
            o=re.sub(ur'\:\d+',ur'',p[0])
            d=re.sub(o+ur'\:',ur'',p[0])
            return int(d);
for x in g:
    df[x]=df[x].map(get_number);

def changeNull(p):
    if(p is int):
             pass;
     else:
             return 0;
def get_time(p):
     #print p;
     s = []
     s=re.sub(ur'\d+\:',ur'',p)
     s=[int(x) for x in s.split(',')]
     #print s,type(s);
     sum=0;
     for i in range(len(s)):
             sum=sum+s[i];
    #         print sum;
     return sum;
df['tod_sum'] = df['tod'].map(get_time);

def get_titles_time(p):
     #print p;
     s = []
     #s=re.sub(pattern = '.*\:', repl='',p)
     s = re.findall(ur'\d+',p)
     s=[int(x) for x in s]
     #print s,type(s);
     sum=0;
     for i in range(len(s)):
             sum=sum+s[i];
    #         print sum;
     return sum;

def get_days(p):
     return len(p);
df['no_of_days']=df['dow_list'].map(get_days)

blanks = []
for i in np.arange(len(main)):
    if '' in main[i]:
        print "{} blanks found at {}".format(len(blanks),i)
        blanks.append(i)
