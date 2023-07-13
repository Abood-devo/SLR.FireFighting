import subprocess

def get_battery_level():
    command = "upower -i /org/freedesktop/UPower/devices/gaming_input_sony_controller_battery_a0oabo51o4eoa2oe3 | grep 'percentage' | awk '{print $2}'"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    battery_level = output.decode("utf-8").strip()
    return battery_level

battery_level = get_battery_level()
print("Battery Level: " + battery_level)
