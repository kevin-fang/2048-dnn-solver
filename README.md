# 2048-solver
An 2048 solver using TensorFlow and its abstraction library TFLearn. The 2048 game is implemented (and I believe it works fine), but the neural network is currently not working.

## How to run

Note that TensorFlow, TFLearn, and NumPy are all required dependencies.

To generate training data, run `python generate_training_data.py`.

To train the neural net on the generated training data, run `python train_nn.py`

Once the neural net is trained, you can check the accuracy by running `python test_nn.py`. 

If you want to see how well the neural net does compared to a random player, try `python random_test.py`.

With the neural net testing, for some reason it will hit a max accuracy of about .55 with a loss around 1. When testing is done, the score is about 160 over 1000 runs. For reference, a random player will get on average 180.

### How it works/how it's supposed to work:

`generate_training_data.py` produces a numpy array called `saved_training.npy` containing random games, that had a threshold of at least `score_requirement`. Each entry in the numpy array looks like:
```
    [[0, 2, 4, 8, 2, 8, 4, 8, 16, 32, 2, 4, 8, 16, 32, 64], [0, 1, 0, 0]]
```

Where the first element is the flattened (raveled) array of the 2048 game, and the second element is a one-hotted array of the move made at that position, with the positions meaning [up, down, left, right].

`train_nn.py` opens `saved_training.npy` and trains the neural net using the following formula with the model provided in `nn_model.py`, and saves the model in `models/trained_nn.model`.

`test_nn.py` opens the model located at `models/trained_nn.model` and runs 1000 (or whatever `num_tests` is) games and calculates the average accuracy and the amount that each button was pressed