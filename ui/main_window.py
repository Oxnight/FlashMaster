from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QListWidget, QStackedWidget,
                             QLineEdit, QDialog, QFrame, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Importation des vues internes
from ui.deck_view import DeckView
from ui.study_view import StudyView
from ui.deck_editor import DeckEditorDialog
from ui.style import get_style

# Définition de la fenêtre principale de l'application
class MainWindow(QMainWindow):
    def __init__(self, deck_manager):
        super().__init__()
        self.deck_manager = deck_manager  # Gestionnaire de decks (base de données)
        self.current_deck_id = None       # Identifiant du deck actuellement sélectionné
        self.init_ui()                    # Initialisation de l'interface graphique

    def init_ui(self):
        """Initialise l'interface utilisateur principale."""
        self.setWindowTitle("FlashMaster")        # Titre de la fenêtre
        self.setMinimumSize(1100, 750)            # Taille minimale de la fenêtre

        # Création du widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Mise en place du layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Utilisation d'un splitter pour séparer la zone gauche et droite
        splitter = QSplitter(Qt.Horizontal)

        # ------------ PANNEAU GAUCHE : Liste des decks ------------

        # Création du cadre de gauche
        left_panel = QFrame()
        left_panel.setObjectName("card_frame")
        left_panel.setMinimumWidth(280)
        left_panel.setMaximumWidth(350)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(15)

        # Titre de la section
        deck_header = QLabel("Mes Decks")
        deck_header.setStyleSheet(get_style("header_label"))
        left_layout.addWidget(deck_header)

        # Barre de recherche
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Rechercher un deck...")
        self.search_edit.textChanged.connect(self.filter_decks)  # Filtrage dynamique
        search_layout.addWidget(self.search_edit)
        left_layout.addLayout(search_layout)

        # Bouton pour créer un nouveau deck
        deck_actions = QWidget()
        deck_actions_layout = QHBoxLayout(deck_actions)
        deck_actions_layout.setContentsMargins(0, 0, 0, 0)
        self.add_deck_btn = QPushButton("+ Nouveau Deck")
        self.add_deck_btn.setStyleSheet(get_style("action_button"))
        self.add_deck_btn.clicked.connect(self.add_deck)
        deck_actions_layout.addWidget(self.add_deck_btn)
        left_layout.addWidget(deck_actions)

        # Ligne de séparation esthétique
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(get_style("separator"))
        left_layout.addWidget(separator)

        # Liste des decks disponibles
        self.deck_list = QListWidget()
        self.deck_list.itemClicked.connect(self.on_deck_selected)  # Sélection d'un deck
        self.deck_list.setAlternatingRowColors(True)
        left_layout.addWidget(self.deck_list, 1)  # Occupe l'espace restant

        # ------------ PANNEAU DROIT : Contenu principal ------------

        # Stack de widgets pour alterner entre vue d'accueil, vue deck, vue étude
        self.right_panel = QStackedWidget()

        # Création de la page d'accueil par défaut
        home_page = QFrame()
        home_page.setObjectName("card_frame")
        home_layout = QVBoxLayout(home_page)
        home_layout.setContentsMargins(30, 30, 30, 30)
        home_layout.setSpacing(20)

        # Logo ou nom de l'app
        logo_label = QLabel("FlashMaster")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_font = QFont("Arial", 32, QFont.Bold)
        logo_label.setFont(logo_font)
        logo_label.setStyleSheet("color: #3498db;")
        home_layout.addWidget(logo_label)

        # Slogan
        welcome_label = QLabel("Améliorez votre mémoire avec des flashcards")
        welcome_label.setStyleSheet(get_style("header_label"))
        welcome_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(welcome_label)

        # Instructions explicatives
        instructions_label = QLabel(
            "FlashMaster vous aide à apprendre efficacement grâce à la répétition espacée.\n\n"
            "• Créez des decks pour organiser vos sujets\n"
            "• Ajoutez des cartes avec questions et réponses\n"
            "• Étudiez régulièrement pour améliorer votre mémorisation\n\n"
            "Sélectionnez un deck existant ou créez-en un nouveau pour commencer."
        )
        instructions_label.setAlignment(Qt.AlignCenter)
        instructions_label.setWordWrap(True)
        home_layout.addWidget(instructions_label)

        # Bouton de création de deck depuis l'accueil
        start_btn = QPushButton("+ Créer mon premier deck")
        start_btn.setMinimumHeight(50)
        start_btn.setStyleSheet(get_style("action_button"))
        start_btn.clicked.connect(self.add_deck)
        home_layout.addWidget(start_btn)

        # Étirement final pour équilibrer la mise en page
        home_layout.addStretch()
        self.right_panel.addWidget(home_page)

        # Ajout des panneaux gauche et droit dans le splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(self.right_panel)
        splitter.setStretchFactor(0, 1)  # Panneau gauche : 1 part
        splitter.setStretchFactor(1, 3)  # Panneau droit : 3 parts

        # Ajout du splitter dans le layout principal
        main_layout.addWidget(splitter)

        # Chargement initial des decks
        self.refresh_deck_list()

    def refresh_deck_list(self):
        """Rafraîchit la liste des decks avec un formatage amélioré."""
        self.deck_list.clear()
        decks = self.deck_manager.get_decks()

        for deck in decks:
            deck_name = deck["name"]
            card_count = self.deck_manager.get_card_count(deck["id"])
            stats = self.deck_manager.get_deck_stats(deck["id"])

            # Par défaut, nom + nombre de cartes
            item_widget = QLabel(f"<b>{deck_name}</b><br/>"
                                 f"<span style='color: #7f8c8d;'>{card_count} cartes")

            # Ajout du taux de réussite si dispo
            if stats and stats["correct_answers"] + stats["incorrect_answers"] > 0:
                success_rate = stats["success_rate"]
                item_widget.setText(f"<b>{deck_name}</b><br/>"
                                    f"<span style='color: #7f8c8d;'>{card_count} cartes • "
                                    f"{success_rate:.1f}% de réussite</span>")

            # Ajout à la liste graphique
            list_item = deck_name
            self.deck_list.addItem(list_item)
            item = self.deck_list.item(self.deck_list.count() - 1)
            item.setData(Qt.UserRole, deck["id"])  # Stocke l'ID du deck

    def filter_decks(self, text):
        """Filtre la liste des decks selon le texte de recherche."""
        text = text.lower()
        for i in range(self.deck_list.count()):
            item = self.deck_list.item(i)
            if text in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def add_deck(self):
        """Ajoute un nouveau deck avec interface améliorée."""
        dialog = DeckEditorDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.name_edit.text()
            description = dialog.description_edit.toPlainText()

            if name:
                deck_id = self.deck_manager.create_deck(name, description)
                self.refresh_deck_list()

                # Sélection du deck fraîchement créé
                for i in range(self.deck_list.count()):
                    item = self.deck_list.item(i)
                    if item.data(Qt.UserRole) == deck_id:
                        self.deck_list.setCurrentItem(item)
                        self.on_deck_selected(item)
                        break

    def on_deck_selected(self, item):
        """Gère la sélection d'un deck dans la liste avec une transition fluide."""
        deck_id = item.data(Qt.UserRole)
        self.current_deck_id = deck_id
        deck = self.deck_manager.get_deck(deck_id)

        # Vérifie si la vue du deck existe déjà
        deck_view = None
        for i in range(self.right_panel.count()):
            widget = self.right_panel.widget(i)
            if isinstance(widget, DeckView) and widget.deck_id == deck_id:
                deck_view = widget
                self.right_panel.setCurrentWidget(deck_view)
                break

        # Sinon, crée la vue et l'ajoute
        if not deck_view:
            deck_view = DeckView(self, self.deck_manager, deck)
            self.right_panel.addWidget(deck_view)
            self.right_panel.setCurrentWidget(deck_view)

    def show_study_view(self, deck_id):
        """Affiche la vue d'étude pour un deck avec transition améliorée."""
        study_view = None
        for i in range(self.right_panel.count()):
            widget = self.right_panel.widget(i)
            if isinstance(widget, StudyView) and widget.deck_id == deck_id:
                study_view = widget
                self.right_panel.setCurrentWidget(study_view)
                break

        # Si elle n'existe pas, on la crée
        if not study_view:
            study_view = StudyView(self, self.deck_manager, deck_id)
            self.right_panel.addWidget(study_view)
            self.right_panel.setCurrentWidget(study_view)