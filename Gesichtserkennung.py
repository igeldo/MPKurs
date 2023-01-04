import cv2


class FaceDetector:
    def __init__(self, capture_device=0):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(capture_device)

    def detect_faces(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.face_cascade.detectMultiScale(gray)

    def draw_faces(self, frame):
        for (x, y, w, h) in self.detect_faces():
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    def show_frame(self, frame):
        cv2.imshow('Frame', frame)

    def run(self):cv2.data.haarcascades
        while True:
            ret, frame = self.cap.read()
            self.draw_faces(frame)
            self.show_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


detector = FaceDetector()
detector.run()