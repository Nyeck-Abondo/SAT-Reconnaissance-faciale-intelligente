import argparse
import os
import pickle

import cv2
import face_recognition
import numpy as np

UNKNOWN = "Inconnu"
# Seuil calibré sur encodings.pickle : à 0.55 la majorité des visages d'une personne
# "ressemblent" déjà à quelqu'un d'autre de la base -> les inconnus étaient reconnus à tort.
DEFAULT_TOLERANCE = 0.42
# Nombre d'encodages d'une même personne utilisés pour calculer sa distance (moyenne des k meilleurs)
DEFAULT_K = 2

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


def distance_to_confidence(distance, tolerance=DEFAULT_TOLERANCE):
    """Convertit une distance en pourcentage : 50 % exactement au seuil de tolérance,
    plus de 50 % = visage reconnu, moins de 50 % = visage inconnu."""
    if distance is None:
        return 0.0
    rng = 1.0 - tolerance
    lin = (1.0 - distance) / (rng * 2.0)
    if distance > tolerance:
        return max(0.0, lin) * 100
    return min(100.0, (lin + (1.0 - lin) * ((lin - 0.5) * 2.0) ** 0.2) * 100)


def match_face(encoding, known_names, known_encodings,
               tolerance=DEFAULT_TOLERANCE, k=DEFAULT_K):
    """Retourne (nom, distance). Le nom vaut UNKNOWN si aucune personne de la base
    n'est assez proche. La distance d'une personne est la moyenne de ses k
    meilleurs encodages, ce qui évite qu'une seule photo "chanceuse" valide un inconnu."""
    if len(known_encodings) == 0:
        return UNKNOWN, None
    distances = face_recognition.face_distance(known_encodings, encoding)
    names = np.asarray(known_names)
    best_name, best_score = UNKNOWN, float("inf")
    for name in np.unique(names):
        score = float(np.sort(distances[names == name])[:k].mean())
        if score < best_score:
            best_name, best_score = str(name), score
    if best_score <= tolerance:
        return best_name, best_score
    return UNKNOWN, best_score


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
        r_name = name
        results.append({
            "name": name,
            "distance": dist,
            "confidence": (distance_to_confidence(dist, tolerance)
                           if r_name != UNKNOWN else 0.0),
            "box": box,
        })
    return results


def recognize_file(path, db_path, tolerance=DEFAULT_TOLERANCE, model="hog"):
    names, encodings = load_known_encodings(db_path)
    rgb = load_image(path)
    return rgb, recognize(rgb, names, encodings, tolerance, model)


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