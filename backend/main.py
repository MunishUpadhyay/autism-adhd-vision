from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.analyze import router as analyze_router

app = FastAPI(title="Behavioral Analysis API", description="Vision-based computational tracking module")

# Enable wide open Cross Origin headers natively so Frontend bindings aren't isolated
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the routing bounds securely
app.include_router(analyze_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Behavioral Analysis API is live and mapped reliably"}
