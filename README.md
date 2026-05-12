# Open-Manipulator-VLM

## 하드웨어
- Jetson orin
- Open Manipulator-X
- Realsense d435
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

- **코드 실행 :**
  수정된 Pick_and_place.py 실행

  - 마이크가 없어 텍스트 입력 기반으로 임시 테스트 진행

  - ☑ Realsense를 통한 색상 기반 객체 탐지
  - ☑ 텍스트 입력으로 LLM이 색상과 동작 추출 후 OMX 제어
  - ☐ OMX가 Pick & Place를 정확하게 수행하는가?
    - Realsense 거치대 및 단색 객체 준비 후 재실험 예정
    - 현재는 카메라 흔들림으로 Calibration 좌표 오차 발생 추정

  - ☐ 음성을 텍스트로 정확히 변환하는가?

## 3. VLM 구현 파이프라인

<img width="2814" height="1536" alt="Gemini_Generated_Image_9oq63i9oq63i9oq6" src="https://github.com/user-attachments/assets/06b35a76-6272-412e-ba3a-11393f920ab4" />


