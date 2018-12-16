import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
import io



def model_builder(sequence_length, chars):
    model = Sequential()
    model.add(LSTM(128, input_shape=(sequence_length, len(chars))))
    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))
        
    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    return model


def sampling(preds, temperature=1.0):
    if temperature == 0:
        temperature = 1

    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def read_lyrics(path):
    
    with io.open(path,'r', encoding= 'utf8') as text:
        LYRICS = text.read().lower()
        return LYRICS


def extract_Lyricsc(lyrics):
    return sorted(list(set(lyrics)))

def newSentences(lyrics, SENTENCE , SENTENCEStep):
    sentences = []
    NextChars = []
    for i in range(0, len(lyrics)- SENTENCE, SENTENCEStep):
        sentences.append(lyrics[i: i + SENTENCE])
        NextChars.append(lyrics[i + SENTENCE])
    return sentences, NextChars


def get_char_index(lyricsc):
    return dict((y, x) for x, y in enumerate(lyricsc)), dict((x, y) for x, y in enumerate(lyricsc))

def vectorize(sentence, SENTENCE, lyricsc, char_index, nextLyricsc):
    X = np.zeros((len(sentence),SENTENCE, len(lyricsc)), dtype = np.bool)
    Y = np.zeros((len(sentence),len(lyricsc)),dtype=np.bool)
    for i, s in enumerate(sentence):
        for t, c in enumerate(s):
            X[i, t, char_index[c]] = 1
        Y[i, char_index[nextLyricsc[i]]] = 1

    return X, Y
