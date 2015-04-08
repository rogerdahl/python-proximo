## python-proximo

Very experimental module to interact with the Kensington Proximo tag and key fob from Python. Requires bluepy, which means that it currently only works on Linux. Tested on Raspberry Pi.

* The Proximo tag (round without button) identifies as: Kensington Eureka 4943
* The Proximo key fob (oblong with button) identifies as: Kensington Eureka 471A

The Proximo tags exposes some standard profiles, but the profile that controls the beeper is custom. In particular, the tags do not use the standard GATT Proximity or Find Me profiles. I have been unable to find anything online about the custom peeper service, so I did some reverse engineering, sending random data to the various characteristics. I got some random beeps and then narrowed things down to get something that kind of works.

The UUID for the beeper service is the same for both the key fob and the tag:

    b96e2b00-12d6-4970-8a20-6c89df2afff0

However, the characteristics are different between the key fob and tag.

Notes:

* After running this code, the tag or key fob will play a short sequence of beeps each time a connection is established to it. I haven't found a way to disable this behavior, and it's the only way I've found to make the devices beep.
* Setting a new sequence of frequencies takes something like 5 seconds.
* I have not found out how to read the button on the key fob.

### Characteristics

##### Kensington Eureka 4943 (the round tag without button)

* All characteristics on the 4943 take 8 bytes.
* No function found (handles): 66, 69, 73, 76, 79, 82, 85, 89, 95
* Handle 92: sets play speed and beep frequencies. first value is speed. others are frequency indexes. valid values = 1 to 41.

##### Kensington Eureka 471A (the oblong key fob with button)

* No function found: 66, 69, 73, 76, 79, 82, 85, 88, 94, 97, 101, 105, 111
* Handle 91: Causes immediate "connect: Device or resource busy (16)"
* Handle 108: 64 bytes, beeps, marked READ WRITE but disconnects when I try to read(). Does not seem to register the write if more than 20  bytes are written.

#####  Standard services exposed by the key fob and tag

* 0x1800: Generic Access
* 0x1801: Generic Attribute
* 0x180a: Device Information
* 0x180f: Battery Service

##### Other custom services

* 0xffa0: Accelerometer Service
* 0xffe0: Simple Keys Service

I tried accessing the accelerometer service, but couldn't get it to work. I'm guessing that there is no accelerometer and that the service is just crud left over in the firmware from a sloppy implementation.


### Usage

You should be able to get some beeps out of the device with:

* Set up the bluez stack (it may be there already)
* Grab bluepy and copy into the same folder as proximo.py
* Find the MAC for your device with `$ hcitool lescan`
* Edit proximo.py and modify the MAC setting to the one of your device.

    $ python proximo.py set
    $ python proximo.py play
