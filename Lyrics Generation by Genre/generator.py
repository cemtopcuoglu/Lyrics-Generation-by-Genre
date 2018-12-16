from __future__ import print_function
import numpy as np
import random
import sys
from keras.models import load_model
import DLmodel
import time
from pathlib import Path
import sys

Steps = 20
Temperature = 1.0
SENTENCE = 40
SENTENCEStep = 3
genre = sys.argv[1]
path = genre + ".txt"
Temperature = float(sys.argv[2])

Lyrics = DLmodel.read_lyrics(path)  #with this step we get the lyrics from given genre

lyricsc = DLmodel.extract_Lyricsc(Lyrics)   # we got the chars which is unique in the text

sentence , nextLyricsc = DLmodel.newSentences(Lyrics, SENTENCE , SENTENCEStep)  # sentence is the sentences with different sequences , nextLyricsc is the char that come after this sentences

char_index , index_char = DLmodel.get_char_index(lyricsc) # this is like dictionary we have the indexes for each char


X,Y = DLmodel.vectorize(sentence, SENTENCE, lyricsc, char_index, nextLyricsc)
dlmodel = DLmodel.model_builder(SENTENCE, lyricsc)

my_file = Path("custom.h5")


if str(genre) == "custom" and not my_file.exists():
    dlmodel.fit(X, Y, batch_size = 128, epochs=Steps)
    dlmodel.save('custom.h5')
else :
    dlmodel = load_model(genre+".h5")



for Temperature in [Temperature]:
    print()
    print('----- Temperature:', Temperature)
    
    generatedL = ''
    startings = ""
    if len(sys.argv) == 3:
        startings = "I was standing over there thinking about"
    else:
        if len(sys.argv[3]) == 40:
            startings = sys.argv[3]
        else:
            print("you need to enter a string which has length = 40")
            exit()
    
    startings = startings.lower()
    generatedL = generatedL + startings
    print('Starting sentence is: ' + startings)
    sys.stdout.write(generatedL)
    
    for i in range(400):
        x = np.zeros((1, SENTENCE, len(lyricsc)))
        for h, char in enumerate(startings):
            x[0, h, char_index[char]] = 1.
    
        predictions = dlmodel.predict(x, verbose =0)[0]
        index_n = DLmodel.sampling(predictions, Temperature)
        char_n = index_char[index_n]
        
        generatedL = generatedL + char_n
        startings = startings[1:] + char_n
        
        sys.stdout.write(char_n)
    sys.stdout.flush()
print()

