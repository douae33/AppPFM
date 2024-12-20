import tkinter as tk
from home_page import HomePage
from map_page import MapPage
from navbar import Navbar
from data_handler import DataHandler
from tkinter import messagebox
from visualisation import VisualizationApp  # Importation de la classe VisualisationApp

def main():
    root = tk.Tk()
    root.title("Analyse des Facteurs de Risque")
    root.geometry("1000x700")

    data_handler = DataHandler()
    navbar = Navbar(root)



    # Fonction pour revenir à la carte
    def go_back_to_map():
        navbar.render([("Accueil", show_home), ("Carte", show_map), ("Étude comparative", show_visualization)])
        map_page.show()

    def show_home():
        navbar.render([("Carte", show_map), ("Étude comparative", show_visualization)])
        home_page.show()

    def show_map():
        navbar.render([("Accueil", show_home), ("Étude comparative", show_visualization)])
        map_page.show()

  


    def show_visualization():
        # Appel de la page de visualisation

        visualisation_obj = VisualizationApp(root, data_handler, go_back_to_map)
        visualisation_obj.show_factor_buttons()

    def show_region_data_callback(region_name):
        region_data = data_handler.get_statistics_for_region(region_name)
        if not region_data:
            messagebox.showinfo("Région", f"Aucune donnée disponible pour {region_name}.")
        else:
            messagebox.showinfo("Données Région", f"Statistiques pour {region_name}: {region_data}")
    
    # Initialisation des pages
    home_page = HomePage(root, show_map)
    map_page = MapPage(root, data_handler, show_region_data_callback)

    # Afficher la barre de navigation et la page d'accueil par défaut
    navbar.render([("Accueil", show_home), ("Carte", show_map), ("Étude comparative",show_visualization)])

    show_home()

    root.protocol("WM_DELETE_WINDOW", root.quit)

    try:
        root.mainloop()
    except Exception as e:
        print("Erreur lors de l'exécution :", e)

if __name__ == "__main__":
    main()
