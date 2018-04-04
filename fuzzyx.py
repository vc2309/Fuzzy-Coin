import numpy as np
import skfuzzy.control as ctrl
import skfuzzy as fuzz
from matplotlib.pyplot import savefig
#Universe variables
x_sent_score = np.arange(-1, 1, 0.001)
x_gradient = np.arange(-1, 1, 0.001)
x_mlp = np.arange(0,1.0,0.001)
x_stockchange  = np.arange(-1, 1, 0.001)


sent_score=ctrl.Antecedent(x_sent_score,'sent_score')
gradient=ctrl.Antecedent(x_gradient,'gradient')
mlp=ctrl.Antecedent(x_mlp,'mlp')
stockchange=ctrl.Consequent(x_sent_score,'stockchange')

#Defining membership functions for each fuzzy variable

def tri_mfs():
	sent_score['VP']=fuzz.trimf(sent_score.universe,[0.75,1,1])
	sent_score['POS']=fuzz.trimf(sent_score.universe,[0.5,0.625,0.8])
	sent_score['SP']=fuzz.trimf(sent_score.universe,[0.25,0.375,0.5])
	sent_score['NTR']=fuzz.trimf(sent_score.universe,[-0.25,0,0.25])
	sent_score['SN']=fuzz.trimf(sent_score.universe,[-0.5,-0.375,-0.25])
	sent_score['NEG']=fuzz.trimf(sent_score.universe,[-0.8,-0.625,-0.5])
	sent_score['VN']=fuzz.trimf(sent_score.universe,[-1,-1,-0.75])
	sent_score.view()
	savefig("tri_sent_score")

	gradient['VP']=fuzz.trimf(gradient.universe,[0.75,1,1])
	gradient['POS']=fuzz.trimf(gradient.universe,[0.5,0.625,0.8])
	gradient['SP']=fuzz.trimf(gradient.universe,[0.2,0.375,0.53])
	gradient['NTR']=fuzz.trimf(gradient.universe,[-0.25,0,0.25])
	gradient['SN']=fuzz.trimf(gradient.universe,[-0.53,-0.375,-0.2])
	gradient['NEG']=fuzz.trimf(gradient.universe,[-0.8,-0.625,-0.53])
	gradient['VN']=fuzz.trimf(gradient.universe,[-1,-1,-0.75])
	gradient.view()
	savefig("tri_gradient")

	mlp['DRP']=fuzz.trimf(mlp.universe,[0,0,0.15])
	mlp['NTR']=fuzz.trimf(mlp.universe,[0.12,0.2,0.3])
	mlp['SLI']=fuzz.gaussmf(mlp.universe,0.55,0.1)
	mlp['HI']=fuzz.trimf(mlp.universe,[0.75,1.0,1.0])
	mlp.view()
	savefig('mlp')

	stockchange['NTR']=fuzz.trimf(stockchange.universe,[-0.3,0,0.3])
	stockchange['POS']=fuzz.trimf(stockchange.universe,[0.275,1,1])
	stockchange['NEG']=fuzz.trimf(stockchange.universe,[-1,-1,-0.275])
	stockchange.view()
	savefig("tri_stockchange")

	

