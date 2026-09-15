import base64
import json
import requests
from pathlib import Path


LLAMA_COMPLETION_URL = "http://127.0.0.1:8080/completion"

BASE_DIR = Path(__file__).resolve().parent

JSON_DIR = BASE_DIR / "Json"
JPG_DIR = BASE_DIR / "jpg"

DETECTED_OBJECTS_JSON = JSON_DIR / "detected_objects.json"
VOICE_COMMAND_JSON = JSON_DIR / "voice_command.json"
VLM_RESULT_JSON = JSON_DIR / "vlm_result.json"
QWEN_RAW_TXT = JSON_DIR / "qwen_raw_response.txt"

CAMERA_OVERLAY_IMAGE = JPG_DIR / "camera_overlay.jpg"


def load_json(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"파일이 없습니다: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def image_to_base64(image_path):
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"이미지 파일이 없습니다: {image_path}")

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def normalize_command(text):
    text = text or ""

    target_hint = None
    action_hint = "none"

    if "마우스" in text:
        target_hint = "mouse"

    elif "컵" in text:
        target_hint = "cup"

    elif "휴대폰" in text or "핸드폰" in text or "폰" in text:
        target_hint = "cell phone"

    elif "병" in text or "물병" in text:
        target_hint = "bottle"

    elif "리모컨" in text or "리모콘" in text or "원격" in text or "remote" in text:
        target_hint = "remote"

    if any(word in text for word in ["집어", "잡아", "들어", "가져와"]):
        action_hint = "pick"
    elif "열어" in text:
        action_hint = "open_gripper"
    elif "닫아" in text:
        action_hint = "close_gripper"
    elif "홈" in text or "기본" in text:
        action_hint = "move_home"

    return {
        "raw_text": text,
        "target_hint": target_hint,
        "action_hint": action_hint
    }


def build_user_text(voice_data, detected_objects):
    command_info = normalize_command(voice_data.get("text", ""))

    return f"""
You are a robot object selector.

Look at the image first.
The image contains object bounding boxes and ID labels.

Use detected_objects as the source of truth.

Command:
{json.dumps(command_info, ensure_ascii=False)}

Detected objects:
{json.dumps(detected_objects, ensure_ascii=False)}

Task:
Choose the target object id.

Rules:
1. Return only valid JSON.
2. No markdown.
3. No explanation outside JSON.
4. target_id must be one of the ids in detected_objects.
5. If action_hint is "pick", choose the object whose class equals target_hint.
6. If no matching object exists, return action "none" and target_id null.
7. Do not create bbox.
8. Do not create center_pixel.
9. Do not create class name.

Return exactly:
{{"action":"pick","target_id":1,"reason":"matched target_hint"}}
""".strip()


def extract_json_from_text(text):
    if not text:
        raise ValueError("empty response")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("JSON block not found")

    return json.loads(text[start:end + 1])


def deterministic_fallback(voice_data, detected_objects, reason):
    command_info = normalize_command(voice_data.get("text", ""))
    action_hint = command_info["action_hint"]
    target_hint = command_info["target_hint"]

    if action_hint in ["open_gripper", "close_gripper", "move_home"]:
        return {
            "action": action_hint,
            "target_id": None,
            "target_class": None,
            "target_center_pixel": None,
            "bbox": None,
            "reason": f"Fallback: {reason}"
        }

    if action_hint == "pick" and target_hint is not None:
        for obj in detected_objects:
            if obj["class"] == target_hint:
                return {
                    "action": "pick",
                    "target_id": obj["id"],
                    "target_class": obj["class"],
                    "target_center_pixel": obj["center_pixel"],
                    "bbox": obj["bbox"],
                    "reason": f"Fallback: command target matched {target_hint}. {reason}"
                }

    return {
        "action": "none",
        "target_id": None,
        "target_class": None,
        "target_center_pixel": None,
        "bbox": None,
        "reason": f"Fallback failed: {reason}"
    }


def fill_result_from_detected_objects(vlm_result, voice_data, detected_objects):
    action = vlm_result.get("action")
    target_id = vlm_result.get("target_id")

    if action in ["open_gripper", "close_gripper", "move_home"]:
        return {
            "action": action,
            "target_id": None,
            "target_class": None,
            "target_center_pixel": None,
            "bbox": None,
            "reason": vlm_result.get("reason", "")
        }

    if action == "pick":
        for obj in detected_objects:
            if obj["id"] == target_id:
                return {
                    "action": "pick",
                    "target_id": obj["id"],
                    "target_class": obj["class"],
                    "target_center_pixel": obj["center_pixel"],
                    "bbox": obj["bbox"],
                    "reason": f"사용자 명령과 일치하는 객체 '{obj['class']}'를 선택했습니다."
                }

    return deterministic_fallback(
        voice_data,
        detected_objects,
        reason=f"Qwen selected invalid target_id={target_id}"
    )


def call_qwen_vlm():
    print("사용 경로 확인")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"DETECTED_OBJECTS_JSON: {DETECTED_OBJECTS_JSON}")
    print(f"VOICE_COMMAND_JSON: {VOICE_COMMAND_JSON}")
    print(f"CAMERA_OVERLAY_IMAGE: {CAMERA_OVERLAY_IMAGE}")
    print(f"VLM_RESULT_JSON: {VLM_RESULT_JSON}")

    voice_data = load_json(VOICE_COMMAND_JSON)
    detected_objects = load_json(DETECTED_OBJECTS_JSON)

    print("\n[DEBUG] voice_data:")
    print(json.dumps(voice_data, ensure_ascii=False, indent=4))

    print("\n[DEBUG] detected_objects:")
    print(json.dumps(detected_objects, ensure_ascii=False, indent=4))

    command_info = normalize_command(voice_data.get("text", ""))
    print("\n[DEBUG] command_info:")
    print(json.dumps(command_info, ensure_ascii=False, indent=4))

    image_base64 = image_to_base64(CAMERA_OVERLAY_IMAGE)
    user_text = build_user_text(voice_data, detected_objects)

    prompt = f"""
    <|im_start|>user
    [img-1]
    {user_text}
    <|im_end|>
    <|im_start|>assistant
    """.strip()

    payload = {
        "prompt": prompt,
        "image_data": [
            {
                "data": image_base64,
                "id": 1
            }
        ],
        "temperature": 0.0,
        "top_p": 0.1,
        "n_predict": 64,
        "stop": ["<|im_end|>", "</s>"]
    }
    print("\nQwen2.5-VL llama.cpp 서버 호출 중...")

    try:
        response = requests.post(
        LLAMA_COMPLETION_URL,
        json=payload,
        timeout=180
    )

        response.raise_for_status()
        result = response.json()

        raw_text = result.get("content", "")

        with open(QWEN_RAW_TXT, "w", encoding="utf-8") as f:
            f.write(raw_text)

        print("\nQwen 원본 응답:")
        print(raw_text)

        parsed = extract_json_from_text(raw_text)

        final_result = fill_result_from_detected_objects(
            parsed,
            voice_data,
            detected_objects
        )

    except Exception as e:
        print(f"\nQwen 처리 실패: {e}")

        final_result = deterministic_fallback(
            voice_data,
            detected_objects,
            reason=str(e)
        )

    with open(VLM_RESULT_JSON, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=4)

    print(f"\nVLM 결과 저장 완료: {VLM_RESULT_JSON}")
    print(json.dumps(final_result, ensure_ascii=False, indent=4))

    return final_result


if __name__ == "__main__":
    call_qwen_vlm()