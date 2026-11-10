"""Document upload routes."""

from fastapi import APIRouter, UploadFile, File, HTTPException

from services.document_service import extract_text

router = APIRouter()


@router.post("/upload-pdd")
async def upload_pdd(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required."
        )

    extension = file.filename.lower().split(".")[-1]

    if extension not in ["pdf", "docx", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are supported."
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File size must be less than 10 MB."
        )

    try:
        extracted_text = extract_text(
            file_bytes=file_bytes,
            filename=file.filename
        )

        return {
            "filename": file.filename,
            "message": "PDD uploaded successfully.",
            "extracted_text": extracted_text
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to extract document text."
        )
