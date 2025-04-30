from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QProgressBar, QSizePolicy, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from ui.style import get_style
from ui.style import ACCENT_COLOR, SECONDARY_COLOR, CARD_COLOR, BORDER_RADIUS
import time

class StudyView(QWidget):
    def __init__(self, parent, deck_manager, deck_id):
        """
        Constructeur pour initialiser la vue d'étude d'un deck.

        :param parent: Parent widget (la fenêtre principale ou autre widget parent)
        :param deck_manager: Objet qui gère les decks et les cartes
        :param deck_id: ID du deck à étudier
        """
        super().__init__(parent)
        self.parent = parent
        self.deck_manager = deck_manager
        self.deck_id = deck_id
        self.deck = deck_manager.get_deck(deck_id)  # Récupérer les informations du deck
        self.cards = deck_manager.get_study_cards(deck_id)  # Récupérer les cartes à étudier
        self.current_card_index = 0  # Index de la carte actuelle
        self.show_answer = False  # Indicateur pour savoir si la réponse doit être montrée
        self.study_start_time = time.time()  # Temps de début de l'étude
        self.correct_answers = 0  # Nombre de réponses correctes
        self.total_answers = 0  # Nombre total de réponses
        self.init_ui()  # Initialisation de l'interface utilisateur

    def init_ui(self):
        """Initialise l'interface utilisateur de la vue d'étude avec style amélioré."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Marges autour du layout
        layout.setSpacing(15)  # Espacement entre les éléments

        # En-tête avec bouton de retour et informations sur l'étude
        header_frame = QFrame()
        header_frame.setObjectName("card_frame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 15, 15, 15)

        back_btn = QPushButton("◀ Retour au deck")
        back_btn.clicked.connect(self.return_to_deck)  # Fonction pour revenir à la vue du deck
        header_layout.addWidget(back_btn)

        title_label = QLabel(f"Étude: {self.deck['name']}")  # Titre de l'étude (nom du deck)
        title_label.setStyleSheet(get_style("header_label"))
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label, 1)

        # Compteur de cartes
        self.counter_label = QLabel()
        self.counter_label.setStyleSheet(get_style("info_label"))
        self.update_counter()  # Mise à jour du compteur
        header_layout.addWidget(self.counter_label)

        layout.addWidget(header_frame)

        # Panel d'information sur la session
        info_frame = QFrame()
        info_frame.setObjectName("card_frame")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)

        progress_label = QLabel("Progression:")  # Titre pour la barre de progression
        progress_label.setStyleSheet(get_style("subheader_label"))
        info_layout.addWidget(progress_label)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self.cards))
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v/%m cartes")
        info_layout.addWidget(self.progress_bar)

        layout.addWidget(info_frame)

        # Conteneur pour la carte avec style amélioré
        self.card_container = QFrame()
        self.card_container.setObjectName("card_frame")
        self.card_container.setMinimumHeight(300)
        self.card_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        card_layout = QVBoxLayout(self.card_container)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setAlignment(Qt.AlignCenter)

        # Contenu de la carte
        self.card_content = QLabel()
        self.card_content.setAlignment(Qt.AlignCenter)
        self.card_content.setWordWrap(True)
        self.card_content.setTextInteractionFlags(Qt.TextSelectableByMouse)
        card_layout.addWidget(self.card_content, 1)

        layout.addWidget(self.card_container, 1)

        # Bouton pour afficher la réponse
        self.show_answer_btn = QPushButton("Afficher la réponse")
        self.show_answer_btn.setStyleSheet(get_style("action_button"))
        self.show_answer_btn.setMinimumHeight(50)
        self.show_answer_btn.clicked.connect(self.toggle_answer)
        layout.addWidget(self.show_answer_btn)

        # Boutons de réponse (correct/incorrect)
        self.response_buttons = QWidget()
        response_layout = QHBoxLayout(self.response_buttons)
        response_layout.setSpacing(15)

        self.correct_btn = QPushButton("Correct ✓")
        self.correct_btn.setStyleSheet(get_style("correct_button"))
        self.correct_btn.setMinimumHeight(50)
        self.correct_btn.clicked.connect(lambda: self.process_answer(True))
        response_layout.addWidget(self.correct_btn)

        self.incorrect_btn = QPushButton("Incorrect ✗")
        self.incorrect_btn.setStyleSheet(get_style("incorrect_button"))
        self.incorrect_btn.setMinimumHeight(50)
        self.incorrect_btn.clicked.connect(lambda: self.process_answer(False))
        response_layout.addWidget(self.incorrect_btn)

        self.response_buttons.setVisible(False)  # Initialement, les boutons de réponse sont cachés
        layout.addWidget(self.response_buttons)

        # Charger la première carte
        if self.cards:
            self.load_current_card()
        else:
            self.show_no_cards_message()

    def update_counter(self):
        """Met à jour le compteur de cartes."""
        current = self.current_card_index + 1
        total = len(self.cards)
        self.counter_label.setText(f"{current}/{total}")

    def load_current_card(self):
        """Charge la carte actuelle avec style amélioré."""
        if not self.cards or self.current_card_index >= len(self.cards):
            self.show_complete_message()
            return

        card = self.cards[self.current_card_index]
        self.show_answer = False

        # Affichage de la question (face avant de la carte)
        self.card_content.setStyleSheet(get_style("card_front"))
        self.card_content.setText(card["front"])

        # Mise à jour du texte du bouton
        self.show_answer_btn.setText("Afficher la réponse")
        self.response_buttons.setVisible(False)

        # Animer la carte (effet de transition simple)
        self.card_container.setStyleSheet(get_style("flashcard"))

    def toggle_answer(self):
        """Affiche ou cache la réponse de la carte actuelle."""
        if not self.cards or self.current_card_index >= len(self.cards):
            return

        card = self.cards[self.current_card_index]

        if self.show_answer:
            # Affiche la question (face avant)
            self.card_content.setStyleSheet(get_style("card_front"))
            self.card_content.setText(card["front"])
            self.show_answer_btn.setText("Afficher la réponse")
            self.response_buttons.setVisible(False)
        else:
            # Affiche la réponse (face arrière)
            self.card_content.setStyleSheet(get_style("card_back"))
            self.card_content.setText(card["back"])
            self.show_answer_btn.setText("Cacher la réponse")
            self.response_buttons.setVisible(True)

        self.show_answer = not self.show_answer

    def process_answer(self, is_correct):
        """Traite la réponse de l'utilisateur et passe à la carte suivante."""
        if not self.cards or self.current_card_index >= len(self.cards):
            return

        card = self.cards[self.current_card_index]

        # Mise à jour des statistiques de la carte
        self.deck_manager.update_card_result(self.deck_id, card["id"], is_correct)

        # Mise à jour des statistiques de la session
        self.total_answers += 1
        if is_correct:
            self.correct_answers += 1

        # Passer à la carte suivante
        self.current_card_index += 1
        self.progress_bar.setValue(self.current_card_index)

        if self.current_card_index < len(self.cards):
            self.update_counter()
            self.load_current_card()
        else:
            self.show_complete_message()

    def show_no_cards_message(self):
        """Affiche un message lorsqu'il n'y a pas de cartes à étudier."""
        self.card_content.setText("Ce deck ne contient aucune carte à étudier !")
        self.show_answer_btn.setEnabled(False)

    def show_complete_message(self):
        """Affiche un message de fin d'étude stylisé."""
        elapsed_time = time.time() - self.study_start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        success_rate = 0
        if self.total_answers > 0:
            success_rate = (self.correct_answers / self.total_answers) * 100

        message = f"""
        <div style='text-align: center;'>
            <h1 style='color: {ACCENT_COLOR}; font-size: 24px;'>Félicitations !</h1>
            <p style='font-size: 16px;'>Vous avez terminé votre session d'étude.</p>
            <br>
            <table style='margin: auto; text-align: left;'>
                <tr>
                    <td style='padding: 8px; font-weight: bold;'>Temps total:</td>
                    <td style='padding: 8px;'>{minutes}m {seconds}s</td>
                </tr>
                <tr>
                    <td style='padding: 8px; font-weight: bold;'>Cartes étudiées:</td>
                    <td style='padding: 8px;'>{len(self.cards)}</td>
                </tr>
                <tr>
                    <td style='padding: 8px; font-weight: bold;'>Réponses correctes:</td>
                    <td style='padding: 8px;'>{self.correct_answers}/{self.total_answers}</td>
                </tr>
                <tr>
                    <td style='padding: 8px; font-weight: bold;'>Taux de réussite:</td>
                    <td style='padding: 8px;'>{success_rate:.1f}%</td>
                </tr>
            </table>
            <br>
            <p style='font-style: italic; color: {SECONDARY_COLOR};'>
                Continuez votre progression en étudiant régulièrement !
            </p>
        </div>
        """

        self.card_content.setText(message)
        self.show_answer_btn.setEnabled(False)
        self.response_buttons.setVisible(False)

        # Application du style pour le conteneur de fin de session
        self.card_container.setStyleSheet(f"""
            background-color: {CARD_COLOR};
            border: 2px solid {ACCENT_COLOR};
            border-radius: {BORDER_RADIUS * 2}px;
            padding: 20px;
        """)

        # Affichage du message de fin de session
        QMessageBox.information(self, "Session terminée",
                                f"Session terminée avec un taux de réussite de {success_rate:.1f}%")

    def return_to_deck(self):
        """Retourne à la vue du deck."""
        # Recherche et mise à jour de la vue du deck dans le panneau principal
        for i in range(self.parent.right_panel.count()):
            widget = self.parent.right_panel.widget(i)
            if hasattr(widget, 'deck_id') and widget.deck_id == self.deck_id:
                self.parent.right_panel.setCurrentWidget(widget)
                widget.refresh_cards()  # Rafraîchir la vue des cartes
                QTimer.singleShot(100, lambda: self.deleteLater())  # Supprimer cette vue après un court délai
                break