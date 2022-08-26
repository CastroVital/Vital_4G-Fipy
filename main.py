import pycom
import time
import utime
import ujson
import os
from L76GNSS import L76GNSS
from machine import RTC
from mqtt import MQTTClient
from pycoproc import Pycoproc
from pytrack import Pytrack
from machine import SD

pycom.heartbeat(False)
NTP_SERVER = "gps.ntp.br"
rtc = RTC()

#mount SD card
sd = SD()
os.mount(sd, '/sd')
FileNo = 0
FileName = ''
while True:  # Find a unique file name on the SD card
    try:
        # Path, file name and extension.
        FileName = '/sd/' + str(FileNo) + '.csv'
        FileNo = FileNo + 1  # Increment through file numbers
        # Test to see if file exists, if not then break out of loop
        open(FileName, 'r')
    except:
        break

f = open(FileName, 'a')  # Open new CSV file
# Add column names for an easier import into Google Maps
f.write('Latitude,' + 'Longitude,' + 'DataHora' '\r\n')
f.close()  # Save and close

def sub_cb(topic, msg):
    """Read received MQTT messages"""
    print(msg)

# setup MQTT connection
client = MQTTClient(config.client_id, config.mqtt_server, port=config.mqtt_port,user=config.mqtt_user, password=config.mqtt_password)
client.set_callback(sub_cb)
client.connect(clean_session=False)
# client.subscribe(config.config_topic)

def setRTC():

    print("Updating RTC from {} ".format(NTP_SERVER), end='')
    rtc.ntp_sync(NTP_SERVER)
    utime.timezone(-10800)
    while not rtc.synced():
        print('.', end='')
        time.sleep(1)
    print(' OK')

# Only returns an RTC object that has already been synchronised with an NTP server.
def getRTC():

    if not rtc.synced():
        setRTC()

    return rtc

def saveToSD():
    I = "%4d-%02d-%02d %02d:%02d:%02d" % utime.localtime()[:6]
    f = open(FileName, 'a')  # Use append mode to add new location data
    # Write new location data and separate using commas
    f.write(str(latitude) + ',' + str(longitude) + ',' + str(I) + '\r\n')
    f.close()
    print(I)

def getGPS():
    py = Pytrack()
    l76 = L76GNSS(py, timeout=30)
    global coord
    coord = l76.coordinates()

    global latitude
    global longitude

    try:

        if type(coord[0]) == "NoneType":
            pycom.rgbled(0x7f7f00)
            latitude = round(0, 5)
        else:
            latitude = round(coord[0], 5)
            pycom.rgbled(0x007f00)

        if type(coord[1]) == "NoneType":

            longitude = round(0, 5)
            pycom.rgbled(0x007f00)
        else:
            longitude = round(coord[1], 5)
            pycom.rgbled(0x007f00)
    except:
        pycom.rgbled(0x7f0000)
        pass
        longitude = 999
        latitude = 999

    gps = '{"localizacao":"%s,%s"}' % (latitude, longitude)
    client.publish(topic="ufpa/circular/2", msg=gps)
    print(gps)

#get the current position
getGPS()
rtc = RTC()
rtc = getRTC()

while True:
    pycom.heartbeat(False)
    saveToSD()
    getGPS()
    time.sleep(1)  # Wait for 5 seconds before next reading



    ''' #get current coordinates
    getGPS()
    gps = '{"localizacao":"%s,%s"}' % (latitude, longitude)
    client.publish(topic="ufpa/circular/2", msg=gps)
    print(gps)
    #print("Time:", utime.localtime())

    global lat_difference
    global lon_difference

    lat_difference = latitude - latitude_previous
    lon_difference = longitude - longitude_previous

    if abs(lat_difference) > 0.00022 and abs(lon_difference) > 0.00022 and longitude != 999:
        saveToSD()

    latitude_previous = latitude
    longitude_previous = longitude

    time.sleep(1)
 '''

#lte = LTE
#lte.pppsuspend()
#lte.send_at_cmd('AT!="showphy"')
#lte.pppresume()
