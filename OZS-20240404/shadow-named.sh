#!/usr/bin/env bash
# stop script on error



# run shadow sample app using certificates downloaded in package
printf "\nRunning shadow name sample application...\n"
python3 shadow-named.py --endpoint a9gxi0conitbh-ats.iot.ap-northeast-2.amazonaws.com --key ~/Raspberry/Iot-2024_3_20/aws-iot-device-sdk-python-v2/OZS-20240404/cert/ozs_0406.private.key --cert ~/Raspberry/Iot-2024_3_20/aws-iot-device-sdk-python-v2/OZS-20240404/cert/ozs_0406.cert.pem  --thing_name ozs_0406
