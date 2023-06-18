from subprocess import Popen, PIPE, STDOUT


ACCEPTED_VENDORS = ["Raspberry Pi", "Arduino"]


def get_device_port(device_serial: str):
    """Find the wanted devices port based on its serial number.

    Does this with the help of the /dev/serial/by_id/ directory,
    which contains this information as a symlink.
    """

    p = Popen("ls -la /dev/serial/by-id/", shell=True,
              stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = p.stdout.read()

    out = output.decode('utf-8').split('\n')

    port = None

    for row in out:
        if device_serial in row:
            row = row.split('/')
            port = '/dev/' + row[-1]

    return port


def get_connected_devices():
    pipe = Popen("lsusb -v", shell=True, stdin=PIPE,
                 stdout=PIPE, stderr=STDOUT)
    output = pipe.stdout.read()

    out = output.decode('utf-8').split('\n')
    find_variables = False

    return_devices = []

    for row in out:
        if len(row.split()) == 0:
            continue
        if (row[0] != " " and
                len([row for vendor in ACCEPTED_VENDORS if vendor.lower() in row.lower()]) > 0):
            find_variables = True
            return_devices.append({})
        elif (row[0] != " " and
              len([row for vendor in ACCEPTED_VENDORS if vendor.lower()
                  in row.lower()]) == 0
              and "Device Descriptor" not in row):
            find_variables = False
        elif find_variables:
            row = row.split()
            if row[0] == "iManufacturer" or row[0] == "iSerial" or row[0] == "iProduct":
                return_devices[-1][row[0][1:].lower()] = " ".join(row[2:])

    return return_devices
