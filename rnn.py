import nltk
import itertools
import csv
import time
import numpy as np
from datetime import datetime
import sys
import os
from RNNTheano import RNNTheano

MESSAGE_START = "MESSAGE_START"
MESSAGE_END = "MESSAGE_END"
VOCABULARY_SIZE = 8000
UNKNOWN_TOKEN = "??????"

user_messages = []
all_messages = []

print(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

for file in os.listdir("extracted_data/"):
    if file.endswith(".csv"):
        with open('extracted_data/'+file,'r', encoding="utf8") as currcsv:
            tab = csv.reader(currcsv)
            for row in tab:
                if "Ritvik Annam" in row[0]:
                    user_messages.append("%s %s %s" % (MESSAGE_START, str("".join(row[4:])).replace("&#039;","'").replace("&quot;",'"').lower(), MESSAGE_END))


# print(ritvikMessages)

#Not using the sentance beraker upper because each message is in and of itself a "sentance"
# sentences = itertools.chain(*[sent for sent in nltk.sent_tokenize(ritvikMessages)])

tokenized_messages = [nltk.word_tokenize(sentence) for sentence in user_messages]

word_freq = nltk.FreqDist(itertools.chain(*tokenized_messages))

print ("Unique word tokens: %d" % len(word_freq))

vocab = word_freq.most_common(VOCABULARY_SIZE-1)

# print([x[0] for x in word_freq.most_common(100)])

index_to_word = [x[0] for x in vocab]
index_to_word.append(UNKNOWN_TOKEN)
word_to_index = dict([(word,index) for index,word in enumerate(index_to_word)])

for i, sent in enumerate(tokenized_messages):
    tokenized_messages[i] = [w if w in word_to_index else UNKNOWN_TOKEN for w in sent]

def softmax(x):
    xt = np.exp(x - np.max(x))
    return xt / np.sum(xt)

def save_model_parameters_theano(outfile, model):
    U, V, W = model.U.get_value(), model.V.get_value(), model.W.get_value()
    np.savez(outfile, U=U, V=V, W=W)
    print ("Saved model parameters to %s." % outfile)

def load_model_parameters_theano(path, model):
    npzfile = np.load(path)
    U, V, W = npzfile["U"], npzfile["V"], npzfile["W"]
    model.hidden_dim = U.shape[0]
    model.word_dim = U.shape[1]
    model.U.set_value(U)
    model.V.set_value(V)
    model.W.set_value(W)
    print ("Loaded model parameters from %s. hidden_dim=%d word_dim=%d" % (path, U.shape[0], U.shape[1]))

def train_with_sgd(model, X_train, y_train, learning_rate=0.005, nepoch=1, evaluate_loss_after=5):
    # We keep track of the losses so we can plot them later
    losses = []
    num_examples_seen = 0
    for epoch in range(nepoch):
        # Optionally evaluate the loss
        if (True):
            loss = model.calculate_loss(X_train, y_train)
            losses.append((num_examples_seen, loss))
            time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            print ("%s: Loss after num_examples_seen=%d epoch=%d: %f" % (time, num_examples_seen, epoch, loss))
            # Adjust the learning rate if loss increases
            if (len(losses) > 1 and losses[-1][1] > losses[-2][1]):
                learning_rate = learning_rate * 0.5
                print ("Setting learning rate to %f" % learning_rate)
            sys.stdout.flush()
            # ADDED! Saving model oarameters
            save_model_parameters_theano("data/rnn-theano-%d-%d-%s.npz" % (model.hidden_dim, model.word_dim, time), model)
        # For each training example...
        for i in range(len(y_train)):
            # One SGD step
            model.sgd_step(X_train[i], y_train[i], learning_rate)
            num_examples_seen += 1

# Create the training data
X_train = np.asarray([[word_to_index[w] for w in sent[:-1]] for sent in tokenized_messages])
y_train = np.asarray([[word_to_index[w] for w in sent[1:]] for sent in tokenized_messages])

model = RNNTheano(VOCABULARY_SIZE, hidden_dim = 80)
t1 = time.time()
model.sgd_step(X_train[1], y_train[1], 0.005)
t2 = time.time()
print ("SGD Step time: %f milliseconds" % ((t2 - t1) * 1000.))

train_with_sgd(model, X_train, y_train, nepoch=100, learning_rate=0.005)

#tesla 11 acapella walked lying fucked distracting calculations garunt lock byron authkey= krape prizes builder acceptable registering git d ent memoir ted groove experiment solubility trees detail company girl eness expo gola beast weekend loved turn refrence solve like copies s loss wilburn cuz oprah angle tan npr removed coins cracking chilling appointed isil parodies kelly mid schoolers banquet workshop scholars magazine giong file yahoo computers bill nap particles unlucky ohhhh ter alec crash hail brawl obamer toucans du disgusting caltech drugs