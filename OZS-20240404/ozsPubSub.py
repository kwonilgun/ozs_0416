# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
import RPi.GPIO as GPIO
import time
import json
from utils.command_line_utils import CommandLineUtils
import serial
import json



#참조 사이트 : https://post.naver.com/viewer/postView.nhn?volumeNo=31037503&memberNo=2534901

line = ''  # 라인 단위로 데이터 가져올 변수
port = '/dev/ttyUSB0' # 시리얼 포트
baud = 115200  # 시리얼 보드레이트(통신속도)

ser = serial.Serial(port, baud, timeout=3)



#GPIO 세팅
pin_18 = 18
pin_23 = 23
pin_24 = 24
pin_25 = 25
pin_8 = 8
pin_7 = 7

# GPIO.setwarnings(True)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin_18, GPIO.OUT)
# GPIO.setup(pin_23, GPIO.OUT)
# GPIO.setup(pin_24, GPIO.OUT)
# GPIO.setup(pin_25, GPIO.OUT)
# GPIO.setup(pin_8, GPIO.OUT)
# GPIO.setup(pin_7, GPIO.OUT)


# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broker,
# since it is subscribed to that same topic.

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
cmdData = CommandLineUtils.parse_sample_input_pubsub()

received_count = 0
received_all_event = threading.Event()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))


def send_serial_data(data):
    #json data -> string 변환 
    #json_string = json.dumps(data)

    # start with '[', end with ']' 추가
    json_string_with_brackets = "[" + data + "]"
    
    print("json data = "+ json_string_with_brackets)
    for char in json_string_with_brackets:
        # print('send char = ' + char)
        ser.write(char.encode())
        time.sleep(0.01)

#send start commmnd to OZS with data
def send_start_ozs(start):
    print('start :', start)
          
    action = start['action']
    duration = start['time']
    wind_speed = start['wind']
    print('action =', action)
    print('time = ', duration)
    print('wind', wind_speed)
    
    #power on 전송
    send_serial_data("{power:on:}")

    #mode 전송
    if action == 1 :
        send_serial_data("{mode:1:}")
    elif action == 2 :
        send_serial_data("{mode:2:}")
    elif action == 3 :
        send_serial_data("{mode:3:}")
    else:
        print("Invalid action command: ",action)

    #wind 세기 전송
    if wind_speed == 1 :
        send_serial_data("{wind:1:}")
    elif wind_speed == 2 :
        send_serial_data("{wind:2:}")
    elif wind_speed == 3 :
        send_serial_data("{wind:3:}")
    else:
        print("Invalid wind speed command: ", wind_speed)

    # time duration
    if duration == 1 :
        send_serial_data("{duration:30:}")
    elif duration == 2 :
        send_serial_data("{duration:60:}")
    elif duration == 3 :
        send_serial_data("{duration:90:}")
    else:
        print("Invalid duration command: ", duration)

    #start ozs
    send_serial_data("{start:act:}")


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))
    data = json.loads(payload.decode('utf-8'))
    
    print('data = ', data)

    try:
        if 'power' in data:
            power_cmd = data['power']
            if power_cmd == 'on':
                GPIO.output(pin_18, True)
                send_serial_data("{power:on:}")
            elif power_cmd == 'off':
                GPIO.output(pin_18, False)
                send_serial_data("{power:off:}")
            else:
                print("Invalid switch command:", power_cmd)
        elif 'wind' in data:
            wind_speed = data['wind']
            # Do something with wind speed, e.g., adjust fan speed
            print("Wind speed:", wind_speed)
            if wind_speed == '1':
                send_serial_data("{wind:1:}")
            elif wind_speed == '2':
                send_serial_data("{wind:2:}")
            elif wind_speed == '3':
                send_serial_data("{wind:3:}")
            else:
                print("Invalid wind speed command: ", wind_speed)
        elif 'duration' in data:
            duration = data['duration']
            # Do something with wind speed, e.g., adjust fan speed
            print("duration:", duration)
            if duration == '30':
                send_serial_data("{duration:30:}")
            elif duration == '60':
                send_serial_data("{duration:60:}")
            elif duration == '90':
                send_serial_data("{duration:90:}")
            else:
                print("Invalid duration command: ", duration)
        elif 'start' in data:
            start = data['start']
            
            send_start_ozs(start)

        else:
            print("Key  not found in data:", data)

    except KeyError as e:
        print("Key not found in data:", e)

    
# Callback when the connection successfully connects
def on_connection_success(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
    print("Connection Successful with return code: {} session present: {}".format(callback_data.return_code, callback_data.session_present))

# Callback when a connection attempt fails
def on_connection_failure(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionFailureData)
    print("Connection failed with error code: {}".format(callback_data.error))

# Callback when a connection has been disconnected or shutdown successfully
def on_connection_closed(connection, callback_data):
    print("Connection closed")

if __name__ == '__main__':
    # Create the proxy options if the data is present in cmdData
    proxy_options = None
    if cmdData.input_proxy_host is not None and cmdData.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=cmdData.input_proxy_host,
            port=cmdData.input_proxy_port)

    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=cmdData.input_endpoint,
        port=cmdData.input_port,
        cert_filepath=cmdData.input_cert,
        pri_key_filepath=cmdData.input_key,
        ca_filepath=cmdData.input_ca,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdData.input_clientId,
        clean_session=False,
        keep_alive_secs=300,
        http_proxy_options=proxy_options,
        on_connection_success=on_connection_success,
        on_connection_failure=on_connection_failure,
        on_connection_closed=on_connection_closed)

    if not cmdData.input_is_ci:
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
    else:
        print("Connecting to endpoint with client ID")
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    
    message_count = cmdData.input_count
    message_topic = cmdData.input_topic
    message_string = cmdData.input_message

    # Subscribe
    print("Subscribing to topic '{}'...".format(message_topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=message_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))
    
    while True:
        time.sleep(5)


    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
