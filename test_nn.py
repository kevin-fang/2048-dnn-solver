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
model.load('trained_nn.model')

scores = []
choices = []

game = Game()
goal_steps = 20000
for each_game in range(5):
    print("Playing game:", each_game)
    score = 0
    game_memory = []
    prev_obs = []
    game.reset()
    for _ in range(goal_steps):
        choice = None
        if len(prev_obs) == 0:
            action = random.choice(moves)
            choice = np.argmax(action)
        else:
            action = [0, 0, 0, 0]
            choice = np.argmax(model.predict(prev_obs.reshape(-1, 16, 1)))
            action[choice] = 1

        choices.append(choice)

        observation, total, reward, valid = game.oneHotMove(action)
        prev_obs = np.array(observation)
        game_memory.append([observation, action])
        score += reward
        if not valid:
            break
    scores.append(score)
    print("Score:", score)

print('Average score', sum(scores)/len(scores))
print('up: {}, down: {}, left: {}, right: {}'.format(choices.count(0)/len(choices), 
                                        choices.count(1)/len(choices), choices.count(2)/len(choices), choices.count(3)/len(choices)))