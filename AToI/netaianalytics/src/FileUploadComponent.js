import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const FileUploadComponent = ({ onFileUpload }) => {
  const onDrop = useCallback(acceptedFiles => {
    // Do something with the files
    onFileUpload(acceptedFiles);
  }, [onFileUpload]);

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()} style={{ border: '2px dashed black', padding: '20px', textAlign: 'center' }}>
      <input {...getInputProps()} />
      <p>Drag 'n' drop some files here, or click to select files</p>
    </div>
  );
};

export default FileUploadComponent;
