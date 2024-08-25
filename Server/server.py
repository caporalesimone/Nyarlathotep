from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta

CONSIDER_OFFLINE_AFTER_SECONDS = 60

app = Flask(__name__)

# Dizionario per memorizzare l'ultimo JSON ricevuto per ogni customName
client_data_map = {}

@app.route('/client_update', methods=['POST'])
def client_update():
    global client_data_map
    # Riceve il JSON dalla richiesta POST
    data = request.json

    # Verifica che il JSON contenga l'customName
    if "customName" not in data:
        return jsonify({"error": "Missing key: customName"}), 400

    customName = data["customName"]
    client_ip = request.remote_addr  # Client IP
    
    last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp corrente

    client_data_map[customName] = {
        "json_data": data,
        "last_update": last_update,
        "client_ip": client_ip,
    }

    return jsonify({"message": f"{customName} update recorded"}), 200

@app.route('/', methods=['GET'])
def status():
    return render_template('status.html')

@app.route('/status_data', methods=['GET'])
def status_data():
    current_time = datetime.now()
    
    for customName, details in client_data_map.items():
        last_update_time = datetime.strptime(details['last_update'], "%Y-%m-%d %H:%M:%S")
        
        if current_time - last_update_time > timedelta(seconds=CONSIDER_OFFLINE_AFTER_SECONDS):
            details['timed_out'] = True
        else:
            details['timed_out'] = False
    
    return jsonify(client_data_map)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
