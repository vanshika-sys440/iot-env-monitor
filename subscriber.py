import json
import sqlite3
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
TOPIC = "vanshika/envmonitor/room1"

db = sqlite3.connect("readings.db")
db.execute(
    "CREATE TABLE IF NOT EXISTS readings ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "device TEXT, temperature REAL, humidity REAL, ts INTEGER)"
)
db.commit()


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to broker")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    db.execute(
        "INSERT INTO readings (device, temperature, humidity, ts) VALUES (?, ?, ?, ?)",
        (data["device"], data["temperature"], data["humidity"], data["ts"]),
    )
    db.commit()
    print("saved", data)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()