Transition = namedtuple("Transition", ("state", "action", "next_state", "reward"))

class ReplayBuffer:

    def __init__(self, capacity: int) -> None:
        self.memory = deque([], maxlen=capacity)
        
    def push(self, *args) -> None:
        """Save a transition"""
       self.memory.append(Transition(*args))
    def sample(self, batch_size) -> list[Transition]:
        return np.random.choice(self.memory, batch_size)
