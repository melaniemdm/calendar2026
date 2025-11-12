#  Génération du Calendrier ASMAA 2026

Ce projet permet de générer automatiquement le **calendrier 2026** de l’Association Saint Maurienne des Amis des Animaux (ASMAA).  
Il crée une **page de couverture** et **12 pages mensuelles**, chacune avec une photo différente, à partir des fichiers du dossier `images/`.

---

##  Installation

###  Cloner le dépôt

```bash
git clone https://github.com/melaniemdm/calendar2026.git
cd calendar2026
```

###  Créer un environnement virtuel Python

```bash
python3 -m venv venv
source venv/bin/activate   # (sous Windows : venv\Scripts\activate)
```

###  Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Les paramètres sont définis dans le fichier `config.yaml` :  
- L’année à générer (`year`)  
- Le nom de l’association  
- Les chemins des images (`images_dir`) et du dossier de sortie (`output_dir`)  
- Les couleurs et marges du calendrier

Exemple minimal :

```yaml
year: 2026
association: "Association Saint Maurienne des Amis des Animaux (ASMAA)"
paths:
  images_dir: "images"
  output_dir: "calendrier_ASMAA_2026"
```

---

##  Génération du calendrier

Pour lancer la génération complète (page de garde + 12 mois) :

```bash
python generate_calendar_visual.py
```

Les fichiers seront générés dans le dossier :
```
calendrier_ASMAA_2026/
```

---

##  Structure du projet

```
calendar2026/
│
├── images/                     # Dossier contenant les images
│   ├── cover.png               # Photo de couverture
│   ├── 01_janvier.png
│   ├── 02_fevrier.png
│   └── ... jusqu'à 12_decembre.png
│
├── calendrier_ASMAA_2026/      # Dossier généré automatiquement
│   ├── ASMAA_Couverture_2026.png
│   ├── ASMAA_Calendrier_2026_01_A4.png
│   └── ... jusqu'à 12
│
├── config.yaml                 # Fichier de configuration
├── requirements.txt            # Dépendances Python
├── generate_calendar_visual.py # Script principal
└── README.md                   # Ce fichier
```

---

##  Nettoyage

Pour supprimer les images générées :

```bash
rm -rf calendrier_ASMAA_2026
```

---

##  Dépendances principales

- `matplotlib`
- `PyYAML`

---

##  Auteur

Projet développé par **Mélanie**  
Association Saint Maurienne des Amis des Animaux (ASMAA)
