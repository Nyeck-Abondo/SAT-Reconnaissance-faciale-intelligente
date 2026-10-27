# SAT — Système de Reconnaissance Faciale Intelligente

##  Présentation du projet

SAT-Reconnaissance-faciale-intelligente est un projet Python qui vise à mettre en œuvre un système capable de détecter des visages dans des images et de reconnaître des personnes à partir de caractéristiques faciales enregistrées dans une base de donnees.Ce projet s'appuie sur des techniques de vision par ordinateur et sur la bibliothèque `face_recognition` pour l'encodage et la comparaison des visages.

##  Objectifs

il a pour objectif: 
- Détecter les visages présents dans des images.
- Extraire les caractéristiques faciales sous forme d'encodages numériques.
- Mettre en place un système de reconnaissance faciale à partir des données enregistrées.

##  Technologies utilisées

 Technologie                                              | Rôle |
 Python                                                    Langage de programmation principal 
 `face_recognition`                                        Détection, encodage et comparaison des visages 
 OpenCV                                                    Traitement et manipulation d'images 
 `pickle`                                                  Sérialisation et sauvegarde des encodages 
 Git et GitHub                                             Gestion du code source et collaboration 

##  Structure du projet

le projet est strucure comme suit:

SAT-Reconnaissance-faciale-intelligente/
│
├── RECONNAISSANCE/    # Composants liés à la reconnaissance faciale
├── Tests/             # Tests du projet
├── faceRecognizer/    # Modules du système de reconnaissance
│
├── encoder.py         # Encodage des visages du dataset
├── encodings.pickle   # Fichier contenant les encodages sauvegardés
├── .gitignore         # Fichiers exclus du suivi Git
├── LICENSE            # Licence MIT
└── README.md          # Documentation du projet

## Prérequis

Avant de commencer, nous nous sommes assurer d'avoir:

- Python installé sur votre ordinateur;
- Git pour récupérer le dépôt;
- Une webcam;
- Les bibliothèques Python nécessaires au fonctionnement du projet;
- installer les dependances;

##  Préparation des données

Le script `encoder.py` utilise un dossier nommé `dataset` contenant les images des personnes à reconnaître.les images sont organiser de la manière suivante :

dataset/
├── personne_1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.jpg
│
├── personne_2/
│   ├── image1.jpg
│   └── image2.jpg
│
└── personne_3/
    ├── image1.jpg
    └── image2.jpg
Chaque sous-dossier correspond à une personne. Son nom sert d'identifiant lors de l'enregistrement des encodages.

##  Utilisation

Après avoir préparé le dossier `dataset`, Le script parcourt les sous-dossiers, charge les images, détecte les visages et calcule leurs encodages numériques.Les encodages et les noms associés sont ensuite sauvegardés dans le fichier : encodings.pickle. Une fois les encodages générés, utilisez le module de reconnaissance présent dans le projet pour tester l'identification des visages.

Le système suit le principe de fonctionnement suivant :

1.  chargement d'une image ou capture d'un visage.
2.  localisation du ou des visages présents dans l'image.
3.  transformation des caractéristiques faciales en représentation numérique.
4.  comparaison avec les encodages déjà enregistrés.
5.  attribution d'un nom lorsqu'une correspondance suffisamment fiable est trouvée.

##  Tests

Le dossier `Tests/` est destiné aux tests du projet.

Les tests peuvent servir à vérifier :
- La détection correcte des visages.
- La reconnaissance des personnes enregistrées.
- Le comportement face à un visage inconnu.

##  Sécurité et confidentialité

Les données biométriques sont sensibles. Leur utilisation doit respecter la vie privée et les règles applicables en matière de protection des données.

- Obtenir le consentement nécessaire avant de collecter ou d'utiliser des images faciales.
- Limitez l'accès aux images et aux fichiers d'encodage.
- Ne pas publier de données biométriques personnelles dans le dépôt GitHub.
