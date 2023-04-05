import random
import json
import pickle
import numpy

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lematizer = WordNetLemmatizer()

intens = json.loads(open('intens.json' , encoding="utf-8").read())

words = pickle.load(open('words.pickle', 'rb'))
classes = pickle.load(open('classes.pickle', 'rb'))
model = load_model('chat-bot.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lematizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words) 
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
    return(numpy.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words)
    res = model.predict(numpy.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intents": classes[r[0]], "probability": str(r[1])})
    return return_list


def get_responses(intents_list, intents_json):
    tag = intents_list[0]['intents']
    list_of_intents = intents_json['intents']    
    result = ''
    for intent in list_of_intents:
        if tag == intent['tag']:
            result = random.choice(intent['responses'])
            break

    return result


print('Bot is running')

def message(message):
    inits = predict_class(message, model)
    print(inits)
    res = get_responses(inits, intens)
    print(res)  
    return res