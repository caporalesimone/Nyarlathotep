""" Simple server for receiving data from clients and serving it as JSON. """

import json
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, request, jsonify, make_response
from jsonschema import validate, ValidationError

from versions import BACKEND_VERSION

CONSIDER_OFFLINE_AFTER_SECONDS = 60

app = Flask(__name__)

# Log backend version at startup
print(f"Nyarlathotep backend version: {BACKEND_VERSION}")

# Dictionary for store all the data from the clients (by client_name field)
client_data_map = {}

# Highest agent version found
highest_agent_version : str = ""


def load_schema() -> dict:
    """Load JSON schema from local or parent directory."""
    candidates = [
        Path(__file__).resolve().parent / "agent_json_schema.json",
        Path(__file__).resolve().parent.parent / "agent_json_schema.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            with open(candidate, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError("agent_json_schema.json not found in expected locations")


AGENT_SCHEMA = load_schema()

def is_v1_higher_v2(version1, version2) -> bool:
    """ Check if version1 is higher than version2. """

    v1 = [int(x) for x in version1.split('.')]
    v2 = [int(x) for x in version2.split('.')]

    max_len = max(len(v1), len(v2))
    v1.extend([0] * (max_len - len(v1)))
    v2.extend([0] * (max_len - len(v2)))

    return v1 > v2

# Accept data from the client
@app.route('/client_update', methods=['POST'])
def client_update():
    """ Accept data from the client. """

    global highest_agent_version # pylint: disable=W0603
    global client_data_map # pylint: disable=W0602

    data = request.json

    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Validate payload against schema
    try:
        validate(instance=data, schema=AGENT_SCHEMA)
    except ValidationError as exc:
        client_name = data.get("client_name", "<unknown>") if isinstance(data, dict) else "<unknown>"
        print(f"[VALIDATION] Invalid payload from {client_name}: {exc.message}")
        return jsonify({"error": "Invalid payload", "details": exc.message}), 400

    # client_name is required
    if "client_name" not in data:
        return jsonify({"error": "Missing key: client_name"}), 400
    
    # client_name is the map key. This is not the best solution but now is ok.
    # It should be a unique identifier for the client.
    client_name = data["client_name"].lower() 

    version = data.get("client_sw_version", "0.0.0")
    new_version_available = ""

    if highest_agent_version == "":
        highest_agent_version = version
    if is_v1_higher_v2(highest_agent_version, version):
        new_version_available = highest_agent_version
    else:
        highest_agent_version = version

    # Store the data in the dictionary
    client_data_map[client_name] = {
        "last_update_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "last_update_epoch": datetime.now(timezone.utc).timestamp(),
        "details": data,
        "new_version_available": new_version_available
    }

    return jsonify({"message": f"update for {client_name} recorded"}), 200

@app.route('/workstations_status', methods=['GET'])
def status_data():
    """ Serve all the data from the clients as an array of JSON objects with metadata. """	

    current_time = datetime.now(timezone.utc).timestamp()

    # Update the timed_out field for each client
    for details in client_data_map.values():
        details['timed_out'] = (current_time -
            details['last_update_epoch'] > CONSIDER_OFFLINE_AFTER_SECONDS)

    # Creates an array of clients' data
    data_list = [details for details in client_data_map.values()]

    # Returns workstations data
    response_data = {
        "workstations": data_list
    }

    response = make_response(jsonify(response_data), 200)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route('/version', methods=['GET'])
def get_version():
    """Return backend version info."""
    return jsonify({"backend_version": BACKEND_VERSION}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
