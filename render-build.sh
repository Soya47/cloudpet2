#!/bin/bash

# Install PyAudio dependencies (for Render's limited environment)
pip install pipwin
pipwin install pyaudio
pip install -r requirements.txt
