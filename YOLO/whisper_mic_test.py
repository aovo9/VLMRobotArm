import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
from faster_whisper import WhisperModel

MODEL_SIZE = "tiny"

# 현재 whisper_mic_test.py 파일이 있는 폴더
BASE_DIR = Path(__file__).resolve().parent

# 프로젝트 내부 폴더
JSON_DIR = BASE_DIR / "Json"
AUDIO_DIR = BASE_DIR / "audio"

# 폴더가 없으면 자동 생성
JSON_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# 파일 경로
AUDIO_FILE = AUDIO_DIR / "mic_test.wav"
OUTPUT_JSON = JSON_DIR / "voice_command.json"


record_cmd = [
    "arecord",
    "-D", "plughw:2,0",
    "-f", "S16_LE",
    "-r", "16000",
    "-c", "1",
    "-d", "5",
    AUDIO_FILE
]

print("5초 동안 말하세요...")
record_result = subprocess.run(record_cmd)

if record_result.returncode != 0:
    print("녹음 실패")
    exit(1)

if not os.path.exists(AUDIO_FILE):
    print(f"녹음 파일이 없습니다: {AUDIO_FILE}")
    exit(1)

print("Whisper 모델 로딩 중...")
model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

print("음성 인식 중...")
segments, info = model.transcribe(
    AUDIO_FILE,
    language="ko",
    beam_size=5,
    initial_prompt="명령어는 마우스, 컵, 병, 휴대폰, 집어, 잡아, 열어, 닫아, 종료 중 하나입니다."
)

texts = []

for segment in segments:
    text = segment.text.strip()
    if text:
        texts.append(text)

final_text = " ".join(texts)

data = {
    "timestamp": datetime.now().isoformat(),
    "language": info.language,
    "text": final_text
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("감지 언어:", info.language)
print("인식 결과:", final_text)
print(f"저장 완료: {OUTPUT_JSON}")