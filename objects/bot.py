class Bot():

    def __init__(self, state, k=0.005):
        self._state = state
        # self._stoch_state = self._state + np.random.randn(2)
        self.input = [0,0]

        self.k = k


    def update(self):
        self._state[0] += self.k * self.input[0]
        self._state[1] += self.k * self.input[1]
        # self._stoch_state = self._state + np.random.randn(2)

        # reset input gradient
        self.input = [0, 0]


    def stoch_state(self):
        return np.array(self._stoch_state)
