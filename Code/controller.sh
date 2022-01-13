#!/bin/sh
./pox.py log.level --DEBUG rand --ip=10.1.0.0 --servers=10.1.1.1,10.1.1.2,10.1.1.3 &
./pox.py log.level --DEBUG round --ip=10.1.0.0 --servers=10.1.2.1,10.1.2.2,10.1.2.3 openflow.of_01 --port=6634 &
./pox.py log.level --DEBUG least --ip=10.1.0.0 --servers=10.1.3.1,10.1.3.2,10.1.3.3 openflow.of_01 --port=6635 &
./pox.py log.level --DEBUG wrr --ip=10.1.0.0 --servers=10.1.4.1:1,10.1.4.2:2,10.1.4.3:3 openflow.of_01 --port=6636 &
