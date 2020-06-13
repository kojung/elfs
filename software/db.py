import pickle
import os.path

class DB():
    def __init__(self):
        """Constructor"""
        self.filename = "stats.pickle"
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.db = pickle.load(f)
        else:
            self.db = {}

    def add(self, user, mode, distance, time, score):
        """Add an entry into the database"""
        # only store if user is defined
        name = user if user != "" else "noname"
        
        if name not in self.db:
            self.db[name] = {}

        if mode not in self.db[name]:
            self.db[name][mode] = {}

        if distance not in self.db[name][mode]:
            self.db[name][mode][distance] = []

        self.db[name][mode][distance].append((time, score))
        
        with open(self.filename, "wb") as f:
            pickle.dump(self.db, f)
