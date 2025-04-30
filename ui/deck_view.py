from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QMenu,
                             QAction, QMessageBox, QDialog, QHeaderView, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

# Importation des boîtes de dialogue personnalisées pour les cartes et les decks
from ui.card_editor import CardEditorDialog
from ui.deck_editor import DeckEditorDialog

# Pour gérer les dates de dernière étude
from datetime import datetime

# Importation du système de styles centralisé
from ui.style import get_style


class DeckView(QWidget):
    def __init__(self, parent, deck_manager, deck):
        """
        Constructeur de la vue de deck.

        :param parent: le widget parent (probablement la fenêtre principale)
        :param deck_manager: objet responsable de la gestion des données (decks et cartes)
        :param deck: dictionnaire contenant les informations du deck affiché
        """
        super().__init__(parent)
        self.parent = parent
        self.deck_manager = deck_manager
        self.deck = deck
        self.deck_id = deck["id"]
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface utilisateur de la vue du deck."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # -------- En-tête avec titre, description, statistiques et actions --------
        header_frame = QFrame()
        header_frame.setObjectName("card_frame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 15, 15, 15)

        # Titre et description du deck
        title_desc_layout = QVBoxLayout()
        self.title_label = QLabel(self.deck["name"])
        self.title_label.setStyleSheet(get_style("header_label"))
        title_desc_layout.addWidget(self.title_label)

        if self.deck["description"]:
            description_label = QLabel(self.deck["description"])
            description_label.setWordWrap(True)
            description_label.setStyleSheet(get_style("info_label"))
            title_desc_layout.addWidget(description_label)

        header_layout.addLayout(title_desc_layout)

        # Statistiques et actions (boutons)
        info_layout = QHBoxLayout()
        info_layout.setSpacing(20)

        # Statistiques : nombre de cartes, taux de réussite, date dernière étude
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(15)

        card_count = self.deck_manager.get_card_count(self.deck_id)
        card_count_label = QLabel(f"{card_count} cartes")
        card_count_label.setStyleSheet(get_style("info_label"))
        stats_layout.addWidget(card_count_label)

        stats = self.deck_manager.get_deck_stats(self.deck_id)
        if stats and stats["correct_answers"] + stats["incorrect_answers"] > 0:
            success_rate = stats["success_rate"]
            stats_label = QLabel(f"{success_rate:.1f}% de réussite")
            stats_label.setStyleSheet(get_style("info_label"))
            stats_layout.addWidget(stats_label)

        if self.deck["last_studied"]:
            last_studied = datetime.fromisoformat(self.deck["last_studied"]).strftime("%d/%m/%Y %H:%M")
            last_studied_label = QLabel(f"Dernière étude: {last_studied}")
            last_studied_label.setStyleSheet(get_style("info_label"))
            stats_layout.addWidget(last_studied_label)

        info_layout.addWidget(stats_widget)
        info_layout.addStretch()

        # Boutons pour modifier ou supprimer le deck
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        self.edit_deck_btn = QPushButton("Modifier")
        action_layout.addWidget(self.edit_deck_btn)

        self.delete_deck_btn = QPushButton("Supprimer")
        self.delete_deck_btn.setObjectName("danger_button")
        action_layout.addWidget(self.delete_deck_btn)

        info_layout.addLayout(action_layout)
        header_layout.addLayout(info_layout)
        layout.addWidget(header_frame)

        # -------- Bouton d'étude --------
        self.study_btn = QPushButton("Étudier maintenant")
        self.study_btn.setObjectName("accent_button")
        self.study_btn.setMinimumHeight(50)
        self.study_btn.clicked.connect(self.start_study)

        # Désactivation si aucune carte
        if card_count == 0:
            self.study_btn.setEnabled(False)
            self.study_btn.setText("Ajoutez des cartes pour étudier")

        layout.addWidget(self.study_btn)

        # -------- Liste des cartes --------
        cards_frame = QFrame()
        cards_frame.setObjectName("card_frame")
        cards_layout = QVBoxLayout(cards_frame)
        cards_layout.setContentsMargins(15, 15, 15, 15)
        cards_layout.setSpacing(15)

        cards_header_layout = QHBoxLayout()
        cards_label = QLabel("Mes cartes")
        cards_label.setStyleSheet(get_style("subheader_label"))
        cards_header_layout.addWidget(cards_label)

        self.add_card_btn = QPushButton("+ Ajouter une carte")
        self.add_card_btn.setStyleSheet(get_style("action_button"))
        self.add_card_btn.clicked.connect(self.add_card)
        cards_header_layout.addWidget(self.add_card_btn)

        cards_layout.addLayout(cards_header_layout)

        # Tableau des cartes (question, réponse, stats, actions)
        self.cards_table = QTableWidget()
        self.cards_table.setColumnCount(4)
        self.cards_table.setHorizontalHeaderLabels(["Question", "Réponse", "Stats", "Actions"])
        self.cards_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cards_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cards_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.cards_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.cards_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.cards_table.customContextMenuRequested.connect(self.show_context_menu)
        self.cards_table.verticalHeader().setVisible(False)
        self.cards_table.setAlternatingRowColors(True)

        cards_layout.addWidget(self.cards_table)
        layout.addWidget(cards_frame, 1)  # Le "1" permet à ce widget de s'étendre

        # Connexion des boutons
        self.edit_deck_btn.clicked.connect(self.edit_deck)
        self.delete_deck_btn.clicked.connect(self.delete_deck)

        # Chargement initial des cartes
        self.refresh_cards()

    def refresh_cards(self):
        """Rafraîchit la liste des cartes affichées dans le tableau."""
        self.cards_table.setRowCount(0)
        cards = self.deck_manager.get_cards(self.deck_id)

        for i, card in enumerate(cards):
            self.cards_table.insertRow(i)

            # Colonne 1 : Question
            front_item = QTableWidgetItem(card["front"])
            self.cards_table.setItem(i, 0, front_item)

            # Colonne 2 : Réponse
            back_item = QTableWidgetItem(card["back"])
            self.cards_table.setItem(i, 1, back_item)

            # Colonne 3 : Statistiques de réussite
            correct = card.get("correct_count", 0)
            incorrect = card.get("incorrect_count", 0)
            total = correct + incorrect

            if total > 0:
                success_rate = (correct / total) * 100
                stats_text = f"{correct}/{total} ({success_rate:.1f}%)"
            else:
                stats_text = "Aucune donnée"

            stats_item = QTableWidgetItem(stats_text)
            self.cards_table.setItem(i, 2, stats_item)

            # Colonne 4 : Boutons Modifier / Supprimer
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)

            edit_btn = QPushButton("Modifier")
            edit_btn.clicked.connect(lambda _, card_id=card["id"]: self.edit_card(card_id))
            actions_layout.addWidget(edit_btn)

            delete_btn = QPushButton("Supprimer")
            delete_btn.clicked.connect(lambda _, card_id=card["id"]: self.delete_card(card_id))
            actions_layout.addWidget(delete_btn)

            self.cards_table.setCellWidget(i, 3, actions_widget)

            # Stockage de l'ID dans la première cellule
            front_item.setData(Qt.UserRole, card["id"])

        # Mise à jour de l'état du bouton d'étude
        card_count = len(cards)
        if card_count > 0:
            self.study_btn.setEnabled(True)
            self.study_btn.setText("Étudier maintenant")
        else:
            self.study_btn.setEnabled(False)
            self.study_btn.setText("Ajoutez des cartes pour étudier")

    def show_context_menu(self, position):
        """Affiche le menu contextuel (clic droit) pour une carte."""
        row = self.cards_table.rowAt(position.y())
        if row < 0:
            return

        card_id = self.cards_table.item(row, 0).data(Qt.UserRole)

        menu = QMenu(self)

        edit_action = QAction("Modifier", self)
        edit_action.triggered.connect(lambda: self.edit_card(card_id))
        menu.addAction(edit_action)

        delete_action = QAction("Supprimer", self)
        delete_action.triggered.connect(lambda: self.delete_card(card_id))
        menu.addAction(delete_action)

        menu.exec_(QCursor.pos())

    def edit_deck(self):
        """Ouvre la boîte de dialogue pour modifier le nom et la description du deck."""
        dialog = DeckEditorDialog(self.parent, self.deck["name"], self.deck["description"])
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.name_edit.text()
            description = dialog.description_edit.toPlainText()

            if name:
                self.deck_manager.update_deck(self.deck_id, name, description)
                self.deck = self.deck_manager.get_deck(self.deck_id)
                self.title_label.setText(name)
                self.parent.refresh_deck_list()

    def delete_deck(self):
        """Supprime le deck après confirmation de l'utilisateur."""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer le deck '{self.deck['name']}' et toutes ses cartes ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.deck_manager.delete_deck(self.deck_id)
            self.parent.refresh_deck_list()
            self.parent.right_panel.setCurrentIndex(0)  # Retour à la vue d'accueil

    def add_card(self):
        """Ajoute une nouvelle carte au deck via une boîte de dialogue."""
        dialog = CardEditorDialog(self.parent)
        if dialog.exec_() == QDialog.Accepted:
            front = dialog.front_edit.toPlainText()
            back = dialog.back_edit.toPlainText()

            if front and back:
                self.deck_manager.create_card(self.deck_id, front, back)
                self.refresh_cards()

    def edit_card(self, card_id):
        """Modifie une carte existante via une boîte de dialogue."""
        card = self.deck_manager.get_card(self.deck_id, card_id)
        if not card:
            return

        dialog = CardEditorDialog(self.parent, card["front"], card["back"])
        if dialog.exec_() == QDialog.Accepted:
            front = dialog.front_edit.toPlainText()
            back = dialog.back_edit.toPlainText()

            if front and back:
                self.deck_manager.update_card(self.deck_id, card_id, front, back)
                self.refresh_cards()

    def delete_card(self, card_id):
        """Supprime une carte après confirmation."""
        card = self.deck_manager.get_card(self.deck_id, card_id)
        if not card:
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Êtes-vous sûr de vouloir supprimer cette carte ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.deck_manager.delete_card(self.deck_id, card_id)
            self.refresh_cards()

    def start_study(self):
        """Lance une session d'étude avec ce deck."""
        self.parent.show_study_view(self.deck_id)