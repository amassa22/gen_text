import string
from random import randint
from numpy import array
from pickle import load, dump
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding


# TODO: train on news dataset --> https://www.kaggle.com/datasets/snapcrack/all-the-news

# load doc into memory
def load_doc(filename):
    # open the file as read only
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text
 
# turn a doc into clean tokens
def clean_doc(doc):
    # replace '--' with a space ' '
    doc = doc.replace('--', ' ')
    # split into tokens by white space
    tokens = doc.split()
    # remove punctuation from each token
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    # make lower case
    tokens = [word.lower() for word in tokens]
    print('Total Tokens: %d' % len(tokens))
    print('Unique Tokens: %d' % len(set(tokens)))
    return tokens
 
# save tokens to file, one dialog per line
def save_doc(lines, filename="sequences.txt"):
    data = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()

def tokens_to_sequences(tokens, length=51):
    sequences = list()
    for i in range(length, len(tokens)):
        # select sequence of tokens
        seq = tokens[i-length:i]
        # convert into a line
        line = ' '.join(seq)
        # store
        sequences.append(line)
    print('Total Sequences: %d' % len(sequences))
    return sequences


def create_model(vocab_size, seq_length):
    model = Sequential()
    model.add(Embedding(vocab_size, 50, input_length=seq_length))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(vocab_size, activation='softmax'))
    print(model.summary())
    return model


def main():
    # load document
    books = [
        "adventures_of_huckleberry_finn.txt",
        "adventures_of_tom_sawyer.txt",
        "life_on_the_mississippi.txt"
    ]

    for b in books:
        print("Prepping Book: '{}'".format(b))
        in_filename = "books/{}".format(b)
        doc = load_doc(in_filename)
        doc = load_doc(in_filename)
        # clean document
        tokens = clean_doc(doc)
        # organize into sequences of tokens
        sequences = tokens_to_sequences(tokens, length=51)
        # save sequences to file
        save_doc(sequences)

    # load
    in_filename = 'sequences.txt'
    doc = load_doc(in_filename)
    lines = doc.split('\n')
    
    # integer encode sequences of words
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)
    sequences = tokenizer.texts_to_sequences(lines)
    # vocabulary size
    vocab_size = len(tokenizer.word_index) + 1
    
    # separate into input and output
    sequences = array(sequences)
    X, y = sequences[:,:-1], sequences[:,-1]
    # X, y = sequences[:30,:-1], sequences[:30,-1] # TEST
    y = to_categorical(y, num_classes=vocab_size)
    seq_length = X.shape[1]

    # create model
    model = create_model(vocab_size, seq_length)
    # compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # # fit model
    model.fit(X, y, batch_size=64, epochs=200)
    
    # # save the model to file
    model.save('model.h5')
    # # save the tokenizer
    dump(tokenizer, open('tokenizer.pkl', 'wb'))


# run
main()
