#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le calendrier complet ASMAA 2026 avec :
- 1 page de couverture avec photo
- 12 pages mensuelles avec photos différentes
Les images sont prises dans le dossier /images
"""

import os
import calendar
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

# --- Constantes ---
YEAR = 2026
ASSOCIATION = "Association Saint Maurienne des Amis des Animaux (ASMAA)"

MONTHS_FR = [
    "JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN",
    "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"
]
WEEKDAYS_FR = ["L", "M", "M", "J", "V", "S", "D"]

HOLIDAYS_2026 = {
    (2026, 1, 1): "Jour de l’An",
    (2026, 4, 6): "Lundi de Pâques",
    (2026, 5, 1): "Fête du Travail",
    (2026, 5, 8): "Victoire 1945",
    (2026, 5, 14): "Ascension",
    (2026, 5, 25): "Lundi de Pentecôte",
    (2026, 7, 14): "Fête nationale",
    (2026, 8, 15): "Assomption",
    (2026, 11, 1): "Toussaint",
    (2026, 11, 11): "Armistice",
    (2026, 12, 25): "Noël",
}

def draw_cover_page(year, outpath, image_path=None):
    """Crée une page de garde du calendrier"""
    dpi = 300
    width_in, height_in = 8.27, 11.69
    bg = "#f2f2f2"
    text_color = "#444444"

    fig = plt.figure(figsize=(width_in, height_in), dpi=dpi)
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xlim(0, 210)
    ax.set_ylim(0, 297)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 210, 297, facecolor=bg, edgecolor="none"))

    # Titre principal
    ax.text(105, 240, f"CALENDRIER {year}", fontsize=36, fontweight="bold",
            color=text_color, ha="center", va="center")
    ax.text(105, 220, ASSOCIATION, fontsize=16, color=text_color,
            ha="center", va="center")

    # Zone photo
    photo_x, photo_y, photo_w, photo_h = 25, 60, 160, 120
    if image_path and os.path.exists(image_path):
        try:
            img = mpimg.imread(image_path)
            print(f"   ✅ Image chargée : {image_path} | type={type(img)}, shape={getattr(img, 'shape', 'inconnu')}")
            if img is None or (hasattr(img, "size") and img.size == 0):
                print("   ⚠️ Image vide ou non lisible, zone grisée utilisée.")
            else:
                ax.imshow(img,
                          extent=[photo_x, photo_x + photo_w, photo_y, photo_y + photo_h],
                          aspect='auto',
                          zorder=5)
                print(f"✅ Image de couverture insérée : {image_path}")
        except Exception as e:
            print(f"⚠️ Erreur lors de l’insertion de l’image de couverture : {e}")
    else:
        print(f"❌ Image non trouvée : {image_path}")
        ax.add_patch(Rectangle((photo_x, photo_y), photo_w, photo_h,
                               facecolor="#e6e6e6", edgecolor="#dddddd", linewidth=1))
        ax.text(photo_x + photo_w/2, photo_y + photo_h/2, "ZONE PHOTO DE COUVERTURE",
                fontsize=14, color="#888888", ha="center", va="center")

    # ✅ C’est cette ligne qui manquait :
    fig.savefig(outpath, dpi=dpi, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"💾 Page de garde enregistrée sous : {outpath}")




def draw_month_visual(year, month, outpath, image_path=None):
    """Crée une page mensuelle du calendrier"""
    dpi = 300
    width_in, height_in = 8.27, 11.69
    bg = "#f2f2f2"
    text_color = "#444444"
    grid_color = "#cccccc"
    weekend_bg = "#e8e8e8"
    holiday_color = "red"

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)

    fig = plt.figure(figsize=(width_in, height_in), dpi=dpi)
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xlim(0, 210)
    ax.set_ylim(0, 297)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 210, 297, facecolor=bg, edgecolor="none"))

    # Titre
    ax.text(10, 282, f"{MONTHS_FR[month-1]} {year}", fontsize=22, color=text_color,
            va="top", ha="left", fontweight="bold")

    # --- Zone photo ---
    photo_x, photo_y, photo_w, photo_h = 10, 160, 190, 110

    if image_path and os.path.exists(image_path):
        try:
            img = mpimg.imread(image_path)
            print(f"   ✅ Image chargée : {image_path} | type={type(img)}, shape={getattr(img, 'shape', 'inconnu')}")

            if img is None or (hasattr(img, 'size') and img.size == 0):
                print(f"   ⚠️ Image vide ou non lisible, zone grisée utilisée pour {MONTHS_FR[month-1]}.")
                ax.add_patch(Rectangle((photo_x, photo_y), photo_w, photo_h,
                                       facecolor="#e6e6e6", edgecolor="#dddddd", linewidth=1))
                ax.text(photo_x + photo_w / 2, photo_y + photo_h / 2, "ZONE PHOTO",
                        fontsize=18, color="#888888", ha="center", va="center")
            else:
                ax.imshow(img,
                          extent=[photo_x, photo_x + photo_w, photo_y, photo_y + photo_h],
                          aspect='auto',
                          zorder=5)
                print(f"✅ Image insérée pour {MONTHS_FR[month-1]} : {image_path}")

        except Exception as e:
            print(f"⚠️ Erreur lors de l’insertion de {MONTHS_FR[month-1]} : {e}")
            ax.add_patch(Rectangle((photo_x, photo_y), photo_w, photo_h,
                                   facecolor="#e6e6e6", edgecolor="#dddddd", linewidth=1))
            ax.text(photo_x + photo_w / 2, photo_y + photo_h / 2, "ZONE PHOTO",
                    fontsize=18, color="#888888", ha="center", va="center")
    else:
        print(f"❌ Image non trouvée pour {MONTHS_FR[month-1]} : {image_path}")
        ax.add_patch(Rectangle((photo_x, photo_y), photo_w, photo_h,
                               facecolor="#e6e6e6", edgecolor="#dddddd", linewidth=1))
        ax.text(photo_x + photo_w / 2, photo_y + photo_h / 2, "ZONE PHOTO",
                fontsize=18, color="#888888", ha="center", va="center")

    # --- Grille du calendrier ---
    left, bottom, right, top = 10, 22, 200, 150
    cols = 7
    rows = 1 + len(month_days)
    cell_w = (right - left) / cols
    cell_h = (top - bottom) / rows

    # Entêtes
    for c in range(cols):
        x = left + c * cell_w
        y = top - cell_h
        ax.add_patch(Rectangle((x, y), cell_w, cell_h,
                               facecolor="white", edgecolor=grid_color, linewidth=0.8))
        ax.text(x + cell_w / 2, y + cell_h / 2, WEEKDAYS_FR[c],
                ha="center", va="center", fontsize=12, color=text_color)

    # Jours
    for r, week in enumerate(month_days):
        for c, day in enumerate(week):
            x = left + c * cell_w
            y = top - (r + 2) * cell_h
            is_weekend = (c >= 5)
            face = weekend_bg if is_weekend else "white"
            ax.add_patch(Rectangle((x, y), cell_w, cell_h,
                                   facecolor=face, edgecolor=grid_color, linewidth=0.8))
            if day != 0:
                color = holiday_color if (year, month, day) in HOLIDAYS_2026 else text_color
                ax.text(x + cell_w * 0.08, y + cell_h * 0.78, str(day),
                        ha="left", va="top", fontsize=11, color=color)

    # --- Sauvegarde ---
    fig.savefig(outpath, dpi=dpi, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"💾 Mois {MONTHS_FR[month-1]} enregistré sous : {outpath}")


def generate_full_calendar():
    """Crée la couverture + les 12 mois avec images"""
    os.makedirs("calendrier_ASMAA_2026", exist_ok=True)
    print("🖨 Création de la page de garde...")
    
    draw_cover_page(
        YEAR,
        "calendrier_ASMAA_2026/ASMAA_Couverture_2026.png",
        "images/cover.png"
    )

    print("🗓 Génération des 12 mois...")
    for month in range(1, 13):
        month_name = MONTHS_FR[month - 1].lower()
        possible_files = [
            f"images/{month:02d}_{month_name}.png",
            ]

        print(f"\n🔍 Recherche d’image pour {MONTHS_FR[month - 1]} :")
        for p in possible_files:
            print("   →", os.path.abspath(p), "✅" if os.path.exists(p) else "❌")

        photo_path = next((p for p in possible_files if os.path.exists(p)), None)

        out = f"calendrier_ASMAA_2026/ASMAA_Calendrier_2026_{month:02d}_A4.png"
        draw_month_visual(YEAR, month, out, photo_path)
        print(f"  → {MONTHS_FR[month - 1]} créé ✅")

    print("\n🎉 Génération complète terminée ! Les fichiers sont dans 'calendrier_ASMAA_2026'.")


if __name__ == "__main__":
    generate_full_calendar()
