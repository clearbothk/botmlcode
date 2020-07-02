class Firmware_version:
    def __init__(self, y):
        #self.y = y["firmware_version"]
        self.y = y[0]
    
    def get_version(self):
        return self.y
    