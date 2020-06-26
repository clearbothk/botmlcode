try:
    from dronekit import connect, VehicleMode, LocationGlobalRelative
except:
    print("No module named dronekit, try to establish connection between jetson nano and mission planner")
    exit(0)

# Connect to the Vehicle
vehicle = connect('/dev/ttyTHS1', wait_ready=True, baud=57600)

vehicle.mode = VehicleMode("MANUAL")
vehicle.armed = True

class test1():
    def firmware_version(self):
        return vehicle.version

    def vehicle_capabilities(self):
        return vehicle.capabilities.ftp

    def do_capture_global_location(self):
        return vehicle.location.global_frame

    def do_capture_relative_global_location(self):
        return vehicle.location.global_relative_frame

    def do_capture_altitude(self):
        return vehicle.altitude
    
    def do_capture_velocity(self):
        return vehicle.velocity
    
    def do_capture_gps(self):
        return vehicle.gps_0

    def do_capture_ground_speed(self):
        return vehicle.groundspeed
    
    def do_capture_air_speed(self):
        return vehicle.airspeed
    
    def gimbal_status(self):
        return vehicle.gimbal
    
    def battery_status(self):
        return vehicle.battery
    
    def EKF_OK(self):
        return vehicle.ekf_ok
    
    def last_heartbeat(self):
        return vehicle.last_heartbeat

    def range_finder(self):
        return vehicle.rangefinder

    def range_finder_distance(self):
        return vehicle.rangefinder.distance

    def range_finder_voltage(self):
        return vehicle.rangefinder.voltage

    def heading(self):
        return vehicle.heading

    def vehicle_is_armable(self):
        return vehicle.is_armable

    def system_status(self):
        return vehicle.system_status.state
    
    def vehicle_mode_name(self):
        return vehicle.mode.name

    def check_vehicle_armed(self):
        return vehicle.armed




# vehicle is an instance of the Vehicle class
#print('Autopilot Firmware version: %s' % vehicle.version)
#print('Autopilot capabilities (supports ftp): %s' % vehicle.capabilities.ftp)
#print('Global Location: %s' % vehicle.location.global_frame)
#print('Global Location (relative altitude): %s' % vehicle.location.global_relative_frame)
#print('Local Location: %s' % vehicle.location.local_frame)    #NED
#print('Attitude: %s' % vehicle.attitude)
#print('Velocity: %s' % vehicle.velocity)
#print('GPS: %s' % vehicle.gps_0)
#print('Groundspeed: %s' % vehicle.groundspeed)
#print('Airspeed: %s' % vehicle.airspeed)
#print('Gimbal status: %s' % vehicle.gimbal)
#print('Battery: %s' % vehicle.battery)
#print('EKF OK?: %s' % vehicle.ekf_ok)
#print('Last Heartbeat: %s' % vehicle.last_heartbeat)
#print('Rangefinder: %s' % vehicle.rangefinder)
#print('Rangefinder distance: %s' % vehicle.rangefinder.distance)
#print('Rangefinder voltage: %s' % vehicle.rangefinder.voltage)
#print('Heading: %s' % vehicle.heading)
#print('Is Armable?: %s' % vehicle.is_armable)
#print('System status: %s' % vehicle.system_status.state)
#print('Mode: %s' % vehicle.mode.name)    # settable
#print('Armed: %s' % vehicle.armed)    # settable