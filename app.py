from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import cv2
import base64
import numpy as np
from modules.gesture_detection import GestureRecognizer
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize gesture recognizer
gesture_recognizer = GestureRecognizer()

# Music control state
music_state = {
    'volume': 0.5,
    'is_playing': False,
    'current_song': 'calm.mp3',
    'gesture_mode': False,
    'playlist': ['calm.mp3', 'peace.mp3', 'relax.mp3']
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera-test')
def camera_test():
    return render_template('camera_test.html')

@app.route('/get_music_state')
def get_music_state():
    return jsonify(music_state)

@socketio.on('process_gesture')
def handle_gesture(data):
    try:
        # Decode the base64 image
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # Get gesture from the image
        current_gesture = gesture_recognizer.get_gesture(image)
        stable_gesture = gesture_recognizer.get_stable_gesture(current_gesture)
        
        # Process gesture commands
        if stable_gesture:
            response = process_gesture_command(stable_gesture)
            emit('gesture_response', response)
            # Also emit the updated music state
            emit('music_state_update', music_state)
        
        # Process volume changes on current gesture (not stable) for continuous adjustment
        if current_gesture and music_state['gesture_mode']:
            volume_response = process_volume_gesture(current_gesture)
            if volume_response['action'] != 'none':
                emit('gesture_response', volume_response)
                emit('music_state_update', music_state)
        
        # Always send current gesture for display
        emit('gesture_detected', {
            'gesture': current_gesture,
            'stable': stable_gesture is not None
        })
        
    except Exception as e:
        print(f"Error processing gesture: {e}")
        emit('error', {'message': str(e)})

def process_gesture_command(gesture):
    global music_state
    
    response = {'action': 'none', 'message': ''}
    
    if gesture == 'Victory':
        # Toggle gesture control mode
        music_state['gesture_mode'] = not music_state['gesture_mode']
        if music_state['gesture_mode']:
            response = {'action': 'mode_change', 'message': 'Gesture control activated!'}
        else:
            response = {'action': 'mode_change', 'message': 'Gesture control deactivated'}
    
    elif music_state['gesture_mode']:
        if gesture == 'Open_Palm':
            # Toggle music play/stop
            if music_state['is_playing']:
                music_state['is_playing'] = False
                response = {'action': 'stop', 'message': 'Music paused'}
            else:
                music_state['is_playing'] = True
                response = {'action': 'play', 'message': 'Music playing'}
    
    return response

def process_volume_gesture(gesture):
    global music_state
    
    response = {'action': 'none', 'message': ''}
    
    if gesture == 'Thumb_Up':
        # Volume up gradually (1% at a time)
        old_volume = music_state['volume']
        music_state['volume'] = min(1.0, music_state['volume'] + 0.01)
        if music_state['volume'] != old_volume:  # Only respond if volume actually changed
            response = {'action': 'volume_change', 'volume': music_state['volume'], 'message': f'Volume: {int(music_state["volume"] * 100)}%'}
    
    elif gesture == 'Thumb_Down':
        # Volume down gradually (1% at a time)
        old_volume = music_state['volume']
        music_state['volume'] = max(0.0, music_state['volume'] - 0.01)
        if music_state['volume'] != old_volume:  # Only respond if volume actually changed
            response = {'action': 'volume_change', 'volume': music_state['volume'], 'message': f'Volume: {int(music_state["volume"] * 100)}%'}
    
    return response

@socketio.on('music_control')
def handle_music_control(data):
    global music_state
    
    action = data.get('action')
    
    if action == 'play':
        music_state['is_playing'] = True
        music_state['current_song'] = data.get('song', music_state['current_song'])
    elif action == 'pause':
        music_state['is_playing'] = False
    elif action == 'volume':
        music_state['volume'] = data.get('volume', music_state['volume'])
    elif action == 'next':
        current_index = music_state['playlist'].index(music_state['current_song'])
        next_index = (current_index + 1) % len(music_state['playlist'])
        music_state['current_song'] = music_state['playlist'][next_index]
    elif action == 'prev':
        current_index = music_state['playlist'].index(music_state['current_song'])
        prev_index = (current_index - 1) % len(music_state['playlist'])
        music_state['current_song'] = music_state['playlist'][prev_index]
    
    emit('music_state_update', music_state)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 