import json
import string
from random import random
import numpy as np
import pickle
import re
import paho.mqtt.client as mqtt
from alert import *
import requests
broker = '172.28.182.49'
MQTT_port = 1883
url1 = "http://172.28.182.49:5000/power/alert-from-ml"
topic = "topic5"
client_id = 'Admin1'
keepalive = 60

#generate client ID

print(client_id)
data_pub_devices = " "
data_pub_alert = " "
model = pickle.load(open("modelA.pkl", "rb"))



def predict(data_input):
    quoted_string = re.search(r'\"([^\"]+)\"', data_input).group(1)
    temp = [float(value) for value in quoted_string.split(',')] # data format: "232, 32, 232, 23"
    data = temp[:4]
    features = [np.array(data)]
    prediction = model.predict(features)
    print(f"Working Device: {prediction}")
    if prediction != 'NO LOAD':
        alert = detect_anomalies(data, mean_values, std_values)
        data_pub1 = alert
        data = {
            'alert': alert,
            'device': prediction
        }
        response = requests.post(url1, data=data)
        if response.status_code == 201:
            print('Request successful!')
            print('Response:', response.text)
        else:
            print('Request failed with status code:', response.status_code)
        print(alert)
    else:
        data = {
            'alert': 'no alert',
            'device': prediction
        }
        response = requests.post(url1, data=data)
        if response.status_code == 201:
            print('Request successful!')
            print('Response:', response.text)
        else:
            print('Request failed with status code:', response.status_code)

    return


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
        # publish(client,data_pub)
        print(msg)
# def publish(client: mqtt, data_pub):
#     client.publish("result", data_pub)
def subscribe(client: mqtt):
    print(" ")
def main():
    client = connect_mqtt()
    client.subscribe("topic5")
    client.on_message = on_message
    # client.publish("result", data_pub_devices)
    # client.publish("result", data_pub_alert)
    client.loop_forever()

if __name__ == '__main__':
    main()
