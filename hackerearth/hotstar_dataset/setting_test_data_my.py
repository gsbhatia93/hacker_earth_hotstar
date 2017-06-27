
#-----------TEST DATA----------
dftest=pd.read_json("test_data.json",orient="index")

dftest['dow_list']=dftest['dow'].str.split(',');
 for i in dow:
         dftest[i]=[re.findall(i+ur'\:\d+',string=x)for x in dftest['dow']]

for x in dow:
    dftest[x]=dftest[x].map(get_number)
    #genres
for x in g:
         dftest[x]=[re.findall(x+ur'\:\d+',string=i) for i in dftest['genres']]
#getNumber function
for x in g:
  dftest[x]=dftest[x].map(get_number);
#get time function
dftest['tod_sum'] = dftest['tod'].map(get_time);

dftest['titles_sum'] = dftest['titles'].map(get_titles_time);
dftest['no_of_days']=dftest['dow_list'].map(get_days)
