import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions
import MySQLdb
import pandas as pd
import re
nlu = NaturalLanguageUnderstandingV1(
  username='fb46fb33-3a6b-4ab1-abd3-1d564faee2e7',
  password='X2wDsDxGoBlm',
  version='2018-03-16')

def analyzer(req):
	response = nlu.analyze(
      text=req,
      features=Features(
        sentiment=SentimentOptions(
          targets=['bitcoin','stock','price','ether','crypto','currency','cryptocurrency','cryptocurrencies','ethereum','ICO','coin','coins','blockchain','trade','trades','exchange'])))

	return response['sentiment']['document']['score']



def preproc(body):
    body=body.strip()
    body=re.sub(r'\s(\n){2,}','. ',body)
    body=re.sub(r'(\n)+','. ',body)
    body=re.sub(r'(\xc2\xa0)+',' ',body)
    idx=body.find('image via Shutterstock')
    body=body[:idx]
    idx2=body.rfind('.')
    body=body[:idx2]+"."
    return body

def get_data():
	db = MySQLdb.connect(host="ece457project.chwjf5irbz2p.us-east-2.rds.amazonaws.com",    
	                     user="aiproject2018",         
	                     passwd="aiproject2018",  
	                     db="bitcoinproject")

	cur=db.cursor()
	cur.execute("use bitcoinproject;")
	dt="2018-03-30"
	cur.execute("SELECT * FROM coindesk_articles WHERE date = %s",(dt,))
	a=cur.fetchall()

	table={
	    "id":[i[0] for i in a],
	    "headline":[i[1] for i in a],
	    "body":[i[2] for i in a],
	    "date":[i[3] for i in a]
	}

	for i,j in enumerate(table["body"]):
		table["body"][i]=preproc(j)

	df = pd.DataFrame(table)
	# print(df)
	scores=[]
	for headline,body in zip(table["headline"],table["body"]):
		# print headline
		try:
			scores.append(
				{
				"title":headline,
				"title-score":analyzer(headline),
				"body-score":analyzer(body)
				}
				)
		except Exception as e:
			print("Keyword not found")
	print scores

get_data()
		