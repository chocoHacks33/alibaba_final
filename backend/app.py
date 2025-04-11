from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
import meta_marketing_api as fb
import qwen13B as model
from pydantic import BaseModel

app = FastAPI()


@app.get("/get-demographics")
def get_demographics(access_token: str):
    return fb.get_demographics(access_token)


@app.get("/get-pages")
def get_pages(token2: str):
    return fb.get_fb_page_id(token2)


@app.post("/create-campaign")
def create_campaign(token2: str, ad_account_id2: str):
    return fb.create_campaign(token2, ad_account_id2)


@app.post("/create-ad-set")
def create_ad_set(token2: str, ad_account_id2: str, campaign_id2: str):
    return fb.create_ad_set(token2, ad_account_id2, campaign_id2)


@app.post("/upload-video")
def upload_video(token2: str, ad_account_id2: str, video: UploadFile = File(...)):
    return fb.upload_facebook_ads(video.file, token2, ad_account_id2)


@app.post("/upload-thumbnail")
def upload_thumbnail(token2: str, ad_account_id2: str, image: UploadFile = File(...)):
    return fb.upload_ad_thumbnail(image.file, token2, ad_account_id2)


@app.post("/upload-creative")
def upload_creative(
    token2: str,
    ad_account_id2: str,
    page_id: str,
    video_id2: str,
    image_hash2: str,
    website_link: str
):
    return fb.upload_ad_creative(token2, ad_account_id2, page_id, video_id2, image_hash2, website_link)


@app.post("/create-ad")
def create_ad(
    token2: str,
    ad_account_id2: str,
    ad_set_id2: str,
    ad_creative_id2: str
):
    return fb.create_paused_ad(token2, ad_account_id2, ad_set_id2, ad_creative_id2)

class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate-video")
def generate_ai_video(request: PromptRequest):
    try:
        output_path = generate_video(request.prompt)
        return {"message": "Video generated successfully", "file_path": output_path}
    except Exception as e:
        return {"error": str(e)}
