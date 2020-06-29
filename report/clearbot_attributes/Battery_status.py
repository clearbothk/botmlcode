class Battery_status:
    def __init__(self, y):
        self.y = y["battery_status"]
    
    def get_battery(self):
        return self.y
    