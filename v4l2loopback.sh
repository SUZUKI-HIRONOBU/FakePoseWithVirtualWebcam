#!/bin/bash
sudo modprobe -r v4l2loopback
sudo modprobe v4l2loopback devices=2 video_nr=20 card_label="Virual Background" exclusive_caps=1
