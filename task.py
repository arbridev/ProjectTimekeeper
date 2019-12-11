class Task():

    id = None
    start = None
    end = None
    description = None

    def __init__(self, id, start=None, end=None, description=None):
        self.id = id
        self.start = start
        self.end = end
        self.description = description

    def __repr__(self):
        return str(self.__dict__)