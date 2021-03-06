from tensorflow.keras.models import load_model
from pickle import load, dump
from random import randint
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import streamlit as st



def index():
    # load cleaned text sequences
    in_filename = 'sequences.txt'
    doc = load_doc(in_filename)
    lines = doc.split('\n')
    seq_length = len(lines[0].split()) - 1
    
    # select a seed text
    seed_text = lines[randint(0,len(lines))]
    print(seed_text + '\n')
    
    # generate new text
    generated = generate_seq(seq_length, seed_text, 50)
    print(generated)
    result = {
        "Input:": seed_text,
        "Generated": generated
    }
    return result


# load doc into memory
def load_doc(filename):
    # open the file as read only
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text


# generate a sequence from a language model
def generate_seq(model, tokenizer, seq_length, seed_text, n_words):
    result = list()
    in_text = seed_text
    # generate a fixed number of words
    for _ in range(n_words):
        # encode the text as integer
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        # truncate sequences to a fixed length
        encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
        # predict probabilities for each word
        # Deprecated
        #yhat = model.predict_classes(encoded, verbose=0)
        yhat = np.argmax(model.predict(encoded), axis=-1)
        # map predicted word index to word
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
        # append to input
        in_text += ' ' + out_word
        result.append(out_word)
    return ' '.join(result)


model = load_model("model.h5")
tokenizer = load(open("tokenizer.pkl", "rb"))

if __name__ == "__main__":
    #model = load_model("model.h5")
    #tokenizer = load(open("tokenizer.pkl", "rb"))
    
    input_text = st.text_input('Input Text', 'I love')
    output_length = st.slider('Output Length', 1, 100, 5)
    if st.button("Generate Text!"):
        seq_length = len(input_text.split()) - 1
        generated = generate_seq(model, tokenizer, seq_length, input_text, output_length)
        st.write(generated)
