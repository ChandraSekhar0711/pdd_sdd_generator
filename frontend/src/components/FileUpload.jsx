
import { useRef } from "react";
import { Upload, FileText, X } from "lucide-react";

function FileUpload({ file, onFileChange, disabled }) {
  const fileInputRef = useRef(null);

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    const allowedExtensions = ["pdf", "docx", "txt"];
    const extension = selectedFile.name
      .split(".")
      .pop()
      .toLowerCase();

    if (!allowedExtensions.includes(extension)) {
      alert("Please upload a PDF, DOCX, or TXT file.");
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      alert("File size must be less than 10 MB.");
      return;
    }

    onFileChange(selectedFile);
  };

  return (
    <div className="upload-section">
      <div className="section-heading">
        <div>
          <h2>Upload PDD Document</h2>
          <p>Upload your Process Design Document</p>
        </div>
      </div>

      {!file ? (
        <div
          className="upload-dropzone"
          onClick={() => !disabled && fileInputRef.current.click()}
        >
          <div className="upload-icon">
            <Upload size={28} />
          </div>

          <h3>Click to upload your PDD</h3>

          <p>
            PDF, DOCX or TXT · Maximum file size 10 MB
          </p>

          <button className="browse-button" type="button">
            Browse Files
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.txt"
            hidden
            disabled={disabled}
            onChange={(event) => {
              handleFile(event.target.files[0]);
              event.target.value = "";
            }}
          />
        </div>
      ) : (
        <div className="uploaded-file">
          <div className="file-icon">
            <FileText size={24} />
          </div>

          <div className="file-details">
            <h4>{file.name}</h4>
            <p>
              {(file.size / 1024).toFixed(2)} KB
            </p>
          </div>

          <button
            type="button"
            className="remove-file"
            disabled={disabled}
            onClick={() => onFileChange(null)}
            aria-label="Remove file"
          >
            <X size={20} />
          </button>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
