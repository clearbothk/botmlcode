class Firmware_version:
    def __init__(self, y):
        self.y = y["firmware_version"]
    
    def get_version(self):
        return self.y
    