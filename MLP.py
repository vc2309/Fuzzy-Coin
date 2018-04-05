import csv
import keras
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from random import randint
import numpy as np

num_dates = 256

def train (price_data = [], data_file_name = 'Dataset no dates.csv', train_to_test_ratio = 10):

    # get data if none
    if price_data == []:
        data_file = open(data_file_name, "rU")
        reader = csv.reader(data_file, delimiter=";")
        price_data = [float(row[0]) for row in reader]
        data_file.close

    # pre-processing
    deltas = []
    index = 0
    for price in price_data:
        if index == 0:
            deltas.append(0)
        else:
            delta = price_data[index] - price_data[index - 1]
            if delta >= 0:
                deltas.append(1)
            else:
                deltas.append(0)
        index += 1

    #normalizer = max(deltas)
    #deltas = [delta / normalizer for delta in deltas]

    # split test and train
    x_train = []
    x_test = []
    y_train = []
    y_test = []

    index = 0
    for delta in deltas[num_dates:]:
        x = deltas[index: index + num_dates]
        y = delta

        num = randint(0, train_to_test_ratio)
        if num == 0:
            x_test.append(x)
            y_test.append(y)
        else:
            x_train.append(x)
            y_train.append(y)
        index += 1

    # convert to np array for keras
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_test = np.array(x_test)
    y_test = np.array(y_test)

    # create model
    model = Sequential()
    model.add(Dense(int(num_dates * 2), input_dim = num_dates, activation = 'relu'))
    model.add(Dense(int(num_dates * 2), activation = 'relu'))
    model.add(Dense(int(num_dates * 2), activation = 'relu'))
    model.add(Dense(int(num_dates / 2), activation = 'relu'))
    model.add(Dense(int(num_dates / 8), activation = 'relu'))
    model.add(Dense(int(num_dates / 32), activation = 'relu'))
    model.add(Dense(1, activation = 'relu'))

    # train model
    model.compile(loss = 'mean_squared_error', optimizer = 'adam', metrics=['accuracy'])
    training = model.fit(x_train, y_train, epochs = 16, batch_size = 16, validation_split = 0.1)

    # test model
    scores = model.evaluate(x_test, y_test)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    predictions = model.predict(x_test)
    print(predictions[:10])

    #save model
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")

    return

def predict (recent_price_data = [], data_file_name = 'Dataset no dates.csv'):

    #get data if none
    if len(recent_price_data) == 0:
        data_file = open(data_file_name, "rU")
        reader = csv.reader(data_file, delimiter=";")
        recent_price_data = [float(row[0]) for row in reader]
        recent_price_data = recent_price_data[20:num_dates+20]
        data_file.close
		
    # pre-processing
    deltas = []
    index = 0
    for recent_price in recent_price_data:
        if index == 0:
            deltas.append(0)
        else:
            delta = recent_price_data[index] - recent_price_data[index - 1]
            if delta >= 0:
                deltas.append(1)
            else:
                deltas.append(0)
        index += 1
    
    # convert to np array for keras	
    deltas = np.array([deltas])

    # load network
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
 
    # evaluate loaded model on test data
    loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    prediction = loaded_model.predict(deltas)

    # hard cap at 1
    index = 0
    for predicted_value in prediction:
        if predicted_value > 1:
            predicted_value = 1
            prediction[index] = predicted_value
        index += 1

    print(prediction)
    
    return prediction
# predict()