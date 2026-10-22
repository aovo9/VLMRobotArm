[cyclo 매뉴얼](https://github.com/user-attachments/files/33797761/Cyclo_Intelligence_Imitation_Learning_Manual.1.pdf)

# Open-Manipulator-VLA

## 프로젝트 소개
본 프로젝트는 Robotics사의 OpenManipulator-X AI와 Cyclointelligence를 활용하여 로봇의 시연 데이터 수집, 모방학습, 자율 동작까지 연결하는 시스템을 구축하는 것을 목표로 한다.
이후 내용은 기존의 VLM deskbot 시스템과 동일하다.

로봇 제어는 Jetson AGX Orin에서 수행하고, 데이터 처리와 AI 모델 학습은 RTX 4090 PC에서 진행하는 분산 환경으로 구성한다.

최종적으로는 사용자의 한국어 명령에 따라 다양한 색상의 레고 블록을 지정된 컵으로 옮기는 Pick & Place 작업을 수행하도록 구현할 예정이다

## Hardware
- **Robot** : ROBOTIS OpenManipulator-X AI
  - OMX-AI Follower
  - OMX-AI Leader
- **Robot Controller** : NVIDIA Jetson AGX orin 64GB
- **AI Training PC** : NVIDIA GeForce RTX 4090
- **Camera** : Realsense d435i

## Software
|구분              |사용 기술                        |
|----------------|-----------------------------|
|개발 환경           |VS Code, Python, Git         |
|Jetson OS       |Ubuntu 22.04                 |
|Robot Middleware|ROS 2 Humble / Jazzy         |
|Robot Control   |ROBOTIS OpenMANIPULATOR      |
|통신              |ROS 2, Zenoh                 |
|개발·실행 환경        |Docker, WSL2                 |
|데이터 수집          |Cyclo Intelligence           |
|데이터 저장          |ROS 2 MCAP                   |
|데이터 처리          |LeRobot Dataset v2.1 / v3.0  |
|AI Framework    |PyTorch, Hugging Face LeRobot|
|모방학습            |SmolVLA                      |
|GPU             |NVIDIA CUDA                  |

## 참고 프로젝트
- [Robotics OpenManipulator-X](https://github.com/ROBOTIS-GIT/open_manipulator)
- [Cyclo Intelligence](https://github.com/ROBOTIS-GIT/cyclo_intelligence)
- [Hugging face lerobot](https://github.com/huggingface/lerobot)

## 프로젝트 진행상황
목표: Jetson 환경에서 Leader–Follower 로봇의 정상 동작 및 외부 제어 환경 구성

☑ Jetson AGX Orin 개발 환경 구성
☑ ROS 2 기반 OpenMANIPULATOR 실행 환경 구축
☑ Leader / Follower 장치 연결
☑ Leader 조작에 따른 Follower 동작 확인
☑ 실제 Pick & Place 수동 시연
☑ RealSense D435i RGB 영상 수신
☑ 관절 상태 및 제어 명령 토픽 확인


  




