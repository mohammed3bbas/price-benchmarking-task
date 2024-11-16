from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.cruds.user_rate import create_user_rate
from app.database_settings import SessionLocal
from app.utils.file_uplode import parse_csv

router = APIRouter()

def get_session_local():
    yield SessionLocal()

@router.post("/csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_session_local)):
    """
    Endpoint to upload a CSV file containing user rates and save it to the database.
    """
    try:
        file_contents = await file.read()

        # convert dates to YY/MM/DD
        user_rates = parse_csv(file_contents)
        
        for rate in user_rates:
            create_user_rate(db, rate)

        return {"message": "File uploaded successfully and data saved."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in processing the CSV file: {e}")
