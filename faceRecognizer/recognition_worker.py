"""
Processus de reconnaissance faciale (sans aucune dépendance Qt).

dlib ne libère pas le GIL Python pendant la détection : dans un simple thread, le calcul
figerait quand même l'affichage de la webcam. On l'exécute donc dans un processus séparé.
"""
import face_recognition

from faceRecognizer.face_recognizer import UNKNOWN, match_face, distance_to_confidence


def recognition_worker(in_queue, out_queue, names, encodings, tolerance, upsample):
    """Reçoit (image RGB réduite, échelle), renvoie la liste
    [(top, right, bottom, left, nom, confiance)] en coordonnées de l'image complète.
    Un message None arrête le processus."""
    while True:
        item = in_queue.get()
        if item is None:
            break
        small_rgb, scale = item

        results = []
        try:
            locations = face_recognition.face_locations(
                small_rgb, number_of_times_to_upsample=upsample)
            face_encodings = (face_recognition.face_encodings(small_rgb, locations)
                              if locations else [])
            for (top, right, bottom, left), enc in zip(locations, face_encodings):
                name, dist = match_face(enc, names, encodings, tolerance)
                confidence = (distance_to_confidence(dist, tolerance)
                              if name != UNKNOWN else 0.0)
                results.append((int(top / scale), int(right / scale),
                                int(bottom / scale), int(left / scale),
                                name, confidence))
        except Exception as e:
            print(f"[ERREUR] Reconnaissance : {e}")

        out_queue.put(results)   # toujours répondre, même vide, pour débloquer la boucle caméra
