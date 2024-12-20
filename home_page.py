import tkinter as tk
from customtkinter import CTkButton
from PIL import Image, ImageTk, ImageOps

class HomePage:
    def __init__(self, root, show_map_callback):
        self.root = root
        self.show_map_callback = show_map_callback

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Conteneur principal
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill="both", expand=True)

        # Charger et ajuster l'image de vague
        try:
            wave_image = Image.open("resources/images/wave2.png")  # Chemin de l'image
            wave_image = wave_image.resize((self.root.winfo_screenwidth(), 200), Image.Resampling.LANCZOS)

            # Appliquer les changements de couleur
            wave_image = ImageOps.colorize(ImageOps.grayscale(wave_image), black="white", white="#8B0000")

            wave_photo = ImageTk.PhotoImage(wave_image)

            # Afficher la vague
            wave_label = tk.Label(main_frame, image=wave_photo, bg="white")
            wave_label.image = wave_photo  # Garder une référence pour éviter le garbage collection
            wave_label.pack(fill="x")
        except Exception as e:
            print("Erreur lors du chargement de l'image de vague :", e)

        # Conteneur pour le texte et l'image
        content_frame = tk.Frame(main_frame, bg="white", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)

        # Texte
        text_frame = tk.Frame(content_frame, bg="white")
        text_frame.pack(side="left", fill="y", expand=True)

        tk.Label(
            text_frame,
            text="Bienvenue à l'Analyse des Facteurs de Risque",
            font=("Arial", 24, "bold"),
            fg="#3c6e71", bg="white"
        ).pack(anchor="w", pady=10)

        tk.Label(
                text_frame,
                text=(
                    "Explorez les données régionales pour mieux comprendre les facteurs de risque liés à la santé. "
                    "Visualisez les statistiques clés et plongez dans l'analyse des données spécifiques à chaque région."
                ),
                font=("Arial", 14),
                wraplength=400,  # Définit la largeur où le texte est replié
                justify="left",  # Alignement à gauche
                anchor="w",  # Place le texte à gauche
                bg="white"
            ).pack(anchor="w", pady=10)

        # Bouton
        CTkButton(
            text_frame,
            text="Carte graphique",
            command=self.show_map_callback,
            fg_color="#8B0000",  # Couleur rouge
            hover_color="#C0392B",  # Rouge foncé au survol
            text_color="white",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=10)

        # Image à droite (agrandie)
        image_frame = tk.Frame(content_frame, bg="white")
        image_frame.pack(side="right", fill="y", expand=True)

        # Agrandir l'image
        image = Image.open("resources/images/c1.png")  # Chemin de l'image
        image = image.resize((600, 300), Image.Resampling.LANCZOS)  # Agrandir ici
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(image_frame, image=photo, bg="white")
        image_label.image = photo  # Garder une référence pour éviter le garbage collection
        image_label.pack()
