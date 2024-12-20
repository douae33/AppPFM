import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from customtkinter import CTkButton, CTkFrame, CTkLabel


class VisualizationApp:
    def __init__(self, root, data_handler, go_back_to_map_callback):
        self.root = root
        self.data_handler = data_handler
        self.go_back_to_map_callback = go_back_to_map_callback

    def show(self):
        # Fermer tous les graphiques Matplotlib pour éviter les conflits
        plt.close('all')

        # Nettoyer les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()

        # Cadre principal
        main_frame = CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True)

        # Titre stylisé
        title_frame = CTkFrame(main_frame, fg_color="#B0E0E6", corner_radius=0)
        title_frame.pack(fill="x", side="top", pady=10)

        title_label = CTkLabel(
            title_frame,
            text="Visualisation des Facteurs de Risque",
            font=("Arial", 16, "bold"),
            text_color="black"
        )
        title_label.pack(pady=5)

        # Bouton retour stylisé
        back_button = CTkButton(
            title_frame, text="Revenir à la Carte", command=self.go_back_to_map_callback,
            fg_color="#8B0000", hover_color="#FFA07A", text_color="white",
            corner_radius=10, font=("Arial", 12, "bold"), width=150
        )
        back_button.pack(side="right", padx=10)

        # Conteneur pour les boutons de facteurs de risque
        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        risk_factors = [
            "Tabagisme", "HPV", "Parite", "Facteurs_genetiques", "Obesite", "Diabete",
            "HTA", "Statut_Menopause", "Absence_frottis", "Debut_precoce", "IST",
            "Immunodepression", "Contraceptifs_oraux"
        ]

        # Création des boutons stylisés
        for index, factor in enumerate(risk_factors):
            button = CTkButton(
                button_frame, text=factor, command=lambda f=factor: self.show_comparison(f),
                fg_color="#8B0000", hover_color="#FFA07A", text_color="white",
                corner_radius=10, font=("Arial", 12, "bold"), width=150, height=40
            )
            button.grid(row=index // 6, column=index % 6, padx=10, pady=10)

    def show_comparison(self, factor):
        try:
            # Fermer tous les graphiques Matplotlib existants
            plt.close('all')

            if self.data_handler.data is None:
                messagebox.showerror("Erreur", "Les données ne sont pas chargées.")
                return

            all_data = self.data_handler.data
            if "Region" not in all_data.columns or factor not in all_data.columns:
                messagebox.showerror("Erreur", f"Les colonnes 'Region' ou '{factor}' sont manquantes.")
                return

            # Filtrer les données et calculer les moyennes
            filtered_data = all_data[["Region", factor]]
            pivot_data = filtered_data.pivot_table(index="Region", values=factor, aggfunc="mean")

            # Générer le graphique
            pivot_data.plot(kind="bar", figsize=(10, 6), color='skyblue', edgecolor='black')
            plt.title(f"Comparaison du Facteur de Risque: {factor}")
            plt.xlabel("Région")
            plt.ylabel("Valeur Moyenne")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Afficher le graphique
            plt.show()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la comparaison: {e}")
