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
[Deskbot_Ultra_EyeToHand_Design_Handoff_2026-08-18.txt](https://github.com/user-attachments/files/31716311/Deskbot_Ultra_EyeToHand_Design_Handoff_2026-08-18.txt)
[분석보고서.txt](https://github.com/user-attachments/files/31716312/default.txt)


 ## 7. 향후 변경점
 # YOLOv8 -> YOLOE
  (YOLOE 관련 내용)[https://docs.ultralytics.com/ko/models/yoloe]
  - **변경점**
    기존 Yolo는 정해진 클래스에 대해서만 물체 판별 가능.
    YOLOE는 제로샷 학습으로 사용자의 사전 학습 없이 의미공간 추론으로 모델이 알지 못하는 새로운 물체 추론이 가능함.
    (데스크 상황에서는 같은 물체여도 다른 생김새를 가지고 있을 수도 있음. YOLOE는 이를 같은 클래스로 판단해 묶을 수 있음)

 # GR-CONV v2 (도입 고려)
  (GR-CONV v2 관련 논문)[https://www.mdpi.com/1424-8220/22/16/6208]
  - **장점**
    OMX 물체 파지시, 특정 물체에 관해서는 파지 점에 맞는 부분을 파지할 필요가 있음.
    GR-CONV는 realsense로 받은 이미지에 관해 가장 원활하게 파지가능한 파지 점을 추론하고,
    얼마나 그리퍼를 닫아야하는지 물체의 길이에 따른 그리퍼 오픈 범위를 추론함.
    또한, 물체를 가장 원할하게 파지할 수 있는 2D grasp 방향 값을 정의함.

 - **왜 도입 고려인가?**
   OMX는 기본적으로 5DOF이므로 그리퍼 모터는 오직 열고 닫는 기능만 가지고 있음.
   OMX는 Arm 4DOF로 자세 제어 범위가 제한되어 GR-ConvNet이 예측한 모든 grasp angle을 실행할 수 없음.
   하지만, 물체 접근 자체는 top-down, side-grasp으로 왠만하면 가능하고, 그리퍼 토크 조절은 YOLOE로 받은 mask를 토대로 조절할 수 있으므로 고려함.

 # Calibration 
 - **변경점**
   기존 클릭으로 진행한 calibration W 행렬 생성 부분을 Aruco 마커를 사용해 자동으로 진행하도록함.
   또한, Aruco 마커로 Z좌표 추정이 가능하므로, Z좌표에 대한 물체 파지 가능 여부도 시험해볼 것

 # VLM
 - **기존 모델 변경**
  Qwen 2.5 VL 3B -> Qwen 3 VL 4B

 # TTS
 - **FSM을 추가하면서 TTS도 같이 구현할 것인지?**
 - 
  
