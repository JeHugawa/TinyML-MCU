from subprocess import Popen, PIPE, STDOUT


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
