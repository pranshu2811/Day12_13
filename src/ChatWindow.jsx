import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import "./App.css";

// Connect to FastAPI WebSocket backend
const socket = io("http://127.0.0.1:8000", {
  transports: ["websocket", "polling"],
});

const ChatWindow = () => {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState([]);

  useEffect(() => {
    // Listen for incoming messages from backend
    socket.on("response", (data) => {
      console.log("Response:", data);
      setResponse((prev) => [...prev, data.data]);
    });

    // Handle connection errors
    socket.on("connect_error", (err) => {
      console.error("❌ Connection error:", err);
    });

    return () => {
      socket.off("response");
      socket.off("connect_error");
    };
  }, []);

  const sendMessage = () => {
    if (message.trim()) {
      socket.emit("message", message); // Send message to backend
      setMessage(""); // Clear input after sending
    }
  };

  return (
    <div className="container">
      <h2>Real-Time Chat</h2>
      <div className="chat-box">
        {response.map((msg, idx) => (
          <div key={idx} className="message-box">
            {msg}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default ChatWindow;
