
import { useState } from "react";
import {
  Sparkles,
  FileCheck,
  RotateCcw,
} from "lucide-react";

import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
import GenerationStatus from "./components/GenerationStatus";
import SDDPreview from "./components/SDDPreview";
import PDDPreview from "./components/PDDPreview";
import DownloadDropdown from "./components/DownloadDropdown";

import {
  uploadPDD,
  generateSDD,
  exportSDD,
} from "./services/api";

import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [pddText, setPddText] = useState("");
  const [sdd, setSdd] = useState(null);

  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [uploadCompleted, setUploadCompleted] =
    useState(false);

  // Handle file selection
  const handleFileChange = (selectedFile) => {
    setFile(selectedFile);
    setFilename(selectedFile?.name || "");

    setPddText("");
    setSdd(null);

    setError("");
    setUploadCompleted(false);
  };

  // Upload and extract PDD
  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDD document first.");
      return;
    }

    try {
      setError("");
      setStatus("uploading");

      const response = await uploadPDD(file);

      setPddText(response.extracted_text);
      setUploadCompleted(true);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to upload and extract PDD."
      );
    } finally {
      setStatus("");
    }
  };

  // Generate SDD using Gen AI
  const handleGenerateSDD = async () => {
    if (!pddText.trim()) {
      setError("Please upload and extract a PDD first.");
      return;
    }

    try {
      setError("");
      setStatus("generating");
      setSdd(null);

      const response = await generateSDD(
        "IT Support Ticket System",
        pddText
      );

      setSdd(response.sdd);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to generate SDD."
      );
    } finally {
      setStatus("");
    }
  };

  // Download SDD as DOCX or PDF

const handleDownload = async (format) => {
  if (!sdd) {
    setError("Please generate the SDD first.");
    return;
  }

  try {
    setError("");
    setStatus("downloading");

    const blob = await exportSDD(sdd, format);

    if (!(blob instanceof Blob) || blob.size === 0) {
      throw new Error("The server returned an empty file.");
    }

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");

    const projectName = (
      sdd.project_name || "Generated_Document"
    ).replace(/\s+/g, "_");

    link.href = url;
    link.download = `${projectName}_SDD.${format}`;

    document.body.appendChild(link);
    link.click();
    link.remove();

    // Give the browser time to start the download
    window.setTimeout(() => {
      window.URL.revokeObjectURL(url);
    }, 1000);

  } catch (err) {
    console.error("SDD download error:", err);

    setError(
      err.message ||
        `Failed to download ${format.toUpperCase()} document.`
    );
  } finally {
    setStatus("");
  }
};


  // Reset application
  const handleReset = () => {
    setFile(null);
    setFilename("");
    setPddText("");
    setSdd(null);

    setStatus("");
    setError("");
    setUploadCompleted(false);
  };

  return (
    <div className="app">
      <Header />

      <main className="main-container">
        {/* Hero Section */}
        <section className="page-intro">
          <span className="eyebrow">
            DOCUMENT AUTOMATION
          </span>

          <h1>
            Transform your PDD into
            <span> a technical design</span>
          </h1>

          <p>
            Upload your Process Design Document and let AI
            generate a structured Solution Design Document
            in seconds.
          </p>
        </section>

        {/* Main Workspace */}
        <div className="workspace">

          {/* LEFT PANEL - PDD */}
          <div className="input-panel">
            <div className="panel-heading">
              <div>
                <span className="step-label">
                  STEP 01
                </span>

                <h2>Input Document</h2>
              </div>

              <FileCheck size={24} />
            </div>

            {/* File Upload */}
            <FileUpload
              file={file}
              onFileChange={handleFileChange}
              disabled={Boolean(status)}
            />

            {/* Extract PDD */}
            {file && !uploadCompleted && (
              <button
                className="primary-button"
                onClick={handleUpload}
                disabled={Boolean(status)}
              >
                <Sparkles size={18} />
                Extract PDD
              </button>
            )}

            {/* Upload Success */}
            {uploadCompleted && (
              <div className="success-message">
                <FileCheck size={18} />
                PDD extracted successfully
              </div>
            )}

            {/* PDD Preview */}
            {uploadCompleted && (
              <PDDPreview
                pddText={pddText}
                filename={filename}
              />
            )}

            {/* Generate SDD */}
            {uploadCompleted && (
              <button
                className="primary-button generate-button"
                onClick={handleGenerateSDD}
                disabled={Boolean(status)}
              >
                <Sparkles size={18} />
                Generate SDD
              </button>
            )}

            {/* Loading Status */}
            {status && (
              <GenerationStatus status={status} />
            )}

            {/* Error */}
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {/* Reset */}
            <button
              className="reset-button"
              onClick={handleReset}
              disabled={Boolean(status)}
            >
              <RotateCcw size={16} />
              Start Over
            </button>
          </div>

          {/* RIGHT PANEL - SDD */}
          <div className="output-panel">
            <div className="panel-heading">
              <div>
                <span className="step-label">
                  STEP 02
                </span>

                <h2>Generated SDD</h2>
              </div>

              <Sparkles size={24} />
            </div>

            {/* Empty State */}
            {!sdd && (
              <div className="empty-state">
                <div className="empty-state-icon">
                  <FileCheck size={38} />
                </div>

                <h3>Your SDD will appear here</h3>

                <p>
                  Upload a PDD and click Generate SDD
                  to create your technical document.
                </p>
              </div>
            )}

            {/* Generated SDD */}
            {sdd && (
              <>
                <SDDPreview sdd={sdd} />

                {/* Download Dropdown */}
                <DownloadDropdown
                  onDownload={handleDownload}
                  disabled={Boolean(status)}
                />
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
