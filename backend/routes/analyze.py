from fastapi import APIRouter, File, UploadFile, HTTPException
from backend.services.analyzer import run_pipeline

router = APIRouter()

@router.post("/analyze")
async def run_behavioral_analysis(video: UploadFile = File(...)):
    """
    Receives raw clinical tracking streams directly from clients for generalized visual parsing natively.
    """
    if not video.filename.endswith(('.mp4', '.webm')):
        raise HTTPException(status_code=400, detail="Invalid media type limits. Only formatting mp4 and webm securely.")
    
    # ----------------------------------------------------
    # Step 3 & 4 Integration: Wrapper execution + JSON output
    # ----------------------------------------------------
    try:
        # Load binary matrix and execute visually
        video_bytes = await video.read()
        results = run_pipeline(video_bytes, video.filename)
        
        # FastAPI natively structure-packs Python Objects into raw JSON targets
        return results
        
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
