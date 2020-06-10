import time
import re
import random

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
        self.status = 'stopped'

    def process(self, cmd):
        """process an action from the action queue"""
        raise NotImplementedError

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

    def start(self, refresh_mode):
        """start the training"""
        super().start()
        assert refresh_mode in ["all", "random"], f"Unsupported refresh_mode '{refresh_mode}'"
        self.refresh_mode = refresh_mode
        self._reset_all_targets()
        self._enable_all_targets()

    def process(self, cmd):
        """process actions"""
        gui = self.state['gui']

        # only process when in running state
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

            # if all targets have been shot, restore targets
            if all(map(lambda target: target['color'] == 'red', gui['target'])):
                if self.refresh_mode == "all":
                    self._enable_all_targets()
                elif self.refresh_mode == "random":
                    ctrl          = self.state['controller']
                    gui           = self.state['gui']
                    num_targets   = len(gui['target'])
                    random_target = random.randint(0, num_targets - 1)
                    ctrl.set_target(random_target, 'ENABLED')
                    gui['target'][random_target]['color'] = 'green'

class TimedMode(PracticeMode):
    # Timed mode is the same as practice mode
    # All differences are in the client side
    pass


class CountdownMode(TrainingMode):
    """Count down training mode"""
    def __init__(self, state):
        """Constructor"""
        super().__init__(state)

    def start(self, refresh_mode, countdown_speed):
        """start the training"""
        super().start()
        self.refresh_mode    = refresh_mode
        self.countdown_speed = countdown_speed
        assert refresh_mode in ["all", "random"], f"Unsupported refresh_mode '{refresh_mode}'"
        self._reset_all_targets()
        gui = self.state['gui']
        ctrl = self.state['controller']
        ctrl.set("TIMER_INTERVAL", countdown_speed)
        num_targets = len(gui['target'])
        for i in range(num_targets):
            ctrl.set_target(i, 'TIMED')
            gui['target'][i]['color'] = 'green'

    def process(self, cmd):
        """process actions"""
        gui  = self.state['gui']
        ctrl = self.state['controller']

        print(f"countdown process(): cmd = {cmd}")
        # only process when in running state
        if self.status == "running":
            hit_status_match = re.search(r'RSP_HIT_STATUS\s+(\d+)\s+(\d+)', cmd)
            countdown_expired_match = re.search(r'RSP_COUNTDOWN_EXPIRED\s+(\d+)\s+(\d+)', cmd)

            # update the target status
            if hit_status_match:
                tid = int(hit_status_match.group(1))
                val = int(hit_status_match.group(2))
                if val == 1:
                    gui['target'][tid]['score'] += 1
                    gui['total_score']          += 1
                    gui['target'][tid]['color'] = 'red'
            elif countdown_expired_match:
                tid = int(countdown_expired_match.group(1))
                val = int(countdown_expired_match.group(2))
                if val == 1:
                    gui['target'][tid]['color'] = 'lightgrey'

            # if all targets have been shot, restore red targets
            if len(list(filter(lambda target: target['color'] == 'green', gui['target']))) == 0:
                red_targets = [(idx, target) for idx, target in enumerate(gui['target']) if target['color'] == 'red']
                if len(red_targets) > 0:
                    if self.refresh_mode == "all":
                        for idx, target in red_targets:
                            ctrl.set_target(idx, 'TIMED')
                            gui['target'][idx]['color'] = 'green'
                    elif self.refresh_mode == "random":
                        idx, target = random.choice(red_targets)
                        ctrl.set_target(idx, 'TIMED')
                        gui['target'][idx]['color'] = 'green'
