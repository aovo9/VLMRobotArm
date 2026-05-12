# Open-Manipulator-VLM

## 하드웨어

	- 젯슨 오린
	
	- Open Manipulator-X
	
	- 리얼센스 d435
	
	- 키보드, 마우스, 모니터, 마이크

## 소프트웨어

	- VS Code

	- Python

	- **로봇제어	:** ROS2 humble / Ubuntu 22.04

	- **음성인식 :** whisper

	- **이미지 :** YOLO V11

	- **손 인식 :** mediapipe or YOLO Pose

## 유사 프로젝트

	[https://github.com/Demolus13/Open-Manipulator-LLM]

	이 프로그램 참고하여 손 인식 등의 추가 옵션 성공하면 VLM을 활용해 음성과 이미지 인식을 통합


## 과정

	환경 설정
	하드웨어 및 각 노드 동작 확인 (omx, whisper 등)
	학습 데이터 수집 및 학습(잡을 물건, 손 등)
	OMX 움직임 미세 조정(크게 움직일 땐 빠르게(move_group), 물건 놓을 땐 미세하게(servo))
	메인 노드 만들어 각 단계 통합(소규모 파라미터 llm 이용)
	실패-재시도 매커니즘 구성
	완성 시 입력-분석 단계를 vlm으로 통합

# 유사 프로젝트 진행 상황
	1. **유사 프로젝트 환경**
		- ROS1 Noetic
		- ** 색상 기반 탐지 :** OpenCV를 활용해 HSV 범위를 기준으로 특정 색상을 지닌 객체 검출
		- ** 좌표 계산(Calibration) :** 화면 상의 물체 위치를 로봇이 이해가능한 3차원 공간 좌표로 변환
		- ** 음성 인식 : ** speech_recognition 라이브러리를 사용해 사용자의 목소리를 텍스트로 변환 (Speach to Text)
		- ** LLM : ** LLM은 입력받은 텍스트를 사용자가 원하는 **색상**과 **동작**을 추출하는 역할
			- LLM은 Groq api를 받아와서 진행함
		- ** 로봇 팔 제어 : ** OMX의 End-Effector가 목표 좌표에 정확히 도달하도록 각 관절의 각도를 계산하는 역기구학(Inverse Kinematics) 적용

	2. ** 프로젝트 진행 **
		- **환경 구축 :** Jetson Orin 환경에서 Ros2 Humble 환경 설정
		- **코드 마이그레이션 :**기존 프로젝트 환경이 ROS Noetic 환경이기에 ROS2 구조로 코드를 변경할 필요가 있었음
			- **클라이언트 라이브러리 교체 :** rospy -> rclpy
			- **빌드 및 실행 환경 변경 :** catkin -> colcon
			- **코드 통신 방식 변경 : ** Service -> Topic (Ros2에서는 옛날 방식인 Service 노드를 열지 않음)
	 	- ** 코드 실행 : ** 수정된 Pick_and_place.py로 코드 실행
			- 마이크가 없는 상태로 실행했기에 음성을 입력받는 것 대신 텍스트로 입력받도록 임시 실행
			- ☑ Realsense를 통한 색상 기반 탐지로 객체를 탐지하는가?
			- ☑ 텍스트 입력으로 LLM이 색상과 동작을 추출해 OMX로 명령을 전달하는가?
			- ☐ 명령을 받은 OMX가 객체에 대한 Pick & place를 정확히 진행하는가?
				- realsense 거치대, 단색 객체, 마이크 준비 후 다시 진행 예정
				- 거치대 없이 진행하여 흔들림으로 인해 calibration한 좌표들이 정확히 매칭이 안되는 것 같음.
			- ☐ 음성을 텍스트로 정확히 변환하는가?
