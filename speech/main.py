import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import sys

# load ascii text and covert to lowercase
filename = "braquo.txt"
raw_text = open(filename).read()
raw_text = raw_text.lower()

# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
# print "chars : ", chars , "\n"



char_to_int = dict((c, i) for i, c in enumerate(chars))

# print "char to int :",char_to_int
# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
# print "Total Characters: ", n_chars
# print "Total Vocab: ", n_vocab
# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
	seq_in = raw_text[i:i + seq_length]
	seq_out = raw_text[i + seq_length]
	dataX.append([char_to_int[char] for char in seq_in])
	dataY.append(char_to_int[seq_out])

n_patterns = len(dataX)
# print "Total Patterns: ", n_patterns
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
# define the checkpoint
# filepath="weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
# checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
# callbacks_list = [checkpoint]

# # fit the model
# model.fit(X, y, epochs=50, batch_size=64, callbacks=callbacks_list)

filename = "weights-improvement-42-1.3614-bigger.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

int_to_char = dict((i, c) for i, c in enumerate(chars))
inv_dict = {v: k for k, v in int_to_char.items()}

# start = numpy.random.randint(0, len(dataX)-1)
# pattern = dataX[start]
# pattern = [40, 37, 44, 44, 47, 2, 45, 57, 2, 36, 37, 33, 50, 2, 38, 50, 41, 37, 46, 36, 14, 2, 40, 37, 44, 44, 47, 2, 45, 57, 2, 36, 37, 33, 50, 2, 38, 50, 41, 37, 46, 36, 14, 2, 41, 2, 40, 33, 54, 37, 46, 8, 52, 2, 51, 37, 37, 46, 2, 57, 47, 53, 2, 38, 47, 50, 2, 33, 2, 55, 40, 41, 44, 37, 14, 2, 40, 47, 55, 2, 41, 51, 2, 44, 41, 38, 37, 2, 39, 47, 41, 46, 39, 2, 28, 2, 36, 47, 2, 57]
# pattern_braquo = [2, 22, 1, 29, 24, 18, 1, 12, 24, 22, 22, 14, 23, 29, 1, 12, 10, 1, 31, 10, 1, 13, 14, 25, 30, 18, 28, 1, 29, 24, 30, 29, 1, 12, 14, 1, 29, 14, 22, 25, 28, 1, 9, 1, 19, 4, 10, 18, 1, 14, 23, 29, 14, 23, 13, 30, 1, 13, 18, 27, 14, 1, 26, 30, 14, 1, 29, 30, 1, 29, 27, 10, 18, 23, 10, 18, 28, 1, 13, 10, 23, 28, 1, 13, 14, 28, 1, 29, 27, 30, 12, 28, 1, 10, 28, 28, 14, 35, 1, 21]
# pattern=pattern_braquo







def generate_text(pattern,n_vocab,model):
	for i in range(100):
		x = numpy.reshape(pattern, (1, len(pattern), 1))
		print "x : ",x
		x = x / float(n_vocab)
		prediction = model.predict(x, verbose=0)
		index = numpy.argmax(prediction)
		result = int_to_char[index]
		seq_in = [int_to_char[value] for value in pattern]
		sys.stdout.write(result)
		pattern.append(index)
		pattern = pattern[1:len(pattern)]
	return pattern






# print "Int to char : ",int_to_char, "\n"
# print "Seed:"
# print "\"", ''.join([int_to_char[value] for value in pattern]), "\""
# # generate characters
# print "Generation de texte : \n"

def ask_and_answer():
	encoded_input =[]
	input_text = raw_input('reponse : ')
	
	for i in input_text.lower():
		encoded_input.append(inv_dict[i])
	
	if len(encoded_input) > 100:	
		encoded_input = encoded_input[0:100]
	
	input_text = encoded_input
	
	generate_text(pattern=input_text,n_vocab=n_vocab,model=model)

for i in range(3):
	ask_and_answer()
