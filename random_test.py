import random
import numpy as np
from statistics import mean, median
from collections import Counter
from game_2048 import Game

LR = 1e-3

up = [1, 0, 0, 0]
down = [0, 1, 0, 0]
left = [0, 0, 1, 0]
right = [0, 0, 0, 1]

moves = [up, down, left, right]

scores = []
choices = []

game = Game()
goal_steps = 20000
training_data = np.load('saved_training.npy')
num_tests = 1000
for each_game in range(num_tests):
    score = 0
    game_memory = []
    prev_obs = []
    game.reset()
    for _ in range(goal_steps):

        action = random.choice(moves)
        choice = np.argmax(action)

        choices.append(choice)

        observation, total, reward, valid = game.oneHotMove(action)
        prev_obs = np.array(observation)
        game_memory.append([observation, action])
        score += reward
        if not valid:
            break
    scores.append(score)
    print('game_num:', each_game, "score:", score)

print('Average score', sum(scores)/len(scores))
print('up: {}, down: {}, left: {}, right: {}'.format(choices.count(0)/len(choices), 
                                        choices.count(1)/len(choices), choices.count(2)/len(choices), choices.count(3)/len(choices)))