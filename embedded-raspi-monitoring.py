import pyembedded
from pyembedded.raspberry_pi_tools.raspberrypi import PI
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt 
import time
import json
import os

print("Starting raspi-monitoring...")
hostname = os.environ["NODE_NAME"]

pi = PI()

def get_data():
    ram_raw = pi.get_ram_info()
    disk_raw = pi.get_disk_space()
    cpu_raw = pi.get_cpu_usage()
    temperature_raw = pi.get_cpu_temp()

    temperature =  {
        "name": "temperatrue",
        "value": temperature_raw,
        "unit": "°C",
        "node": hostname
    }
    ram =  {
        "name": "ram",
        "value": {
            "total": round(int(ram_raw[0])/1000000,1),
            "used": round(int(ram_raw[1])/1000000,1),
            "free": round(int(ram_raw[2])/1000000,1)
        },
        "unit": "GB",
        "node": hostname
    }
    disk = {
        "name": "disk",
        "value": {
        "total": disk_raw[0],
        "used": disk_raw[1],
        "free": disk_raw[2],
        },
        "unit": "GB",
        "node": hostname
    }
    cpu = {
        "name": "cpu",
        "value": cpu_raw,
        "unit": "Percent",
        "node": hostname
    }
    return temperature, ram, disk, cpu

mqtt_client = mqtt.Client("k3s")
mqtt_client.connect("mosquitto.mqtt.svc.cluster.local", 1883, 60)
mqtt_client.loop_start()

while True:
    temperature, ram, disk, cpu = get_data()
    mqtt_client.publish("test", "Hello from " + hostname)
    mqtt_client.publish("raspi/" + hostname + "/temperature", str(temperature))
    mqtt_client.publish("raspi/"+hostname + "/ram" ,json.dumps(ram))
    mqtt_client.publish("raspi/"+hostname + "/disk", json.dumps(disk))
    mqtt_client.publish("raspi/"+hostname+"/cpu", json.dumps(cpu))
    time.sleep(5)# sleep for 5 seconds before next call