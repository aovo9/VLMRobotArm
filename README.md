하드웨어

	젯슨 오린
	
	Open Manipulator-X
	
	리얼센스 d435
	
	키보드, 마우스, 모니터, 마이크

소프트웨어

	VS Code

	Python

	로봇제어	: ROS2 humble / Ubuntu 22.04

	음성인식 : whisper

	이미지 : YOLO V11

	손 인식 : mediapipe or YOLO Pose

유사 프로젝트

	https://github.com/Demolus13/Open-Manipulator-LLM

	이 프로그램 참고하여 손 인식 등의 추가 옵션 성공하면 VLM을 활용해 음성과 이미지 인식을 통합


과정

	환경 설정
	하드웨어 및 각 노드 동작 확인 (omx, whisper 등)
	학습 데이터 수집 및 학습(잡을 물건, 손 등)
	OMX 움직임 미세 조정(크게 움직일 땐 빠르게(move_group), 물건 놓을 땐 미세하게(servo))
	메인 노드 만들어 각 단계 통합(소규모 파라미터 llm 이용)
	실패-재시도 매커니즘 구성
	완성 시 입력-분석 단계를 vlm으로 통합
