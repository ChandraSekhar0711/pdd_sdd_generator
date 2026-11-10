
import { useState } from "react";
import {
  Download,
  FileText,
  File,
  ChevronDown,
} from "lucide-react";

function DownloadDropdown({ onDownload, disabled }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleDownload = async (format) => {
    setIsOpen(false);
    await onDownload(format);
  };

  return (
    <div className="download-dropdown">
      <button
        className="download-main-button"
        disabled={disabled}
        onClick={() => setIsOpen((prev) => !prev)}
      >
        <Download size={18} />
        Download SDD
        <ChevronDown size={16} />
      </button>

      {isOpen && (
        <div className="download-menu">
          <button
            onClick={() => handleDownload("docx")}
          >
            <FileText size={18} />
            <span>
              <strong>Download DOCX</strong>
              <small>Microsoft Word document</small>
            </span>
          </button>

          <button
            onClick={() => handleDownload("pdf")}
          >
            <File size={18} />
            <span>
              <strong>Download PDF</strong>
              <small>Portable document format</small>
            </span>
          </button>
        </div>
      )}
    </div>
  );
}

export default DownloadDropdown;
