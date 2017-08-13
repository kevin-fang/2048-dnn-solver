import random
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from nn_model import neural_network_model
from statistics import median, mean
from collections import Counter

def train_model(training_data, model=False):
    # get training data from numpy array training_data
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]), 1)
    y = [i[1] for i in training_data]

    # if there isn't a pretrained model, give it one
    if not model:
        model = neural_network_model(input_size = len(X[0]))
    
    model.fit({'input': X}, {'targets': y}, n_epoch=5, snapshot_step=500, show_metric=True, run_id='2048_learning')
    return model

def run_train():
    training_data = np.load('saved_training.npy')
    model = train_model(training_data)
    model.save('models/trained_nn.model')

if __name__ == "__main__":
    run_train()