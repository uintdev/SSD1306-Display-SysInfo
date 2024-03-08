# SSD1306 Display SysInfo

System information for the SSD1306 OLED Display on Raspberry Pi

This project was designed around the Adafruit PiOLED 128x32 OLED display.
<br>
As it involves a SSD1306 chipset, this can be adapted for such displays and of other resolutions.

This project is based on the Python script and instructions from [here](https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage).

## What does this do?

Mainly, this displays the following system information:

-   Time
-   IP address (IPv4)
-   CPU load
-   Memory usage
-   Disk usage

Also, when a `msg.txt` file is created in the same directory as the Python script, the file contents will be outputted and centered (x & y) on the display. The file then gets removed and there will be a delay before it updates the display again (to either display the next message from said file or to go back to the system information view).

## Configuration

This was tested with a Raspberry Pi Zero W. If it is a different device, then further modifications may have to be done to the scripts or system.

### Getting i2c ready

The i2c interface first needs to be enabled. You can do this through the `raspi-config` TUI. Alternatively, you can run a command to achieve this.

```bash
sudo raspi-config nonint do_i2c 0
```

Once set to enabled, the device has to be rebooted. But in this case, we will shutdown instead.

```bash
sudo shutdown now
```

Connect the display to the respective GPIO and then power the device back on again.

To verify that the display is being picked up on, run the following:

```bash
sudo apt install i2c-tools
sudo i2cdetect -y 1
```

If all goes well, you should see a mention of `3c` (0x3c address) mentioned.

### Gathering the Python packages

The Python script has several requirements.

First, we first make sure we have PIP (package manager) installed.

```bash
sudo apt-get install python3-pip
```

We then need PIL for drawing images for the display.

```bash
sudo apt-get install python3-pil
```

We are going to assume that we are in the home directory of the current user. Adjust the steps as needed.

We will need to change directory into where the Python script is.

```bash
cd ~/SSD1306-Display-SysInfo
```

A Python virtual environment will need to be created.

```bash
python -m venv env --system-site-packages
```

Get into the context of that virtual environment.

```bash
source env/bin/activate
```

There is a package that is required in order to drive the display.

```bash
pip3 install adafruit-circuitpython-ssd1306
```

### Additional configuration

If your display is not 128x32, then adjust the width and height values under the `disp` variable.

### Running the script

To run, simply run:

```bash
python main.py
```

If you get an Import error, make sure you are using the virtual environment.

If you wish to run the Python script such as in the context of a service or to just run it more directly, you can use the virtual environment in a single command.

```bash
/home/{USER}/SSD1306-Display-SysInfo/env/bin/python3 /home/{USER}/SSD1306-Display-SysInfo/main.py
```
