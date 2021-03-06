import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

# this file is needed so train and test have the same model.

learning_rate = 1e-3 

def neural_network_model(input_size):

    network = input_data(shape=[None, input_size, 1], name='input')

    network = fully_connected(network, 16, activation='relu')
    #network = dropout(network, 0.8)
    network = fully_connected(network, 32, activation='relu')
    
    network = fully_connected(network, 16, activation='relu')

    network = fully_connected(network, 4, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy', name='targets') 

    model = tflearn.DNN(network, tensorboard_dir='log')

    return model