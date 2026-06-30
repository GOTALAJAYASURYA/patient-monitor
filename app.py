from flask import Flask, render_template, jsonify, request
import sqlite3
from simulator import generate_patient_data
from database import init_db, save_vitals
from ai_model import predict_patient_status

app = Flask(__name__)
init_db()

# Global variable to hold the current active patient name on the machine
current_patient_name = "Shanmukh"

@app.route('/')
def home():
    return render_template('index.html')

# NEW ROUTE: Listens for when a nurse submits a new name via the dashboard
@app.route('/api/update_patient', methods=['POST'])
def update_patient():
    global current_patient_name
    # Extract the name typed into the form
    new_name = request.json.get('name', 'Unknown')
    if new_name.strip():
        current_patient_name = new_name
    return jsonify({"success": True, "current_patient": current_patient_name})

@app.route('/api/vitals')
def get_vitals():
    data = generate_patient_data()
    ai_verdict, ai_suggestion = predict_patient_status(data['temperature'], data['pulse'], data['spo2'])
    
    # Include the dynamically tracked patient name in our data packet
    data['patient_name'] = current_patient_name
    data['status'] = ai_verdict
    data['suggestion'] = ai_suggestion
    
    save_vitals(data['temperature'], data['pulse'], data['spo2'])
    return jsonify(data)

@app.route('/api/history')
def get_history():
    conn = sqlite3.connect("patient.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, temperature, pulse, spo2 FROM vitals_history ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    history_list = []
    for r in rows:
        ai_verdict, _ = predict_patient_status(r[1], r[2], r[3])
        history_list.append({
            "timestamp": r[0], "temperature": r[1], "pulse": r[2], "spo2": r[3], "status": ai_verdict
        })
    return jsonify(history_list)

if __name__ == '__main__':
    app.run(debug=True)
