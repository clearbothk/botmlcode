class Gimbal_status:
    def __init__(self, y):
        self.y = y["gimbal_status"]
    
    def get_status(self):
        return self.y
    