from tkinter import messagebox
from tkintermapview import TkinterMapView
from customtkinter import CTkFrame
import pandas as pd
from dashboard_page import DashboardPage
from customtkinter import CTkLabel
from navbar import Navbar
from visualisation import VisualizationApp  # Importation de la classe VisualisationApp





class MapPage:
    def __init__(self, root, data_handler,show_region_data_callback):
        self.root = root
        self.data_handler = data_handler
        self.show_region_data_callback = show_region_data_callback


    def show(self):
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Navbar
        navbar = Navbar(self.root)
        navbar.render([("Accueil", self.show_home), ("Étude comparative", self.show_visualization),("Étude analytique", self.show_analytic_study)])
        
        # Carte
        map_widget = TkinterMapView(self.root, width=800, height=600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)
        map_widget.set_position(31.63, -8.00)
        map_widget.set_zoom(6)
    
        regions = {"Dakhla": (23.68, -15.94), "Marrakech": (31.63, -8.00), "Kenitra": (34.26, -6.58), "Meknes": (33.89, -5.55)}
        for region, coords in regions.items():
            map_widget.set_marker(coords[0], coords[1], text=region, command=lambda m: self.on_region_click(m))


    def show_home(self):
        from home_page import HomePage
        home_page = HomePage(self.root, self.show)
        home_page.show()

   

    def show_visualization(self):
        # Vérifier si la méthode go_back_to_map_callback est définie
        def go_back_to_map_callback():
            self.show()  # Retour à la carte
         # Appel de la page de visualisation
        visualisation_obj = VisualizationApp(self.root, self.data_handler,go_back_to_map_callback)
        visualisation_obj.show()  # Appel à la méthode correcte pour afficher la page de visualisation



    def on_region_click(self, marker_object):
        region_name = marker_object.text
        region_data = self.data_handler.get_statistics_for_region(region_name)
        if region_data is None or region_data.empty:
            messagebox.showinfo("Région", f"Aucune donnée pour {region_name}.")
        else:
            dashboard = DashboardPage(self.root, region_name, region_data, self.show)
            dashboard.show_dashboard()
    
    #bouton étude analytique ; Cette fonction importe et affiche une page ou une logique d'analyse à partir d'un fichier analytic_study.py

    def show_analytic_study(self):
        from analytic_study import AnalyticStudyPage

        analytic_study =AnalyticStudyPage(self.root, self.data_handler, self.show)
        analytic_study.show()
