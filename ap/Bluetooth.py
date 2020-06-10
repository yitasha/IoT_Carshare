#!/usr/bin/env python3
#ifdef _WIN32
#include <Winsock2.h>
#endif

import bluetooth

print("local Bluetooth device address - {}".format(bluetooth.read_local_bdaddr()))

print("Performing inquiry...")

nearby_devices = bluetooth.discover_devices(duration=8,
                                            lookup_names=True,
                                            flush_cache=True,
                                            lookup_class=False)

print("Found {} devices".format(len(nearby_devices)))

for addr, name in nearby_devices:
    try:
        print("   {} - {}".format(addr, name))
    except UnicodeEncodeError:
        print("   {} - {}".format(addr, name.encode("utf-8", "replace")))

print(nearby_devices)

Engineer_devices = ['9C:B6:D0:FA:B0:54', 'others']
print(Engineer_devices)

for addr, name in nearby_devices:
    if addr in Engineer_devices:
        print(addr)