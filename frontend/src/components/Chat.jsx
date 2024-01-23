import React, { useState, useEffect, useRef } from "react";
import chaticon from "../assets/images/chaticon.png";

const Chat = ({ isOpen, onClose }) => {
  const [showChat, setShowChat] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const messagesRef = useRef(null);

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);
  };

  const handleSendMessage = () => {
    if (inputMessage.trim() !== "") {
      const prevMessages = messages;
      setMessages([
        ...prevMessages,
        { text: inputMessage, sender: "user" },
        { text: "Sure, I'll get back to you!", sender: "bot" }, //We can set the logic here
      ]);
      setInputMessage("");
    }
  };

  useEffect(() => {
    // Scroll to the bottom when messages change
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    // Main Div
    <>
      {/* Chat Button */}
      <button
        type="button"
        className="absolute bottom-5 right-5 w-40 h-15 py-2 px-4 bg-white rounded-lg text-black font-medium shadow-lg transform transition-transform duration-300 hover:scale-110"
        onClick={() => {
          setShowChat(true);
          setMessages([
            { text: "Welcome! How can I assist you?", sender: "bot" },
          ]);
        }}
      >
        <img alt="chat-icon" src={chaticon} className="h-20 inline mr-2" />
        QnA
      </button>

      {/* Chat Interface */}
      <div
        className={`${
          showChat ? "block" : "hidden"
        } absolute z-10 bottom-32 right-5 w-100 `}
        id="Chat"
      >
        <div className="flex flex-col h-full bg-white rounded-lg overflow-hidden shadow-lg">
          {/* Chat Messages */}
          <div
            className="flex-1 px-4 py-2 overflow-y-auto max-h-64"
            ref={messagesRef}
          >
            {messages.map((message) => (
              <div
                className={`${
                  message.sender === "bot" ? "text-gray-700" : "text-black"
                } ${
                  message.sender === "bot" ? "text-left" : "text-right"
                } mb-2`}
              >
                {message.text}
              </div>
            ))}
          </div>

          {/* Chat Input */}
          <div className="flex items-center border-t border-gray-300 p-2">
            <input
              type="text"
              value={inputMessage}
              onChange={handleInputChange}
              placeholder="Type your message..."
              className="flex-1 outline-none focus:outline-black rounded bg-blue-100 p-2 mr-2"
            />
            <button
              type="button"
              className="py-2 px-4 bg-black rounded-lg text-white font-medium hover:bg-white hover:text-black hover: mr-2 transition duration-300"
              onClick={handleSendMessage}
            >
              Send
            </button>
            <button
              type="button"
              className="py-2 px-4 bg-red-500 rounded-lg text-white hover:bg-white hover:text-black hover: transition duration-300"
              onClick={onClose}
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Chat;
