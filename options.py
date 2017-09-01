class Options:
    def __init__(self):
        self.op = {"exprender": ("Use Experimental Fast Render", False)}
    def update(self, *args, **kwargs):
        for ar in kwargs:
            self.op[ar] = (self.op[ar][0], kwargs[ar])
    def get(self, arg):
        return self.op[arg][1]
    def listopt(self):
        return [(x, self.op[x][0], self.op[x][1]) for x in self.op]
    def __eq__(self, other):
        return self.op == other.op
