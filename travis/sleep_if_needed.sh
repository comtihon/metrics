#!/usr/bin/env bash
HTTPD=`curl -H "Content-Type: application/json" -X POST -d '{"temperature":0}' -sL --connect-timeout 3 -w "%{http_code}\n" "http://127.0.0.1:8080/api/v1/sensors/wait_sensor/measurements" -o /dev/null`
until [ "$HTTPD" == "200" ]; do
    printf '.'
    sleep 3
    HTTPD=`curl -H "Content-Type: application/json" -X POST -d '{"temperature":0}' -sL --connect-timeout 3 -w "%{http_code}\n" "http://127.0.0.1:8080/api/v1/sensors/wait_sensor/measurements" -o /dev/null`
done