
import requests
import time

EAS_URL = "http://quickstart-deploy-20250410-g9hk.5158343315505498.ap-northeast-1.pai-eas.aliyuncs.com"
EAS_TOKEN = "MWFjNDk4NDlkYTRjOTFhOTY4NjE0NDE1ZWFiZWVhMjhjMDFkN2VhNw=="


class TaskStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


response = requests.post(
    f"{EAS_URL}/generate",
    headers={
        "Authorization": f"{EAS_TOKEN}"
    },
    json={
        "prompt": "A spaceship orbiting Earth",
        "seed": 42,
        "neg_prompt": "low quality, blurry",
        "infer_steps": 50,
        "cfg_scale": 7.5,
        "height": 720,
        "width": 1280
    }
)
task_id = response.json()["task_id"]
print(response.json())

while True:
    status_response = requests.get(
        f"{EAS_URL}/tasks/{task_id}/status",
        headers={
            "Authorization": f"{EAS_TOKEN}"
        })
    status = status_response.json()

    print(f"Current status: {status['status']}")

    if status["status"] == TaskStatus.COMPLETED:
        print("Video ready!")
        break
    elif status["status"] == TaskStatus.FAILED:
        print(f"Failed: {status['error']}")
        exit(1)

    time.sleep(30)

video_response = requests.get(
    f"{EAS_URL}/tasks/{task_id}/video",
    headers={
        "Authorization": f"{EAS_TOKEN}"
    })
with open("generated_video.mp4", "wb") as f:
    f.write(video_response.content)

print("Video downloaded successfully!")

