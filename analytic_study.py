import tkinter as tk
from customtkinter import CTkButton, CTkLabel, CTkFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class AnalyticStudyPage:
    def __init__(self, root, data_handler, go_back_to_map_callback):
        self.root = root
        self.data_handler = data_handler
        self.go_back_to_map_callback = go_back_to_map_callback

    def show(self):
        # Nettoyer les graphiques matplotlib
        plt.close('all')

        # Réinitialiser les widgets de la fenêtre principale
        for widget in self.root.winfo_children():
            widget.destroy()

        # Conteneur principal
        main_frame = CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True)

        # Titre
        title_frame = CTkFrame(main_frame, fg_color="#B0E0E6")
        title_frame.pack(fill="x", side="top")

        title_label = CTkLabel(
            title_frame,
            text="Étude Analytique et Dépendances",
            font=("Arial", 18, "bold"),
            text_color="black"
        )
        title_label.pack(pady=10)

        # Bouton pour revenir à la carte
        back_button = CTkButton(
            title_frame, text="Revenir à la Carte", command=self.go_back_to_map_callback,
            fg_color="darkred", hover_color="#FFA07A", text_color="white",
            corner_radius=10, font=("Arial", 12, "bold"), width=150
        )
        back_button.pack(side="right", padx=10)

        # Conteneur pour les graphiques
        graph_frame = tk.Frame(main_frame, bg="white")
        graph_frame.pack(expand=True, fill="both")

        # Charger et afficher les heatmaps des régions dans une disposition 2x2
        regions = self.data_handler.get_unique_regions()
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]  # Disposition en grille 2x2
        for i, region in enumerate(regions[:4]):  # Limité à 4 régions pour 2x2
            self._display_region_heatmap(graph_frame, region, positions[i])

    def _display_region_heatmap(self, parent_frame, region_name, position):
        """
        Affiche la heatmap pour une région donnée dans une disposition en grille.
        
        Arguments :
        - parent_frame : le conteneur Tkinter pour afficher les graphiques.
        - region_name : le nom de la région à analyser.
        - position : tuple (row, col) indiquant la position dans la grille.
        """
        region_data = self.data_handler.get_statistics_for_region(region_name)

        if region_data is None or region_data.empty:
            print(f"Pas de données disponibles pour la région : {region_name}")
            return

        # Calcul des facteurs de risque
        risk_factors = [
            col for col in region_data.columns
            if col not in ["ID_Patient", "Region", "Age_exact"]
        ]
        correlation_matrix = region_data[risk_factors].corr()

        # Créer la heatmap
        fig, ax = plt.subplots(figsize=(5, 4))  # Taille ajustée pour chaque graphique
        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            cbar=True,
            ax=ax,
            annot_kws={"size": 7}  # Réduction de la taille des annotations
        )
        ax.set_title(f"Heatmap des corrélations - {region_name}", fontsize=10, pad=10)
        plt.xticks(rotation=45, fontsize=7, ha="right")  # Rotation et réduction de taille
        plt.yticks(fontsize=7)
        plt.tight_layout(pad=2)  # Ajout de marges pour éviter les chevauchements

        # Intégrer la heatmap dans la grille Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=position[0], column=position[1], padx=10, pady=10, sticky="nsew")

        # Configurer les colonnes et lignes pour s'étendre uniformément
        parent_frame.grid_rowconfigure(position[0], weight=1)
        parent_frame.grid_columnconfigure(position[1], weight=1)





    def _show_error_message(self, message):
        tk.messagebox.showerror("Erreur", message)


