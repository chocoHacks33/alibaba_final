
# eas_inference.py

import requests
import time

EAS_URL = "http://quickstart-deploy-20250410-g9hk.5158343315505498.ap-northeast-1.pai-eas.aliyuncs.com"
EAS_TOKEN = "MWFjNDk4NDlkYTRjOTFhOTY4NjE0NDE1ZWFiZWVhMjhjMDFkN2VhNw=="


class TaskStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


def generate_video(prompt: str, output_path: str = "generated_video.mp4") -> str:
    # Step 1: Submit generation request
    response = requests.post(
        f"{EAS_URL}/generate",
        headers={"Authorization": EAS_TOKEN},
        json={
            "prompt": prompt,
            "seed": 42,
            "neg_prompt": "low quality, blurry",
            "infer_steps": 50,
            "cfg_scale": 7.5,
            "height": 720,
            "width": 1280
        }
    )

    if response.status_code != 200:
        raise Exception(f"Failed to start generation: {response.text}")

    task_id = response.json()["task_id"]
    print(f"🎬 Task submitted. ID: {task_id}")

    # Step 2: Poll for status
    while True:
        status_response = requests.get(
            f"{EAS_URL}/tasks/{task_id}/status",
            headers={"Authorization": EAS_TOKEN}
        )

        if status_response.status_code != 200:
            raise Exception(f"Status check failed: {status_response.text}")

        status = status_response.json()
        print(f"⏳ Status: {status['status']}")

        if status["status"] == TaskStatus.COMPLETED:
            break
        elif status["status"] == TaskStatus.FAILED:
            raise Exception(f"Generation failed: {status['error']}")

        time.sleep(30)

    # Step 3: Download video
    video_response = requests.get(
        f"{EAS_URL}/tasks/{task_id}/video",
        headers={"Authorization": EAS_TOKEN}
    )

    with open(output_path, "wb") as f:
        f.write(video_response.content)

    print("✅ Video downloaded successfully.")
    return output_path