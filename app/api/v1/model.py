from fastapi import APIRouter, Depends

from app.core.config import settings
from app.schemas.prompt import PromptRequest
from app.services.gemini_configurations import get_gemini_response
from app.services.get_current_user import get_current_user
from app.services.save_html import save_generated_html
from app.services.system_prompts import generate_description_from_title, generate_webpage_from_description

router = APIRouter()


@router.post("/generate-webpage")
async def generate_description(request: PromptRequest, current_user=Depends(get_current_user)):
    response_html = get_gemini_response(request.prompt, generate_webpage_from_description,
                                        f"Creator Name is {current_user.name}")

    file_id = save_generated_html(response_html)

    project_url = f"{settings.BASE_URL}projects/{file_id}.html"

    return {
        "project_url": project_url
    }


@router.post("/generate-description")
async def generate_description(request: PromptRequest, current_user=Depends(get_current_user)):
    response_text = get_gemini_response(request.prompt, generate_description_from_title, "")

    return {"description": response_text}
