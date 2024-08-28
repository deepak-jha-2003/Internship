from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Initial device states and base energy consumption
device_status = {
    "lights": "on",
    "ac": "off",
    "washing_machine": "off",
    "refrigerator": "on",
    "solar_panels": "on",  # Assume solar panels are generating energy
    "battery_storage": "off"
}

# Energy consumption values for each device (in kW)
device_energy = {
    "lights": 10,
    "ac": 50,
    "washing_machine": 30,
    "refrigerator": 20
}

# Renewable energy contribution (negative values reduce total consumption)
renewable_energy = {
    "solar_panels": -40,  # Solar panels generate energy, reducing consumption
    "battery_storage": -20  # Battery discharges stored energy, reducing consumption
}

# Base energy consumption when devices are off
base_energy_consumption = 50

def calculate_total_energy():
    """Calculate the total energy consumption based on device states."""
    total_energy = base_energy_consumption
    for device, status in device_status.items():
        if device in device_energy and status == "on":
            total_energy += device_energy[device]
        elif device in renewable_energy and status == "on":
            total_energy += renewable_energy[device]
    return total_energy

@app.route("/")
def dashboard():
    total_energy = calculate_total_energy()
    return render_template("dashboard.html", energy=total_energy, device_status=device_status)

@app.route("/control")
def control():
    return render_template("control.html", device_status=device_status)

@app.route("/toggle_device", methods=["POST"])
def toggle_device():
    device = request.json.get("device")
    status = request.json.get("status")
    device_status[device] = status
    total_energy = calculate_total_energy()
    return jsonify({"success": True, "total_energy": total_energy})

if __name__ == "__main__":
    app.run(debug=True)
