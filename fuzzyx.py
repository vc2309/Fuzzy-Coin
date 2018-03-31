import numpy as np
import skfuzzy.control as ctrl
import skfuzzy as fuzz

#Universe variables
x_headline = np.arange(-3, 4, 1)
x_mlp = np.arange(-3, 4, 1)
x_stockchange  = np.arange(0, 4, 1)

headline=ctrl.Antecedent(x_headline,'headline')
mlp=ctrl.Antecedent(x_mlp,'mlp')
stockchange=ctrl.Consequent(x_headline,'stockchange')

#Defining membership functions for each fuzzy variable

headline['neg']=fuzz.trapmf(headline.universe, [-3,-2,-1,0])
headline['ntr']=fuzz.trapmf(headline.universe, [-0.5,0,1,1.5])
headline['pos']=fuzz.trapmf(headline.universe, [0.5,1,2,3])

mlp['bear']=fuzz.trapmf(mlp.universe, [-3,-2,-1,0])
mlp['same']=fuzz.trapmf(mlp.universe, [-0.5,0,1,1.5])
mlp['bull']=fuzz.trapmf(mlp.universe, [0.5,1,2,3])

stockchange['drop']=fuzz.trimf(stockchange.universe, [-3,-1.5,0])
stockchange['same']=fuzz.trimf(stockchange.universe, [-0.5,0.5,1.5])
stockchange['rise']=fuzz.trimf(stockchange.universe, [1,2,3])


#Defining the fuzzy inferencing rules
rule1 = ctrl.Rule(headline['neg'] | mlp['bear'], stockchange['drop'])
rule2 = ctrl.Rule(headline['ntr'] & mlp['same'], stockchange['same'])
rule3 = ctrl.Rule(headline['ntr'] & mlp['bull'], stockchange['rise'])
rule4 = ctrl.Rule(headline['pos'] & mlp['bull'], stockchange['rise'])
rule5 = ctrl.Rule(headline['pos'] & mlp['same'], stockchange['same'])

StockControl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
Stock=ctrl.ControlSystemSimulation(StockControl)

Stock.input['headline']=3
Stock.input['mlp']=-2.9

Stock.compute()
print(Stock.output)