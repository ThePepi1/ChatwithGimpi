import random
import json
import pickle
import numpy 

import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


lematizer = WordNetLemmatizer

intents = json.loads(open('intens.json').read())

words = []
classes = []
documents =[]
ignore_letters = ['?', '!', '.', ',']


for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag'] ))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


print(documents)