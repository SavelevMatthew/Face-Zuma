class Ball:
    def __init__(self, type, radius, pos, status=0):
        self.pos = pos
        self.type = type
        self.r = radius
        self.goal = 1
        self.status = status

    def move(self, dx, dy):
        pos = self.pos
        self.pos = (pos[0] + dx, pos[1] + dy)
