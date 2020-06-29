class Ekf_ok:
    def __init__(self, y):
        self.y = y["EKF_OK"]
    
    def get_ekf(self):
        return self.y