def gauss_mfs():
	sent_score['VP']=fuzz.gaussmf(sent_score.universe,1,0.075)
	sent_score['POS']=fuzz.gaussmf(sent_score.universe,0.625,0.075)
	sent_score['SP']=fuzz.gaussmf(sent_score.universe,0.35,0.075)
	sent_score['NTR']=fuzz.gaussmf(sent_score.universe,0,0.075)
	sent_score['SN']=fuzz.gaussmf(sent_score.universe,-1,0.075)
	sent_score['NEG']=fuzz.gaussmf(sent_score.universe,-0.625,0.075)
	sent_score['VN']=fuzz.gaussmf(sent_score.universe,-0.35,0.075)
	sent_score.view()
	savefig("gauss_sent_score")


	gradient['VP']=fuzz.gaussmf(gradient.universe,1,0.075)
	gradient['POS']=fuzz.gaussmf(gradient.universe,0.625,0.075)
	gradient['SP']=fuzz.gaussmf(gradient.universe,0.35,0.075)
	gradient['NTR']=fuzz.gaussmf(gradient.universe,0,0.075)
	gradient['SN']=fuzz.gaussmf(gradient.universe,-1,0.075)
	gradient['NEG']=fuzz.gaussmf(gradient.universe,-0.625,0.075)
	gradient['VN']=fuzz.gaussmf(gradient.universe,-0.35,0.075)

	gradient.view()
	savefig("gauss_gradient")

	mlp['DRP']=fuzz.trimf(mlp.universe,[0,0,0.15])
	mlp['NTR']=fuzz.trimf(mlp.universe,[0.12,0.2,0.3])
	mlp['SLI']=fuzz.gaussmf(mlp.universe,0.55,0.1)
	mlp['HI']=fuzz.trimf(mlp.universe,[0.75,1.0,1.0])
	mlp.view()
	savefig('mlp')

	stockchange['NTR']=fuzz.gaussmf(stockchange.universe,0,0.15)
	stockchange['POS']=fuzz.gaussmf(stockchange.universe,0.625,0.2)
	stockchange['NEG']=fuzz.gaussmf(stockchange.universe,-0.625,0.2)

	stockchange.view()
	savefig("gauss_stockchange")


#Defining the fuzzy inferencing rules
rule=[]

