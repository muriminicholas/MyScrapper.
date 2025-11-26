from fastapi import APIRouter
router = APIRouter()
@router.get("/test")
async def test():
    return {"message": "ScrapyFlow API is alive!"}
