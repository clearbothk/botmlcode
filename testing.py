from dronekit import connect, VehicleMode, LocationGlobalRelative
print("stage 1 done")

connection_port="/dev/ttyTHS1"

baud=57600
vehicle = connect(connection_port, wait_ready=False, baud=baud)
vehicle.mode = VehicleMode("MANUAL")

print("stage 2 done")
# print('Autopilot Firmware version: %s' % vehicle.version)
# print('Autopilot capabilities (supports ftp): %s' % vehicle.capabilities.ftp)
print('Global Location: %s' % vehicle.location.global_frame)
# print('Global Location (relative altitude): %s' % vehicle.location.global_relative_frame)
# print('Local Location: %s' % vehicle.location.local_frame)
# print('Attitude: %s' % vehicle.attitude)
# print('Velocity: %s' % vehicle.velocity)
# print('GPS: %s' % vehicle.gps_0)
# print('Groundspeed: %s' % vehicle.groundspeed)
# print('Airspeed: %s' % vehicle.airspeed)
# print('Gimbal status: %s' % vehicle.gimbal)
# print('Battery: %s' % vehicle.battery)
# print('EKF OK?: %s' % vehicle.ekf_ok)
# print('Last Heartbeat: %s' % vehicle.last_heartbeat)
# print('Rangefinder: %s' % vehicle.rangefinder)
# print('Rangefinder distance: %s' % vehicle.rangefinder.distance)
# print('Rangefinder voltage: %s' % vehicle.rangefinder.voltage)
# print('Heading: %s' % vehicle.heading)
# print('Is Armable?: %s' % vehicle.is_armable)
# print('System status: %s' % vehicle.system_status.state)
# print('Mode: %s' % vehicle.mode.name)
# print('Armed: %s' % vehicle.armed)
