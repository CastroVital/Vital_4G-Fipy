
from machine import UART
from network import LTE
import pycom
import socket
import config
import machine
import time
import os

pycom.heartbeat(False)

def connect_wifi():
    """Establish Wi-Fi connection"""

    from network import WLAN
    
    wlan = WLAN()  # get current object, without changing the mode

    if machine.reset_cause() != machine.SOFT_RESET:
        wlan.init(mode=WLAN.STA)

    if not wlan.isconnected():
        wlan.connect(config.ssid, auth=(config.authMode,
                     config.wifi_password), timeout=config.wifi_timeout)
        while not wlan.isconnected():
            machine.idle()  # save power while waiting

        print(wlan.ifconfig())


def connect_lte():
    """Establish LTE connection"""

    from network import LTE
    #pycom.heartbeat(False)
    lte = LTE()         # instantiate the LTE object
    lte.init()

    # attach the cellular modem to a base station
    lte.attach(band=config.band, apn=config.apn)
    while not lte.isattached():
        time.sleep(0.25)
        print(lte.send_at_cmd('AT!="fsm"'))

    lte.connect()       # start a data session and obtain an IP address
    while not lte.isconnected():
        time.sleep(0.25)
        print(lte.send_at_cmd('AT!="fsm"'))
        #pycom.rgbled(0x7f7f00)


# setup WatchDog
wdt = machine.WDT(timeout=config.watchdog_timeout)

# setup uart
uart = UART(0, baudrate=115200)
os.dupterm(uart)
wdt.feed()

# Estccablish internet connection
if config.lte == True:
    connect_lte()
    pycom.rgbled(0x007f7f)
    wdt.feed()
else:
    connect_wifi()
    wdt.feed()

machine.main('main.py')
