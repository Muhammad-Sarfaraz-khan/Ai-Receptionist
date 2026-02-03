import { useState } from "react";

export default function ChatBox() {
  const [message, setMessage] = useState("");

  return (
    <div className="chat-container">
      <div className="chat-window">
        <div className="bot">👩‍💼 Hello! How can I assist you today?</div>
      </div>

      <div className="input-area">
        <input
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button>Send</button>
      </div>
    </div>
  );
}
