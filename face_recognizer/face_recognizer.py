import argparse
import os
import pickle

import cv2
import face_recognition
import numpy as np

UNKNOWN = "Inconnu"
DEFAULT_TOLERANCE = 0.5   

def load_image(path):
    
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Image introuvable : {path}")
    
    data = np.fromfile(path, dtype=np.uint8)
    bgr = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError(f"Image illisible : {path}")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def load_known_encodings(path):

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Fichier d'encodages introuvable : {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext in (".pkl", ".pickle"):
        with open(path, "rb") as f:  
            data = pickle.load(f)
        names, encodings = data["names"], data["encodings"]
    elif ext == ".npz":
        data = np.load(path, allow_pickle=True)
        names, encodings = data["names"], data["encodings"]
    else:
        raise ValueError("Format non géré (utiliser .pkl ou .npz)")
    names = [str(n) for n in names]
    encodings = [np.asarray(e, dtype=np.float64) for e in encodings]
    if len(names) != len(encodings):
        raise ValueError("Le nombre de noms et d'encodages est différent")
    return names, encodings


def detect_faces(rgb, model="hog", upsample=2):
    
    return face_recognition.face_locations(
        rgb, number_of_times_to_upsample=upsample, model=model)


def encode_faces(rgb, locations):
    return face_recognition.face_encodings(rgb, known_face_locations=locations)


def distance_to_confidence(distance):
    return max(0.0, 1.0 - distance) * 100


def match_face(encoding, known_names, known_encodings, tolerance=DEFAULT_TOLERANCE):

    if not known_encodings:
        return UNKNOWN, None
    distances = face_recognition.face_distance(known_encodings, encoding)
    best = int(np.argmin(distances))
    dist = float(distances[best])
    if dist <= tolerance:
        return known_names[best], dist
    return UNKNOWN, dist


def recognize(rgb, known_names, known_encodings,
              tolerance=DEFAULT_TOLERANCE, model="hog"):

    if not 0 < tolerance < 1:
        raise ValueError("La tolérance doit être comprise entre 0 et 1")
    locations = detect_faces(rgb, model=model)
    if not locations:
        return []
    encodings = encode_faces(rgb, locations)
    results = []
    for box, enc in zip(locations, encodings):
        name, dist = match_face(enc, known_names, known_encodings, tolerance)
        results.append({
            "name": name,
            "distance": dist,
            "confidence": distance_to_confidence(dist) if dist is not None else 0.0,
            "box": box,
        })
    return results


def recognize_file(path, db_path, tolerance=DEFAULT_TOLERANCE, model="hog"):
    names, encodings = load_known_encodings(db_path)
    rgb = load_image(path)
    return rgb, recognize(rgb, names, encodings, tolerance, model)


def recognize_frame(frame_bgr, known_names, known_encodings,
                    tolerance=DEFAULT_TOLERANCE, model="hog", scale=0.5):

    if frame_bgr is None or frame_bgr.size == 0:
        return []
    if not 0 < scale <= 1:
        raise ValueError("scale doit être compris entre 0 (exclu) et 1")
    small = frame_bgr if scale == 1 else cv2.resize(frame_bgr, (0, 0), fx=scale, fy=scale)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    results = recognize(rgb, known_names, known_encodings, tolerance, model)
    if scale != 1:
        for r in results:
            r["box"] = tuple(int(v / scale) for v in r["box"])
    return results


def annotate_frame(frame_bgr, results):
    
    img = frame_bgr.copy()
    for r in results:
        top, right, bottom, left = r["box"]
        color = GREEN if r["name"] != UNKNOWN else RED
        cv2.rectangle(img, (left, top), (right, bottom), color, 2)
        label = f"{r['name']} {r['confidence']:.0f}%"
        cv2.putText(img, label, (left, max(top - 8, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return img


class FaceRecognizer:

    def __init__(self, db_path, tolerance=DEFAULT_TOLERANCE, model="hog"):
        self.names, self.encodings = load_known_encodings(db_path)
        self.model = model
        self.set_tolerance(tolerance)

    def set_tolerance(self, tolerance):
        if not 0 < tolerance < 1:
            raise ValueError("La tolérance doit être comprise entre 0 et 1")
        self.tolerance = tolerance

    
    def process_image(self, path):
        rgb = load_image(path)
        results = recognize(rgb, self.names, self.encodings,
                            self.tolerance, self.model)
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        return annotate_frame(bgr, results), results

def main():
    parser = argparse.ArgumentParser(description="Reconnaissance faciale sur image")
    parser.add_argument("--image", required=True, help="chemin de l'image")
    parser.add_argument("--db", required=True, help="fichier d'encodages (.pkl ou .npz)")
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE)
    parser.add_argument("--model", default="hog", choices=["hog", "cnn"])
    args = parser.parse_args()

    try:
        rgb, results = recognize_file(args.image, args.db, args.tolerance, args.model)
    except (FileNotFoundError, ValueError) as e:
        print(f"Erreur : {e}")
        return

    if not results:
        print("Aucun visage détecté.")
        return

    for i, r in enumerate(results, 1):
        dist = "n/a" if r["distance"] is None else f"{r['distance']:.3f}"
        print(f"Visage {i} : {r['name']} | distance {dist} | confiance {r['confidence']:.1f}%")


if __name__ == "__main__":
    main()                                                                                                                                                                                                                                                                                            