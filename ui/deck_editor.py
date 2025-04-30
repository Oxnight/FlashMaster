from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QLineEdit, QTextEdit, QFormLayout, QFrame)
from ui.style import get_style  # Importation de la fonction pour appliquer des styles

class DeckEditorDialog(QDialog):
    def __init__(self, parent=None, name="", description=""):
        """
        Constructeur pour initialiser la boîte de dialogue d'édition de deck.

        :param parent: Parent widget (par défaut None)
        :param name: Nom du deck (par défaut une chaîne vide)
        :param description: Description du deck (par défaut une chaîne vide)
        """
        super().__init__(parent)
        self.name = name  # Nom du deck
        self.description = description  # Description du deck
        self.init_ui()  # Appel à la méthode pour initialiser l'interface

    def init_ui(self):
        """Initialise l'interface utilisateur de la boîte de dialogue pour éditer ou créer un deck."""
        self.setWindowTitle("Éditer un deck")  # Titre de la fenêtre
        self.setMinimumWidth(500)  # Largeur minimale de la fenêtre
        self.setMinimumHeight(350)  # Hauteur minimale de la fenêtre

        # Layout principal vertical pour l'organisation des widgets
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Espaces internes autour du layout
        layout.setSpacing(15)  # Espacement entre les éléments

        # Titre de la boîte de dialogue
        title_label = QLabel("Créer ou modifier un deck")
        title_label.setStyleSheet(get_style("header_label"))  # Application du style "header_label"
        layout.addWidget(title_label)

        # Instruction affichée sous le titre
        instruction_label = QLabel("Donnez un nom et une description à votre deck de cartes.")
        instruction_label.setStyleSheet(get_style("info_label"))  # Application du style "info_label"
        layout.addWidget(instruction_label)

        # Séparateur horizontal entre les sections
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)  # Ligne horizontale
        separator.setStyleSheet(get_style("separator"))  # Application du style pour le séparateur
        layout.addWidget(separator)

        # Formulaire avec des champs pour entrer le nom et la description du deck
        form_layout = QFormLayout()  # Disposition sous forme de formulaire
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 10, 0, 10)

        # Champ pour le nom du deck
        name_label = QLabel("Nom:")  # Étiquette pour le nom
        self.name_edit = QLineEdit()  # Champ de texte pour le nom
        self.name_edit.setPlaceholderText("Entrez le nom du deck...")  # Texte d'exemple dans le champ
        self.name_edit.setText(self.name)  # Remplissage initial du champ avec le nom
        form_layout.addRow(name_label, self.name_edit)  # Ajout du champ au formulaire

        # Champ pour la description du deck
        description_label = QLabel("Description:")  # Étiquette pour la description
        self.description_edit = QTextEdit()  # Champ de texte pour la description
        self.description_edit.setPlaceholderText("Entrez une description (optionnelle)...")  # Texte d'exemple
        self.description_edit.setPlainText(self.description)  # Remplissage initial du champ avec la description
        self.description_edit.setMinimumHeight(120)  # Hauteur minimale du champ de description
        form_layout.addRow(description_label, self.description_edit)  # Ajout du champ au formulaire

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