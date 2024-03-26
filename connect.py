import json
import string
from random import random
import numpy as np
import pickle
import paho.mqtt.client as mqtt

broker = '172.28.182.44'
MQTT_port = 1883
topic = "topic"
client_id = 'Admin1'
keepalive = 60


#generate client ID
print(client_id)
data_pub = " "
model = pickle.load(open("modelA.pkl", "rb"))
def predict(data_input):
    data = [float(value) for value in data_input.split(',')]
    features = [np.array(data)]
    prediction = model.predict(features)

    print(f"Working Device: {prediction}")
    return prediction
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Successfully Connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, MQTT_port, keepalive)
    return client
def on_message(client, userdata, msg):
        msg_payload = msg.payload.decode()
        print(f"{msg.topic} {msg_payload}")
        data_pub = str(predict(msg_payload))
        publish(client,data_pub)
def publish(client: mqtt, data_pub):
    client.publish("result", data_pub)
def subscribe(client: mqtt):
    print(" ")
def main():
    client = connect_mqtt()
    client.subscribe("topic")
    client.on_message = on_message
    client.publish("result", data_pub)
    client.loop_forever()

if __name__ == '__main__':
    main()
