# SAT — Système de Reconnaissance Faciale Intelligente

##  Présentation du projet

**SAT-Reconnaissance-faciale-intelligente** est un projet Python réalisé dans le cadre du cours **QNI-2083**. Il vise à mettre en œuvre un système capable de détecter des visages dans des images et de reconnaître des personnes à partir de caractéristiques faciales préalablement enregistrées.

Le projet s'appuie sur des techniques de vision par ordinateur et sur la bibliothèque `face_recognition` pour l'encodage et la comparaison des visages.

##  Objectifs

- Détecter les visages présents dans des images.
- Extraire les caractéristiques faciales sous forme d'encodages numériques.
- Associer les encodages aux personnes correspondantes.
- Constituer une base de données d'encodages faciaux.
- Mettre en place un système de reconnaissance faciale à partir des données enregistrées.
- Tester le fonctionnement du système et identifier les possibilités d'amélioration.

##  Technologies utilisées

| Technologie | Rôle |
|---|---|
| Python | Langage de programmation principal |
| `face_recognition` | Détection, encodage et comparaison des visages |
| OpenCV (`cv2`) | Traitement et manipulation d'images |
| `pickle` | Sérialisation et sauvegarde des encodages |
| Git et GitHub | Gestion du code source et collaboration |

##  Structure du projet

```text
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
```

## Prérequis

Avant de commencer, assurez-vous de disposer des éléments suivants :

- Python installé sur votre ordinateur.
- Git pour récupérer le dépôt.
- Une webcam si le module de reconnaissance utilise la capture vidéo en direct.
- Les bibliothèques Python nécessaires au fonctionnement du projet.

La bibliothèque `face_recognition` dépend notamment de `dlib`, dont l'installation peut nécessiter une configuration supplémentaire selon le système d'exploitation.

## Installation

### 1. Cloner le dépôt

Ouvrez un terminal et exécutez :

```bash
git clone https://github.com/Nyeck-Abondo/SAT-Reconnaissance-faciale-intelligente.git
```

Accédez ensuite au dossier du projet :

```bash
cd SAT-Reconnaissance-faciale-intelligente
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

Activez-le sous Windows :

```powershell
.venv\Scripts\Activate.ps1
```

Sous Linux ou macOS :

```bash
source .venv/bin/activate
```

### 3. Installer les dépendances

Installez les bibliothèques nécessaires :

```bash
python -m pip install opencv-python face_recognition
```

Si l'installation de `face_recognition` échoue, vérifiez les prérequis de `dlib` pour votre environnement.

##  Préparation des données

Le script `encoder.py` utilise un dossier nommé `dataset` contenant les images des personnes à reconnaître.

Organisez les images de la manière suivante :

```text
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
```

Chaque sous-dossier correspond à une personne. Son nom sert d'identifiant lors de l'enregistrement des encodages.

**Conseils :**
- Utilisez des images nettes où les visages sont clairement visibles.
- Privilégiez plusieurs images représentatives par personne.
- Utilisez uniquement des images obtenues avec l'autorisation des personnes concernées.

##  Utilisation

### Étape 1 : Encoder les visages

Après avoir préparé le dossier `dataset`, lancez :

```bash
python encoder.py
```

Le script parcourt les sous-dossiers, charge les images, détecte les visages et calcule leurs encodages numériques.

Les encodages et les noms associés sont ensuite sauvegardés dans le fichier :

```text
encodings.pickle
```

### Étape 2 : Effectuer la reconnaissance

Une fois les encodages générés, utilisez le module de reconnaissance présent dans le projet pour tester l'identification des visages.

La commande exacte dépend du fichier qui sert de point d'entrée dans le dossier `RECONNAISSANCE` ou `faceRecognizer`. Consultez le code de ce module pour connaître les paramètres et la commande de lancement.

##  Fonctionnement général

Le système suit le principe de fonctionnement suivant :

1. **Acquisition :** chargement d'une image ou capture d'un visage.
2. **Détection :** localisation du ou des visages présents dans l'image.
3. **Encodage :** transformation des caractéristiques faciales en représentation numérique.
4. **Comparaison :** comparaison avec les encodages déjà enregistrés.
5. **Identification :** attribution d'un nom lorsqu'une correspondance suffisamment fiable est trouvée.

Le résultat dépend notamment de la qualité des images, des conditions de capture et du seuil de comparaison utilisé.

##  Tests

Le dossier `Tests/` est destiné aux tests du projet.

Les tests peuvent servir à vérifier :
- La détection correcte des visages.
- La génération des encodages.
- La reconnaissance des personnes enregistrées.
- Le comportement face à un visage inconnu.
- La robustesse du système selon la qualité des images.

Consultez les fichiers présents dans ce dossier pour connaître les tests déjà implémentés et la façon de les exécuter.

##  Sécurité et confidentialité

Les données biométriques sont sensibles. Leur utilisation doit respecter la vie privée et les règles applicables en matière de protection des données.

- Obtenez le consentement nécessaire avant de collecter ou d'utiliser des images faciales.
- Limitez l'accès aux images et aux fichiers d'encodage.
- Ne publiez pas de données biométriques personnelles dans le dépôt GitHub.
- Prévoyez des mesures de protection pour le stockage et la suppression des données.
- Ne considérez pas une correspondance faciale comme une preuve absolue d'identité.

##  Contribution

Les contributions visant à améliorer le projet sont les bienvenues.

Pour proposer une modification :

1. Forkez le dépôt.
2. Créez une branche dédiée à votre