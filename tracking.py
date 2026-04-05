import cv2
import numpy as np
from ultralytics import YOLO
from facerec import detect_faces, train_model, recognize_face

class PersonTracker:
    def __init__(self):
        self.trackers = {}
        self.next_id = 1
        self.names = {}
        self.yolo_model = YOLO('yolov8n.pt')

    def detect_persons_yolo(self, frame):
        results = self.yolo_model(frame, verbose=False)
        persons = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                if cls == 0 and conf > 0.5:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x, y, w, h = int(x1), int(y1), int(x2 - x1), int(y2 - y1)
                    persons.append((x, y, w, h, conf))

        return persons

    def add_tracker(self, frame, bbox, name):
        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, bbox)
        person_id = self.next_id
        self.trackers[person_id] = tracker
        self.names[person_id] = name
        self.next_id += 1
        return person_id

    def update_trackers(self, frame):
        to_remove = []
        tracked_boxes = {}

        for person_id, tracker in self.trackers.items():
            success, bbox = tracker.update(frame)
            if success:
                tracked_boxes[person_id] = bbox
            else:
                to_remove.append(person_id)

        for pid in to_remove:
            del self.trackers[pid]
            del self.names[pid]

        return tracked_boxes

    def is_new_person(self, bbox, tracked_boxes):
        x, y, w, h = bbox
        center = (x + w/2, y + h/2)

        for tracked_bbox in tracked_boxes.values():
            tx, ty, tw, th = tracked_bbox
            tcenter = (tx + tw/2, ty + th/2)
            dist = np.sqrt((center[0]-tcenter[0])**2 + (center[1]-tcenter[1])**2)
            if dist < 100:
                return False
        return True

def track_video(video_path):
    cap = cv2.VideoCapture(video_path)
    person_tracker = PersonTracker()
    model, names = train_model()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1, 0)
        tracked_boxes = person_tracker.update_trackers(frame)

        for person_id, bbox in tracked_boxes.items():
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            name = person_tracker.names[person_id]
            cv2.putText(frame, f"{name} (ID:{person_id})", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if frame_count % 15 == 0:
            persons_detected = person_tracker.detect_persons_yolo(frame)

            for person_bbox in persons_detected:
                x, y, w, h, conf = person_bbox

                roi = frame[y:y+h, x:x+w]
                if roi.size == 0:
                    continue

                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                faces = detect_faces(gray_roi)

                if len(faces) > 0:
                    frame_roi = roi.copy()
                    frame_temp, recognized = recognize_face(model, frame_roi, gray_roi, faces, names)

                    if len(recognized) > 0:
                        name, rec_conf = recognized[0]
                        body_bbox = (x, y, w, h)

                        if person_tracker.is_new_person(body_bbox, tracked_boxes):
                            person_tracker.add_tracker(frame, body_bbox, name)

        cv2.imshow('Criminal Tracking', frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        track_video(sys.argv[1])
    else:
        track_video(0)
