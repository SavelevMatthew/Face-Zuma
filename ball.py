class Ball:
    def __init__(self, ball_type, radius, pos, status=0):
        self.pos = pos
        self.type = ball_type
        self.r = radius
        self.goal = 1
        self.status = status

    def move(self, dx, dy):
        """
        Moves ball by changing coords on (dx, dy)

        dx, dy - coordinates of ball center
        """
        pos = self.pos
        self.pos = (pos[0] + dx, pos[1] + dy)
