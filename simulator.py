import random
import time

def generate_patient_data():
    """Generates random but realistic vital signs for a single patient check"""
    # Healthy temp fluctuates slightly around 98.6°F
    temperature = round(random.uniform(97.5, 102.5), 1) 
    
    # Heart rate in beats per minute
    pulse = random.randint(60, 130) 
    
    # Blood oxygen saturation percentage
    spo2 = random.randint(88, 100) 
    
    return {
        "temperature": temperature,
        "pulse": pulse,
        "spo2": spo2
    }

# This part lets us test the simulator independently if we run this file directly
if __name__ == "__main__":
    print("Testing the patient data simulator. Press Ctrl+C to stop.\n")
    while True:
        vitals = generate_patient_data()
        print(f"Generated Vitals -> Temp: {vitals['temperature']}°F | Pulse: {vitals['pulse']} BPM | SpO2: {vitals['spo2']}%")
        time.sleep(3) # Wait 3 seconds before generating the next set