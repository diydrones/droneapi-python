from droneapi import connect
from droneapi.lib import VehicleMode
from droneapi.tools import with_sitl
from pymavlink import mavutil
import time
import sys
import os
from nose.tools import assert_equals

@with_sitl
def test_115(connpath):
    v = connect(connpath, await_params=True)

    # Dummy callback
    def mavlink_callback(*args):
        mavlink_callback.count += 1
    mavlink_callback.count = 0

    # Set the callback.
    v.set_mavlink_callback(mavlink_callback)

    # Change the vehicle into STABILIZE mode
    v.mode = VehicleMode("STABILIZE")
    # NOTE wait crudely for ACK on mode update
    time.sleep(3)

    # Expect the callback to have been called
    assert mavlink_callback.count > 0

    # Unset the callback.
    v.unset_mavlink_callback()
    savecount = mavlink_callback.count

    # Disarm. A callback of None should not throw errors
    v.armed = False
    v.flush()
    # NOTE wait crudely for ACK on mode update
    time.sleep(3)

    # Expect the callback to have been called
    assert_equals(savecount, mavlink_callback.count)

    # Re-arm should not throw errors.
    v.armed = True
    v.flush()
    # NOTE wait crudely for ACK on mode update
    time.sleep(3)
