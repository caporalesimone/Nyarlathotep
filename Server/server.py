import os
from flask import Flask, request, jsonify, render_template, send_from_directory, make_response
from datetime import datetime, timedelta

CONSIDER_OFFLINE_AFTER_SECONDS = 60

app = Flask(__name__)

# Dictionary for store all the data from the clients (by client_name field)
client_data_map = {}

# Highest agent version found
highest_agent_version = ""

def is_v1_higher_v2(version1, version2) -> bool:
    v1 = [int(x) for x in version1.split('.')]
    v2 = [int(x) for x in version2.split('.')]
    
    max_len = max(len(v1), len(v2))
    v1.extend([0] * (max_len - len(v1)))
    v2.extend([0] * (max_len - len(v2)))
    
    if v1 > v2:
        return True  # versione1 è maggiore
    elif v1 < v2:
        return False  # versione2 è maggiore
    else:
        return False  # Le versioni sono uguali


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Accept data from the client
@app.route('/client_update', methods=['POST'])
def client_update():
    global client_data_map
    global highest_agent_version

    data = request.json

    # client_name is required
    if "client_name" not in data:
        return jsonify({"error": "Missing key: client_name"}), 400
    client_name = data["client_name"]

    version = data.get("client_sw_version", "0.0.0")
    new_version_available = ""
    if highest_agent_version == "":
        highest_agent_version = version
    if is_v1_higher_v2(highest_agent_version, version):
        new_version_available = highest_agent_version
    else:
        highest_agent_version = version

    client_data_map[client_name] = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # Now
        "from_ip": request.remote_addr, # Client's IP
        "details": data,
        "new_version_available": new_version_available
    }

    return jsonify({"message": f"{client_name} update recorded"}), 200

# Homepage
@app.route('/', methods=['GET'])
def status():
    return render_template('status.html')

# Serve all the data from the clients as single JSON
@app.route('/status_data', methods=['GET'])
def status_data():
    current_time = datetime.now()
    
    for customName, details in client_data_map.items():
        last_update_time = datetime.strptime(details['last_update'], "%Y-%m-%d %H:%M:%S")
        if current_time - last_update_time > timedelta(seconds=CONSIDER_OFFLINE_AFTER_SECONDS):
            details['timed_out'] = True
        else:
            details['timed_out'] = False

    response = make_response(jsonify(client_data_map), 200)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
