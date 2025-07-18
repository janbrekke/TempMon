# TempMon
Monitor the temperature of the CPU using Python.
I know there are a lot of these lying around the big web.
I made it a little bit for science, but also because i needed a small script that changed color based on what temperature it was.
Also, i didn't need anything fancy like power stuff, and any other extra that you find in many of the bigger softwares.
It's cool and all, but i just wanted the color change, and the temperature.
So, TADA! here's my version..

Feel free to use it as you wish.
The DLL file needs to be there in the same folder as the PY file.
The "OpenHardwareMonitorLib.dll" is a library that needs to be used to access and read the CPU temperature in real-time so it can be displayed in the GUI.

# What? Only Celcius?
Yes; Currently only in Celcius, sorry murrica.
I shall add a slider later that swich between the units.

# Requirements
You would need the following packages to make it work.
"pythonnet", "tk", and "pillow"

Just run:
pip install -r requirements.txt

# Usage
Just run the Python file as is.
Shouldn't require any argument magic.

# FAQ
Q: I am getting "AttributeError: module 'clr' has no attribute 'AddReference'"

A: Run "pip uninstall clr"
This is apparently a wrong version.
Please use "pythonnet" instead of "clr" as stated in the requirements.

# Screenshot
![Alt text](https://www.digitalbrekke.com/res/tempmon.png "ScreenShot")
