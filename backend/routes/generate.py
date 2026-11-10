"""SDD generation and document export routes."""

import json
import re

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from schemas.sdd_schema import SDDExportRequest
from services.document_service import generate_docx, generate_pdf
from services.sdd_service import generate_sdd

router = APIRouter()


class GenerateSDDRequest(BaseModel):
    project_name: str = Field(default="IT Support Ticket System", min_length=1)
    pdd_text: str = Field(min_length=20)


@router.post("/generate-sdd")
async def generate_sdd_endpoint(request: GenerateSDDRequest):
    try:
        sdd = generate_sdd(
            pdd_text=request.pdd_text,
            project_name=request.project_name,
        )
        return {
            "message": "SDD generated successfully.",
            "sdd": sdd.model_dump(),
        }
    except (ValueError, json.JSONDecodeError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except Exception as error:
        # Avoid returning internal implementation details to the client.
        raise HTTPException(
            status_code=502,
            detail="SDD generation failed. Check the backend logs for details.",
        ) from error


@router.post("/sdd/export/docx")
async def export_sdd_docx(request: SDDExportRequest):
    try:
        buffer = generate_docx(request.sdd, request.project_name)
        filename = re.sub(r"[^a-zA-Z0-9_-]", "_", request.project_name)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{filename}_SDD.docx"'},
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="DOCX generation failed. Check the backend logs for details.",
        ) from error


@router.post("/sdd/export/pdf")
async def export_sdd_pdf(request: SDDExportRequest):
    try:
        buffer = generate_pdf(request.sdd, request.project_name)
        filename = re.sub(r"[^a-zA-Z0-9_-]", "_", request.project_name)
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}_SDD.pdf"'},
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="PDF generation failed. Check the backend logs for details.",
        ) from error
