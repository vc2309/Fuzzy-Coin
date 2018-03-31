# Fuzzy-Coin
Project aimed at building a system of web scrapers, MLPs and fuzzy logic systems to predict the changes in Bitcoin stock prices based on sentiment analysis of Bitcoin related web articles/news headlines


## Process

1. Sentiment Analysis Using IBM Watson
	- `pip install --upgrade watson-developer-cloud`
	- https://www.ibm.com/watson/developercloud/natural-language-understanding/api/v1/?python#introduction
	- Query AWS DB to get all entries from start date - end date
	- Feed text into API, entry by entry
	- Aggregate scores
	- Feed into fuzzy system

2. Fuzzy Control System
	- Using python package skfuzzy http://pythonhosted.org/scikit-fuzzy/
	- Define Fuzzy variables, membership functions and rules of inference
	- Store in .fcl file (optional but helps in documentation)
	- Script using skfuzzy
