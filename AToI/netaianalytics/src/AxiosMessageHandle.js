import axios from 'axios';

function sendMessage(message) {
  axios.post('/chat/message', { message })
    .then(response => {
      // Handle the response from the server
      console.log(response.data);
    })
    .catch(error => {
      // Handle any errors
      console.error('There was an error!', error);
    });
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('data_file', file);
  
    axios.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(response => {
      // Handle the response from the server
      console.log(response.data);
    })
    .catch(error => {
      // Handle any errors
      console.error('There was an error!', error);
    });
  }

  export { sendMessage };
  export { uploadFile };
  