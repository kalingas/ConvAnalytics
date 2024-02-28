import React, { useState } from 'react';
import './App.css';
import ChatbotComponent from './ChatbotComponent';

function App() {
  const [messages, setMessages] = useState([]);

  const handleUserInput = (input) => {
    // Handle user input here
    const newMessage = { text: input, isBot: false };
    setMessages([...messages, newMessage]);

    // Simulate bot response
    setTimeout(() => {
      const botMessage = { text: `You said: ${input}`, isBot: true };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    }, 1000);
  };

  return (
    <div className="App">
      <header className="App-header">
        NetAiAnalytics
      </header>
      <ChatbotComponent messages={messages} onUserInput={handleUserInput} />
    </div>
  );
}

export default App;
