class Gimbal_status:
    def __init__(self, y):
        self.y = y[8]
    
    def get_status(self):
        return self.y
    