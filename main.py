import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from models.deck_manager import DeckManager
from ui.style import apply_stylesheet


def main():
    """
    Point d'entrée principal de l'application FlashMaster.
    Initialise l'application, applique le style, crée la fenêtre principale
    et lance la boucle événementielle.
    """
    # Création de l'application Qt
    app = QApplication(sys.argv)
    app.setApplicationName("FlashMaster")

    # Application du thème personnalisé
    apply_stylesheet(app)

    # Chargement du gestionnaire de paquets de cartes
    deck_manager = DeckManager()

    # Création et affichage de la fenêtre principale
    window = MainWindow(deck_manager)
    window.show()

    # Lancement de la boucle événementielle Qt
    sys.exit(app.exec_())

# Vérifie si le script est exécuté directement (et non importé)
if __name__ == "__main__":
    main()