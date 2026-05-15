# 🎵 Gesture-Controlled Music Web App

A modern web application that allows you to control music playback using hand gestures detected through your camera.

## Demo

<video width="100%" controls autoplay muted loop playsinline>
   <source src="./DEMO.webm" type="video/webm">
   Your browser does not support the video tag. You can download the demo video [here](DEMO.webm).
</video>

## Features

- **🎶 Music Player**: Play, pause, stop, and navigate through your music playlist
- **👋 Gesture Control**: Control music using hand gestures detected by your camera
- **🎨 Modern UI**: Clean, responsive interface with a beautiful gradient design
- **📱 Mobile Friendly**: Works on both desktop and mobile devices

## Gesture Commands

1. **✌️ Victory Sign**: Toggle gesture control mode (enter/exit)
2. **👍 Thumbs Up**: Increase volume gradually (1% per detection)
3. **👎 Thumbs Down**: Decrease volume gradually (1% per detection)
4. **✋ Open Palm**: Toggle music play/pause

## Installation

1. Make sure you have Python 3.8+ installed
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Allow camera access when prompted

4. Use the traditional music controls or activate gesture mode:
   - Show a **victory sign** ✌️ to activate gesture control
   - Use the gesture commands listed above
   - Show **victory sign** ✌️ again to exit gesture mode

## Music Files

The app includes three sample music tracks:
- `calm.mp3`
- `peace.mp3`
- `relax.mp3`

You can add your own music files to the `static/music/` directory.

## How It Works

- **Frontend**: HTML5 with WebSockets for real-time communication
- **Backend**: Flask server with Socket.IO for gesture processing
- **Computer Vision**: MediaPipe for hand gesture recognition
- **Camera**: Uses your device's camera to detect hand gestures

## System Requirements

- Python 3.8+
- Webcam/Camera
- Modern web browser with WebRTC support
- Internet connection (for loading Socket.IO from CDN)

## Troubleshooting

- **Camera not working**: Make sure to allow camera access in your browser
- **Gestures not detected**: Ensure good lighting and show your hand clearly to the camera
- **App not loading**: Check that all dependencies are installed and the virtual environment is activated

## License

This project is open source and available under the MIT License. 