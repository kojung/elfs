class TrainingMode():
    """Base class for all training modes"""
    def __init__(self, state):
        """Constructor"""
        self.state = state

    def start(self):
        """start the training"""
        raise NotImplementedError

    def stop(self):
        """stop the training"""
        raise NotImplementedError

    def process(self):
        """process an action from the action queue"""
        raise NotImplementedError

class PracticeMode(TrainingMode):
    """Practice training mode"""
    def __init__(self, state):
        """Constructor"""
        super().__init__(state)

    def start(self):
        """start the training"""
        pass

    def stop(self):
        """stop the training"""
        pass

    def process(self):
        """stop the training"""
        pass


class TimedMode(TrainingMode):
    """Timed training mode"""
    def __init__(self, state):
        """Constructor"""
        super().__init__(state)

    def start(self):
        """start the training"""
        pass

    def stop(self):
        """stop the training"""
        pass

    def process(self):
        """stop the training"""
        pass


class CountdownMode(TrainingMode):
    """Count down training mode"""
    def __init__(self, state):
        """Constructor"""
        super().__init__(state)

    def start(self):
        """start the training"""
        pass

    def stop(self):
        """stop the training"""
        pass

    def process(self):
        """stop the training"""
        pass
