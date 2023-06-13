from subprocess import Popen, PIPE, STDOUT
import getpass

DOCKERHUB_USER = "ohtuprojtinymlaas"


def install_inference(device: dict, model: dict):
    installers = {
        "RPI": upload_rpi,
        "Arduino IDE": arduino_installer
    }
    installer = device["installer"]
    try:
        installers[installer](device, model)
    except KeyError:
        return False
    finally:
        return True


def arduino_installer(device: dict, model: dict):
    """Install the wanted model to a Arduino
    """

    port = get_device_port(device["serial"])
    # image = f"{DOCKERHUB_USER}/nano33ble"
    # subprocess.run([f"docker pull {image}"], shell=True)
    # cmd = f"docker run --privileged {image} upload -p {port} --fqbn arduino:mbed_nano:nano33ble template"
    # subprocess.run([cmd], shell=True)


def upload_rpi():
    "Uploads compiled person detection uf2 file to device. The device must be in the USB Mass Storage Mode and `device_path` should be the absolute path at which the device is mounted at."
    # This can actually get mounted elsewhere, perhaps you could find the path by looking for the files that exist in that directory
    device_path = f"/media/{getpass.getuser()}/RPI-RP2"
    docker_img = f"{DOCKERHUB_USER}/pico"
    subprocess.run([f"docker pull {docker_img}"], shell=True)
    # this mounts the device_path inside the container and copies the uf2 file from the container to device_path
    cmd = f"docker run --rm -v {device_path}:/opt/mount --entrypoint cp {docker_img} person_detection_screen_int8.uf2 /opt/mount/app.uf2"
    subprocess.run([cmd], shell=True)


def get_device_port(device_serial: str):
    p = Popen("ls -la /dev/serial/by-id/", shell=True,
              stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = p.stdout.read()

    out = output.decode('utf-8').split('\n')

    for row in out:
        if device_serial in row:
            row = row.split('/')
            port = '/dev/' + row[-1]
    return port
