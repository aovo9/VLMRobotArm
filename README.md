# Deskbot: VLM 기반 LEGO Pick & Place 시스템

## 0. 정리 페이지
[Deskbot-V1 프로젝트 진행](https://www.notion.so/LLM-OMX-Project-6c2483626a744a5f862b65cb9a10cb19?p=35b7883f6ca8807f8b74f070a14859a5&pm=s)

[Deskbot-V1 Deskbot PPT](https://github.com/user-attachments/files/28954631/VLM_._Deskbot_.2.zip)

[Deskbot-V2 프로젝트 진행](https://app.notion.com/p/3d4714226cef80d19c32fd2c04ed26b5)

## 1. 프로젝트 개요
Deskbot은 Vision-Language Model(VLM), 객체 인식, RGB-D 카메라, ROS2 및 OpenManipulator-X를 결합한 멀티모달 로봇 Pick & Place 시스템​이다.

사용자가 자연어로 작업을 지시하면 시스템이 명령의 의미와 카메라 영상을 분석하여 대상 LEGO를 선택하고, RealSense D435i를 통해 대상의 위치를 로봇 좌표계로 변환한 뒤 OpenManipulator-X가 해당 LEGO를 집어 지정된 색상의 그릇으로 이동시킨다.

현재는 작업 환경과 검증 범위를 명확하게 하기 위해 대상 물체를 빨강·초록·파랑색 LEGO로, 목적지는 빨강·초록·파랑 3개의 고정된 그릇으로 제한한다. 또한 텍스트 명령을 사용하여 전체 Pick & Place 파이프라인을 검증하고, 시스템 안정화 후 Whisper 기반 음성 입력을 다시 연결할 예정이다.

### 명령 예시
"빨간 레고를 빨간 그릇에 넣어줘"
"초록색 레고를 파란 그릇으로 옮겨줘"
"파란 레고를 초록 그릇에 넣어줘"

## 2. 프로젝트 목표
본 프로젝트의 핵심 목표는 단순한 색상 기반 로봇 제어가 아니라 다음 기술을 하나의 시스템으로 통합하는 것이다.
- 자연어 명령 해석
- VLM 기반 시각·언어 정보 통합
- LEGO 객체 탐지 및 대상 선택
- RealSense 기반 위치 정보 획득
- Camera Pixel → Robot Coordinate 변환
- ROS2 기반 로봇 제어
- OpenManipulator-X Pick & Place
- 로봇 동작의 안정성 추구 및 실패 처리

최종적으로 다음과 같은 흐름을 구현하는 것을 목표로 한다.

사용자 명령 → VLM 명령 해석 → 카메라 영상 + 객체 탐지 결과 분석 → Target LEGO 선택 → Target Bounding Box / Center Pixel → RealSense / Calibration → Robot Coordinate (X, Y, Z) → ROS2 Pick & Place 요청 → OpenManipulator-X → 지정된 색상 그릇에 LEGO 배치

## 3. 하드웨어
- NVIDIA Jetson Orin
- ROBOTIS OpenManipulator-X
- Intel RealSense D435i
- Keyboard, Mouse, Monitor, Microphone

### 작업 환경
- Target Object: Red LEGO, Green LEGO, Blue LEGO
- Destination: Red Bowl, Green Bowl, Blue Bowl

LEGO는 색상뿐만 아니라 형태에도 차이를 두어 객체 인식 및 대상 선택 성능을 검증한다.

그릇도 작업 공간 내의 고정된 위치에 배치하며, 각 위치의 Robot Coordinate를 사전에 등록하여 사용한다.

## 4. 소프트웨어 및 기술 스택
### 개발 환경
- Ubuntu 22.04
- ROS2 Humble-
- Python
- VS Code
- Jetson Orin

### Robot Control
- ROS2
- MoveIt
- OpenManipulator-X
- ROS2 Service
- Top-down Grasp
- Pick & Place State Sequence

### Vision
- Intel RealSense D435i
- OpenCV
- YOLO
- RGB / Depth Image
- Bounding Box
- ROI

### Coordinate Estimation
- Eye-to-Hand Calibration
- Homography
- Pixel → Robot Coordinate 변환
- Workspace Validation

### Vision-Language Model
- Qwen2.5-VL 기반 VLM 테스트(현재)
- Qwen3-VL 4B(향후 검토)

### Speech Recognition
- Whisper(향후 통합)

## 5. ROS2 구성
### omx_control
OpenManipulator-X의 실제 동작을 담당한다.

주요 구성:
<img width="1526" height="312" alt="image" src="https://github.com/user-attachments/assets/ea74ae67-bcc8-4ef9-b04a-a4e49aab7ab6" />

### manipulator_control_node.py
/pick_and_place 요청을 받아 실제 Pick & Place sequence를 실행한다.

입력 예:
<img width="1526" height="298" alt="image" src="https://github.com/user-attachments/assets/5c13b34a-9872-4a34-9dd0-afe982115041" />

### safety.py
로봇 동작 전에 다음 조건을 검사한다.
- Robot Workspace
- Object Class
- Grasp Mode
- Destination

### config.py
다음 설정을 관리한다.
- Robot Workspace
- Grasp Mode
- LEGO Class
- Bowl Destination
- Bowl Coordinate
- Pre-grasp Height
- Lift Height
- Pre-place Height
- omx_vision

### omx_vision
카메라 좌표와 로봇 좌표를 연결한다.

주요 구성:
<img width="1524" height="342" alt="image" src="https://github.com/user-attachments/assets/aa121451-5249-4955-aac5-53b0e2fbae58" />

### bbox_to_position_node.py
현재 LEGO Pick & Place 연결의 핵심 노드.

<img width="1886" height="736" alt="image" src="https://github.com/user-attachments/assets/1890ec2b-d72f-42e1-9d8a-172bbaaf6ac0" />

실제 로봇 동작 전에는 execute_motion=False를 사용하여 계산된 좌표만 검증할 수 있도록 구성한다.

## 6. VLM 출력 구조
VLM은 로봇을 직접 제어하지 않는다.

VLM의 역할은 사용자의 명령과 시각 정보를 바탕으로 어떤 LEGO를 어느 그릇으로 이동시킬지를 결정하는 것이다.
<img width="1880" height="330" alt="image" src="https://github.com/user-attachments/assets/3dfb85f8-0545-4a82-87b1-decc1909ec49" />

위 결과는 이후 로봇 제어 단계에서 다음과 같이 변환된다.
<img width="1886" height="622" alt="image" src="https://github.com/user-attachments/assets/b370c339-5f4d-4c36-b874-da0b869f4e61" />

## 7. Calibration

카메라 영상에서 검출한 LEGO를 실제 로봇이 집기 위해서는 Camera Coordinate와 Robot Coordinate 사이의 변환이 필요하다.

현재 프로젝트에서는 Eye-to-Hand 방식의 Calibration을 사용한다. Z 좌표는 현재 작업 환경과 물체 높이에 맞춘 값을 사용하여 검증하며, 향후 RealSense Depth 및 자동 Calibration 방식을 추가로 검토한다.

## 8. 안전 기능

실제 로봇 동작 중 잘못된 VLM 출력이나 좌표 계산으로 인한 오동작을 줄이기 위해 제어 단계에서 별도의 안전 검증을 수행한다.

현재 적용된 주요 안전 기능:
- Robot Workspace 제한
- 지원하지 않는 Object Class 거부
- 지원하지 않는 Grasp Mode 거부
- 잘못된 Destination 거부
- Bowl Coordinate 미설정 시 동작 거부
- 로봇 동작 중 중복 요청 방지
- 동일 VLM 결과 반복 실행 방지
- 실제 동작 전 Dry Run 지원

## 9. 현재 프로젝트 진행 상황
### 완료 또는 구현 중
- ☑ Jetson Orin + Ubuntu 22.04 환경 구축
- ☑ ROS2 Humble 환경 구축
- ☑ OpenManipulator-X 기본 제어
- ☑ MoveIt 기반 로봇 제어
- ☑ Gripper 제어
- ☑ RealSense D435i 연결
- ☑ ROI 기반 작업 영역 설정
- ☑ Eye-to-Hand Calibration 기반 코드 구성
- ☑ Pixel → Robot XY 변환
- ☑ /pick_and_place ROS2 Service 구성
- ☑ Top-down Pick & Place sequence
- ☑ LEGO 전용 Safety Validation
- ☑ Red / Green / Blue Bowl 목적지 구조
- ☑ VLM 결과 → Target ID 처리
- ☑ Bounding Box → Robot Coordinate 연결 노드
- ☑ 실제 동작 전 Dry Run 구조

### 현재 검증 필요
- ☐ 실제 LEGO 객체 탐지 성능
- ☐ LEGO 색상 구분
- ☐ 실제 Bowl XYZ 측정 및 등록
- ☐ LEGO Pick 높이(Z) 미세 조정
- ☐ Bounding Box 중심과 실제 Grasp Point 오차 측정
- ☐ VLM → Vision → ROS2 전체 Pipeline 통합 테스트
- ☐ 반복 Pick & Place 성공률 측정

## 10. 향후 개발 계획
### 10.1 YOLO → YOLOE 전환 검토
현재 객체 인식 구조를 향후 YOLOE 기반으로 확장하는 것을 검토한다.

기존 YOLO 방식은 사전에 정의하고 학습한 클래스에 대한 객체 탐지를 중심으로 사용하지만, YOLOE를 활용하면 보다 유연한 객체 인식 구조를 실험할 수 있다.

Deskbot에서는 LEGO를 이용해 기본 Pick & Place 시스템을 안정화한 뒤 다양한 데스크 객체로 확장하는 단계에서 적용 가능성을 검토한다.

### 10.2 GR-CONV 계열 Grasp Detection 검토
현재 Deskbot은 Bounding Box 중심과 Top-down Grasp를 기본 파지 전략으로 사용한다.

그러나 물체의 형태가 복잡해지면 Bounding Box 중심이 항상 최적의 Grasp Point라고 볼 수 없다.

향후에는 RGB-D 정보를 이용하여 다음 정보를 예측하는 Grasp Detection 방식의 도입을 검토한다.
- Grasp Point
- Grasp Width
- Grasp Orientation
- Grasp Quality

다만 OpenManipulator-X의 자유도와 End-Effector 구조상 예측된 모든 Grasp Orientation을 그대로 실행하기 어려우므로, 실제 로봇의 동작 가능 범위에 맞는 방식으로 제한하여 적용할 필요가 있다.

### 10.3 ArUco 기반 Calibration 자동화
현재 Calibration 과정의 수동 작업을 줄이기 위해 ArUco Marker 기반 자동 Calibration을 검토한다.

목표: ArUco Marker Detection → Camera Reference Point 자동 획득 → Robot Reference Point 대응 → Transformation 계산

RealSense Depth와 함께 사용하여 Z 좌표 추정 정확도를 높이는 방법도 실험한다.

### 10.4 VLM 모델 변경
현재 사용 중인 VLM 환경에서 전체 시스템을 먼저 검증한 뒤 향후 모델 변경을 검토한다.
- Qwen2.5-VL 3B(현재)
- Qwen3-VL 4B(검토)

모델 변경 시 Jetson Orin에서의 추론 속도, 메모리 사용량 및 객체 선택 정확도를 함께 비교한다.

### 10.5 Whisper 음성 입력 재통합
현재는 시스템 디버깅을 위해 텍스트 명령을 사용한다.

전체 Pick & Place Pipeline이 안정화되면: 사용자 음성 → Whisper → Text → VLM → Vision → ROS2 → Pick & Place

### 10.6 FSM 및 실패 복구
최종 시스템에서는 각 단계를 상태 기반으로 관리하는 FSM 도입을 검토한다.
- IDLE → COMMAND_RECEIVED → DETECTING → TARGET_SELECTED → COORDINATE_ESTIMATION → APPROACH → GRASP → LIFT → PLACE → VERIFY → DONE

실패가 발생하면 해당 단계와 실패 원인을 판단하여 재탐지 또는 재시도를 수행하도록 확장한다.

### 10.7 TTS

FSM과 전체 시스템이 안정화된 이후 사용자에게 현재 상태를 알려주는 TTS 기능을 추가하는 것을 검토한다.

"빨간 레고를 확인했습니다."
"물체를 이동하겠습니다."
"작업이 완료되었습니다."

## 11. 참고 프로젝트 및 자료
### [Open-Manipulator-LLM](https://github.com/Demolus13/Open-Manipulator-LLM)
기존 OpenManipulator 기반 자연어 로봇 제어 프로젝트를 초기 ROS2 마이그레이션 및 시스템 구조 설계 시 참고하였다.

### [Lerobot](https://github.com/huggingface/lerobot/blob/main/examples/omx/README.md)
OpenManipulator-X 기반 ACT 및 imitation learning 관련 향후 확장 가능성을 검토하기 위한 참고 자료로 사용한다.

현재 LEGO Pick & Place 기본 시스템에서는 ACT를 사용하지 않는다.


