from sentiment_analysis import get_score, analyzer, preproc
import MySQLdb
import pandas as pd
import re
from datetime import datetime,timedelta
from math import tanh
from numpy import random
from MLP import predict

dt=datetime(2017,11,17)

class FeatureEngine(object):
	"""docstring for FeatureEngine"""
	def __init__(self):
		self.db = MySQLdb.connect(host="ece457project.chwjf5irbz2p.us-east-2.rds.amazonaws.com",    
	                     user="aiproject2018",         
	                     passwd="aiproject2018",  
	                     db="bitcoinproject")

	def get_prices(self,date):
		
		data=pd.read_csv('bitcoindata.csv',names=['date','price'])
		time=str(date)[:-3]
		idx=data[data["date"]==time].index[0]
		prices=data.iloc[idx-256:idx]["price"]
		return list(prices)

	def get_dates(self):
		cur=self.db.cursor()
		cur.execute("SELECT * FROM daily_gradient ")
		results=cur.fetchall()
		dates = [i[0] for i in results]
		return dates
	
	def generate_all(self,date):
		sent_score=get_score(str(date.date()))
		if not sent_score:
			return None
		grads=self.get_gradient(date)

		mlp_pred=predict(self.get_prices(date))
		print(mlp_pred)

		features={
		"date":date,
		"sent_score":sent_score,
		"gradient":grads[0],
		"mlp_pred":mlp_pred,
		"next_grad":grads[1]

		}

		return features

	def find_next_week(self,dates,final_date):
		for i,d in enumerate(dates):
			# print d
			if final_date==d:
				final_date=d
				break
			else:
				if i!=len(dates)-1:
					if final_date>d and final_date<dates[i+1]:
						final_date=d
						break
				else:
					final_date=d
		return final_date
		

	def get_gradient(self,dt):
		cur=self.db.cursor()
		cur.execute("SELECT * FROM weekly_gradient ")
		results=cur.fetchall()
		dates = [i[0] for i in results]
		final_date=datetime(dt.year,dt.month,dt.day,23,0,0)
		fd=final_date
		# print final_date
		# final_date=self.find_next_week(dates,final_date)
		query_date=datetime(final_date.year,final_date.month,final_date.day,23,0,0)
		# print query_date
		cur.execute("SELECT gradient from daily_gradient where date = %s", (str(fd),))
		gradient=(cur.fetchall())[0][0]
		# print fd+timedelta(7)
		next_week_date=self.find_next_week(dates,fd+timedelta(7))
		# print next_week_date

		# query_date1=datetime(final_date.year,final_date.month,final_date.day+7,23)
		cur.execute("SELECT gradient,date from weekly_gradient where date = %s", (str(next_week_date),))
		gradient2=(cur.fetchall()) 
		# g=float(gradient2[0][0])
		# print float(gradient),gradient2

		return (tanh(float(gradient)/25),tanh(float(gradient2[0][0])/25))

def fuzzify_res(inp):
	if inp<=-0.25:
		return "NEG"
	elif inp>=0.25:
		return "POS"
	else:
		return "NTR"

def fuzzify_MLP(inp):
	pass

def fuzzify(inp):
	if inp>=-0.2 and inp<=0.2:
		return "NTR"
	elif inp>0.2 and inp<=0.5:
		return "SP"
	elif inp>0.5 and inp<=0.75:
		return "POS"
	elif inp>0.75:
		return "VP"
	elif inp<-0.2 and inp>=-0.5:
		return "SN"
	elif inp<-0.5 and inp>=-0.75:
		return "NEG"
	elif inp<-0.75:
		return "VN"

def classify(packet,results):
	results["date"].append(packet["date"])
	results["G"].append(float(packet["gradient"]))
	results["SA"].append(float(packet["sent_score"]))
	results["MLP"].append(float(packet["mlp_pred"]))
	results["RES"].append(fuzzify_res(packet["next_grad"]))

	print (results["G"][-1],results["SA"][-1],results["RES"][-1],results["MLP"][-1])

def get_current_data():
	df=pd.read_csv("fuzzified2.csv")
	data=dict(df)
	return data

def main():
	results={
	"G":[],
	"SA":[],
	"RES":[],
	"MLP":[],
	"date":[]
	}
	FE=FeatureEngine()
	d=FE.get_dates()
	dates=d[100:len(d)-8]
	# print dates[0],len(dates)
	
	for i in range(500):
		#Generate random date to add to dataset
		date=dates[random.randint(len(dates))]
		feats=FE.generate_all(date)
		if not feats:
			continue
		classify(feats,results)
	df=pd.DataFrame(results)
	df.to_csv('fuzzified4.csv')
	print(df)


if __name__ == '__main__':
	main()

