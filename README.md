[VLM_음성인식_Deskbot_(2).zip](https://github.com/user-attachments/files/28954631/VLM_._Deskbot_.2.zip)
# Open-Manipulator-VLM

## 하드웨어
- Jetson orin
- Open Manipulator-X
- Realsense d435i
- 키보드, 마우스, 모니터, 마이크

## 소프트웨어
- VS Code
- Python
- **로봇제어 :** ROS2 humble / Ubuntu 22.04
- **음성인식 :** whisper
- **이미지 :** YOLO V11
- **손 인식:** mediapipe or YOLO Pose

## 유사 프로젝트
[Open-Manipulator-LLM](https://github.com/Demolus13/Open-Manipulator-LLM)

이 프로그램 참고하여 손 인식 등의 추가 옵션 성공하면
VLM을 활용해 음성과 이미지 인식을 통합

## 과정

- 환경 설정
- 하드웨어 및 각 노드 동작 확인 (omx, whisper 등)
- 학습 데이터 수집 및 학습(잡을 물건, 손 등)
- OMX 움직임 미세 조정
  - 크게 움직일 땐 빠르게(move_group)
  - 물건 놓을 땐 미세하게(servo)
- 메인 노드 만들어 각 단계 통합
  - 소규모 파라미터 llm 이용
- 실패-재시도 매커니즘 구성
- 완성 시 입력-분석 단계를 vlm으로 통합

# 프로젝트 진행 상황

## 1. 유사 프로젝트 동작 정리
- [각 파일별 기능 설명](https://www.notion.so/LLM-OMX-Project-6c2483626a744a5f862b65cb9a10cb19?p=35b7883f6ca8807f8b74f070a14859a5&pm=s)
- **환경 :** ROS1 Noetic
- **색상 기반 탐지 :** OpenCV를 활용해 HSV 범위를 기준으로 특정 색상을 지닌 객체 검출
- **좌표 계산(Calibration) :**
  화면 상의 물체 위치를 로봇이 이해 가능한 3차원 공간 좌표로 변환
- **음성 인식 :** speech_recognition 라이브러리를 사용해 사용자의 목소리를 텍스트로 변환
- **LLM :**
  입력받은 텍스트에서 사용자가 원하는 색상과 동작을 추출
  - Groq API 사용
- **로봇 팔 제어 :**
  OMX End-Effector가 목표 좌표에 도달하도록
  역기구학(Inverse Kinematics) 적용

## 2. 유사 프로젝트 진행

- **환경 구축 :**
  Jetson Orin 환경에서 ROS2 Humble 환경 설정

- **코드 마이그레이션 :**
  기존 ROS1 Noetic 기반 프로젝트를 ROS2 구조로 변경

  - **클라이언트 라이브러리 교체 :** rospy → rclpy
  - **빌드 환경 변경 :** catkin → colcon
  - **통신 방식 변경 :** Service → Topic
     - (ros2_control이 topic [publisher-subscriber] 방식을 사용함)

- **코드 실행 :**
  수정된 Pick_and_place.py 실행

  - 마이크가 없어 텍스트 입력 기반으로 임시 테스트 진행

  - ☑ Realsense를 통한 색상 기반 객체 탐지
  - ☑ 텍스트 입력으로 LLM이 색상과 동작 추출 후 OMX 제어
  - ☑ OMX가 Pick & Place를 정확하게 수행하는가?
  - ☑ 음성을 텍스트로 정확히 변환하는가?

## 3. 음성기반 VLM 데스크 로봇 시스템 파이프라인

<img width="1536" height="1024" alt="ChatGPT Image 2026년 5월 30일 오전 03_10_53" src="https://github.com/user-attachments/assets/e5b1dbb1-8915-4686-bd74-0cc4dde8e2e1" />



## 4. 프로젝트 역할
  - **1.ROS2 제어**
      - [구현 목표 및 단계별 서술](https://www.notion.so/LLM-OMX-Project-6c2483626a744a5f862b65cb9a10cb19?p=3697883f6ca880d09e28d8913dbbe224&pm=s)
  - **2.Vision Sensor 제어**
      - [구현 목표 및 단계별 서술](https://www.notion.so/LLM-OMX-Project-6c2483626a744a5f862b65cb9a10cb19?p=3697883f6ca88023a1f6cb946a59b5b0&pm=s)
  - **3.VLM/음성인식**
      - [구현 목표 및 단계별 서술](https://www.notion.so/LLM-OMX-Project-6c2483626a744a5f862b65cb9a10cb19?p=36c7883f6ca880a7aa09e69ab5f09f7e&pm=s)
  - **4.YOLO**
      - [구현 목표 및 단계별 서술](https://www.notion.so/LLM-OMX-Project-6c2483626a744a5f862b65cb9a10cb19?p=36c7883f6ca880d9b2b3e4b0b26c8a23&pm=s)
   
  ## 5. 기타
  https://gemini.google.com/share/11095d97b8e4

[VLM 음성인식 Deskbot.pptx](https://github.com/user-attachments/files/28959043/VLM.Deskbot.pptx)

  ## 6. 현재 프로젝트 상황 및 분석 내용
  # Deskbot / VLM 기반 OpenManipulator-X 독립 정밀 검증 보고서

## Executive Summary

표기:

- [확인] 파일 또는 로그에서 직접 확인
- [추론] 여러 근거를 결합한 판단
- [확인 불가] 현재 자료만으로 증명 불가

핵심 결론

1. [확인] 사람 손이 실제 motion 대상이 된 기록이 있다.
   최신 산출물은 손 집어줘 → YOLO person → VLM target_id=1 → (0.187,-0.024,0.035) → /pick_and_place 호출 순서다. Overlay의 bbox/center도 사람 손 위에 있다. 제어 로그에는 해당 person 요청이 home부터 최종 home까지 모든 action 단계를 통과한 기록이 있다.
   근거: /home/jetson/.ros/log/python3_7053_1787029912448.log:21
         /home/jetson/.ros/log/python3_6463_1787029762035.log:129

2. [확인] success=true는 물리적 grasp 성공 증거가 아니다.
   그리퍼 result field, load/current, stalled, reached_goal, 후속 vision을 검사하지 않는다. 동일 세션에 Dynamixel 통신 오류도 기록됐다.

3. [확인] mic 실행 순서는 음성→카메라가 아니다.
   최초 depth 확보 → YOLO RGB 촬영 → 5초 녹음/STT → VLM → 기존 depth로 좌표 계산 순서다. 실행 직전 재검출도 없다.

4. [확인] RGB와 depth는 시간 동기화되지 않는다.
   timestamp·frame ID를 보존하거나 비교하지 않고, blocking subprocess 동안 ROS callback이 돌지 않는다. 최신 실행에서는 사용 가능한 depth가 RGB보다 최소 약 5.75초 오래됐고, 좌표 계산 시점에는 약 9.18초 오래됐을 수 있다.

5. [확인] MoveIt2는 현재 전체 trajectory planner가 아니다.
   /compute_ik로 최종 joint solution만 구한 뒤 1-point FollowJointTrajectory를 controller에 직접 보낸다. 중간 path에 대한 MoveIt collision 검사는 없다.

6. [확인] 현재 calibration은 pixel_uv → base_xy 2D affine + fixed Z이다.
   camera XYZ 변환은 계산하지만 최종 XY에는 쓰지 않는다. 저장 평균 오차 7.208 mm는 독립 검증이 아닌 12개 training sample residual이다.

7. [판단] 현재 상태는 정적 파이프라인 시연 기능은 갖췄지만, 실제 로봇 재시험 전 안전 보완이 필수다.
   특히 사람 class 차단, fresh perception, action cancellation, waypoint 검증, hardware 통신/초기 joint 점검이 선행되어야 한다.

## 현재 실제 프로젝트 구조

| 위치 | 현재 역할 | 사용 상태 |
|---|---|---|
| /home/jetson/Desktop/start_deskbot_system.sh | RealSense, hardware, MoveGroup, llama-server, control service 기동 | 현재 표준 system wrapper |
| /home/jetson/Desktop/deskbot_run_mic.sh | Desktop v4를 STT mode로 실행 | 현재 |
| /home/jetson/Desktop/deskbot_run_text.sh | Desktop v4를 text mode로 실행 | 현재 |
| /home/jetson/Desktop/deskbot_file_pipeline_node_v4.py | one-shot E2E orchestration | 현재 핵심 진입점 |
| /home/jetson/Desktop/deskbot_params.yaml | Vision/STT/VLM/좌표/service 설정 | 현재 wrapper가 로드 |
| /home/jetson/Desktop/YOLO | YOLO, Whisper, VLM client, 모델, JSON/JPEG/WAV | 현재 |
| /home/jetson/colcon_ws/src/omx_control | /pick_and_place, IK, arm/gripper action | 현재 |
| /home/jetson/colcon_ws/src/omx_interfaces | ROS2 service interface | 현재 |
| /home/jetson/colcon_ws/src/omx_vision | calibration 수집·모델·touch-to-pick | 모델 JSON만 active pipeline에서 직접 사용 |
| open_manipulator/* | URDF, bringup, MoveIt, ros2_control config | 현재 |
| /home/jetson/colcon_ws/install | ros2 run이 import하는 overlay | 현재 |
| /home/jetson/.ros/log | 실제 과거 실행 근거 | 분석 대상 |
| /home/jetson/colcon_ws/src/deskbot_pipeline | Desktop v4보다 오래된 package pipeline | 현 wrapper 미사용 |
| omx_vision/omx_vision/bbox_to_position_node.py | placeholder | 미구현 |
| Desktop/Folder, open_manipulator_llm, vla_deskbot | Ollama/LLM/direct trajectory 실험 | 현 wrapper 미사용 |

현재 구현 상태:

- 구현: one-shot text/mic 명령, RGB detection, VLM target ID 선택, fixed-Z 좌표, top-down pick sequence.
- 부분 구현: depth validity gate, class별 grasp-mode 정책, timeout, safety validation.
- 설계만 존재하거나 미구현: side_grasp, 명시적 FSM, safe recovery, grasp verification, TTS, full MoveIt path planning.
- 중복: PickAndPlace.srv가 omx_control/srv에도 있지만 서버는 omx_interfaces.srv를 import한다.
- 과거 설치 산출물: deskbot_pipeline build/install에 source에서 사라진 큰 deskbot_pipeline_node.py가 남아 있으나 console entry point가 없어 표준 실행 경로는 아니다.

## 현재 실제 실행 경로

/home/jetson/Desktop/start_deskbot_system.sh는 pipeline 자체를 실행하지 않는다. 사용자가 별도 mic/text wrapper를 실행해야 한다.

start_deskbot_system.sh
├─ realsense2_camera (align_depth.enable=true)
├─ open_manipulator_x hardware.launch.py
│  └─ ros2_control_node
│     ├─ joint_state_broadcaster
│     ├─ arm_controller
│     └─ gripper_controller
├─ move_group
│  └─ /compute_ik
├─ llama-server
│  └─ Qwen2.5-VL-3B GGUF
└─ ros2 run omx_control manipulator_control_node
   └─ /pick_and_place

별도 사용자 실행:

deskbot_run_mic.sh 또는 deskbot_run_text.sh
→ /usr/bin/python3 deskbot_file_pipeline_node_v4.py
→ YOLO/STT/VLM subprocess
→ /pick_and_place
→ /compute_ik
→ /arm_controller/follow_joint_trajectory
→ /gripper_controller/gripper_cmd
→ ros2_control
→ DynamixelHardware
→ OpenManipulator-X

현재 파일 판단 근거:

- mic/text wrapper 모두 Desktop v4 경로를 명시한다.
- deskbot_pipeline/setup.py에는 유효한 console script가 없다.
- start_deskbot_system.sh는 /home/jetson/colcon_ws/install을 source하므로 ros2 run omx_control ...은 설치본을 import한다.
- omx_control 핵심 Python source/build/install hash는 현재 동일하다.

## End-to-End 데이터 흐름

실제 mic mode에서는 음성보다 카메라 촬영이 먼저다.

| 데이터 | 생성 위치·형식 | 다음 소비자 |
|---|---|---|
| 최초 depth | /camera/camera/aligned_depth_to_color/image_raw, sensor_msgs/Image | pipeline callback |
| CameraInfo | /camera/camera/color/camera_info | pixel_to_camera_xyz() |
| RGB | /camera/camera/color/image_raw | YOLO subprocess |
| snapshot | jpg/camera_snapshot.jpg | 산출물 |
| bbox | [x1,y1,x2,y2] | YOLO JSON/VLM |
| confidence/class | float/string | VLM 및 service class |
| center | round((x1+x2)/2), round((y1+y2)/2) | depth lookup/calibration |
| object ID | center-x 정렬 후 매 snapshot 1부터 부여 | VLM 선택 |
| detection JSON | object list | VLM client, pipeline |
| overlay | ID·bbox·center가 그려진 JPEG | VLM image input |
| waveform | 16 kHz mono S16_LE, 고정 5초 WAV | faster-whisper |
| STT JSON | {timestamp,language,text} | VLM |
| text JSON | {language,text} | VLM |
| VLM prompt | command 정보 + object JSON + base64 overlay | llama.cpp /completion |
| raw VLM | {action,target_id,reason} | client 후처리 |
| validated plan | {target_id,action,grasp_mode,destination,reason} | pipeline |
| depth | center 주변 median | validity/camera XYZ |
| camera XYZ | pinhole projection | 로그 및 3×4 모델용 |
| base XYZ | 현재 pixel affine XY + fixed Z | service request |
| service request | x,y,z,class_name,grasp_mode,destination | omx_control |
| IK request | GetPositionIK, group arm, link end_effector_link | MoveGroup |
| selected joints | joint1~4 | arm action |
| trajectory | JointTrajectoryPoint 1개 | JTC |
| gripper command | position/effort | gripper controller |
| execution result | service bool/message | JSON |

run_once()의 정확한 순서:

1. depth와 CameraInfo가 한 번 들어올 때까지 spin_once()
2. YOLO subprocess
3. STT subprocess 또는 text JSON 생성
4. VLM subprocess
5. VLM JSON validation
6. target_id로 YOLO object 재조회
7. 기존 depth로 좌표 계산
8. execution_request.json 저장
9. enable_motion=false면 종료
10. true면 /pick_and_place
11. execution_result.json 저장

## VLM

### 실제 runtime과 모델

현재 launcher는 Ollama가 아니라 llama.cpp를 실행한다.

- 모델: Qwen2.5-VL-3B-Instruct-Q4_K_M.gguf
- projector: mmproj-F16.gguf
- endpoint: http://127.0.0.1:8080/completion
- port 8080, -ngl 99, context 8192
- 모델과 projector 파일은 실제 존재한다.
- [확인 불가] 최신 과거 산출물을 만들던 순간에도 정확히 이 server/model이 떠 있었는지는 artifact에 모델 ID가 없어 증명할 수 없다.

### 입력

qwen_vlm_llamacpp_client.py는 다음을 사용한다.

- voice_command.json
- detected_objects.json
- camera_overlay.jpg의 base64 image
- command normalization 결과
- temperature 0, top_p=0.1, 최대 64 token

Prompt가 요구하는 핵심 출력:

{"action":"pick","target_id":1,"reason":"matched target_hint"}

### 실제 robot control에 쓰이는 필드

- VLM 직접 영향: target_id, action
- YAML/default에서 채워짐: grasp_mode=top_down, destination=trash_zone
- YOLO에서 다시 조회됨: class, bbox, center
- VLM의 reason: 로그용
- VLM은 현재 prompt에서 x/y/z, joint, pose, trajectory를 생성하지 않는다.

### Validator 구조

Pipeline validator는:

- top-level x, y, z, joint*, trajectory, pose, waypoints, velocity, speed를 blacklist로 거부한다.
- action, grasp mode, destination을 제한된 집합으로 검사한다.
- target_id가 YOLO ID에 존재하는지 검사한다.
- 정규화 후 허용된 키만 새 dict로 출력한다.

따라서 nested JSON 안의 금지 키는 input 검사 자체는 통과할 수 있지만 정규화 결과에서 폐기된다. 현재 downstream에서 nested 좌표/joint가 로봇으로 가는 경로는 없다.

그러나 semantic safety는 부족하다.

- command의 target_hint와 선택 class가 일치하는지 재검사하지 않는다.
- class allowlist가 없다.
- 유효한 ID이면 person도 수용한다.
- action 누락 시 pick 동작으로 기본화될 수 있다.
- Python bool이 int 하위 타입이어서 target_id=true가 ID 1로 변환될 여지가 있다.

### Fallback

HTTP·parse 오류를 모두 catch하고 deterministic fallback을 수행한다. 알려진 target hint가 있으면 해당 class의 왼쪽 첫 object를 선택한다. client는 fallback이어도 exit 0이므로 pipeline은 정상 VLM과 VLM server 실패 후 fallback을 구분하지 못한다. enable_motion=true면 fallback도 실제 service 호출로 이어질 수 있다.

## YOLO / Vision

### 모델과 source

- Ultralytics 환경: 8.4.62
- effective model: yolov8n.pt
- checkpoint 유형: DetectionModel / Detect
- dataset class: COCO 80개
- segmentation이 아닌 bbox detection
- effective RGB topic: /camera/camera/color/image_raw
- YAML의 camera_index=4는 ROS script에서 명시적으로 무시된다.

현재 YAML은 confidence 0.4와 다음 ROI를 전달한다.

149,65;464,60;511,383;144,399

### 후보 class

yolo_ros_snapshot_once.py는 --target-classes 기능을 갖고 있지만, pipeline command가 이 인자를 전달하지 않는다.

따라서:

- person 포함 COCO 80개 전체가 후보
- picking class allowlist 없음
- mouse, cell phone, person, traffic light가 모두 다음 단계로 전달 가능
- 과거 직접-camera object_recognition_test.py의 제한 class 정책은 현 경로에 적용되지 않음

### ROI, bbox, center, ID

1. polygon bounding rectangle로 crop
2. polygon 바깥을 mask
3. bbox를 원본 좌표로 복원하고 이미지 경계 clamp
4. bbox 중심을 반올림해 center_pixel 생성
5. center가 polygon 내부인지 검사
6. center X로 정렬하고 ID 1부터 재부여

영향:

- bbox 일부가 ROI 밖이어도 center가 ROI 안이면 남는다.
- ID tracking이 없어서 frame마다 안정적이지 않다.
- 같은 class 여러 개는 transient ID로만 구분한다.
- fallback은 동일 class 중 왼쪽 첫 object를 고른다.
- 실제 grasp point는 bbox 중심이며 keypoint, segmentation mask, surface selection은 없다.

## RGB-D

### 정합성 결과

| 질문 | 답 |
|---|---|
| YOLO RGB와 depth가 동일 capture인가 | NO |
| timestamp가 비교되는가 | NO |
| RGB/depth 해상도를 runtime에서 비교하는가 | NO |
| message_filters 또는 동등한 sync가 있는가 | NO |
| stale depth가 사용될 수 있는가 | YES |
| CameraInfo와 image 해상도를 검사하는가 | NO |
| aligned depth인가 | 공간 정렬 설정은 YES, 시간 동기화는 NO |
| frame ID 일치 검사인가 | NO |
| center가 depth 밖이면 | 현재 require_valid_depth=true에서 좌표 계산 중단 |

근거:

- depth callback은 image 배열과 encoding만 저장하고 header stamp/frame ID를 버린다.
- RGB callback은 stamp를 읽지만 반환 JSON에 보존하지 않고 frame ID도 저장하지 않는다.
- pipeline main()은 executor를 계속 spin하지 않고 run_once()를 직접 호출한다.
- YOLO/STT/VLM은 blocking subprocess.run()이다.
- 좌표 계산 시 두 번째 depth wait는 기존 값이 non-None이므로 즉시 반환한다.
- RealSense는 align_depth.enable=true이지만 enable_sync를 지정하지 않아 설치 launcher 기본 false다.

### 최신 로그에서 확인된 시간 관계

최신 run:

- pipeline이 YOLO를 시작: ROS time 1787029914.599
  /home/jetson/.ros/log/python3_7053_1787029912448.log:4
- RGB capture: 1787029920.347
  /home/jetson/.ros/log/python3_7086_1787029919354.log:2
- 좌표 계산: 1787029923.777
  /home/jetson/.ros/log/python3_7053_1787029912448.log:104

마지막 depth callback은 YOLO subprocess 시작 전이어야 한다. 따라서 사용 가능한 depth는 RGB보다 최소 약 5.75초, 좌표 계산보다 최소 약 9.18초 오래됐다.

### mic mode의 구체적 위험 시나리오

t0: depth D0 수신
t1: RGB R1 촬영
t2: YOLO 완료
t3~t8: 5초 음성 녹음
t9: Whisper model load/inference
t10: VLM
t11: R1 center + D0로 좌표 계산
t12: 로봇 실행

움직이는 손이나 물체는 R1 이후 이미 이동했을 수 있다. 현재 fixed-XY/fixed-Z 모델에서는 stale depth가 최종 XYZ 숫자를 직접 바꾸지는 않지만, 오래된 책상/배경 depth가 validity gate를 잘못 통과시킬 수 있다. 반면 stale RGB center는 최종 X/Y를 직접 바꾸므로 더 즉각적인 위험이다.

최신 저장 RGB와 aligned depth 로그는 모두 640×480이었지만, 이는 한 실행의 관찰값일 뿐 코드상 보장은 아니다. Native RealSense depth profile은 848×480, color는 640×480으로 기록됐으며 aligned 출력이 color 크기로 변환된 것이다.

## Calibration

### 모델 유형과 수식

/home/jetson/colcon_ws/src/omx_vision/ee_camera_to_base_model.json:

- model_type: pixel_uv_to_base_xy_affine_fixed_z
- input: pixel_uv
- output: base_xy
- W shape: 2×3
- z_policy: fixed Z
- model JSON fixed_z: 0.030 m

따라서 camera XYZ→base XYZ 모델이 아니라 pixel UV→base XY affine이다.

현재 W의 수식:

base_x =
  0.00007704863835*u
- 0.00085983813266*v
+ 0.278381166939

base_y =
- 0.00083496626350*u
- 0.00009959644785*v
+ 0.300937128648

Runtime Z는 model JSON 값이 아니라 YAML의 fixed_z=0.035와 z_offset=0을 사용한다.

### sample과 오차 독립 재계산

모델 내부 training sample 12개와 W로 다시 계산한 결과:

| 지표 | 결과 |
|---|---:|
| sample 수 | 12 |
| base X 분포 | 0.14, 0.16, 0.18, 0.22 m |
| base Y 분포 | -0.08, 0, +0.08 m |
| pixel U 범위 | 240–444 |
| pixel V 범위 | 104–202 |
| mean Euclidean error | 7.207707 mm |
| Euclidean RMSE | 8.342024 mm |
| max error | 15.389592 mm |
| X RMSE | 7.547651 mm |
| Y RMSE | 3.552792 mm |

최악 sample:

pixel: (353,155)
true:  (0.160000, 0.000000)
pred:  (0.172304,-0.009243)
error: (+12.304,-9.243) mm
distance: 15.390 mm

저장된 error와 재계산값은 부동소수 오차 범위에서 일치한다.

Collector는 같은 sample로 fitting한 직후 같은 sample에서 error를 계산한다. 따라서 약 7.2 mm는:

- training residual: YES
- 독립 validation: NO
- cross-validation: NO

### 별도 sample 파일과의 불일치

/home/jetson/colcon_ws/src/omx_vision/ee_calibration_samples.json은:

- model보다 약 25.6초 늦은 mtime
- fixed Z 0.040 m
- sample 단 1개
- (u,v)=(242,230) → (x,y)=(0.14,-0.08)

현재 model 예측은 약 (0.099264,+0.075968)이며 오차는 약 161.2 mm다.

- [확인] model과 외부 sample 파일이 같은 calibration 상태를 나타내지 않는다.
- [확인 불가] 카메라 이동, 오클릭, 좌표 convention 변경, 미완료 재수집 중 어떤 원인인지는 알 수 없다.

### 방식의 한계

- affine 모델이므로 perspective/depth 변화 및 camera pose 변화에 취약
- calibration sample 영역 밖 extrapolation 검사 없음
- current ROI는 U 약 144–511, V 약 60–399로 training 범위보다 훨씬 넓음
- accepted workspace도 training base 영역보다 넓음
- camera serial, pose, image resolution, intrinsics, frame ID, 수집 시각 metadata 없음
- model fixed Z와 runtime fixed Z가 다름
- held-out 정확도 없음

Runtime은 W shape 2×3과 model_type의 pixel 문자열을 보고 [u,v,1]을 적용하므로 현재 model format과는 호환된다. 다만 input, output, z_policy를 엄격히 검증하지 않고 model 내부 fixed_z도 사용하지 않는다.

## STT

/home/jetson/Desktop/YOLO/whisper_mic_test.py와 YAML script 이름은 현재 정확히 일치한다.

| 항목 | 현재 값 |
|---|---|
| library | faster-whisper 1.2.1 |
| model | tiny |
| device | CUDA |
| compute type | float16 |
| language | ko |
| beam size | 5 |
| 녹음 | 고정 5초 |
| ALSA | plughw:2,0 |
| format | S16_LE, mono, 16 kHz |
| VAD | 명시 안 됨, 설치 버전 기본 false |
| outer timeout | 120초 |

실행 구조:

1. arecord로 5초 녹음
2. 그 뒤 WhisperModel("tiny", device="cuda", compute_type="float16") 생성
3. inference
4. {timestamp, language, text} JSON 저장

Pipeline은 매 명령마다 새 Python subprocess를 시작한다. 따라서 model도 요청마다 새로 생성되며 persistent STT process가 아니다. 최소 지연은 5초 + GPU model load + inference다.

일반적인 nonzero exit면 pipeline이 중단되므로 즉시 과거 JSON을 쓰지는 않는다. 하지만 기존 JSON 삭제·mtime·run ID 검사가 없어 대체 script가 exit 0이지만 새 JSON을 쓰지 않는 경우 stale JSON을 수용할 수 있다. run_stt=false이면서 빈 text를 줄 때는 기존 JSON을 의도적으로 재사용한다.

최신 voice_command.json에는 STT writer가 항상 쓰는 timestamp가 없고 WAV mtime도 2026-06-19이다. 따라서 최신 손 집어줘는 text mode 또는 수동 생성일 가능성이 높다. 현재 파일만으로 STT 오인식 사례는 확인 불가다.

## Coordinate computation

compute_coordinate()의 단계:

1. YOLO center_pixel=(u,v) 사용
2. depth median lookup
3. CameraInfo K로 camera XYZ 계산
4. calibration model 적용
5. Z 선택
6. target workspace 검사

### Depth 읽기

- 반경: 5, 10, 15, 20
- 실제 window: 11×11, 21×21, 31×31, 41×41
- 첫 번째로 positive value가 하나라도 존재하는 window의 median
- 32FC1: m
- 그 외 encoding: 모두 mm로 가정 후 /1000
- 최소 valid sample 수 없음
- 최대/최소 depth range 없음
- bbox 내부 clamp 없음
- segmentation mask 없음
- 별도의 cluster/outlier rejection 없음

작거나 얇은 물체에서는 책상/배경 depth가 median에 포함될 수 있다. 실제 오차 크기는 하드웨어 실험 없이 단정할 수 없다.

### Camera XYZ

camera_x = (u-cx)*depth/fx
camera_y = (v-cy)*depth/fy
camera_z = depth

### 최종 robot/base XYZ

현재 2×3 pixel model에서는:

base_xy = W @ [u,v,1]
base_z  = YAML fixed_z + z_offset

따라서:

- camera_xyz는 로그에는 남지만 최종 XY에 미사용
- use_depth_z=false
- 현재 model에서는 use_depth_z=true로 바꿔도 2×3 branch의 measured_z가 없어서 fixed Z를 사용
- require_valid_depth=true이므로 depth는 validity gate 역할
- require_valid_depth=false에서 invalid depth를 0으로 바꿔도 곧바로 pixel_to_camera_xyz()가 depth<=0 예외를 내므로 해당 옵션은 실질적으로 깨져 있다
- TF lookup은 없다
- calibration의 base_xy를 service의 x/y로 그대로 전달한다

## OMX control

### /pick_and_place 정의

/home/jetson/colcon_ws/src/omx_interfaces/srv/PickAndPlace.srv:

float64 x
float64 y
float64 z
string class_name
string grasp_mode
string destination
---
bool success
string message

Server:

- ManipulatorControlNode
- service /pick_and_place
- ReentrantCallbackGroup
- MultiThreadedExecutor(num_threads=4)
- boolean is_busy

### 실제 top-down sequence

| 순서 | 목표 | 값/offset | nominal duration |
|---:|---|---|---:|
| 1 | home | named joint target | 2.0 s |
| 2 | open | 0.017, effort 0.3 | action |
| 3 | ready | named joint target | 2.0 s |
| 4 | pre-grasp | (x,y,z+0.08) | 1.5 s |
| 5 | descend | (x,y,z) | 1.5 s |
| 6 | close | 0.0, effort 0.3 | action |
| 7 | lift | (x,y,z+0.10) | 1.5 s |
| 8 | destination | named joint target | 2.0 s |
| 9 | release | 0.017 | action |
| 10 | home | named joint target | 2.0 s |

각 단계 실패 시 즉시 response failure로 종료한다. retract, release, home recovery는 없다.

### 기타 grasp mode

- side_grasp: schema와 validator에서는 허용하지만 항상 not implemented로 실패
- calibration: 외부 service caller가 사용할 수 있는 특수 mode. 일반 grasp-mode validator 전에 분기하며 ready → requested xyz만 수행하고 home 복귀하지 않는다. Dummy cup/top_down/drop_zone으로 workspace validation은 재사용한다.
- 현재 pipeline validator는 calibration을 허용하지 않아 통상 pipeline에서는 접근할 수 없지만 직접 service 호출은 가능하다.

## MoveIt2 / IK

### MoveIt2의 실제 역할

moveit_interface.py에서 확인되는 client:

- /compute_ik
- /arm_controller/follow_joint_trajectory

확인되지 않는 호출:

- MoveGroup planning action
- MotionPlan
- GetCartesianPath
- ExecuteTrajectory
- OMPL planning request

따라서 MoveGroup이 OMPL capability를 로드하더라도 active Deskbot 경로는 이를 사용하지 않는다.

FollowJointTrajectory.Goal에는 정확히 1개의 JointTrajectoryPoint만 들어간다. Controller가 current/last-command에서 목표 joint까지 spline 보간하며, 그 중간 경로를 MoveIt planning scene에 대조하지 않는다.

### avoid_collisions=True의 범위

IK request는 최종 IK candidate가 현재 planning scene에서 collision-free인지 검사하도록 요청한다. 보호하지 못하는 것:

- seed/current joint에서 solution까지의 전체 경로
- controller spline 중간 상태
- planning scene에 없는 책상·주변 장비
- collision geometry가 없는 end_effector_link

정적 구성과 최신 MoveGroup 로그에서는:

- Deskbot이 table collision object를 추가하는 코드 없음
- octomap 3D sensor plugin 없음
- camera와 world TF tree disconnected 경고 반복
- end_effector_link collision geometry 없음
- self-collision URDF/SRDF는 존재
- [확인 불가] 외부 사용자가 수동으로 planning scene object를 넣었는지 여부

### top-down orientation

코드 quaternion:

x=0.001, y=0.757, z=0.001, w=0.647

그러나 kinematics.yaml은 position_only_ik: True이고 최신 MoveGroup 로그도 Using position only ik를 기록한다. 따라서 quaternion은 현재 IK orientation constraint로 적용되지 않는다.

현재 top-down 자세는 orientation 제약이 아니라 seed와 joint heuristic에 의존한다.

### Seed

joint1_seed = clamp(atan2(y,x), -1.2, 1.2)

close: x < 0.14        → 4 seeds
mid:   0.14 ≤ x < 0.24 → 4 seeds
far:   x ≥ 0.24        → 6 seeds

- close joint2: 약 -0.90~-0.45
- mid joint2: 약 -0.35~+0.15
- far joint2: 약 +0.20~+0.70
- Z와 현재 joint state는 seed 선택에 사용되지 않는다.

### Scoring

score =
  4*abs(joint2-preferred_joint2)
+ 4*abs(joint4-preferred_joint4)
+ conditional penalties

| 거리 | preferred joint2 | preferred joint4 |
|---|---:|---:|
| close | -0.65 | 1.15 |
| mid | 0.00 | 1.20 |
| far | 0.50 | 1.35 |

Penalty/reject:

- joint3 > 0.9 penalty
- joint4 < 0.9 penalty
- joint4 > 1.7 큰 penalty
- joint4 > 1.75 hard reject
- joint3 > 1.20 hard reject
- far에서 joint2 < 0.05 또는 joint4 < 0.9 reject
- close에서 joint2 < -1.30 reject

현재 joint와의 이동 거리, path length, joint1 변화는 score에 반영되지 않는다.

### Joint limit 비교

| Joint | 자체 code limit | URDF limit | 판정 |
|---|---:|---:|---|
| joint1 | [-3.14,3.14] | [-π,π] | 거의 동일 |
| joint2 | [-2.0,2.0] | [-1.5,1.5] | code가 0.5 rad씩 넓음 |
| joint3 | [-2.0,2.0] | [-1.5,1.4] | code가 넓음 |
| joint4 | [-2.0,2.0] | [-1.7,1.97] | code가 넓음 |

근거:

- /home/jetson/colcon_ws/src/omx_control/omx_control/moveit_interface.py:58
- /home/jetson/colcon_ws/src/open_manipulator/open_manipulator_x_description/urdf/open_manipulator_x.urdf.xacro:36

Named targets는 정적으로 URDF 범위 안이다. 다만 home의 joint4는 1.952758, upper 1.97까지 약 0.0172 rad뿐이다. Named target은 자체 joint-limit 검사, IK, collision 검사를 거치지 않고 직접 전송된다.

Deskbot home [0.2255,-1.4189,0.0828,1.9528]은 SRDF home [0,-1,0.7,0.3]과 다르며 SRDF named state를 사용하지 않는다.

## Gripper

/home/jetson/colcon_ws/src/omx_control/omx_control/gripper_interface.py:

- action: /gripper_controller/gripper_cmd
- open: position 0.017, effort 0.3
- close: position 0.0, effort 0.3
- server wait: 5초
- goal response: 5초
- result: 8초

URDF 범위는 [-0.010,0.019], SRDF close는 -0.01이다. 현재 close 0.0은 SRDF 완전 닫힘보다 10 mm 열려 있다. 이것이 물체 보호를 위한 의도인지 단순 설정 차이인지는 확인 불가다.

result future가 완료되면 다음을 검사하지 않고 성공을 반환한다.

- action status
- reached_goal
- stalled
- final position
- effort/load

클래스별 gripper position/effort policy도 없다.

action future 완료
≠ 목표 position 도달
≠ 물체를 잡음
≠ lift 후 물체가 유지됨

## Safety

| 계층 | 현재 처리 | 판단 |
|---|---|---|
| Perception class | COCO 전체, target allowlist 미전달 | fail-open |
| ROI | center가 polygon 내부인지 검사 | 부분적 |
| VLM robot field | 좌표/joint top-level blacklist, 정규화 출력 제한 | 직접 좌표 제어는 차단 |
| VLM semantic grounding | ID 존재만 확인, command↔class 미검사 | 취약 |
| Pipeline workspace | target XYZ 검사 | 존재 |
| Control workspace | target XYZ 검사, xmax가 더 좁음 | 존재 |
| Class policy | 알려진 class일 때만 mode 제한 | fail-open |
| Derived waypoint | pre/lift 재검사 없음 | 없음 |
| Named pose | joint limit/collision 검사 없음 | 없음 |
| IK endpoint | avoid_collisions=True | endpoint만 |
| Full trajectory | collision 검사 없음 | 없음 |
| Controller result | future 완료 중심 | 제한적 |
| Gripper grasp | 센서/vision 확인 없음 | 없음 |
| Timeout cancellation | 없음 | 없음 |
| Recovery | 없음 | 없음 |

### Class 정책

safety.py는 class가 ALLOWED_GRASP_MODES에 들어 있을 때만 mode를 제한한다. Dictionary 밖 class를 거부하지 않는다.

현재 control validator 결과:

| class | top_down 요청 |
|---|---|
| person | 통과 |
| mouse | 통과 |
| cell phone | 통과 |
| traffic light | 통과 |
| 임의 unknown string | 통과 |
| 빈 string | 통과 가능 |
| 알려진 cup, bottle 등 | 등록된 mode만 검사 |

따라서 deny-by-default가 아니다. YOLO와 control 양쪽에 중복된 class 안전 검사가 있는 것도 아니다.

### Workspace와 파생 좌표

Pipeline workspace:

x 0.05~0.30
y -0.18~0.18
z 0.02~0.20

Control workspace:

x 0.05~0.28
y -0.18~0.18
z 0.02~0.20

검사 대상은 request target뿐이다. 예를 들어 target z=0.20은 유효하지만:

- pre-grasp: z=0.28
- lift: z=0.30

이 되어 선언 workspace를 벗어나도 실행 전 거부되지 않는다.

### Pipeline 외부 호출

Control server에는 enable_motion parameter가 없다. 따라서 node가 실행 중이면 외부 caller가 /pick_and_place를 직접 호출해 다음을 우회할 수 있다.

- pipeline enable_motion
- VLM validator
- YOLO target ID 존재 검사
- command/class grounding

남는 방어는 control의 target workspace, mode, destination, 약한 class-mode 검사뿐이다.

### 기존 위험 class 실행

최신 control 로그:

- traffic light 하나는 pre-grasp IK 후보의 joint4가 높아 실패
  /home/jetson/.ros/log/python3_6463_1787029762035.log:2
- 다른 traffic light 요청은 전체 sequence 완료
  /home/jetson/.ros/log/python3_6463_1787029762035.log:34
- person 요청은 home→open→ready→pre-grasp→descend→close→lift→trash→open→home 완료
  /home/jetson/.ros/log/python3_6463_1787029762035.log:129

이는 사람/물체 접촉이나 grasp 성공 증거는 아니지만, 위험 class가 control validator와 controller action까지 통과한 직접 증거다.

## FSM / Recovery

활성 경로에는 명시적 FSM class나 state enum이 없다.

- Pipeline: 한 번 실행되는 procedural run_once()
- Control: local steps list의 for-loop
- 저장 state: boolean is_busy
- persistent state: 없음
- restart recovery: 없음
- 실패 단계: response/log 문자열에만 존재
- grasp success state: 없음

단계별 실패 후 가능한 잔류 상태:

| 실패 위치 | 가능한 실제 상태 |
|---|---|
| pre-grasp | ready 또는 이동 중간 |
| descend | 책상/물체 근처 낮은 자세 |
| close | 낮은 자세에서 부분적으로 닫힌 gripper |
| lift | 물체를 쥐었을 가능성이 있는 낮은 자세 |
| destination | 물체를 쥔 채 이동 중간 |
| release | destination에서 물체를 계속 쥔 상태 |
| final home | destination 부근에 잔류 |

어느 경우에도 자동 safe retract, release, home retry가 없다.

vla_deskbot/blind_motion_node.py에는 간이 state 문자열이 있지만 현재 wrapper와 무관한 별도 실험 executable이며, 현 Deskbot FSM의 근거가 아니다.

## Timeout / concurrency

| 대상 | Timeout | Cancel 처리 |
|---|---:|---|
| YOLO subprocess | 60초 | process timeout 종료에 의존 |
| STT subprocess | 120초 | 내부 녹음/model 단계 cancel 없음 |
| VLM subprocess | 240초 | HTTP client 자체 180초 |
| service availability | 5초 | 해당 없음 |
| service result | 120초 | server request 취소 없음 |
| IK service availability | 5초 | 없음 |
| 각 IK request 내부 | 1초 | 없음 |
| IK future wait | seed당 3초 | 없음 |
| arm server | 10초 | 없음 |
| arm goal response | 10초 | 없음 |
| arm result | duration+10초 | cancel_goal_async() 없음 |
| gripper server | 5초 | 없음 |
| gripper goal response | 5초 | 없음 |
| gripper result | 8초 | 없음 |

가능한 실제 시나리오:

controller가 action goal을 accept
→ client result wait timeout
→ control step은 실패 반환
→ finally에서 is_busy=false
→ 실제 controller는 이전 goal을 계속 실행
→ 새 service request가 수락될 수 있음

Goal-response timeout도 caller가 goal handle을 받기 전에 controller가 늦게 accept할 수 있어 동일 위험이 있다.

Concurrency도 취약하다.

- Reentrant callback
- 4-thread executor
- if self.is_busy와 self.is_busy=True가 lock 없는 별도 연산
- arm/gripper interface 객체 공유

따라서 두 service callback이 check와 set 사이에 진입하면 동시에 실행될 가능성이 있다. 정적 코드상 race 가능성이며 실제 동시 요청 테스트는 수행하지 않았다.

## Configuration consistency

| 개념 | 파일 A | 값 | 파일 B | 값 | 실제 runtime 우선값 | 불일치 |
|---|---|---|---|---|---|---|
| enable_motion | Python default | false | Desktop YAML | true | wrapper CLI: dry=false, live=true | YES |
| mic 기본 motion | mic wrapper | dry | YAML | true | 무인자 false | 명확히 override |
| text 기본 motion | text wrapper | dry | YAML | true | 무인자 false | 명확히 override |
| fixed_z | model JSON | 0.030 | YAML | 0.035 | YAML 0.035 | YES |
| fixed_z | Python default | 0.070 | collector default | 0.070 | YAML 사용 시 0.035 | YES |
| 외부 calibration sample Z | samples JSON | 0.040 | model samples | 0.030 | model fit은 0.030, runtime 0.035 | YES |
| touch-to-pick Z | touch config/code | 0.040 | active pipeline | 0.035 | 실행 경로별 다름 | YES |
| z_offset | pipeline YAML | 0 | touch-to-pick | 약 -0.102 | 실행 경로별 다름 | YES |
| workspace xmax | pipeline | 0.30 | control | 0.28 | service에서 0.28 | YES |
| grasp mode | schema/control | top/side | 구현 | top만 | top만 실제 성공 가능 | YES |
| destination | pipeline default | trash | touch path | drop | 실행 경로별 | YES |
| pre/lift | control | +0.08/+0.10 | pipeline safety | 정의 없음 | control 값 | 단일 정의 |
| joint2 limit | code | ±2.0 | URDF | ±1.5 | IK solver/URDF가 실질 기준 | YES |
| joint3 limit | code | ±2.0 | URDF | -1.5~1.4 | URDF | YES |
| joint4 limit | code | ±2.0 | URDF | -1.7~1.97 | URDF | YES |
| XYZ duration | 코드 주석 | 4초 권장 | 실제 call | 1.5초 | 1.5초 | YES |
| MoveGroup time | move_group default | sim time true | hardware | false | 표준 wrapper에서 불일치 | YES |
| Dynamixel timeout | xacro | error_timeout_sec=0.2 | plugin | error_timeout_ms, default 500 | 500 ms | YES |
| depth sync | start wrapper | align=true | RealSense default | enable_sync=false | 공간 align만 | 조건부 |
| RGB topic | YOLO default | color raw | pipeline | override 없음 | color raw | NO |
| depth topic | YAML | aligned depth | RealSense wrapper | align=true | aligned depth | NO |
| camera_index | YAML | 4 | ROS YOLO | ignored | ROS topic | 이름상 혼란 |
| YOLO model | YAML | yolov8n.pt | 과거 script | yolov8s.pt | yolov8n.pt | 과거 코드와 다름 |
| confidence | YAML | 0.4 | Python/Downloads | 0.25 | wrapper에서 0.4 | YES |
| target classes | YOLO 지원 | CLI 가능 | pipeline | 미전달 | COCO 전체 | 위험 |
| STT script | YAML | whisper_mic_test.py | 실제 파일 | 동일 | 동일 | NO |
| calibration model | YAML | source JSON 절대경로 | install | 모델 복사 없음 | source JSON 직접 읽음 | 의도적 |
| service | YAML/control | /pick_and_place | client | 동일 | 동일 | NO |

enable_motion 최종값:

- deskbot_run_mic.sh 무인자/dry: false
- deskbot_run_mic.sh live|true|motion: true
- deskbot_run_text.sh 무인자/dry: false
- deskbot_run_text.sh ... live|true|motion: true
- Desktop YAML만 사용한 Python 직접 실행: true
- YAML 없이 Python default: false
- start_deskbot_system.sh만 실행: pipeline 자체가 실행되지 않음

따라서 기본 motion이 항상 활성화라는 주장은 반박되지만, YAML 직접 실행 경로는 true라 안전한 단일 기본값도 아니다.

## Runtime artifacts/logs

최신 산출물 mtime:

14:12:01.256 camera_snapshot.jpg
14:12:01.260 camera_overlay.jpg
14:12:01.264 detected_objects.json
14:12:02.940 voice_command.json
14:12:03.732 qwen_raw_response.txt
14:12:03.736 vlm_result.json
14:12:03.772 vlm_result_validated.json
14:12:03.776 execution_request.json
14:12:17.260 execution_result.json

동일 실행일 가능성이 매우 높다.

최신 내용:

- command: 손 집어줘
- YOLO: person, confidence 0.4866
- bbox: [292,62,453,218]
- center: (372,140)
- VLM: action=pick,target_id=1
- validated: top_down, trash_zone
- coordinate: (0.186666,-0.023614,0.035)
- logged depth: 0.491 m
- service result: success=true, pick_and_place done

근거:

- /home/jetson/Desktop/YOLO/Json/detected_objects.json
- /home/jetson/Desktop/YOLO/Json/execution_request.json
- /home/jetson/Desktop/YOLO/Json/execution_result.json

Overlay 직접 확인 결과 bbox와 center는 사람 손 위에 있다.

직전 기록:

- 병 집어줘인데 traffic light 선택 → pre-grasp IK 실패
- 손 집어줘인데 traffic light 선택 → 전체 sequence 완료
- object 없음 → invalid target/fallback 후 execution 전 중단
- 최신 person → 전체 sequence 완료

Hardware 로그에는 같은 시스템 세션 중:

- Communication error 5회
- Dynamixel read failure 11회
- write failure 11회
- controller Goal reached 로그 16회

가 함께 존재한다. 이는 action success가 항상 물리적 정상 동작을 의미하지 않는다는 근거지만, 개별 통신 오류가 최신 person action의 특정 순간과 정확히 대응한다는 점은 확인하지 못했다.

최신 startup joint state에는 joint2=-2.03406이 기록되어 URDF와 자체 code limit 밖이다. 과거 로그에도 비슷한 joint2 및 joint4 초과값이 반복된다. 실제 기구 자세, zero offset, wrapping, calibration 중 원인은 확인 불가다.

2026-08-18 약 14:52 KST 읽기 전용 process 조회에서는 Deskbot, RealSense, llama-server, YOLO, Whisper, control 관련 프로세스가 보이지 않았다. 따라서 최신 산출물은 약 40분 전 실행 기록이며 감사 시점에는 시스템이 기동 중이지 않았던 것으로 판단한다.

## Source/install drift

| 범위 | 결과 |
|---|---|
| omx_control 핵심 Python source/build/install | 현재 SHA-256 동일 |
| omx_vision 핵심 Python source/install | 동일 |
| omx_interfaces/PickAndPlace.srv source/install | 동일/symlink |
| OpenManipulator launch/config install | 주로 source symlink |
| Desktop v4 | 직접 Python 경로 실행, install과 무관 |
| calibration JSON | YAML이 source 절대경로를 읽음 |
| deskbot_pipeline | source/build/install 내부에 구형·orphan copy 존재 |
| /home/jetson/install, 중첩 build/install | 표준 wrapper가 source하지 않음 |

현재 즉각적인 핵심 source/install drift는 확인되지 않았다.

다만:

- omx_control install Python은 일반 복사본이므로 향후 source 변경 후 rebuild하지 않으면 오래된 install이 실행된다.
- 표준 shell은 install overlay를 source하므로 ros2 run은 source Python이 아니라 install module을 import한다.
- Desktop pipeline과 scripts는 절대경로로 직접 실행한다.
- deskbot_pipeline build/install에 source에서 사라진 구현이 남아 있어 수동 import 시 혼동 가능하다.

## Tests

현재 존재하는 테스트는 대부분 ament 생성 lint boilerplate다.

- test_flake8.py
- test_pep257.py
- skip된 test_copyright.py
- omx_interfaces에는 실질 동작 테스트 없음

확인되지 않는 테스트:

- VLM validator와 nested/unknown field
- command↔class semantic grounding
- person 거부
- coordinate transform
- RGB-D timestamp/resolution
- calibration refit/held-out error
- workspace와 derived waypoint
- joint limit
- IK seed/filter/scoring
- gripper result 판정
- timeout cancellation
- concurrent service
- failure recovery
- full E2E mock integration

이번 작업에서는 pytest/colcon 실행이 cache·build·test 산출물을 만들 수 있어 실행하지 않았다. 따라서 기존 lint/test의 현재 pass 여부는 확인 불가다.

## 문서와 실제 구현 차이

| 문서/주석의 주장 | 실제 구현 | 판단 | 영향 |
|---|---|---|---|
| VLM이 grasp mode/destination도 선택 | Prompt는 action/target ID/reason만 요청; mode/destination은 default | 불일치 | VLM 역할 오해 |
| pixel+depth→camera→EE model | 현재 XY는 pixel affine, Z fixed | 불일치 | depth 기반 3D라고 오해 |
| TF 기반 coordinate | active pipeline에는 TF lookup 없음 | 반박됨 | frame 의미 불명확 |
| MoveIt2 사용 | /compute_ik만 쓰고 action에 1 point 직접 전송 | 부분 확인 | full planning/collision 보호를 과대평가 |
| FSM/Validator/TTS pipeline | active v4는 procedural, TTS 없음 | 불일치 | 완성도 과대평가 |
| side_grasp 지원 | schema만 허용, 실행은 항상 미구현 실패 | 불일치 | API가 거짓 capability 노출 |
| fixed Z | 0.030/0.035/0.040/0.070 분산 | 불일치 | 실행 경로별 높이 변화 |
| YOLO main | 과거 직접-camera object_recognition_test.py 설명 | 현재 ROS snapshot v4 | 구형 문서 |
| YOLO model | 과거 yolov8s | 현재 yolov8n | 성능 기대 혼동 |
| current pipeline | ROS package pipeline처럼 설명 | 실제 wrapper는 Desktop v4 절대경로 | 실행 진입점 혼동 |
| llama projector | 긴 이름의 mmproj 안내 | launcher는 mmproj-F16.gguf | 실행 실패 가능 |
| 첫 실행 dry-run | 코드 warning 존재 | YAML 직접 실행은 motion true | 안전 지침과 default 충돌 |
| calibration은 homography | active v4는 affine model JSON | 구형 설명 | 잘못된 model 이해 |
| end-effector collision 보호 | end_effector_link collision geometry 없음 | 부분 불일치 | collision 보호 공백 |

## 검증 질문 결과표

| 검증 대상 주장 | 판정 | 근거 |
|---|---|---|
| RGB와 depth가 시간 동기화되지 않는다 | 확인됨 | header 폐기, blocking subprocess, sync 없음 |
| stale depth를 사용할 수 있다 | 확인됨 | 최신 실행에서 최소 5.75초 차이 |
| RGB/depth 해상도 직접 비교가 없다 | 확인됨 | 비교 코드 없음 |
| 기본 motion이 활성화되어 있다 | 부분적으로 확인 | YAML 직접 실행 true, wrapper 무인자 false |
| person 같은 unknown class가 pick 대상이 될 수 있다 | 확인됨 | fail-open class 정책 |
| 기존 기록에 person 실행이 존재한다 | 확인됨 | control log lines 129–223 |
| MoveIt2는 full planning이 아니라 IK만 사용된다 | 확인됨 | /compute_ik + 직접 FJT |
| 실제 path 전체 collision check가 없다 | 확인됨 | 1-point goal, planning call 없음 |
| timeout 후 action cancel이 없다 | 확인됨 | cancel API 호출 없음 |
| derived waypoint workspace validation이 없다 | 확인됨 | target만 검사 |
| 자체 joint limit과 URDF가 다르다 | 확인됨 | joint2~4 code 범위가 넓음 |
| side_grasp는 허용하지만 미구현이다 | 확인됨 | server가 명시적으로 실패 |
| explicit FSM이 없다 | 확인됨 | procedural sequence + boolean |
| recovery가 없다 | 확인됨 | 실패 즉시 return |
| grasp success verification이 없다 | 확인됨 | gripper/vision/load 검사 없음 |
| fixed Z가 여러 파일에서 다르다 | 확인됨 | 0.030/0.035/0.040/0.070 |
| calibration은 pixel→base XY affine이다 | 확인됨 | model type, W 2×3 |
| calibration 평균 오차가 약 7 mm다 | 확인됨 | 7.2077 mm, 단 training residual |
| STT가 요청마다 Whisper model을 새로 로드한다 | 확인됨 | 매번 subprocess와 model 생성 |

## 위험요소 전체 목록

### Critical

| 제목 | 근거·정확한 원인 | 증상·재현 조건 | 수정 방향 | 규모 | 실제 로봇 없이 검증 |
|---|---|---|---|---|---|
| C1. 사람/unknown class fail-open | YOLO target filter 미전달, VLM ID만 검증, pipeline class 검사 없음, control safety가 알려진 class에만 조건 적용 | person, traffic light, 임의 class가 workspace 내이면 full sequence. 실제 person 기록 존재 | YOLO·pipeline·control 모두 deny-by-default allowlist, person hard reject, command/class 일치 검증 | Small–Medium | YES |
| C2. 실행 직전 fresh perception 없음 | run_once에서 YOLO가 STT보다 먼저이며 재검출 없음 | 5초 녹음/추론 중 손·물체 이동 시 과거 center로 접근 | STT 후 synchronized snapshot, max-age gate, execution 직전 재확인 | Medium | rosbag/mock으로 YES |
| C3. 전체 motion path collision 검사 없음 | 최종 IK 후 1-point FJT, 책상 scene 없음 | endpoint는 valid여도 중간 spline에서 self/table/person 충돌 가능 | table scene 포함 MoveIt plan/execute 또는 모든 interpolated state collision 검증 | Large | simulation으로 대부분 YES |
| C4. Timeout 후 accepted goal 지속 가능 | arm/gripper wait 함수와 cancel API 부재 | 상위 failure 후 기존 arm이 계속 움직이고 is_busy=false 뒤 새 goal 중첩 | goal handle 보관, cancel 요청·확인, controller hold, cancel 실패 시 motion lock | Medium | mock action server로 YES |

### High

| 제목 | 근거·정확한 원인 | 증상·재현 조건 | 수정 방향 | 규모 | 무로봇 검증 |
|---|---|---|---|---|---|
| H1. stale/unsynchronized RGB-D | callbacks에서 stamp/frame/resolution 비교와 executor spin 없음 | 오래된 depth가 gate를 통과하거나 미래 3D model에서 잘못된 XYZ | synchronized RGB/depth/CameraInfo bundle, age/frame/size 검사 | Medium | YES |
| H2. calibration model과 최신 sample 불일치 | 두 JSON, sample 직접 대입 시 161.2 mm | 현재 camera pose가 sample 상태와 같다면 대규모 좌표 오류 | camera 고정 후 full 재수집, provenance, held-out 검증, 기존 model 사용 중단 판단 | Medium | 파일 검증 YES, 재보정 NO |
| H3. top-down orientation 미강제 | kinematics.yaml의 position-only IK | 같은 XYZ에서 seed branch에 따라 손목 방향 변화 | orientation-aware IK로 전환하고 자세 tolerance test | Small–Medium | YES |
| H4. 실패 recovery 없음 | sequence 실패 시 즉시 return | 낮은 자세·닫힌 gripper·물체 보유 상태에 잔류 | 단계별 state, safe retract/release/home recovery | Medium | mock YES, 최종 hardware 필요 |
| H5. Gripper/grasp 성공 오판 | command()에서 result field 미검사 | stall/abort/빈 grasp도 sequence success | status·position·effort·stalled 검사, lift 후 vision/load 확인 | Medium | result logic YES, 물리 grasp NO |
| H6. 파생 waypoint 미검증 | target만 workspace 검사, pre +0.08, lift +0.10 | boundary target이 선언 workspace 밖으로 이동 | 모든 waypoint를 먼저 생성해 일괄 workspace/IK/collision 검사 | Small | YES |
| H7. Hardware timeout key 오류와 통신 실패 | xacro는 error_timeout_sec, plugin은 error_timeout_ms | 의도보다 느린 error 전파, action success와 physical state 불일치 | key/unit 수정, 통신 이상 시 controller abort/hold 검증 | Small–Medium | parsing YES, 장애 시험 NO |
| H8. Startup joint가 model limit 밖인 로그 | 최신·과거 hardware startup에서 joint2 약 -2.034 | 잘못된 zero/wrap 상태에서 torque/motion 시작 가능 | motion 전 feedback/URDF limit preflight, 원인 규명 전 실제 시험 금지 | Medium | 로그 검증 YES, 원인 확인 NO |
| H9. is_busy race | Reentrant+4 threads, lock 없는 check-then-set | 동시 service 요청이 둘 다 arm/gripper 사용 | mutex/MutuallyExclusive callback 또는 atomic reservation | Small | YES |
| H10. VLM failure fallback이 motion까지 진행 | 예외 후 fallback이 exit 0 | VLM 장애를 정상 선택으로 오인하고 첫 class를 pick | provenance 필드, fallback 시 motion abort/dry-run 기본 | Small | YES |
| H11. YAML 직접 실행의 motion 기본 true | deskbot_params.yaml enable_motion=true | wrapper를 우회한 문서상 직접 실행으로 바로 service 호출 | 모든 authoritative config false, 별도 명시적 arming token | Small | YES |

### Medium

| 제목 | 근거·원인 | 증상·재현 조건 | 수정 방향 | 규모 | 무로봇 검증 |
|---|---|---|---|---|---|
| M1. 자체 joint limit과 URDF 불일치 | code가 joint2~4에 더 넓은 범위 허용 | code safety가 invalid solution을 안전하다고 판단 | URDF/MoveIt limit 단일 source 사용 | Small | YES |
| M2. Named pose 검사 우회와 home margin | named target 직접 action, home joint4 upper까지 0.017 rad | calibration/feedback 오차 시 limit 근접 | named pose도 URDF limit·collision·current path 검사 | Medium | YES |
| M3. MoveGroup use_sim_time 불일치 | startup이 use_sim을 안 넘기고 MoveGroup default true | state/TF timestamp 처리 이상 가능 | real launcher에서 명시적 false | Small | YES |
| M4. fixed Z/config 분산 | 0.030/0.035/0.040/0.070 | 실행 경로마다 grasp 높이 변화 | authoritative Z 정책 하나와 metadata | Small | YES |
| M5. require_valid_depth=false가 실제로 깨짐 | invalid depth 0 처리 후 projection이 다시 예외 | 설정을 false로 바꿔도 실행 중단 | projection branch와 validity 정책 분리 | Small | YES |
| M6. bbox center/window depth 취약 | bbox 밖 큰 window, mask/valid-count 없음 | 작은 물체에서 책상 depth 사용 | bbox-clipped inner ROI, percentile/valid-count, mask | Small–Medium | synthetic test YES |
| M7. STT 매 요청 model load | 매 요청 Whisper model 생성 | 긴 latency와 stale visual target | persistent STT node/worker, VAD | Medium | YES |
| M8. 산출물 provenance 부족 | 동일 filename overwrite, run ID/model/stamp 없음 | 서로 다른 실행 JSON을 잘못 결합 | run directory와 manifest, atomic write, model/config hash | Medium | YES |
| M9. calibration 특수 mode가 종료 자세를 복구하지 않음 | ready→xyz 후 그대로 종료 | 수동 calibration 호출 뒤 임의 자세 잔류 | 별도 explicit calibration node/arming과 복귀 정책 | Small–Medium | mock YES |
| M10. 핵심 자동 테스트 부재 | lint boilerplate만 존재 | 안전 수정의 regression 탐지 불가 | validator/coordinate/action mock unit·integration test | Medium | YES |
| M11. source/install/실험 코드 분산 | Desktop, package, orphan install, direct-control nodes 공존 | 잘못된 executable 수동 실행 가능 | active/deprecated 경계와 실행 권한·문서 정리 | Medium | YES |

### Low

| 제목 | 근거·원인 | 증상 | 수정 방향 | 규모 | 무로봇 검증 |
|---|---|---|---|---|---|
| L1. 문서·주석의 구형 pipeline 설명 | 파일 설명서, v4 docstring, AGENTS와 실제 구현 차이 | 잘못된 운영 절차 | active call graph 기준 문서 갱신 | Small | YES |
| L2. 중복 PickAndPlace.srv | omx_control/srv와 omx_interfaces/srv | interface authority 혼동 | omx_interfaces만 authoritative로 정리 | Small | YES |
| L3. placeholder/dead code | bbox node, orphan pipeline, 과거 YOLO/LLM code | 유지보수 비용 | archive/deprecation 표시 | Small | YES |
| L4. target_id=true 허용 가능성 | Python bool→int 변환 | malformed VLM output이 ID 1 선택 | exact integer type 검사 | Small | YES |

## 완성도 평가

| 영역 | 점수 /10 | 근거 |
|---|---:|---|
| Architecture | 5 | 계층은 분리됐지만 Desktop/package/install 경로가 분산 |
| Perception | 5 | ROS RGB snapshot과 ROI는 동작, class safety/tracking/grasp point 부족 |
| RGB-D handling | 2 | 공간 alignment만 있고 시간·frame·resolution 보장 없음 |
| STT | 4 | 로컬 faster-whisper 동작 구조, persistent/VAD/freshness 없음 |
| VLM grounding | 2 | image+JSON 사용하지만 command/class 의미 검증 실패 |
| Validator | 3 | 직접 좌표/joint 경로는 차단, class/semantic은 fail-open |
| Calibration | 3 | 수학적 모델은 명확하나 sample 불일치·held-out 없음 |
| Coordinate estimation | 4 | pipeline은 완성됐지만 fixed 2D affine과 stale input |
| Manipulation | 5 | top-down sequence는 실제 controller 단계까지 실행 기록 있음 |
| IK | 4 | 다중 seed/filter/scoring은 존재, orientation/path/current-state 문제 |
| Motion safety | 2 | endpoint IK collision만 있고 full path/table/cancel 부족 |
| Gripper | 3 | action wrapper는 있으나 result/grasp 판정 없음 |
| FSM | 1 | explicit FSM 없음 |
| Recovery | 1 | 실패 즉시 종료 |
| Grasp verification | 1 | action 완료 외 확인 없음 |
| Testing | 1 | lint boilerplate 수준 |
| Logging/observability | 5 | 단계 로그와 JSON은 풍부하나 run provenance 부족 |
| TTS/UX | 2 | 입력 pipeline은 있으나 TTS/대화 응답 없음 |
| Maintainability | 3 | config 중복·구형 코드·source/install 경로 혼재 |
| Overall demo readiness | 3 | 제한된 감독 dry-run에는 가능, live 재시험은 안전 보완 필요 |

별도 평가:

- 정적 코드 완성도: 5/10
  주요 happy-path가 구현됐고 실제 controller 단계 로그도 존재한다.
- 실제 데모 준비도: 3/10
  사람 class 실행, stale perception, recovery/cancel 부재가 데모 실패와 안전 위험으로 직결된다.
- 무인 반복 운용 준비도: 1/10
  grasp verification, FSM, recovery, hardware health gate, persistent state가 없다.

## Phase A/B/C 수정 로드맵

### Phase A — 실제 로봇 재시험 전에 반드시

| 우선순위 | 작업 | 안전 영향 | 데모 성공률 | 난이도 | 기존 코드 파괴 위험 | 예상 파일 수 | Hardware 검증 |
|---:|---|---|---|---|---|---:|---|
| 1 | YOLO·pipeline·control에 deny-by-default class 정책, person hard reject, command/class 일치 | 매우 큼 | 큼 | 낮음 | 낮음 | 3–5 | 불필요 |
| 2 | 모든 enable_motion default false, 별도 명시적 arming 절차 | 매우 큼 | 중간 | 낮음 | 낮음 | 2–4 | 불필요 |
| 3 | STT 후 fresh synchronized RGB-D capture, timestamp/frame/size/max-age 검사 | 매우 큼 | 매우 큼 | 중간 | 중간 | 2–4 | rosbag 후 camera 확인 |
| 4 | arm/gripper cancel-confirm, timeout 중 motion lock, is_busy mutex | 매우 큼 | 큼 | 중간 | 중간 | 3–4 | mock 우선, hardware 최종 |
| 5 | target/pre/lift/named pose 전체 workspace·URDF limit 사전검사 | 큼 | 큼 | 낮음 | 낮음 | 2–3 | 불필요 |
| 6 | error_timeout_ms, use_sim_time, startup joint/communication health preflight 수정·점검 | 매우 큼 | 큼 | 중간 | 중간 | 3–6 | 필요 |
| 7 | 책상 collision object와 collision-checked trajectory 도입 | 매우 큼 | 큼 | 높음 | 중간~높음 | 4–8 | simulation 후 필요 |

### Phase B — 졸업작품 데모 안정화 전에

| 우선순위 | 작업 | 안전 영향 | 데모 성공률 | 난이도 | 파괴 위험 | 파일 수 | Hardware 검증 |
|---:|---|---|---|---|---|---:|---|
| 8 | camera 고정 후 calibration 재수집, model/sample 통일, held-out 검증, fixed Z 단일화 | 큼 | 매우 큼 | 중간 | 낮음 | 3–6 | 필요 |
| 9 | 최소 FSM과 단계별 recovery, gripper result 및 lift 후 grasp 확인 | 큼 | 매우 큼 | 중간 | 중간 | 4–7 | 필요 |

### Phase C — 시간이 남으면

| 우선순위 | 작업 | 안전 영향 | 데모 성공률 | 난이도 | 파괴 위험 | 파일 수 | Hardware 검증 |
|---:|---|---|---|---|---|---:|---|
| 10 | persistent STT/VAD, depth inner-ROI·segmentation, run manifest, TTS, side grasp, 구형 코드 정리 | 낮음~중간 | 중간~큼 | 중간~높음 | 중간 | 6–12 | 기능별 선택 |

## 현재 상태에서 가장 먼저 고칠 단 하나의 문제

Class safety를 deny-by-default로 바꾸고 person을 perception, pipeline validator, control server 세 계층에서 모두 명시적으로 거부해야 한다.

## 그 문제를 선택한 이유

- 이론적 가능성이 아니라 실제 사람 손이 person으로 선택되어 /pick_and_place와 전체 controller sequence까지 전달된 직접 증거가 있다.
- 사람 안전과 장비 안전에 동시에 영향을 준다.
- 수정 범위가 비교적 작다.
- 실제 로봇 없이 JSON·unit test·mock service로 완전히 회귀검증할 수 있다.
- pipeline을 우회한 직접 /pick_and_place 호출에도 control server 차단을 적용할 수 있다.
- 이후 RGB-D, calibration, planning 개선이 끝나기 전에도 즉시 위험 표면을 크게 줄인다.

## 확인하지 못한 것

- 최신 success=true 실행에서 실제 TCP가 요청 좌표에 도달했는지
- 사람 손 또는 다른 물체와 물리적으로 접촉했는지
- 그리퍼가 실제 물체를 잡거나 이동시켰는지
- 최신 artifact 당시 정확히 어떤 llama-server binary/model이 실행 중이었는지
- 최신 RGB/depth/CameraInfo의 정확한 header timestamp와 frame ID
- RealSense 내부 frameset의 실제 timestamp pairing 정책
- 현재 camera mount가 calibration model 생성 당시와 동일한지
- model/sample 불일치 원인이 camera 이동, 오클릭, convention 변경 중 무엇인지
- 현재 camera pose에서 held-out calibration 정확도
- 작은 물체·얇은 물체의 실제 depth 오차
- 최신 command가 text wrapper인지 수동 JSON 생성인지
- 현재 보존된 자료에서 실제 STT 오인식 사례
- STT의 현재 실제 latency와 ALSA device 가용성
- timeout 후 controller가 실제로 얼마나 오래 계속 움직이는지
- 동시 service race가 실제 executor에서 재현되는지
- 최신 통신 오류와 각 action의 정확한 시간적 대응
- startup joint 초과값의 물리적 원인
- 외부에서 planning scene에 table/collision object를 수동 등록했는지
- 실제 환경의 비상정지, 사람 접근 제한, torque-off 절차
- use_sim_time 불일치가 해당 실행의 IK/state timestamp에 끼친 정확한 영향
- 기존 lint/test의 현재 pass 여부
- 수동으로 구형 direct-control executable을 최근 사용했는지 여부
