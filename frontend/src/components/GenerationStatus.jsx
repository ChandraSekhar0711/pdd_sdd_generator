
import { Bot, LoaderCircle } from "lucide-react";

function GenerationStatus({ status }) {
  if (!status) return null;

  return (
    <div className="generation-status">
      <div className="bot-icon">
        <Bot size={26} />
      </div>

      <div className="status-content">
        <h3>
          {status === "uploading"
            ? "Extracting PDD document..."
            : "Generating your SDD..."}
        </h3>

        <p>
          {status === "uploading"
            ? "Reading document content."
            : "AI is analyzing requirements and preparing the technical design."}
        </p>
      </div>

      <LoaderCircle className="loading-spinner" size={26} />
    </div>
  );
}

export default GenerationStatus;
