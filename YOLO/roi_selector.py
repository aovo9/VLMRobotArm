import cv2
import numpy as np


class ROISelector4Points:
    def __init__(self, camera_index=4):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

        if not self.cap.isOpened():
            raise RuntimeError("카메라를 열 수 없습니다.")

        self.points = []
        self.window_name = "ROI Selector 4 Points"

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.points) >= 4:
                print("이미 4개 점이 선택되었습니다. r 키로 초기화하세요.")
                return

            self.points.append((x, y))
            print(f"Point {len(self.points)}: ({x}, {y})")

            if len(self.points) == 4:
                print("\n선택된 4점 ROI:")
                print(f"self.roi_points = {self.points}")

                pts = np.array(self.points, dtype=np.int32)
                x, y, w, h = cv2.boundingRect(pts)

                print("\nYOLO crop용 bounding rectangle:")
                print(f"self.roi_rect = ({x}, {y}, {x + w}, {y + h})")
                print()

    def draw_points_and_polygon(self, frame):
        display = frame.copy()

        # 찍은 점 표시
        for idx, point in enumerate(self.points):
            cv2.circle(display, point, 6, (0, 0, 255), -1)
            cv2.putText(
                display,
                f"P{idx + 1} {point}",
                (point[0] + 10, point[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2
            )

        # 점끼리 선 연결
        if len(self.points) >= 2:
            for i in range(len(self.points) - 1):
                cv2.line(display, self.points[i], self.points[i + 1], (255, 0, 0), 2)

        # 4개 점이 선택되면 닫힌 다각형 표시
        if len(self.points) == 4:
            pts = np.array(self.points, dtype=np.int32)
            cv2.polylines(display, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

            # 반투명 ROI 영역 표시
            overlay = display.copy()
            cv2.fillPoly(overlay, [pts], color=(255, 0, 0))
            display = cv2.addWeighted(overlay, 0.25, display, 0.75, 0)

            cv2.putText(
                display,
                f"ROI Points: {self.points}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 0, 0),
                2
            )

        return display

    def run(self):
        print("4점 ROI 선택 프로그램 시작")
        print("--------------------------------")
        print("마우스 왼쪽 클릭 4번: ROI 꼭지점 지정")
        print("r 키: 다시 선택")
        print("s 키: 현재 ROI 출력")
        print("q 키: 종료")
        print("--------------------------------")

        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            display = self.draw_points_and_polygon(frame)

            cv2.imshow(self.window_name, display)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):
                self.points = []
                print("ROI 초기화")

            elif key == ord("s"):
                if len(self.points) == 4:
                    pts = np.array(self.points, dtype=np.int32)
                    x, y, w, h = cv2.boundingRect(pts)

                    print("\n현재 4점 ROI:")
                    print(f"self.roi_points = {self.points}")
                    print(f"self.roi_rect = ({x}, {y}, {x + w}, {y + h})")
                    print()
                else:
                    print(f"아직 4개 점이 선택되지 않았습니다. 현재 {len(self.points)}개 선택됨.")

            elif key == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    selector = ROISelector4Points(camera_index=4)
    selector.run()