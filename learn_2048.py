import random
import numpy as np
import gym
#import tflearn
#from tflearn.layers.core import input_data, dropout, fully_connected
#from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
from game_2048 import Game

LR = 1e-3

goal_steps = 100000
score_requirement = 120

up = [1, 0, 0, 0]
down = [0, 1, 0, 0]
left = [0, 0, 1, 0]
right = [0, 0, 0, 1]

moves = [up, down, left, right]

initial_games = 500

game = Game(False)

def some_random_games_first():
    for episode in range(5):
        game.reset()
        for _ in range(goal_steps):
            action = random.choice(moves)
            observation, score, highest, valid = game.oneHotMove(action)
            print(observation, score, highest, valid)
            if not valid:
                break

#some_random_games_first()

def generate_initial_population():
    # [observations, moves]
    training_data = []

    # all scores
    scores = []

    # scores above threashold
    accepted_scores = []

    for i in range(initial_games):
        score = 0
        # [observation, action]
        game_memory = []
        prev_observation = []

        for _ in range(goal_steps):
            action = random.choice(moves)
            observation, total, reward, valid = game.oneHotMove(action)

            if len(prev_observation) > 0:
                game_memory.append([prev_observation, action])
            prev_observation = observation
            score = total
            if not valid:
                print("not valid; block total:", total, "score", score)
                break

        if score >= score_requirement:
            print("score", score, "iter:", i, "accepted len:", len(accepted_scores) + 1)
            accepted_scores.append(score)
                # [observation, action]
            for data in game_memory:
                training_data.append([data[0], data[1]])

        game.reset()
        scores.append(score)


    training_data_save = np.array(training_data)
    np.save('saved_training.npy', training_data_save)

    print('Average accepted score:', mean(accepted_scores))
    print('Median score for accepted scores:',median(accepted_scores))
    print(Counter(accepted_scores))
    
    return training_data

generate_initial_population()
