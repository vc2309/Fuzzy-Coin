import numpy as np
import skfuzzy.control as ctrl
import skfuzzy as fuzz

#Universe variables
x_sent_score = np.arange(-1, 1, 0.001)
x_gradient = np.arange(-1, 1, 0.001)
x_stockchange  = np.arange(-1, 1, 0.001)

sent_score=ctrl.Antecedent(x_sent_score,'sent_score')
gradient=ctrl.Antecedent(x_gradient,'gradient')
stockchange=ctrl.Consequent(x_sent_score,'stockchange')

#Defining membership functions for each fuzzy variable

sent_score['VP']=fuzz.trimf(sent_score.universe,[0.75,1,1])
sent_score['POS']=fuzz.trimf(sent_score.universe,[0.5,0.625,0.8])
sent_score['SP']=fuzz.trimf(sent_score.universe,[0.25,0.375,0.5])
sent_score['NTR']=fuzz.trimf(sent_score.universe,[-0.25,0,0.25])
sent_score['SN']=fuzz.trimf(sent_score.universe,[-0.5,-0.375,-0.25])
sent_score['NEG']=fuzz.trimf(sent_score.universe,[-0.8,-0.625,-0.5])
sent_score['VN']=fuzz.trimf(sent_score.universe,[-1,-1,-0.75])

gradient['VP']=fuzz.trimf(gradient.universe,[0.75,1,1])
gradient['POS']=fuzz.trimf(gradient.universe,[0.5,0.625,0.8])
gradient['SP']=fuzz.trimf(gradient.universe,[0.2,0.375,0.53])
gradient['NTR']=fuzz.trimf(gradient.universe,[-0.25,0,0.25])
gradient['SN']=fuzz.trimf(gradient.universe,[-0.5,-0.375,-0.2])
gradient['NEG']=fuzz.trimf(gradient.universe,[-0.8,-0.625,-0.53])
gradient['VN']=fuzz.trimf(gradient.universe,[-1,-1,-0.75])

# sent_score['VP']=fuzz.gaussmf(sent_score.universe,1,0.2)
# sent_score['POS']=fuzz.gaussmf(sent_score.universe,0.625,0.1)
# sent_score['SP']=fuzz.gaussmf(sent_score.universe,0.35,0.1)
# sent_score['NTR']=fuzz.gaussmf(sent_score.universe,0,0.1)
# sent_score['SN']=fuzz.gaussmf(sent_score.universe,-1,0.2)
# sent_score['NEG']=fuzz.gaussmf(sent_score.universe,-0.625,0.1)
# sent_score['VN']=fuzz.gaussmf(sent_score.universe,-0.35,0.1)

# gradient['VP']=fuzz.gaussmf(gradient.universe,1,0.2)
# gradient['POS']=fuzz.gaussmf(gradient.universe,0.625,0.1)
# gradient['SP']=fuzz.gaussmf(gradient.universe,0.35,0.1)
# gradient['NTR']=fuzz.gaussmf(gradient.universe,0,0.1)
# gradient['SN']=fuzz.gaussmf(gradient.universe,-1,0.2)
# gradient['NEG']=fuzz.gaussmf(gradient.universe,-0.625,0.1)
# gradient['VN']=fuzz.gaussmf(gradient.universe,-0.35,0.1)

# stockchange['NTR']=fuzz.gaussmf(stockchange.universe,0,0.15)
# stockchange['POS']=fuzz.gaussmf(stockchange.universe,0.625,0.2)
# stockchange['NEG']=fuzz.gaussmf(stockchange.universe,-0.625,0.2)
stockchange['NTR']=fuzz.trimf(stockchange.universe,[-0.3,0,0.3])
stockchange['POS']=fuzz.trimf(stockchange.universe,[0.275,1,1])
stockchange['NEG']=fuzz.trimf(stockchange.universe,[-1,-1,-0.275])

#Defining the fuzzy inferencing rules
rule=[]
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
rule.append(ctrl.Rule(sent_score['NTR'] & gradient['NEG'], stockchange['NEG']))
rule.append(ctrl.Rule(sent_score['SN'] & gradient['NTR'], stockchange['NTR']))
rule.append(ctrl.Rule(sent_score['SP'] & gradient['NTR'], stockchange['NTR']))
rule.append(ctrl.Rule(sent_score['NTR'] & gradient['SN'], stockchange['NTR']))
rule.append(ctrl.Rule(sent_score['NTR'] & gradient['SP'], stockchange['NTR']))
StockControl = ctrl.ControlSystem(rule)
Stock=ctrl.ControlSystemSimulation(StockControl)



# Stock.input['sent_score']=0.30480534375
# Stock.input['gradient']=-0.06943366459623272

# Stock.compute()
# print(Stock.output)

import pandas as pd
def fuzzify_res(inp):
	if inp<=-0.3:
		return "NEG"
	elif inp>=0.3:
		return "POS"
	else:
		return "NTR"

def tester():
	df=pd.read_csv("fuzzified3.csv")
	score=0
	tot=float((len(df))-1)
	for i in range(len(df)):
		sent_score=df.iloc[i]["SA"]
		gradient=df.iloc[i]["G"]
		res=df.iloc[i]["RES"]
		Stock.input['sent_score']=sent_score
		Stock.input['gradient']=gradient
		
		try:
			Stock.compute()
		except Exception as e:
			print sent_score,gradient
			print("error")
			tot-=1
			
		pred=fuzzify_res(Stock.output["stockchange"])
		if pred==res:
			score+=1
		else:
			print sent_score,gradient,res,pred,Stock.output["stockchange"]
	print(score)
	# tot=float((len(df))-1)
	acc=float((score/tot))*100
	# print((score/tot)*100)
	print("Accuracy = {}%".format(acc))

tester()

	