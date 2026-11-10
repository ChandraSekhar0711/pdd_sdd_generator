
import { FileText, FileCheck } from "lucide-react";

function PDDPreview({ pddText, filename }) {
  if (!pddText) {
    return (
      <div className="pdd-empty">
        <FileText size={32} />
        <h3>PDD Preview</h3>
        <p>Upload and extract a PDD to preview its content.</p>
      </div>
    );
  }

  return (
    <div className="pdd-preview">
      <div className="pdd-preview-header">
        <div className="pdd-file-icon">
          <FileCheck size={22} />
        </div>

        <div className="pdd-file-info">
          <h3>{filename || "PDD Document"}</h3>
          <p>Extracted document content</p>
        </div>
      </div>

      <div className="pdd-preview-content">
        <pre>{pddText}</pre>
      </div>
    </div>
  );
}

export default PDDPreview;