def SA_G():
	
	rule.append( ctrl.Rule(gradient['VN'],stockchange["NEG"]))
	rule.append( ctrl.Rule(gradient['VP'],stockchange["POS"]))
	rule.append( ctrl.Rule(sent_score['VN'] | gradient['VN'], stockchange['NEG']))
	rule.append( ctrl.Rule(sent_score['VP'] | gradient['VP'], stockchange['POS']))
	rule.append( ctrl.Rule(sent_score['NTR'] & gradient['NTR'], stockchange['NTR']))
	rule.append( ctrl.Rule(sent_score['NTR'] & gradient['SP'], stockchange['NTR']))
	rule.append( ctrl.Rule(sent_score['NTR'] & gradient['VP'], stockchange['NTR']))
	rule.append( ctrl.Rule(sent_score['SN'] & gradient['SN'], stockchange['NEG']))
	rule.append( ctrl.Rule(sent_score['SP'] & gradient['SN'], stockchange['POS']))
	rule.append( ctrl.Rule(sent_score['SN'] & gradient['SP'], stockchange['POS']))
	rule.append( ctrl.Rule(sent_score['NTR'] & gradient['SN'], stockchange['NTR']))
	rule.append( ctrl.Rule(sent_score['SP'] & gradient['SP'], stockchange['POS']))
	rule.append( ctrl.Rule(sent_score['SN'] & gradient['SN'], stockchange['NEG']))
	rule.append( ctrl.Rule(sent_score['NEG'] & gradient['SN'], stockchange['NEG']))
	rule.append( ctrl.Rule(sent_score['POS'] & gradient['SN'], stockchange['POS']))
	rule.append( ctrl.Rule(sent_score['POS'] & gradient['SP'], stockchange['POS']))
	rule.append( ctrl.Rule(sent_score['POS'] & gradient['POS'], stockchange['POS']))
	rule.append( ctrl.Rule(sent_score['SN'] & gradient['POS'], stockchange['NTR']))
	rule.append( ctrl.Rule(sent_score['SP'] & gradient['POS'], stockchange['POS']))
	rule.append( ctrl.Rule(sent_score['SN'] & gradient['POS'], stockchange['NTR']))
	rule.append( ctrl.Rule(sent_score['NEG'] & gradient['NEG'], stockchange['NEG']))
	rule.append( ctrl.Rule(sent_score['NEG'] & gradient['POS'], stockchange['POS']))
	rule.append( ctrl.Rule(sent_score['NEG'] & gradient['SN'], stockchange['NEG']))
	rule.append( ctrl.Rule(sent_score['NEG'] & gradient['SP'], stockchange['NTR']))
	rule.append( ctrl.Rule(sent_score['SN'] & gradient['NEG'], stockchange['NEG']))
	rule.append( ctrl.Rule(sent_score['SP'] & gradient['NEG'], stockchange['NTR']))
	rule.append( ctrl.Rule(sent_score['POS'] & gradient['NEG'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['POS'] & gradient['NTR'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['NTR'] & gradient['POS'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['NEG'] & gradient['NTR'], stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['NTR'] & gradient['NEG'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['SN'] & gradient['NTR'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['SP'] & gradient['NTR'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['NTR'] & gradient['SN'], stockchange['NTR']))

def SA_MLP():
	rule.append(ctrl.Rule(sent_score['SP'] & mlp['DRP'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['SN'] & mlp['DRP'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['POS'] & mlp['HI'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['SN'] & mlp['DRP'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['NEG'] & mlp['DRP'], stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['VN'] & mlp['DRP'], stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['POS'] & mlp['DRP'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['NTR'] & mlp['DRP'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['VN'], stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['VP'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['SP'] & mlp['SLI'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['SN'] & mlp['NTR'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['SN'] & mlp['HI'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['NEG'] & mlp['HI'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['NEG'] & mlp['SLI'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['NEG'] & (mlp ['DRP'] | mlp['NTR']), stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['SN'] & (mlp ['DRP'] | mlp['NTR']), stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['POS'] & (mlp ['DRP'] | mlp['NTR']), stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['SP'] & (mlp ['DRP'] | mlp['NTR']), stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['SP'] & (mlp ['HI'] | mlp['SLI']), stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['SN'] & (mlp ['HI'] | mlp['SLI']), stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['NEG'] & (mlp ['HI'] | mlp['SLI']), stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['POS'] & (mlp ['HI'] | mlp['SLI']), stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['NTR'] & (mlp ['HI'] | mlp['SLI']), stockchange['POS']))
	

def SA_MLP_G():
	rule.append(ctrl.Rule(sent_score['NTR'] & mlp['HI'] & gradient['NTR'], stockchange['NTR']))
	rule.append(ctrl.Rule(gradient['POS'] & mlp['SLI'], stockchange['POS']))
	rule.append(ctrl.Rule(gradient['POS'] & mlp['HI'], stockchange['POS']))
	rule.append(ctrl.Rule(gradient['NTR'] & mlp['NTR'], stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['SP'] & mlp['DRP'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['SN'] & mlp['DRP'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['POS'] & mlp['HI'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['SN'] & mlp['DRP'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['NEG'] & mlp['DRP'], stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['VN'] & mlp['DRP'], stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['POS'] & mlp['DRP'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['NTR'] & mlp['DRP'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['VN'], stockchange['NEG']))
	rule.append(ctrl.Rule(sent_score['VP'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['SP'] & mlp['SLI'], stockchange['POS']))
	rule.append(ctrl.Rule(sent_score['SN'] & mlp['NTR'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['SN'] & mlp['HI'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['NEG'] & mlp['HI'], stockchange['NTR']))
	rule.append(ctrl.Rule(sent_score['NEG'] & mlp['SLI'], stockchange['NTR']))
	SA_G()

	
import pandas as pd
def fuzzify_res(inp):
	if inp<=-0.3:
		return "NEG"
	elif inp>=0.3:
		return "POS"
	else:
		return "NTR"


def print_rules():
	for i,r in enumerate(rule):
		r.view()
		savefig('SA_G_rule'+str(i))

import sys
def tester():
	#DEFINE MFS

	tri_mfs()
	# gauss_mfs()

	#SET RULEBASE
	# SA_G()
	# SA_MLP()
	SA_MLP_G()

	StockControl = ctrl.ControlSystem(rule)
	Stock=ctrl.ControlSystemSimulation(StockControl)

	df=pd.read_csv("fuzzified4.csv")
	score=0
	tot=float((len(df))-1)
	for i in range(len(df)):
		sent_score=df.iloc[i]["SA"]
		gradient=df.iloc[i]["G"]
		res=df.iloc[i]["RES"]
		mlp=df.iloc[i]["MLP"]
		Stock.input['sent_score']=sent_score
		Stock.input['gradient']=gradient
		Stock.input['mlp']=mlp
		
		try:
			Stock.compute()	
			# stockchange.view(sim=Stock)
			# savefig("output")
		except Exception as e:
			print (sent_score,gradient)
			print("error")
			tot-=1
			
		pred=fuzzify_res(Stock.output["stockchange"])
		if pred==res:
			score+=1
		
	# print(score)
	
	acc=float((score/tot))*100
	
	print("Accuracy = {}%".format(acc))

tester()

	