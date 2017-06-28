import json
import numpy as np
import pandas as pd
import re
#import matplotlib.pyplot as plt


train_data = pd.read_json('train_data.json',orient="index")
test_data = pd.read_json('test_data.json',orient='index')
#set index
train_data.reset_index(level = 0, inplace = True)
train_data.rename(columns={'index':'ID'}, inplace=True)

test_data.reset_index(level = 0, inplace = True)
test_data.rename(columns={'index':'ID'}, inplace=True)

train_data = train_data.replace({'segment':{'pos':1,'neg':0}})
#END OF STAGE 1

#------creating seperate columns for genre and dow--------------
train_data['g1'] = [re.sub(pattern='\:\d+',repl='',string=x) for x in train_data['genres']]
train_data['g1'] = train_data['g1'].apply(lambda x: x.split(','))

train_data['g2'] = [re.sub(pattern='\:\d+', repl='', string = x) for x in train_data['dow']]
train_data['g2'] = train_data['g2'].apply(lambda x: x.split(','))

t1 = pd.Series(train_data['g1']).apply(frozenset).to_frame(name='t_genre')
t2 = pd.Series(train_data['g2']).apply(frozenset).to_frame(name='t_dow')
 #using frozenset trick - might take few minutes to process
for t_genre in frozenset.union(*t1.t_genre):
    t1[t_genre] = t1.apply(lambda _: int(t_genre in _.t_genre), axis=1)

for t_dow in frozenset.union(*t2.t_dow):
    t2[t_dow] = t2.apply(lambda _: int(t_dow in _.t_dow), axis = 1)

train_data = pd.concat([train_data.reset_index(drop=True), t1], axis=1)
train_data = pd.concat([train_data.reset_index(drop=True), t2], axis=1)

#-----------------similarly for test data ----------------------
test_data['g1'] = [re.sub(pattern='\:\d+',repl='',string=x) for x in test_data['genres']]
test_data['g1'] = test_data['g1'].apply(lambda x: x.split(','))

test_data['g2'] = [re.sub(pattern='\:\d+', repl='', string = x) for x in test_data['dow']]
test_data['g2'] = test_data['g2'].apply(lambda x: x.split(','))

t1_te = pd.Series(test_data['g1']).apply(frozenset).to_frame(name='t_genre')
t2_te = pd.Series(test_data['g2']).apply(frozenset).to_frame(name='t_dow')

for t_genre in frozenset.union(*t1_te.t_genre):
    t1_te[t_genre] = t1_te.apply(lambda _: int(t_genre in _.t_genre), axis=1)
for t_dow in frozenset.union(*t2_te.t_dow):
    t2_te[t_dow] = t2_te.apply(lambda _: int(t_dow in _.t_dow), axis = 1)
test_data = pd.concat([test_data.reset_index(drop=True), t1_te], axis=1)
test_data = pd.concat([test_data.reset_index(drop=True), t2_te], axis=1)

#---SUM OF WATCH TIMES------------
#the rows aren't list exactly. They are object, so we convert them to list and extract the watch time
w1 = train_data['titles']
w1 = w1.str.split(',')

#create a nested list of numbers
main = []
for i in np.arange(train_data.shape[0]):
    d1 = w1[i]
    nest = []
    nest = [re.sub(pattern = '.*\:', repl=' ', string= d1[k]) for k in list(np.arange(len(d1)))]
    main.append(nest)


print len(main)
#print main;

blanks = []
for i in np.arange(len(main)):
    if '' in main[i]:
        print i;
        print "{} blanks found".format(len(blanks))
        blanks.append(i)
    else:
        pass;
#replacing blanks with 0
for i in blanks:
    main[i] = [x.replace('','0') for x in main[i]]

#converting string to integers
main = [[int(y) for y in x] for x in main]

#adding the watch time
tosum = []
for i in np.arange(len(main)):
    s = sum(main[i])
    tosum.append(s)

train_data['title_sum'] = tosum
# ------------MAKING CHANGES IN TEST_DATA-------------
w1_te = test_data['titles']
w1_te = w1_te.str.split(',')
main_te = []
for i in np.arange(test_data.shape[0]):
    d1 = w1_te[i]
    nest = []
    nest = [re.sub(pattern = '.*\:', repl=' ', string= d1[k]) for k in list(np.arange(len(d1)))]
    main_te.append(nest)

blanks_te = []
for i in np.arange(len(main_te)):
    if '' in main_te[i]:
        print "{} blanks found".format(len(blanks_te))
        blanks_te.append(i)

#replacing blanks with 0
for i in blanks_te:
    main_te[i] = [x.replace('','0') for x in main_te[i]]

#converting string to integers
main_te = [[int(y) for y in x] for x in main_te]

#adding the watch time
tosum_te = []
for i in np.arange(len(main_te)):
    s = sum(main_te[i])
    tosum_te.append(s)

test_data['title_sum'] = tosum_te


def wcount(p):
    return p.count(',')+1
train_data['title_count'] = train_data['titles'].map(wcount)
train_data['genres_count'] = train_data['genres'].map(wcount)
train_data['cities_count'] = train_data['cities'].map(wcount)
train_data['tod_count'] = train_data['tod'].map(wcount)
train_data['dow_count'] = train_data['dow'].map(wcount)

test_data['title_count'] = test_data['titles'].map(wcount)
test_data['genres_count'] = test_data['genres'].map(wcount)
test_data['cities_count'] = test_data['cities'].map(wcount)
test_data['tod_count'] = test_data['tod'].map(wcount)
test_data['dow_count'] = test_data['dow'].map(wcount)


test_id = test_data['ID']
train_data.drop(['ID','cities','dow','genres','titles','tod','g1','g2','t_genre','t_dow'], inplace=True, axis=1)
test_data.drop(['ID','cities','dow','genres','titles','tod','g1','g2','t_genre','t_dow'], inplace=True, axis=1)

#train model
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import roc_auc_score, make_scorer
from sklearn.model_selection import train_test_split
target = train_data['segment']
train_data.drop('segment',axis=1, inplace=True)

#train final model
rf_model = RandomForestClassifier(n_estimators=500,max_depth=12, max_features=10)
rf_model.fit(train_data, target)

rf_pred = rf_model.predict_proba(test_data)
#print rf_pred
columns = ['segment']
sub = pd.DataFrame(data=rf_pred[:,1], columns=columns)
sub['ID'] = test_id
sub = sub[['ID','segment']]
sub.to_csv("sub_hot.csv", index=False)
