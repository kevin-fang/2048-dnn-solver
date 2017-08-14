import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
from game_2048 import Game, moves
from nn_model import neural_network_model

model = neural_network_model(16)
model.load('models/trained_nn.model')

scores = []
choices = []

game = Game()
goal_steps = 20000 # max number of steps
num_tests = 1000 # number of tests to amke

def test_run():
    random_moves = 0 # counter for number of times the model predicated an impossible move

    for each_game in range(num_tests):
        score = 0
        prev_obs = []
        game.reset()
        for _ in range(goal_steps):

            choice = None
            # if there wasn't a previous prediction, make a random choice
            if len(prev_obs) == 0:
                action = random.choice(moves)
                choice = np.argmax(action)
            else: # predict a move based on the board state based on the neural network
                action = [0, 0, 0, 0]
                choice = np.argmax(model.predict(game.scale(prev_obs).reshape(-1, 16, 1)))
                action[choice] = 1

            observation, total, reward, valid = game.oneHotMove(action)
            # if the move was invalid (i.e., reward was 0), make a random choice.
            while reward == 0:
                action = random.choice(moves)
                random_moves += 1
                choice = np.argmax(action)
                observation, total, reward, valid = game.oneHotMove(action)
                
                #print('bad guess')

            choices.append(choice)

            prev_obs = np.array(observation)
            score += reward
            if not valid:
                break
        scores.append(score)
        print('game_num:', each_game, "score:", score) #diagnostics information

    # print game statistics
    print('Average score', sum(scores)/len(scores))
    print('up: {}, down: {}, left: {}, right: {}'.format(choices.count(0)/len(choices), 
                                            choices.count(1)/len(choices), choices.count(2)/len(choices), choices.count(3)/len(choices)))
    print("num random moves:", random_moves, "num NN moves:", len(choices) - random_moves)

if __name__ == "__main__":
    test_run()