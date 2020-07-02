class Ekf_ok:
    def __init__(self, y):
        self.y = y[10]
    
    def get_ekf(self):
        return self.y