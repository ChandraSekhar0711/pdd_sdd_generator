
import {
  FileText,
  Layers,
  Code,
  Database,
  ShieldCheck,
  CircleAlert,
  ListChecks,
  Server,
} from "lucide-react";

function Section({ title, icon: Icon, children }) {
  return (
    <section className="sdd-section">
      <div className="sdd-section-heading">
        <Icon size={20} />
        <h3>{title}</h3>
      </div>

      {children}
    </section>
  );
}

function SDDPreview({ sdd }) {
  if (!sdd) return null;

  return (
    <div className="sdd-preview">
      <div className="sdd-document-header">
        <div className="document-icon">
          <FileText size={26} />
        </div>

        <div>
          <span className="document-label">
            GENERATED DOCUMENT
          </span>

          <h2>{sdd.project_name}</h2>
          <p>Solution Design Document</p>
        </div>
      </div>

      <Section title="Overview" icon={FileText}>
        <p className="section-description">
          {sdd.overview}
        </p>
      </Section>

      <Section title="System Architecture" icon={Layers}>
        <div className="architecture-card">
          {sdd.architecture}
        </div>
      </Section>

      <Section title="Frontend Components" icon={Code}>
        <ul className="sdd-list">
          {sdd.frontend_components?.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Section>

      <Section title="Backend Modules" icon={Server}>
        <ul className="sdd-list">
          {sdd.backend_modules?.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Section>

      <Section title="API Specifications" icon={Code}>
        <div className="api-list">
          {sdd.api_endpoints?.map((api, index) => (
            <div className="api-card" key={index}>
              <div className="api-header">
                <span className={`method method-${api.method.toLowerCase()}`}>
                  {api.method}
                </span>

                <code>{api.endpoint}</code>
              </div>

              <p>{api.description}</p>

              {api.request_body && (
                <div className="api-detail">
                  <strong>Request:</strong>
                  <p>{api.request_body}</p>
                </div>
              )}

              {api.response && (
                <div className="api-detail">
                  <strong>Response:</strong>
                  <p>{api.response}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </Section>

      <Section title="Database Design" icon={Database}>
        {sdd.database_entities?.map((entity, index) => (
          <div className="database-card" key={index}>
            <h4>{entity.name}</h4>
            <p>{entity.description}</p>

            <div className="field-list">
              {entity.fields?.map((field, fieldIndex) => (
                <span className="field-tag" key={fieldIndex}>
                  {field}
                </span>
              ))}
            </div>
          </div>
        ))}
      </Section>

      <Section title="Business Logic" icon={ListChecks}>
        <ul className="sdd-list">
          {sdd.business_logic?.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Section>

      <Section title="Validation Rules" icon={ListChecks}>
        <ul className="sdd-list">
          {sdd.validation_rules?.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Section>

      <Section title="Security Requirements" icon={ShieldCheck}>
        <ul className="sdd-list">
          {sdd.security_requirements?.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Section>

      <Section title="Error Handling" icon={CircleAlert}>
        <ul className="sdd-list">
          {sdd.error_handling?.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Section>

      <Section title="Assumptions" icon={ListChecks}>
        <ul className="sdd-list">
          {sdd.assumptions?.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Section>

      <Section title="Open Questions" icon={CircleAlert}>
        <ul className="sdd-list">
          {sdd.open_questions?.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Section>
    </div>
  );
}

export default SDDPreview;
