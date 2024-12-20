import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from customtkinter import CTkButton, CTkFrame, CTkLabel

class DashboardPage:
    def __init__(self, root, region_name, region_data, back_callback):
        self.root = root
        self.region_name = region_name
        self.region_data = region_data
        self.back_callback = back_callback
        self.dashboard_frame = None

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Cadre principal avec couleur de fond similaire au navbar
        self.dashboard_frame = CTkFrame(self.root, fg_color="white")
        self.dashboard_frame.pack(fill="both", expand=True)

        # Titre stylisé avec fond
        title_frame = CTkFrame(self.dashboard_frame, fg_color="#B0E0E6", corner_radius=0)
        title_frame.pack(fill="x", side="top", pady=10)

        title_label = CTkLabel(
            title_frame,
            text=f"Analyse des tendances et relations - {self.region_name}",
            font=("Arial", 16, "bold"),
            text_color="black"
        )
        title_label.pack(pady=5)

        # Bouton stylisé pour revenir à la carte
        back_button = CTkButton(
            title_frame, text="Revenir à la carte", command=self.back_callback,
            fg_color="#8B0000", hover_color="#FFA07A", text_color="white",
            corner_radius=10, font=("Arial", 12, "bold"), width=150
        )
        back_button.pack(side="right", padx=10)

        # Préparer les graphiques
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # 1. Répartition des facteurs de risque
        factors = self.region_data.drop(columns=["ID_Patient", "Region", "Age_exact"], errors="ignore").sum()
        factors.plot(kind='bar', ax=axes[0, 0], color='skyblue')
        axes[0, 0].set_title("Répartition des facteurs de risque", fontsize=12)
        axes[0, 0].set_ylabel("Nombre de cas", fontsize=10)
        axes[0, 0].tick_params(axis='x', rotation=30, labelsize=9)  # Rotation plus douce
        axes[0, 0].set_xticks(range(len(factors.index)))  # Assurez-vous que les ticks sont bien placés
        axes[0, 0].set_xticklabels(factors.index, ha='right')  # Alignement horizontal à droite

 


        # 2. Répartition des âges
        age_bins = [0, 20, 40, 60, 80, 100]
        age_labels = ["0-20", "21-40", "41-60", "61-80", "81-100"]
        region_data_copy = self.region_data.copy()
        region_data_copy["Age_bins"] = pd.cut(region_data_copy["Age_exact"], bins=age_bins, labels=age_labels)
        age_distribution = region_data_copy["Age_bins"].value_counts().sort_index()
        age_distribution.plot(kind='bar', ax=axes[0, 1], color='orange')
        axes[0, 1].set_title("Répartition des âges", fontsize=12)
        axes[0, 1].set_xlabel("Tranches d'âge", fontsize=10)
        axes[0, 1].set_ylabel("Nombre de patients", fontsize=10)
        axes[0, 1].tick_params(axis='x', rotation=0, labelsize=8)

        # 3. Répartition des facteurs par tranche d'âge (correctement)
        factor_columns = [col for col in self.region_data.columns if col not in ["ID_Patient", "Region", "Age_exact"]]
        age_factors_count = region_data_copy.groupby("Age_bins", observed=True)[factor_columns].apply(lambda x: (x > 0).sum())
        age_factors_count.T.plot(kind="bar", stacked=True, ax=axes[1, 0], colormap="tab20")
        axes[1, 0].set_title("Répartition des facteurs par tranche d'âge", fontsize=12)
        axes[1, 0].set_xlabel("Facteurs de risque", fontsize=10)
        axes[1, 0].set_ylabel("Nombre de cas", fontsize=10)
        axes[1, 0].tick_params(axis='x', rotation=30, labelsize=9)
        axes[1, 0].set_xticks(range(len(age_factors_count.columns)))  # Placement des ticks
        axes[1, 0].set_xticklabels(age_factors_count.columns, ha='right')  # Alignement horizontal à droite
        
        # 4. Top 5 des facteurs dominants
        top_factors = factors.nlargest(5)
        top_factors.plot(kind="pie", ax=axes[1, 1], autopct='%1.1f%%', textprops={'fontsize': 8})
        axes[1, 1].set_title("Top 5 des facteurs dominants", fontsize=12)
        axes[1, 1].set_ylabel("")

        # Ajustements de mise en page
        fig.tight_layout()
        plt.subplots_adjust(hspace=0.5, wspace=0.3)

        # Afficher les graphiques
        canvas = FigureCanvasTkAgg(fig, master=self.dashboard_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
