import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";

function App() {
  const [message, setMessage] = useState("");
  const [fileName, setFileName] = useState("");

  const onDrop = useCallback((acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    setFileName(uploadedFile.path);
    onUpload(uploadedFile);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const onUpload = (fileToUpload) => {
    const formData = new FormData();
    formData.append("file", fileToUpload);

    fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          window.location.href = `http://localhost:5000/download/${data.filename}`;
          setMessage("Erfolgreich");
        } else {
          setMessage("Fehler");
        }
      })
      .catch((error) => {
        console.error("Error uploading the file:", error);
        setMessage("Fehler");
      });
  };

  return (
    <div className="bg-[#F2F6FF] flex flex-col  w-[100%] p-4 select-none">
      <h1 className="text-[#2B83FB] font-bold text-3xl mx-auto">
        ETM - Converter
      </h1>
      <div className="relative m-auto mt-10 bg-white max-w-[1000px] w-full min-h-[800px] flex flex-col p-10 shadow-2xl items-center">
        <div
          {...getRootProps()}
          className="cursor-pointer mx-auto border border-[#2B83FB] border-dashed  w-full max-w-[600px] h-[160px] flex flex-col items-center p-4 gap-4 "
        >
          <input {...getInputProps()} />
          <p className="text-black font-medium text-2xl">
            Drag & Drop to upload
          </p>
          <p className="text-black font-light text-sm ">CSV Files only</p>
          <p className="text-sm text-gray-500">{"File name : " + fileName}</p>
        </div>
        <p className="mt-5 text-sm text-[#636E72] font-medium translate-x-[-19px] ">
          Once the processing is done your file should download:
        </p>
        <p
          className={
            message === "Erfolgreich"
              ? "text-green-500 font-bold"
              : "text-red-500 font-bold"
          }
        >
          {message}
        </p>{" "}
      </div>
    </div>
  );
}

export default App;
