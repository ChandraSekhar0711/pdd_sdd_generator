"""Schemas for structured software design documents."""

from typing import Any

from pydantic import BaseModel, Field


class SDDExportRequest(BaseModel):
    project_name: str
    sdd: dict[str, Any]


class APIEndpoint(BaseModel):
    method: str = Field(description="HTTP method")
    endpoint: str = Field(description="API path")
    description: str = Field(description="Purpose of the endpoint")
    request_body: str = Field(description="Request body/schema; use 'None' if absent")
    response: str = Field(description="Successful response/schema")
    authentication: str = Field(description="Authentication required; distinguish PDD facts from assumptions")
    authorization: str = Field(description="Role/permission requirement, or 'Not specified in PDD'")
    status_codes: list[str] = Field(description="Relevant HTTP status codes and meanings")
    requirement_traceability: str = Field(description="PDD requirement supporting this endpoint, or 'Assumption'/'Open question'")


class DatabaseEntity(BaseModel):
    name: str = Field(description="Database entity/table name")
    fields: list[str] = Field(description="Fields with types where known; unknown types should be marked unspecified")
    description: str = Field(description="Purpose of the entity")
    relationships: list[str] = Field(description="Relationships to other entities, only if supported or marked as assumptions")


class SDD(BaseModel):
    project_name: str
    document_information: list[str] = Field(description="Document version/status and source PDD details if available; otherwise say Not specified")
    overview: str
    scope: list[str] = Field(description="In-scope and out-of-scope items explicitly supported by PDD; unknowns marked")
    requirements_summary: list[str] = Field(description="Functional requirements distilled from PDD, each traceable")
    architecture: str = Field(description="Layered architecture description and request/data flow; no unsupported design decisions")
    component_design: list[str] = Field(description="Components and responsibilities across layers")
    frontend_components: list[str]
    backend_modules: list[str]
    api_endpoints: list[APIEndpoint]
    database_entities: list[DatabaseEntity]
    data_flow: list[str] = Field(description="Step-by-step key flows supported by PDD; gaps flagged")
    business_logic: list[str]
    ticket_lifecycle: list[str] = Field(description="Lifecycle states and transitions only as specified; uncertainties in open_questions")
    validation_rules: list[str]
    security_requirements: list[str]
    error_handling: list[str]
    non_functional_requirements: list[str] = Field(description="Performance, availability, scalability, maintainability etc. only if specified; missing ones become open questions")
    logging_monitoring: list[str] = Field(description="Logging/monitoring needs supported by PDD, or identify as not specified")
    deployment_architecture: list[str] = Field(description="Environment and deployment details from PDD; unsupported details marked as assumptions")
    assumptions: list[str]
    dependencies: list[str] = Field(description="External/system/library dependencies from PDD or explicitly labeled assumptions")
    acceptance_criteria: list[str] = Field(description="Criteria derived from PDD requirements; avoid inventing thresholds")
    open_questions: list[str]
