#!/usr/bin/env bash
# stop script on error


# run pub/sub sample app using certificates downloaded in package
printf "\nRunning ozs bd 시리얼 테스트...\n"
# python3 ~/Raspberry/Iot-2024_3_20/aws-iot-device-sdk-python-v2/samples/basic_connect.py --endpoint a9gxi0conitbh-ats.iot.ap-northeast-2.amazonaws.com --port 8883 --ca_file cert/root-CA.crt --cert cert/ozs_0406.cert.pem --key cert/ozs_0406.private.key --client_id ozs-device-2 --topic ozs/test --count 10 --message 'kwon hello'

python3 ozsPubSub.py --endpoint a9gxi0conitbh-ats.iot.ap-northeast-2.amazonaws.com --port 8883 --ca_file cert/root-CA.crt --cert cert/ozs_0406.cert.pem --key cert/ozs_0406.private.key --client_id ozs-device-2 --topic ozs/test --count 10 --message 'kwon hello'