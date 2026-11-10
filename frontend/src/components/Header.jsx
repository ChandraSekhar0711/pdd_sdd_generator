
import { FileText, Sparkles } from "lucide-react";

function Header() {
  return (
    <header className="app-header">
      <div className="brand">
        <div className="brand-icon">
          <FileText size={24} />
        </div>

        <div>
          <h1>PDD to SDD Generator</h1>
          <p>AI-powered solution design documentation</p>
        </div>
      </div>

      <div className="header-badge">
        <Sparkles size={16} />
        <span>Powered by Gen AI</span>
      </div>
    </header>
  );
}

export default Header;
