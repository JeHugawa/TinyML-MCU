from flask import Flask, abort, request, jsonify
from relay.components.install import get_device_port, install_inference
from relay.tflm_hello_world.observing import read_person_detection_from_serial


app = Flask(__name__)
port = 5000


@app.route('/install/', methods=['POST'])
def install():
    if request.method == 'POST':
        if "device" not in request.get_json():
            return "No device in request", 400
        res = request.get_json()
        device = res["device"]
        model = res["model"]

        if not install_inference(device, model):
            return f"Device with installer \"{device['installer']}\" is not supported"

        return 'Success', 200
    else:
        abort(400)


@app.route('/prediction', methods=['GET'])
def get_prediction():
    device = request.args.get("device", None)
    if not device:
        return "No device selected in request", 400
    port = get_device_port(device)
    pred = read_person_detection_from_serial(port)
    if not pred:
        return "Failed to read prediction from device", 404
    return jsonify(pred)


if __name__ == "__main__":
    app.run()
