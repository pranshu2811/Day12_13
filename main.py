import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Create Socket.IO server with Async mode
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()

# Create Socket.IO ASGI application
socket_app = socketio.ASGIApp(sio, app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("response", {"data": "Welcome! You are connected."}, to=sid)

@sio.event
async def message(sid, data):
    print(f" Message from {sid}: {data}")
    
    try:
        # Use gemini-1.5-flash for fast responses
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(data)

        # Send AI-generated response
        if response.text:
            await sio.emit("response", {"data": f"Bot: {response.text}"}, to=sid)
        else:
            await sio.emit("response", {"data": "Bot: Sorry, I couldn't process that."}, to=sid)
    
    except Exception as e:
        print(f" Error generating response: {e}")
        await sio.emit("response", {"data": "Bot: An error occurred while generating a response."}, to=sid)

@sio.event
async def disconnect(sid):
    print(f" Client disconnected: {sid}")

# Root endpoint to verify server is running
@app.get("/")
async def root():
    return {"message": "WebSocket Backend Running Successfully"}
