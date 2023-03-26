import random
import json
import pickle
import numpy 

import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers.legacy import SGD


lematizer = WordNetLemmatizer()

intents = json.loads(open('intens.json',encoding="utf-8").read())

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
words = [lematizer.lemmatize(word) for word in words if word  not in ignore_letters]
words = sorted(set(words))
#print(words)
classes = sorted(set(classes))

pickle.dump(words, open('words.pickle' , "wb"))
pickle.dump(classes, open('classes.pickle' ,'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_pattern = document[0]
    word_pattern = [lematizer.lemmatize(word.lower()) for word in word_pattern]
    for word in words:
        bag.append(1) if word in word_pattern else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
    


random.shuffle(training)
training = numpy.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])
                        
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation ='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hits = model.fit(numpy.array(train_x), numpy.array(train_y), epochs=200, batch_size=5, verbose= 1)
model.save('chat-bot.h5', hits)
print("Done")
