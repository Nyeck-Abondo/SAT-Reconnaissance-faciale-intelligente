import face_recognition
import pickle
import os
import cv2

# Chemin vers le dossier contenant les images d'entraînement
CHEMIN_DATASET = "dataset"
# Nom du fichier de sortie
FICHIER_SORTIE = "encodings.pickle"

known_encodings = []
known_names = []

print("[INFO] Début de l'encodage des visages...")

# Parcourir chaque sous-dossier (qui correspond au nom de l'étudiant)
for nom_etudiant in os.listdir(CHEMIN_DATASET):
    chemin_dossier_etudiant = os.path.join(CHEMIN_DATASET, nom_etudiant)
    
    # Ignorer si ce n'est pas un dossier
    if not os.path.isdir(chemin_dossier_etudiant):
        continue
        
    print(f"[INFO] Traitement des images pour : {nom_etudiant}")
    
    # Parcourir les images de cet étudiant
    for nom_image in os.listdir(chemin_dossier_etudiant):
        chemin_image = os.path.join(chemin_dossier_etudiant, nom_image)
        
        try:
            # Charger l'image avec face_recognition
            # Par défaut, face_recognition charge l'image en RGB
            image = face_recognition.load_image_file(chemin_image)
            
            # Détecter les coordonnées (bounding boxes) des visages dans l'image
            boxes = face_recognition.face_locations(image)
            
            # Calculer les encodages pour chaque visage détecté
            encodings = face_recognition.face_encodings(image, boxes)
            
            # Ajouter l'encodage et le nom aux listes
            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(nom_etudiant)
                
        except Exception as e:
            print(f"[ERREUR] Impossible de traiter {chemin_image}: {e}")

print(f"[INFO] Sérialisation des encodages vers {FICHIER_SORTIE}...")

# Créer un dictionnaire contenant les encodages et les noms
data = {"encodings": known_encodings, "names": known_names}

# Sauvegarder les données dans un fichier pickle
with open(FICHIER_SORTIE, "wb") as f:
    pickle.dump(data, f)

print(f"[INFO] Encodage terminé ! {len(known_encodings)} visages encodés au total.")