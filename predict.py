from RNNTheano import RNNTheano
import csv
import glob
import os
import nltk
import numpy as np
import itertools


newest = max(glob.iglob('data/*'), key=os.path.getctime)

MESSAGE_START = "MESSAGE_START"
MESSAGE_END = "MESSAGE_END"
VOCABULARY_SIZE = 8000
UNKNOWN_TOKEN = "??????"

user_messages = []
all_messages = []

for file in os.listdir("extracted_data/"):
    if file.endswith(".csv"):
        with open('extracted_data/'+file,'r', encoding="utf8") as currcsv:
            tab = csv.reader(currcsv)
            for row in tab:
                if "Ritvik Annam" in row[0]:
                    user_messages.append("%s %s %s" % (MESSAGE_START, str("".join(row[4:])).replace("&#039;","'").replace("&quot;",'"').lower(), MESSAGE_END))

tokenized_messages = [nltk.word_tokenize(sentence) for sentence in user_messages]

word_freq = nltk.FreqDist(itertools.chain(*tokenized_messages))

print ("Unique word tokens: %d" % len(word_freq))

vocab = word_freq.most_common(VOCABULARY_SIZE-1)

index_to_word = [x[0] for x in vocab]
index_to_word.append(UNKNOWN_TOKEN)
word_to_index = dict([(word,index) for index,word in enumerate(index_to_word)])

def load_model_parameters_theano(path, model):
    npzfile = np.load(path)
    U, V, W = npzfile["U"], npzfile["V"], npzfile["W"]
    model.hidden_dim = U.shape[0]
    model.word_dim = U.shape[1]
    model.U.set_value(U)
    model.V.set_value(V)
    model.W.set_value(W)
    print ("Loaded model parameters from %s. hidden_dim=%d word_dim=%d" % (path, U.shape[0], U.shape[1]))


model = RNNTheano(VOCABULARY_SIZE, hidden_dim = 80)

load_model_parameters_theano(newest, model)

def generate_sentence(model):
    # We start the sentence with the start token
    new_sentence = [word_to_index[MESSAGE_START]]
    # Repeat until we get an end token
    while not new_sentence[-1] == word_to_index[MESSAGE_END]:
        next_word_probs = model.forward_propagation(new_sentence)
        sampled_word = word_to_index[UNKNOWN_TOKEN]
        # We don't want to sample unknown words
        while sampled_word == word_to_index[UNKNOWN_TOKEN]:
            samples = np.random.multinomial(1, next_word_probs[-1])
            sampled_word = np.argmax(samples)
        new_sentence.append(sampled_word)
        print(" ".join([index_to_word[x] for x in new_sentence[1:-1]]))
    sentence_str = [index_to_word[x] for x in new_sentence[1:-1]]
    return sentence_str

for i in range(10):
    sent = generate_sentence(model)
    # We want long sentences, not sentences with one or two words
    print (" ".join(sent))