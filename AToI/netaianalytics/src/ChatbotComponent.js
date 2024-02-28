import React, { useState, useRef } from 'react';
import './ChatbotComponent.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faPlus } from '@fortawesome/free-solid-svg-icons';
import { sendMessage } from './AxiosMessageHandle';
import { uploadFile } from './AxiosMessageHandle';
import axios from 'axios';

const ChatbotComponent = ({ messages, onUserInput }) => {
  const [input, setInput] = useState('');
  const fileInputRef = useRef(null);

  // const handleSubmit = (event) => {
  //   event.preventDefault();
  //   if (input.trim()) {
  //     onUserInput(input);
  //     setInput('');
  //   }
  // };
  const handleSubmit = (event) => {
    // Assuming `input` is the state variable that holds the message from the textarea
    sendMessage(input)
      .then(response => {
        // Handle the response from the server
        console.log(response.data);
        // Clear the input field after sending the message
        setInput('');
      })
      .catch(error => {
        // Handle any errors
        console.error('There was an error!', error);
      });
  };

  // const handleFileUpload = (event) => {
  //   const files = event.target.files;
  //   console.log(files);
  //   uploadFile(files)
  //   .then(response => {
  //     // Handle the successful file upload response
  //     console.log('File uploaded successfully', response.data);
  //     // You can call onFileUpload here if you want to lift the state up or trigger a callback
  //     // onFileUpload(files);
  //   })
  //   .catch(error => {
  //     // Handle any errors during file upload
  //     console.error('Error uploading file:', error);
  //   });
  // };

  function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
  
      axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(response => {
        console.log(response.data);
        // Handle the response data
      })
      .catch(error => {
        console.error('Error:', error);
      });
    }
  }

  const handleFileButtonClick = () => {
    fileInputRef.current.click();
  };
  

  return (
    <div className="chat-container">
      <div className="message-area">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.isBot ? 'bot-message' : 'user-message'}`}>
            {message.text}
          </div>
        ))}
      </div>
      <form className="input-area" onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
          className="input-field"
          rows={1}
        />
        <button type="button" className="icon-button file-upload-button" onClick={handleFileButtonClick}>
          <FontAwesomeIcon icon={faPlus} />
        </button>
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileUpload}
        />
        <button type="submit" className="icon-button send-button">
          <FontAwesomeIcon icon={faPaperPlane} />
        </button>
      </form>
    </div>
  );
};

export default ChatbotComponent;

