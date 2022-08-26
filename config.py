
from network import WLAN
from network import LTE
import time
import socket

# Bus
circular_id = "01"
circular_name = "bus"
sent_interval = 2  # Interval between updates in seconds
ntp_server = "pool.ntp.org"
timezone = 10800  # Timezone in seconds
watchdog_timeout = 60000  # timeout in ms

# Network configurations
# if lte = false, wifi connection will be used.
lte = True

# LTE configurations
band = None  # if None the device will test all availables bands
apn = "zap.vivo.com.br"  # timbrasil.br ; zap.vivo.com.br ; claro.com.br

# Wi-Fi configurations
ssid = "Castro"
authMode = WLAN.WPA2
wifi_password = "82167417k"
wifi_timeout = 5000

#MQTT connection configurations
client_id = circular_name
mqtt_server = "broker.hivemq.com"  # 192.168.0.104 "broker.emqx.io"
mqtt_port = 1883
mqtt_user = "user"
mqtt_password = "password"
mqtt_keepalive = 60
mqtt_ssl = False
gps_topic = "ufpa/circular/2"
