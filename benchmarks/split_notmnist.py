import numpy as np
import gzip
import pickle
from scipy.io import loadmat

class SplitNotMNIST():
    def __init__(self):
        f = gzip.open('data/notMNIST_small.pkl.gz', 'rb')
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        train_set, valid_set, test_set = u.load()
        f.close()

        self.X_train = train_set[0]
        self.X_valid = valid_set[0]
        self.X_test = test_set[0]

        self.train_label = train_set[1]
        self.valid_label = valid_set[1]
        self.test_label = test_set[1]

        self.sets_0 = ['A', 'B', 'C', 'D', 'E']
        self.sets_1 = ['F', 'G', 'H', 'I', 'J']
        self.max_iter = len(self.sets_0)
        self.cur_iter = 0

    def get_dims(self):
        # Get data input and output dimensions
        return self.X_train.shape[1], 2

    def next_task(self):
        if self.cur_iter >= self.max_iter:
            raise Exception('Number of tasks exceeded!')
        else:
            # Retrieve train data
            train_0_id = np.where(self.train_label == self.sets_0[self.cur_iter])[0]
            train_1_id = np.where(self.train_label == self.sets_1[self.cur_iter])[0]
            next_x_train = np.vstack((self.X_train[train_0_id], self.X_train[train_1_id]))

            next_y_train = np.vstack((np.ones((train_0_id.shape[0], 1)), np.zeros((train_1_id.shape[0], 1))))
            next_y_train = np.hstack((next_y_train, 1-next_y_train))

            # Retrieve validation data
            valid_0_id = np.where(self.valid_label == self.sets_0[self.cur_iter])[0]
            valid_1_id = np.where(self.valid_label == self.sets_1[self.cur_iter])[0]
            next_x_valid = np.vstack((self.X_valid[valid_0_id], self.X_valid[valid_1_id]))
            
            next_y_valid = np.vstack((np.ones((valid_0_id.shape[0], 1)), np.zeros((valid_1_id.shape[0], 1))))
            next_y_valid = np.hstack((next_y_valid, 1-next_y_valid))

            # Retrieve test data
            test_0_id = np.where(self.test_label == self.sets_0[self.cur_iter])[0]
            test_1_id = np.where(self.test_label == self.sets_1[self.cur_iter])[0]
            next_x_test = np.vstack((self.X_test[test_0_id], self.X_test[test_1_id]))

            next_y_test = np.vstack((np.ones((test_0_id.shape[0], 1)), np.zeros((test_1_id.shape[0], 1))))
            next_y_test = np.hstack((next_y_test, 1-next_y_test))

            self.cur_iter += 1

            next_x_train = np.vstack((next_x_train, next_x_valid, next_x_test))
            next_y_train = np.vstack((next_y_train, next_y_valid, next_y_test))

            return next_x_train, next_y_train, next_x_train, next_y_train, next_x_train, next_y_train