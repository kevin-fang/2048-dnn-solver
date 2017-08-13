import random
import numpy as np
from statistics import mean, median
from collections import Counter
from game_2048 import Game

LR = 1e-3

goal_steps = 20000
score_requirement = 300

up = [1, 0, 0, 0]
down = [0, 1, 0, 0]
left = [0, 0, 1, 0]
right = [0, 0, 0, 1]

movesEnglish = ['up', 'down', 'left', 'right']
moves = [up, down, left, right]

initial_games = 100000

game = Game(False)

def generate_initial_population():
    # [observations, moves]
    training_data = []

    # all scores
    scores = []
    choices = []

    # scores above threashold
    accepted_scores = []

    for i in range(initial_games):
        score = 0
        # [observation, action]
        game_memory = []
        prev_observation = []

        for step in range(goal_steps):
            action = random.choice(moves)
            observation, total, reward, valid = game.oneHotMove(action)
            choices.append(movesEnglish[np.argmax(action)])

            if len(prev_observation) > 0:
                game_memory.append([observation, action])
            prev_observation = observation
            score += reward
            if not valid:
                #print("not valid; block total:", score)
                break

        if score >= score_requirement:
            print("score", score, "total:", total, "iter:", i, "accepted len:", len(accepted_scores) + 1)
            accepted_scores.append(score)
                # [observation, action]
            for data in game_memory:
                #print(data[0])
                board = np.array(data[0])
                board = game.scaled(board)
                training_data.append([board.ravel(), np.array(data[1])])

        game.reset()
        scores.append(score)


    training_data_save = np.array(training_data)
    np.save('saved_training.npy', training_data_save)

    print('Average accepted score:', mean(accepted_scores))
    print('Median score for accepted scores:',median(accepted_scores))
    print(Counter(accepted_scores))
    print(Counter(choices))

    return training_data

if __name__ == '__main__':
    generate_initial_population()
