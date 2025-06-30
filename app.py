from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import mediapipe as mp
import pickle
from googletrans import Translator

app = Flask(__name__)
CORS(app)

# Load the model
model_dict = pickle.load(open('./modelwords.p', 'rb'))
model = model_dict['modelwords']

# Setup mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Labels dictionary
labels_dict = {
    0: 'Hello', 1: "Bye", 2: 'man', 3: 'Women', 4: 'Thankyou', 
    5: 'welcome', 6: 'Sorry', 7: 'Namasthe', 8: 'Yes', 9: 'No',
    10: 'Good', 11: 'Bad', 12: 'Correct', 13: 'Wrong', 14: 'Easy', 
    15: 'Difficult'
}

def process_frame(frame):
    data_aux = []
    x_ = []
    y_ = []
    
    H, W, _ = frame.shape
    
    # Convert to RGB for mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame for hand landmarks
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)
            
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))
        
        # Pad data for consistent input size
        if len(results.multi_hand_landmarks) == 1:
            while len(data_aux) < 84:
                data_aux.append(0)
                
        if len(results.multi_hand_landmarks) == 2:
            while len(data_aux) < 84:
                data_aux.append(0)
                
        prediction = model.predict([np.asarray(data_aux)])
        return labels_dict[int(prediction[0])]
    
    return "No hand detected"

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # Read image file
    filestr = request.files['image'].read()
    npimg = np.frombuffer(filestr, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    # Process the frame
    gesture = process_frame(frame)
    
    return jsonify({'gesture': gesture})

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text')
        target_lang = data.get('target_lang')
        
        if not text or not target_lang:
            return jsonify({'error': 'Missing text or target language'}), 400
        
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        
        return jsonify({
            'translation': translation.text,
            'source_lang': translation.src,
            'target_lang': translation.dest
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
