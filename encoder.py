import os
import pickle
from deepface import DeepFace

DOSSIER_IMAGES = "images"
FICHIER_ENCODAGES = os.path.join("donnees", "encodages.pkl")


def encoder_images():
    noms = []
    encodages = []

    os.makedirs("donnees", exist_ok=True)

    for fichier in os.listdir(DOSSIER_IMAGES):
        chemin = os.path.join(DOSSIER_IMAGES, fichier)

        if not fichier.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        try:
            resultats = DeepFace.represent(
                img_path=chemin,
                model_name="Facenet",
                detector_backend="opencv",
                enforce_detection=True
            )

            for resultat in resultats:
                noms.append(os.path.splitext(fichier)[0])
                encodages.append(resultat["embedding"])

            print(f"Photo encodée : {fichier}")

        except Exception as erreur:
            print(f"Impossible d'encoder {fichier} : {erreur}")

    if not encodages:
        print("Aucun visage n'a pu être encodé.")
        return

    donnees = {
        "noms": noms,
        "encodages": encodages
    }

    with open(FICHIER_ENCODAGES, "wb") as fichier:
        pickle.dump(donnees, fichier)

    print(f"{len(encodages)} encodage(s) sauvegardé(s).")
    print(f"Fichier créé : {FICHIER_ENCODAGES}")


def charger_encodages():
    if not os.path.exists(FICHIER_ENCODAGES):
        print("Aucun fichier d'encodages trouvé.")
        return None

    with open(FICHIER_ENCODAGES, "rb") as fichier:
        donnees = pickle.load(fichier)

    print("Encodages chargés avec succès.")
    return donnees


if __name__ == "__main__":
    encoder_images()