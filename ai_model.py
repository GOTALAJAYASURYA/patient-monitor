import numpy as np
from sklearn.tree import DecisionTreeClassifier

# [Temperature, Pulse, SpO2]
X_train = np.array([
    [98.6,  72,  98], [98.2,  65,  99], [97.8,  75,  97],  # Normal
    [99.8,  95,  95], [101.2, 105, 94], [98.6,  115, 96],  # Warning
    [103.0, 125, 88], [97.0,  45,  89], [98.6,  80,  85]   # Critical
])
y_train = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])

ai_classifier = DecisionTreeClassifier()
ai_classifier.fit(X_train, y_train)

def predict_patient_status(temperature, pulse, spo2):
    """Predicts status and provides a smart clinical suggestion based on combinations"""
    input_data = np.array([[temperature, pulse, spo2]])
    prediction_code = ai_classifier.predict(input_data)[0]
    
    if prediction_code == 0:
        status = "NORMAL"
        suggestion = "Patient is stable. Continue routine monitoring."
    elif prediction_code == 1:
        status = "WARNING"
        # Logic combination check
        if temperature >= 100.5:
            suggestion = "Elevated temperature detected. Monitor for potential infection. Keep patient hydrated."
        elif pulse >= 100:
            suggestion = "Mild tachycardia (high heart rate). Ensure patient is resting calmly and re-check."
        else:
            suggestion = "Vitals are drifting from baseline. Observe closely."
    else:
        status = "CRITICAL"
        if spo2 <= 92:
            suggestion = "EMERGENCY: Hypoxemia (low oxygen). Check oxygen line connection and clear airway immediately!"
        elif temperature >= 102.0 and pulse >= 110:
            suggestion = "EMERGENCY: Severe hyperthermia & racing pulse. Notify the on-duty physician for immediate intervention."
        else:
            suggestion = "EMERGENCY: Multiple critical physiological vital threshold breaches. Prepare crash cart."

    return status, suggestion