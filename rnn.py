import os
import nltk
import itertools
import csv
import time
import numpy as np
from RNNTheano import RNNTheano
from utils import *
MESSAGE_START = "MESSAGE_START"
MESSAGE_END = "MESSAGE_END"
VOCABULARY_SIZE = 5000
UNKNOWN_TOKEN = "??????"

ritvik_messages = []
all_messages = []

for file in os.listdir("ritvik/new/"):
    if file.endswith(".csv"):
        with open('ritvik/new/'+file,'r', encoding="utf8") as currcsv:
            tab = csv.reader(currcsv)
            for row in tab:
                if "Ritvik" in row[0]:
                    ritvik_messages.append("%s %s %s" % (MESSAGE_START, str("".join(row[4:])).replace("&#039;","'").replace("&quot;",'"').lower(), MESSAGE_END))


# print(ritvikMessages)

#Not using the sentance beraker upper because each message is in and of itself a "sentance"
# sentences = itertools.chain(*[sent for sent in nltk.sent_tokenize(ritvikMessages)])

tokenized_messages = [nltk.word_tokenize(sentence) for sentence in ritvik_messages]

word_freq = nltk.FreqDist(itertools.chain(*tokenized_messages))

print ("Unique word tokens: %d" % len(word_freq))

vocab = word_freq.most_common(VOCABULARY_SIZE-1)

# print([x[0] for x in word_freq.most_common(100)])

index_to_word = [x[0] for x in vocab]
index_to_word.append(UNKNOWN_TOKEN)
word_to_index = dict([(word,index) for index,word in enumerate(index_to_word)])

for i, sent in enumerate(tokenized_messages):
    tokenized_messages[i] = [w if w in word_to_index else UNKNOWN_TOKEN for w in sent]


def train_with_sgd(model, X_train, y_train, learning_rate=0.005, nepoch=1, evaluate_loss_after=5):
    # We keep track of the losses so we can plot them later
    losses = []
    num_examples_seen = 0
    for epoch in range(nepoch):
        # Optionally evaluate the loss
        if (epoch % evaluate_loss_after == 0):
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
            save_model_parameters_theano("./data/rnn-theano-%d-%d-%s.npz" % (model.hidden_dim, model.word_dim, time), model)
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

train_with_sgd(model, X_train, y_train, nepoch=1, learning_rate=0.005)
