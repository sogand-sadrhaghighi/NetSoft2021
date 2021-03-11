#!/bin/bash

sudo mn -c; clear;sudo rm port_mirror/*.txt; sudo rm sent_perflow/*.txt; sudo rm port_mirror/client/*.txt; sudo python3 topology.py; sudo python3 flow.py; 
