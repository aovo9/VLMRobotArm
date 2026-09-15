import cv2
import json
import os
import subprocess
import numpy as np
from ultralytics import YOLO
from pathlib import Path

# 현재 실행 중인 object_recognition_test.py 파일이 있는 폴더
BASE_DIR = Path(__file__).resolve().parent

# 프로젝트 내부 폴더
JPG_DIR = BASE_DIR / "jpg"
JSON_DIR = BASE_DIR / "Json"

# 폴더가 없으면 자동 생성
JPG_DIR.mkdir(parents=True, exist_ok=True)
JSON_DIR.mkdir(parents=True, exist_ok=True)

# 이미지 저장 경로
CAMERA_SNAPSHOT = JPG_DIR / "camera_snapshot.jpg"
ORIGINAL_IMAGE_PATH = JPG_DIR / "camera_snapshot.jpg"
OVERLAY_IMAGE_PATH = JPG_DIR / "camera_overlay.jpg"

# JSON 저장 경로
DETECTED_JSON_PATH = JSON_DIR / "detected_objects.json"
VOICE_JSON_PATH = JSON_DIR / "voice_command.json"
VOICE_COMMEND_PATH = JSON_DIR / "voice_command.json"
VLM_INPUT_JSON_PATH = JSON_DIR / "vlm_input.json"

# 실행할 파이썬 파일 경로
WHISPER_FILE_PATH = BASE_DIR / "whisper_mic_test.py"
QWEN_VLM_FILE_PATH = BASE_DIR / "qwen_vlm_llamacpp_client.py"

