import pandas as pd

class DataHandler:
    def __init__(self, file_path="resources/data/data.csv"):
        """
        Initialise le gestionnaire de données en chargeant les données depuis un fichier CSV.
        """
        try:
            self.data = pd.read_csv(file_path)
            print("Fichier chargé avec succès !")
            print("Colonnes disponibles :", self.data.columns.tolist())
        except FileNotFoundError:
            print("Erreur : Le fichier spécifié est introuvable.")
            self.data = None
        except Exception as e:
            print(f"Erreur lors du chargement du fichier : {e}")
            self.data = None

    def get_statistics_for_region(self, region):
        """
        Retourne les statistiques pour une région donnée.
        """
        if self.data is None:
            print("Erreur : Aucune donnée chargée.")
            return None
        
        # Normalisation pour éviter les erreurs de casse
        region_data = self.data[self.data['Region'].str.lower() == region.lower()]
        
        if region_data.empty:
            print(f"Aucune donnée trouvée pour la région : {region}")
            return None
        return region_data

    def plot_risk_factors_for_region(self, region):
        """
        Affiche un graphique des facteurs de risque pour une région donnée.
        """
        import matplotlib.pyplot as plt
        
        # Liste des facteurs de risque
        risk_factors = [
            "Tabagisme", "Facteurs_genetiques", "Parite", "HPV", "Obesite", "Diabete",
            "HTA", "Statut_Menopause", "Absence_frottis", "Debut_precoce", "IST",
            "Immunodepression", "Contraceptifs_oraux",
        ]
        
        # Obtenir les données pour la région
        region_data = self.get_statistics_for_region(region)
        if region_data is None:
            print("Impossible de générer un graphique : Aucune donnée disponible.")
            return

        # Calculer la moyenne pour chaque facteur de risque
        risk_means = region_data[risk_factors].mean()
        plt.figure(figsize=(10, 6))
        risk_means.plot(kind="bar", color="skyblue", edgecolor="black")

        # Ajouter des titres et des étiquettes
        plt.title(f"Facteurs de Risque Moyens - Région {region}", fontsize=14)
        plt.xlabel("Facteurs de Risque", fontsize=12)
        plt.ylabel("Moyenne", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()
    #méthode pour fichier anlytic
    def get_unique_regions(self):
        """
        Retourne une liste des régions uniques dans les données.
        """
        if self.data is None:
            print("Erreur : Aucune donnée chargée.")
            return []
        return self.data['Region'].dropna().unique().tolist()
