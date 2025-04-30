from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTextEdit, QFormLayout, QFrame)
from ui.style import get_style  # Importation de la fonction pour appliquer des styles

class CardEditorDialog(QDialog):
    def __init__(self, parent=None, front="", back=""):
        """
        Constructeur pour initialiser la boîte de dialogue d'édition de carte.

        :param parent: Parent widget (par défaut None)
        :param front: Texte de la question (face avant de la carte)
        :param back: Texte de la réponse (face arrière de la carte)
        """
        super().__init__(parent)
        self.front = front  # Texte de la question
        self.back = back    # Texte de la réponse
        self.init_ui()      # Appel à la méthode pour initialiser l'interface

    def init_ui(self):
        """Initialise l'interface utilisateur de la boîte de dialogue pour éditer ou créer une carte."""
        self.setWindowTitle("Éditer une carte")  # Titre de la fenêtre
        self.setMinimumWidth(600)  # Largeur minimale de la fenêtre
        self.setMinimumHeight(450)  # Hauteur minimale de la fenêtre

        # Layout principal vertical pour l'organisation des widgets
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Espaces internes autour du layout
        layout.setSpacing(15)  # Espacement entre les éléments

        # Titre de la boîte de dialogue
        title_label = QLabel("Créer ou modifier une carte")
        title_label.setStyleSheet(get_style("header_label"))  # Application du style "header_label"
        layout.addWidget(title_label)

        # Instruction affichée sous le titre
        instruction_label = QLabel("Entrez la question et la réponse pour cette carte.")
        instruction_label.setStyleSheet(get_style("info_label"))  # Application du style "info_label"
        layout.addWidget(instruction_label)

        # Séparateur horizontal entre les sections
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)  # Ligne horizontale
        separator.setStyleSheet(get_style("separator"))  # Application du style pour le séparateur
        layout.addWidget(separator)

        # Formulaire avec des champs pour entrer la question et la réponse
        form_layout = QFormLayout()  # Disposition sous forme de formulaire
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 10, 0, 10)

        # Champ pour la question (face avant de la carte)
        front_label = QLabel("Question:")  # Étiquette pour la question
        self.front_edit = QTextEdit()  # Zone de texte pour la question
        self.front_edit.setMinimumHeight(120)  # Hauteur minimale de la zone de texte
        self.front_edit.setPlaceholderText("Entrez votre question ici...")  # Texte d'exemple dans le champ
        self.front_edit.setPlainText(self.front)  # Remplissage initial du champ avec la question
        form_layout.addRow(front_label, self.front_edit)  # Ajout du champ au formulaire

        # Champ pour la réponse (face arrière de la carte)
        back_label = QLabel("Réponse:")  # Étiquette pour la réponse
        self.back_edit = QTextEdit()  # Zone de texte pour la réponse
        self.back_edit.setMinimumHeight(120)  # Hauteur minimale de la zone de texte
        self.back_edit.setPlaceholderText("Entrez votre réponse ici...")  # Texte d'exemple dans le champ
        self.back_edit.setPlainText(self.back)  # Remplissage initial du champ avec la réponse
        form_layout.addRow(back_label, self.back_edit)  # Ajout du champ au formulaire

        layout.addLayout(form_layout)  # Ajout du formulaire au layout principal

        # Disposition des boutons d'annulation et d'enregistrement
        buttons_layout = QHBoxLayout()  # Disposition horizontale des boutons
        buttons_layout.setSpacing(10)

        # Bouton d'annulation
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)  # Ferme la boîte de dialogue sans enregistrer
        buttons_layout.addWidget(cancel_btn)

        # Bouton d'enregistrement
        save_btn = QPushButton("Enregistrer")
        save_btn.setObjectName("accent_button")  # Application du style pour le bouton accentué
        save_btn.clicked.connect(self.accept)  # Accepte et ferme la boîte de dialogue
        buttons_layout.addWidget(save_btn)

        layout.addLayout(buttons_layout)  # Ajout des boutons au layout principal