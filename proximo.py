#!/usr/bin/env python

import random
import os
import struct
import sys
import time

import btle

MAC = '78:C5:E5:A1:49:43' # Kensington Eureka 4943 (the round tag without button)
#MAC = '00:18:30:EB:47:1A' # Kensington Eureka 471A (the oblong key fob with button)
BEEP_SERVICE_UUID = 'b96e2b00-12d6-4970-8a20-6c89df2afff0'


def main():
    if len(sys.argv) < 2:
        print 'need arg'
        return
    
    arg = sys.argv[1]

    # Attempt at getting the device to play a new sequence of frequencies each time.
    if arg == 'dynamic':
        #set_beeps_round_tag([30, 35, 30, 35, 30, 35, 30]) # loud frequencies
        #set_beeps_round_tag([5, 3, 1, 5, 3, 1, 5]) # softer
        for i in range(3):
            print i
            listen()
            time.sleep(3) # no 2nd beep with sleep(1)
        connect_write_disconnect(92, list_to_bytes((0, 0, 0, 0, 0, 0, 0, 0))) # off and fast (to kind of skip the tones it plays on the end)
        #set_beeps_round_tag([0, 0, 0, 0, 0, 0, 0]) # off
        #connect_write_disconnect(66, list_to_bytes((0, 0, 0, 0, 0, 0, 0, 0)))
        #connect_write_disconnect(66, list_to_bytes((255, 255, 255, 255, 255, 255, 255, 255)))
        
    elif arg == 'set':
        set_beeps_round_tag([30, 35, 30, 35, 30, 35, 30]) # loud frequencies
        #set_beeps_round_tag([5, 3, 1, 5, 3, 1, 5]) # softer

    elif arg == 'play':
        for i in range(3):
            print i
            time.sleep(2) # no 2nd beep with sleep(1)

    elif arg == 'fuzzle':
        fuzzle()

    else:
        print 'invalid arg'

def set_beeps_oblong_tag(frequency_list):
    song = []
    for i in range(64):
        #if i & 1:
        #    n = 0
        #else:
        #n = 50 - i
        n = i
        song.append(n)

    #song = range(0, 100, 3)
    song[0] = 100 # speed. 50 = fast, 100 = normal
    song[1] = 100 # speed
    print song
    
    #song = random_string(10)
    
    set_song(song)
    #set_song(song)

def listen():
    peripheral = btle.Peripheral(MAC)
    peripheral.disconnect()

def set_beeps_round_tag(frequency_list):
    assert len(frequency_list) == 7
    connect_write_disconnect(92, list_to_bytes([200] + frequency_list))

def fuzzle():
    peripheral = btle.Peripheral(MAC)
    service = peripheral.getServiceByUUID(BEEP_SERVICE_UUID)
    char_dict = get_characteristics_dict(service)

    for i in range(100):
        print i
        handle = random.choice(char_dict)
        char_dict[handle].write(random_string(8))

    peripheral.disconnect()

def find_max_bytes_for_characteristic():
    peripheral = btle.Peripheral(MAC)
    service = peripheral.getServiceByUUID(BEEP_SERVICE_UUID)
    char_dict = get_characteristics_dict(service)
    handles = sorted(char_dict.keys())
    peripheral.disconnect()
    for h in handles:
        print 'handle: ', h
        for n in range(1, 1023):
            try:
                connect_write_disconnect(h, random_string(n))
            except:
                print 'broke: ', n
                break

#
# Private.
#

def list_to_bytes(v_list):
    b = ''
    for i in v_list:
        b += struct.pack('B', i)
    return b

def to_hex_str(s):
    h = []
    for c in s:
        h.append('{:x}'.format(ord(c)))
    return ' '.join(h)

def random_string(n):
    return os.urandom(n)

def connect_write_disconnect(handle, msg_bytes):
    peripheral = btle.Peripheral(MAC)
    service = peripheral.getServiceByUUID(BEEP_SERVICE_UUID)
    char_dict = get_characteristics_dict(service)
    print '{} <- {}'.format(handle, to_hex_str(msg_bytes))
    char_dict[handle].write(msg_bytes)
    peripheral.disconnect()

def get_characteristics_dict(service):
    characteristics_list = service.getCharacteristics()
    char_dict = {}
    for c in characteristics_list:
        char_dict[c.getHandle()] = c
    return char_dict

def get_all_handles():
    peripheral = btle.Peripheral(MAC)
    service = peripheral.getServiceByUUID(BEEP_SERVICE_UUID)
    char_dict = get_characteristics_dict(service)
    handles = sorted(char_dict)
    peripheral.disconnect()
    return handles

if __name__ == '__main__':
    main()
