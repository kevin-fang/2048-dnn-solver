import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
from game_2048 import Game
from nn_model import neural_network_model

LR = 1e-3

up = [1, 0, 0, 0]
down = [0, 1, 0, 0]
left = [0, 0, 1, 0]
right = [0, 0, 0, 1]

moves = [up, down, left, right]

model = neural_network_model(16)
model.load('models/trained_nn.model')

scores = []
choices = []

game = Game()
goal_steps = 20000
num_tests = 1000

def test_run():
    random_moves = 0
    for each_game in range(num_tests):
        score = 0
        prev_obs = []
        game.reset()
        for _ in range(goal_steps):
            choice = None
            if len(prev_obs) == 0:
                action = random.choice(moves)
                choice = np.argmax(action)
            else:
                action = [0, 0, 0, 0]
                choice = np.argmax(model.predict(game.scale(prev_obs).reshape(-1, 16, 1)))
                action[choice] = 1


            observation, total, reward, valid = game.oneHotMove(action)
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
        print('game_num:', each_game, "score:", score)

    print('Average score', sum(scores)/len(scores))
    print('up: {}, down: {}, left: {}, right: {}'.format(choices.count(0)/len(choices), 
                                            choices.count(1)/len(choices), choices.count(2)/len(choices), choices.count(3)/len(choices)))
    print("Num random:", random_moves, "total moves:", len(choices))

if __name__ == "__main__":
    test_run()