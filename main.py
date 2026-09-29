from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from similarity import compute_similarity

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/compare")
async def compare_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    code1 = (await file1.read()).decode("utf-8", errors="ignore")
    code2 = (await file2.read()).decode("utf-8", errors="ignore")

    result = compute_similarity(code1, code2)
    result["file1_name"] = file1.filename
    result["file2_name"] = file2.filename
    result["file1_content"] = code1
    result["file2_content"] = code2

    return result


@app.get("/")
def root():
    return {"message": "Code Similarity Checker API is running"}