class ObjectRecognizer:
    def __init__(self, camera_index=4, model_path="yolov8s.pt"):
        self.model = YOLO(model_path)

        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
        self.cap.set(cv2.CAP_PROP_FPS,30)


        if not self.cap.isOpened():
            raise RuntimeError("카메라를 열 수 없습니다.")

        # ROI 범위: 640x480 기준 중앙 영역
        # 필요하면 숫자 조정
        
        self.roi_points = [(601, 163), (1170, 249), (1274, 612), (323, 443)]
        

        # 인식하고 싶은 물체만 필터링
        # None이면 모든 클래스 표시
        self.target_classes = None

        # 예시: 컵, 병, 휴대폰만 보고 싶으면 아래처럼 사용
        # self.target_classes = ["cup", "bottle", "cell phone"]

        self.conf_threshold = 0.50

    def save_original_image(self, frame):
        success = cv2.imwrite(ORIGINAL_IMAGE_PATH, frame)

        if success:
            print(f"원본 이미지 저장 완료: {ORIGINAL_IMAGE_PATH}")
        else:
            print("원본 이미지 저장 실패")

        return success

    def save_camera_snapshot(self, frame):
        success = cv2.imwrite(CAMERA_SNAPSHOT, frame)

        if success:
            print(f"카메라 화면 저장 완료: {CAMERA_SNAPSHOT}")
            return True
        else:
            print("카메라 화면 저장 실패")
            return False

    def save_overlay_image(self, frame, detected_objects):
        overlay = frame.copy()

        # JSON과 같은 순서로 정렬
        sorted_objects = sorted(
            detected_objects,
            key=lambda obj: obj["center"][0]
        )

        for idx, obj in enumerate(sorted_objects, start=1):
            name = obj["name"]
            conf = obj["confidence"]
            bx1, by1, bx2, by2 = obj["box"]
            cx, cy = obj["center"]

            bx1 = int(bx1)
            by1 = int(by1)
            bx2 = int(bx2)
            by2 = int(by2)
            cx = int(cx)
            cy = int(cy)

            # bbox 사각형
            cv2.rectangle(
                overlay,
                (bx1, by1),
                (bx2, by2),
                (0, 255, 0),
                2
            )

            # 중심점
            cv2.circle(
                overlay,
                (cx, cy),
                6,
                (0, 0, 255),
                -1
            )

            # ID 크게 표시
            cv2.putText(
                overlay,
                f"ID {idx}",
                (bx1, max(30, by1 - 35)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                3
            )

            # 클래스명 + confidence 표시
            cv2.putText(
                overlay,
                f"{name} {conf:.2f}",
                (bx1, max(55, by1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # center 좌표 표시
            cv2.putText(
                overlay,
                f"center=({cx},{cy})",
                (cx + 10, cy),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 255),
                2
            )

        success = cv2.imwrite(OVERLAY_IMAGE_PATH, overlay)

        if success:
            print(f"overlay 이미지 저장 완료: {OVERLAY_IMAGE_PATH}")
        else:
            print("overlay 이미지 저장 실패")

        return success

    def save_detected_objects_to_json(self, detected_objects):
        # center_pixel의 x 좌표 기준으로 왼쪽 → 오른쪽 정렬
        detected_objects = sorted(
            detected_objects,
            key=lambda obj: obj["center"][0]
        )

        json_data = []

        for idx, obj in enumerate(detected_objects, start=1):
            name = obj["name"]
            conf = obj["confidence"]
            bx1, by1, bx2, by2 = obj["box"]
            cx, cy = obj["center"]

            item = {
                "id": idx,
                "class": name,
                "confidence": round(conf, 4),
                "bbox": [int(bx1), int(by1), int(bx2), int(by2)],
                "center_pixel": [int(cx), int(cy)]
            }

            json_data.append(item)

        with open(DETECTED_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        print(f"\nJSON 저장 완료: {DETECTED_JSON_PATH}")
        print(json.dumps(json_data, ensure_ascii=False, indent=4))

        return json_data

    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            # --------------------------------------------------
            # 1. 4점 ROI 준비
            # --------------------------------------------------
            # self.roi_points 형식:
            # [
            #   (x1, y1),  # 꼭지점 1
            #   (x2, y2),  # 꼭지점 2
            #   (x3, y3),  # 꼭지점 3
            #   (x4, y4)   # 꼭지점 4
            # ]
            pts = np.array(self.roi_points, dtype=np.int32)

            # 4점 ROI를 감싸는 최소 사각형 구하기
            # YOLO에는 사각형 crop 이미지를 넣어야 하므로 boundingRect를 사용
            x, y, w, h = cv2.boundingRect(pts)

            # 전체 화면 기준 crop 좌표
            crop_x1 = x
            crop_y1 = y
            crop_x2 = x + w
            crop_y2 = y + h

            # bounding rectangle 영역만 crop
            crop_frame = frame[crop_y1:crop_y2, crop_x1:crop_x2]

            # --------------------------------------------------
            # 2. 4점 ROI 마스크 만들기
            # --------------------------------------------------
            # 전체 프레임 크기의 검은 마스크 생성
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)

            # 4점 ROI 내부만 흰색으로 채움
            cv2.fillPoly(mask, [pts], 255)

            # crop 영역에 해당하는 마스크만 잘라냄
            crop_mask = mask[crop_y1:crop_y2, crop_x1:crop_x2]

            # crop 이미지에서 4점 ROI 바깥은 검은색으로 제거
            roi_frame = cv2.bitwise_and(crop_frame, crop_frame, mask=crop_mask)

            # --------------------------------------------------
            # 3. YOLO 실행
            # --------------------------------------------------
            results = self.model(roi_frame, verbose=False)

            detected_objects = []

            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    name = self.model.names[cls_id]

                    if conf < self.conf_threshold:
                        continue

                    if self.target_classes is not None and name not in self.target_classes:
                        continue

                    bx1, by1, bx2, by2 = box.xyxy[0].tolist()

                    # --------------------------------------------------
                    # 4. crop 좌표를 전체 frame 좌표로 변환
                    # --------------------------------------------------
                    bx1 = int(bx1 + crop_x1)
                    by1 = int(by1 + crop_y1)
                    bx2 = int(bx2 + crop_x1)
                    by2 = int(by2 + crop_y1)

                    cx = int((bx1 + bx2) / 2)
                    cy = int((by1 + by2) / 2)

                    # --------------------------------------------------
                    # 5. 검출 중심점이 4점 ROI 내부인지 재확인
                    # --------------------------------------------------
                    # YOLO는 crop 전체를 보고 판단하므로,
                    # 검출된 물체 중심이 실제 4점 ROI 안에 있는지 검사
                    inside = cv2.pointPolygonTest(pts, (cx, cy), False)

                    if inside < 0:
                        continue

                    detected_objects.append({
                        "name": name,
                        "confidence": conf,
                        "box": (bx1, by1, bx2, by2),
                        "center": (cx, cy)
                    })

            # --------------------------------------------------
            # 6. 4점 ROI 화면에 표시
            # --------------------------------------------------
            overlay = frame.copy()

            # ROI 내부를 반투명 파란색으로 표시
            cv2.fillPoly(overlay, [pts], (255, 0, 0))
            frame = cv2.addWeighted(overlay, 0.20, frame, 0.80, 0)

            # ROI 외곽선 표시
            cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

            # 꼭지점 번호 표시
            for idx, point in enumerate(self.roi_points):
                px, py = point

                cv2.circle(frame, (px, py), 5, (0, 0, 255), -1)
                cv2.putText(
                    frame,
                    f"P{idx + 1}",
                    (px + 8, py - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

            cv2.putText(
                frame,
                "4-Point ROI",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            # --------------------------------------------------
            # 7. 인식 결과 표시
            # --------------------------------------------------
            for obj in detected_objects:
                name = obj["name"]
                conf = obj["confidence"]
                bx1, by1, bx2, by2 = obj["box"]
                cx, cy = obj["center"]

                cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

                label = f"{name} {conf:.2f} ({cx},{cy})"

                cv2.putText(
                    frame,
                    label,
                    (bx1, by1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            # --------------------------------------------------
            # 8. 터미널에도 가장 확률 높은 물체 출력
            # --------------------------------------------------
            # 터미널에 ROI 안의 모든 물체 출력
            # if detected_objects:
            #     print("\n[ROI 안에서 인식된 물체 목록]")

            #     for idx, obj in enumerate(detected_objects, start=1):
            #         name = obj["name"]
            #         conf = obj["confidence"]
            #         cx, cy = obj["center"]
            #         bx1, by1, bx2, by2 = obj["box"]

            #         print(
            #             f"{idx}. object={name}, "
            #             f"conf={conf:.2f}, "
            #             f"center=({cx}, {cy}), "
            #             f"box=({bx1}, {by1}, {bx2}, {by2})"
            #         )
            # else:
            #     print("ROI 안에서 인식된 물체 없음")

            cv2.imshow("Object Recognition Test", frame)

            key = cv2.waitKey(1) & 0xFF

            # s 키: 현재 ROI 안 물체 정보 저장
            if key == ord("s"):
                if detected_objects:
                    print("\n[현재 ROI 안에서 인식된 물체 목록]")

                    for idx, obj in enumerate(detected_objects, start=1):
                        name = obj["name"]
                        conf = obj["confidence"]
                        cx, cy = obj["center"]
                        bx1, by1, bx2, by2 = obj["box"]

                        print(
                            f"{idx}. object={name}, "
                            f"conf={conf:.2f}, "
                            f"center=({cx}, {cy}), "
                            f"box=({bx1}, {by1}, {bx2}, {by2})"
                        )

                    self.save_detected_objects_to_json(detected_objects)

                else:
                    print("\n현재 ROI 안에서 인식된 물체가 없습니다.")

            # v 키: Whisper 실행 후 VLM 입력 데이터 생성
            elif key == ord("v"):
                print("\n[V 키 입력] 현재 화면/객체 데이터 저장 및 VLM 입력 생성")

                # 1. 원본 카메라 이미지 저장
                self.save_original_image(frame)

                # 2. detected_objects.json 저장
                if detected_objects:
                    saved_json_data = self.save_detected_objects_to_json(detected_objects)

                    # 3. bbox ID overlay 이미지 저장
                    self.save_overlay_image(frame, detected_objects)

                else:
                    print("현재 ROI 안에서 인식된 물체가 없습니다.")
                    saved_json_data = []

                    with open(DETECTED_JSON_PATH, "w", encoding="utf-8") as f:
                        json.dump([], f, ensure_ascii=False, indent=4)

                    # 물체가 없어도 현재 화면은 overlay로 저장
                    cv2.imwrite(OVERLAY_IMAGE_PATH, frame)

                # 4. Whisper 실행
                whisper_ok = self.run_whisper_and_save_text()

                # 5. VLM 입력 생성
                if whisper_ok:
                    self.send_to_vlm()

                    # 5. Qwen2.5-VL 실행
                    self.run_qwen_vlm()
            
            elif key == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def run_whisper_and_save_text(self):
        whisper_file = WHISPER_FILE_PATH

        if not os.path.exists(whisper_file):
            print(f"Whisper 파일을 찾을 수 없습니다: {whisper_file}")
            return False

        print("\nWhisper 음성 인식을 실행합니다...")

        result = subprocess.run(
            ["python3", whisper_file],
            text=True
        )

        print(result.stdout)

        if result.returncode != 0:
            print("Whisper 실행 중 오류 발생:")
            print(result.stderr)
            return False

        if not os.path.exists(VOICE_COMMEND_PATH):
            print("voice_command.json 파일이 생성되지 않았습니다.")
            return False

        print("voice_command.json 생성 완료")
        return True


    def load_json_file(self, filename):
        if not os.path.exists(filename):
            print(f"{filename} 파일이 없습니다.")
            return None

        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)


    def send_to_vlm(self):
        objects_data = self.load_json_file(DETECTED_JSON_PATH)
        voice_data = self.load_json_file(VOICE_JSON_PATH)

        if objects_data is None:
            print("detected_objects.json 데이터가 없습니다.")
            return

        if voice_data is None:
            print("voice_command.json 데이터가 없습니다.")
            return

        vlm_input = {
            "voice_command": voice_data,
            "detected_objects": objects_data,
            "images": {
                "rgb_original": str(ORIGINAL_IMAGE_PATH),
                "bbox_overlay": str(OVERLAY_IMAGE_PATH)
            },
            "coordinate_system": {
                "bbox": "original_rgb_pixel_xyxy",
                "center_pixel": "original_rgb_pixel_xy",
                "origin": "top_left",
                "x_direction": "right",
                "y_direction": "down"
            }
        }


        with open(VLM_INPUT_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(vlm_input, f, ensure_ascii=False, indent=4)

        print("\nVLM에 넘길 통합 입력 데이터 생성 완료: vlm_input.json")
        print(json.dumps(vlm_input, ensure_ascii=False, indent=4))

        # 나중에 여기에 실제 VLM 호출 코드를 넣으면 됨
        # 예:
        # response = your_vlm_model(vlm_input)
        # print(response)

    def run_qwen_vlm(self):
        qwen_file = QWEN_VLM_FILE_PATH

        if not os.path.exists(qwen_file):
            print(f"Qwen VLM 파일을 찾을 수 없습니다: {qwen_file}")
            return False

        print("\nQwen2.5-VL 판단 실행 중...")

        result = subprocess.run(
            ["python3", qwen_file],
            text=True
        )

        if result.returncode != 0:
            print("Qwen2.5-VL 실행 중 오류 발생")
            return False

        print("Qwen2.5-VL 판단 완료")
        return True

if __name__ == "__main__":
    recognizer = ObjectRecognizer(camera_index=4, model_path="yolov8n.pt")
    recognizer.run()