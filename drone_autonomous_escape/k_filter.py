from pykalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt


class K_Filter(object):

    def __init__(self):

        self.cap = 0
        self.refresh = 100
        self.delete = 1000
        self.count_to_refresh = self.refresh
        self.measurements_a = np.asarray([(0, 0), (0, 0)])

        self.measurements_b = np.asarray([(0, 0), (0, 0)])

        initial_state_mean = [self.measurements_a[0, 0],
                              0,
                              self.measurements_a[0, 1],
                              0]

        transition_matrix = [[1, 1, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 1],
                             [0, 0, 0, 1]]

        observation_matrix = [[1, 0, 0, 0],
                              [0, 0, 1, 0]]

        self.kf1 = KalmanFilter(transition_matrices=transition_matrix,
                                observation_matrices=observation_matrix,
                                initial_state_mean=initial_state_mean)
        self.kf2 = KalmanFilter(transition_matrices=transition_matrix,
                                observation_matrices=observation_matrix,
                                initial_state_mean=initial_state_mean)

        self.kf1 = self.kf1.em(self.measurements_a, n_iter=self.cap)
        self.kf2 = self.kf2.em(self.measurements_b, n_iter=self.cap)

    def show(self):

        plt.figure(1)
        times = range(self.measurements_a.shape[0])
        plt.plot(times, self.measurements_a[:, 0], 'bo',
                 times, self.measurements_a[:, 1], 'ro',
                 times, self.smoothed_state_means_a[:, 0], 'b--',
                 times, self.smoothed_state_means_a[:, 2], 'r--', )
        # plt.show()

        plt.figure(1)
        times = range(self.measurements_b.shape[0])
        plt.plot(times, self.measurements_b[:, 0], 'bo',
                 times, self.measurements_b[:, 1], 'ro',
                 times, self.smoothed_state_means_b[:, 0], 'b--',
                 times, self.smoothed_state_means_b[:, 2], 'r--', )
        # plt.show()

    def add_update_get(self, input):
        """ get tuple (1,1,3,4)-> split (1,1), (3,4) -> update and predition

        :param input:
        :return:
        """
        input_a = input[:2]
        input_b = input[2:]
        add_a = np.asarray([input_a])
        add_b = np.asarray([input_b])
        self.measurements_a = np.vstack((self.measurements_a, add_a))
        self.measurements_b = np.vstack((self.measurements_b, add_b))
        if self.count_to_refresh == self.refresh:
            self.count_to_refresh = 0
            self.kf1 = self.kf1.em(self.measurements_a, n_iter=self.cap)
            self.kf2 = self.kf2.em(self.measurements_b, n_iter=self.cap)
        else:
            self.count_to_refresh += 1
        (self.smoothed_state_means_a, smoothed_state_covariances) = self.kf1.smooth(self.measurements_a)
        (self.smoothed_state_means_b, smoothed_state_covariances) = self.kf2.smooth(self.measurements_b)
        return self.smoothed_state_means_a[:, 0][-1], self.smoothed_state_means_a[:, 2][-1], \
               self.smoothed_state_means_b[:, 0][-1], self.smoothed_state_means_b[:, 2][-1]


kk = K_Filter()
for i in range(300):
    # x = np.random.rand(1)[0]
    #
    # if x<0.2:
    #     y = np.random.uniform(100)
    #     z = np.random.uniform(100)
    #     print(kk.add_update_get((i,i+y,i,i-z)))
    # else:
    print(kk.add_update_get((i, i + 1, i, i + 2)))

kk.show()
