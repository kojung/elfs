import time
import re

class TrainingMode():
    """Base class for all training modes"""
    def __init__(self, state):
        """Constructor"""
        self.state = state
        self.status = 'stopped'

    def start(self):
        """start the training"""
        self.status = 'running'

    def stop(self):
        """stop the training"""
        self._stop_timer()
        self.status = 'stopped'

    def process(self, cmd):
        """process an action from the action queue"""
        raise NotImplementedError

    def _update_timer(self, stop_value, curr_value):
        """Pause timer and update the stop and current value. Resume afterwards"""
        timer = self.state['timer']
        timer['pause_timer'] = True
        time.sleep(1)
        timer['stop_value']  = stop_value
        timer['curr_value']  = curr_value
        timer['pause_timer'] = False
        
    def _stop_timer(self):
        """Pause timer without resetting value"""
        timer = self.state['timer']
        timer['pause_timer'] = True

    def _reset_all_targets(self):
        """reset all targets to 0"""
        gui = self.state['gui']
        ctrl = self.state['controller']
        gui['total_score'] = 0
        num_targets = len(gui['target'])
        for i in range(num_targets):
            ctrl.set_target(i, 'DISABLED')
            gui['target'][i]['score'] = 0
            gui['target'][i]['color'] = 'lightgray'

    def _enable_all_targets(self):
        """set all target to given mode without altering the score"""
        gui = self.state['gui']
        ctrl = self.state['controller']
        num_targets = len(gui['target'])
        for i in range(num_targets):
            ctrl.set_target(i, 'ENABLED')
            gui['target'][i]['color'] = 'green'

class PracticeMode(TrainingMode):
    """Practice training mode"""
    def __init__(self, state):
        """Constructor"""
        super().__init__(state)

    def start(self):
        """start the training"""
        super().start()
        # practice has no time limit
        self._reset_all_targets()
        self._enable_all_targets()
        self._update_timer(stop_value=-1, curr_value=0)

    def process(self, cmd):
        """process actions"""
        timer = self.state['timer']
        gui = self.state['gui']

        # only process when timer is running
        if self.status == "running":
            hit_status_match = re.search(r'RSP_HIT_STATUS\s+(\d+)\s+(\d+)', cmd)
            # update the target status
            if hit_status_match:
                tid = int(hit_status_match.group(1))
                val = int(hit_status_match.group(2))
                if val == 1:
                    gui['target'][tid]['score'] += 1
                    gui['total_score']          += 1
                    gui['target'][tid]['color'] = 'red'

            # if all targets have been shot, restore all targets
            if all(map(lambda target: target['color'] == 'red', gui['target'])):
                self._enable_all_targets()

class TimedMode(TrainingMode):
    """Timed training mode"""
    def __init__(self, state):
        """Constructor"""
        super().__init__(state)

    def start(self, time_limit):
        """start the training"""
        super().start()
        # set timer to time_limit
        self._enable_all_targets()
        self._update_timer(stop_value=time_limit, curr_value=0)

    def process(self, cmd):
        """process actions"""
        pass


class CountdownMode(TrainingMode):
    """Count down training mode"""
    def __init__(self, state):
        """Constructor"""
        super().__init__(state)

    def start(self):
        """start the training"""
        super().start()
        # count down does not need timer
        self._reset_all_targets()
        self._update_timer(stop_value=0, curr_value=-3)

    def process(self, cmd):
        """process actions"""
        pass
