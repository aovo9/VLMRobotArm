# Version History
## **26/09/14 original**
[deskbot.zip](https://github.com/user-attachments/files/32176559/deskbot.zip)
- 기존 Deskbot 코드 백업.

## **26/09/14 v2.0.0 + v2.0.1**
[deskbot v2.0.0.zip](https://github.com/user-attachments/files/32181785/deskbot.v1.0.0.zip)
[deskbot v2.0.1.zip](https://github.com/user-attachments/files/32184649/deskbot.v1.01.zip)
- LEGO Pick & Place 구조로 프로젝트 변경 시작.
- LEGO 전용 Object Class 구성
- Red / Green / Blue Bowl Destination 추가
- Bowl XYZ 기반 Place 구조 추가
- Safety Validation 변경
- bbox_to_position_node 구현
- VLM Target → Robot Coordinate 연결 구조 추가

## **26/09/15 v2.0.2**
[deskbot.v2.0.2.zip](https://github.com/user-attachments/files/32218292/deskbot.v1.0.2.zip)
- ROS2 / OMX 제어 코드 수정 및 안정화
- LEGO Pick & Place 통합 구조 보완
- Calibration 및 실제 동작 검증을 위한 코드 정리

## **26/09/15 v2.0.3**
[deskbotv2.0.3.zip](https://github.com/user-attachments/files/32244827/deskbotv2.0.3.zip)
* LEGO 1-class YOLO + VLM 색상 판별 구조 추가
* Red / Green / Blue Bowl 매핑 추가
* LEGO 전용 Top-down Pick & Place 흐름 추가
* Eye-to-Hand 3D 좌표 및 동일 RGB-D 검증 구조 추가
* 파지·운반·놓기 상태 및 완료 확인 로직 추가
* v2.0.2의 LEGO 구조 중 필요한 부분을 기존 Deskbot 코드에 선별 반영
* 사용자 요청 색과 VLM 관측 색을 분리해 검증하도록 변경
* 공통 LEGO 파지 profile과 개별 물체 ID를 분리하도록 변경
* MoveIt 경로·Scene·실패/정지 처리 보완
* 콘솔 결과 및 실패 사유 출력 개선
* 빨간 LEGO 1개 기준 end-to-end software dry-run 완료
* 관련 회귀 테스트 및 3개 ROS2 패키지 build 통과

## **26/09/17 Gum-Sample**
[runs.zip](https://github.com/user-attachments/files/32314453/runs.zip)


