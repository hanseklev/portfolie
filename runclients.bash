#!/bin/bash

for i in {1..20}
do
    name="bot${i}" 
    python3 client.py -p 2450 -ip '123123' -b $name &
    echo $name
    sleep 1
done