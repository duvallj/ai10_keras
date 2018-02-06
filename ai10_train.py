from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import numpy as np

import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('--base_dir', type=str, default='.',
                    help='Directory where to load all files out of')

parser.add_argument('--epochs', type=int, default=20,
                    help='Number of epochs to run.')

parser.add_argument('--batch_size', type=int, default=128,
                    help='Batch size to use.')
                    
parser.add_argument('--dropout', type=float, default=0.3,
                    help='Amount of dropout to use.')

def make_model():
    model = Sequential()
    
    model.add(Dense(1024, input_dim=64))
    model.add(Activation('relu'))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(FLAGS.dropout))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(FLAGS.dropout))
    model.add(Dense(13))
    model.add(Activation('softmax'))
    
    return model
    
def compile(model):
    model.compile(
        optimizer='rmsprop',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
def train(model, data, labels):
    model.fit(data, labels, epochs=FLAGS.epochs, batch_size=FLAGS.batch_size)
    
def evaluate(model, data, labels):
    return model.evaluate(data, labels, batch_size=FLAGS.batch_size)
    
def load_train_data():
    train_files = [os.path.join(FLAGS.base_dir, file) for file in os.listdir(FLAGS.base_dir) \
        if os.path.isfile(os.path.join(FLAGS.base_dir, file)) and file.startswith("train")]
    data = None
    labels = None
    for file in train_files:
        file_data = np.load(file)
        if data is not None: data = np.concatenate((data, file_data['x_train']))
        else: data = file_data['x_train']
        if labels is not None: labels = np.concatenate((labels, file_data['y_train']))
        else: labels = file_data['y_train']
        
    return data, labels
    
def load_test_data():
    data = None
    lables = None
    return data, labels
    
def main():
    model = make_model()
    compile(model)
    data, labels = load_train_data()
    train(model, data, labels)
    #data, labels = load_test_data()
    print(evaluate(model, data, labels))
    model.save("model1.h5")
    

if __name__ == "__main__":
    FLAGS = parser.parse_args()
    main()