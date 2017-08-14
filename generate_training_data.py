import random
import numpy as np
from statistics import mean, median
from collections import Counter
from game_2048 import Game, moves

# max number of steps for the game to run
goal_steps = 20000
# requirement for score to be added to the training data
score_requirement = 300

initial_games = 1000000

game = Game(testing=False)

def generate_initial_population():
    # [observations, moves]
    training_data = []

    # all scores
    scores = []
    # all choices made
    choices = []

    # scores above threashold
    accepted_scores = []

    for i in range(initial_games):
        score = 0
        # [observation, action]
        game_memory = []
        prev_observation = []

        # loop until hit max number of steps
        for step in range(goal_steps):
            # generate an action. If it's unvalid (i.e., reward == 0), make a different choice.
            action = random.choice(moves)
            observation, total, reward, valid = game.oneHotMove(action)
            while (reward == 0):
                action = random.choice(moves)
                observation, total, reward, valid = game.oneHotMove(action)

            choices.append(movesEnglish[np.argmax(action)])

            # if there has been a previous observation, add the observation and the action made.
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

            for data in game_memory:
                # scale the board and add to training data
                board = np.array(data[0])
                board = game.scale(board)
                training_data.append([board.ravel(), np.array(data[1])])

        game.reset()
        scores.append(score)

    # save the training data
    training_data_save = np.array(training_data)
    np.save('saved_training_less.npy', training_data_save)

    # print diagnostics information
    print('Average accepted score:', mean(accepted_scores))
    print('Median score for accepted scores:',median(accepted_scores))
    print(Counter(accepted_scores))
    print(Counter(choices))

    return training_data

if __name__ == '__main__':
    generate_initial_population()
