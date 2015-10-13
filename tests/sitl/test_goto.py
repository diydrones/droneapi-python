"""
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)

The example demonstrates how to arm and takeoff in Copter and how to navigate to 
points using Vehicle.commands.goto.

Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

import time
from dronekit import connect
from dronekit.lib import VehicleMode, LocationGlobal
from dronekit.tools import with_sitl
from pymavlink import mavutil
from nose.tools import assert_equals

@with_sitl
def test_goto(connpath):
    vehicle = connect(connpath, await_params=True)

    # NOTE these are *very inappropriate settings*
    # to make on a real vehicle. They are leveraged
    # exclusively for simulation. Take heed!!!
    vehicle.parameters['ARMING_CHECK'] = 0
    vehicle.parameters['FS_THR_ENABLE'] = 0
    vehicle.parameters['FS_GCS_ENABLE'] = 0
    vehicle.parameters['EKF_CHECK_THRESH'] = 0

    def arm_and_takeoff(aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        # print "Basic pre-arm checks"
        # Don't let the user try to fly autopilot is booting
        if vehicle.mode.name == "INITIALISING":
            # print "Waiting for vehicle to initialise"
            time.sleep(1)
        while vehicle.gps_0.fix_type < 2:
            # print "Waiting for GPS...:", vehicle.gps_0.fix_type
            time.sleep(1)
            
        # print "Arming motors"
        # Copter should arm in GUIDED mode
        vehicle.mode    = VehicleMode("GUIDED")
        vehicle.flush()

        i = 60
        while vehicle.mode.name != 'GUIDED' and i > 0:
            # print " Waiting for guided %s seconds..." % (i,)
            time.sleep(1)
            i = i - 1

        vehicle.armed = True
        vehicle.flush()

        i = 60
        while not vehicle.armed and vehicle.mode.name == 'GUIDED' and i > 0:
            # print " Waiting for arming %s seconds..." % (i,)
            time.sleep(1)
            i = i - 1

        # Failure will result in arming but immediately landing
        assert vehicle.armed
        assert_equals(vehicle.mode.name, 'GUIDED')

        # print "Taking off!"
        vehicle.commands.takeoff(aTargetAltitude) # Take off to target altitude
        vehicle.flush()

        # Wait until the vehicle reaches a safe height before
        # processing the goto (otherwise the command after
        # Vehicle.commands.takeoff will execute immediately).
        while True:
            # print " Altitude: ", vehicle.location.alt
            # Test for altitude just below target, in case of undershoot.
            if vehicle.location_global.alt >= aTargetAltitude * 0.95: 
                # print "Reached target altitude"
                break

            assert_equals(vehicle.mode.name, 'GUIDED')
            time.sleep(1)

    arm_and_takeoff(10)

    # print "Going to first point..."
    point1 = LocationGlobal(-35.361354, 149.165218, 20, is_relative=True)
    vehicle.commands.goto(point1)
    vehicle.flush()

    # sleep so we can see the change in map
    time.sleep(3)

    # print "Going to second point..."
    point2 = LocationGlobal(-35.363244, 149.168801, 20, is_relative=True)
    vehicle.commands.goto(point2)
    vehicle.flush()

    # sleep so we can see the change in map
    time.sleep(3)

    # print "Returning to Launch"
    vehicle.mode = VehicleMode("RTL")
    vehicle.flush()
