import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
TOPIC = "vanshika/envmonitor/room1"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, 1883, 60)
client.loop_start()

temp = 28.0
hum = 55.0

while True:
    temp += random.uniform(-0.3, 0.3)
    hum += random.uniform(-0.8, 0.8)
    payload = {
        "device": "esp32-sim-01",
        "temperature": round(temp, 1),
        "humidity": round(max(0, min(100, hum)), 1),
        "ts": int(time.time()),
    }
    client.publish(TOPIC, json.dumps(payload))
    print("sent", payload)
    time.sleep(3)