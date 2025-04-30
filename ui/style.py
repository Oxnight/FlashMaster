from PyQt5.QtGui import QPalette, QColor, QFont


# === Palette de couleurs ===
PRIMARY_COLOR = "#2c3e50"      # Bleu foncé pour les éléments principaux
SECONDARY_COLOR = "#3498db"    # Bleu clair pour les accents
ACCENT_COLOR = "#1abc9c"       # Vert-bleu pour les actions positives
WARNING_COLOR = "#f39c12"      # Orange pour les avertissements
DANGER_COLOR = "#e74c3c"       # Rouge pour les actions destructives

# === Nuances de gris ===
BACKGROUND_COLOR = "#f5f5f5"   # Gris très clair pour le fond
CARD_COLOR = "#ffffff"         # Blanc pour les cartes
TEXT_COLOR = "#2c3e50"         # Couleur du texte principale
LIGHT_TEXT_COLOR = "#7f8c8d"   # Couleur du texte secondaire
BORDER_COLOR = "#dcdde1"       # Couleur des bordures

# === Espacement et dimensions ===
PADDING = 12                   # Espacement standard
BORDER_RADIUS = 6              # Arrondi des coins
BUTTON_HEIGHT = 36             # Hauteur des boutons standard

def apply_stylesheet(app):
    """
    Applique la feuille de style globale à l'application Qt.
    Personnalise la palette de couleurs et applique un thème QSS.
    """

    # Définition de la police globale
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Création et application de la palette personnalisée
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BACKGROUND_COLOR))
    palette.setColor(QPalette.WindowText, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Base, QColor(CARD_COLOR))
    palette.setColor(QPalette.AlternateBase, QColor(BACKGROUND_COLOR))
    palette.setColor(QPalette.ToolTipBase, QColor(PRIMARY_COLOR))
    palette.setColor(QPalette.ToolTipText, QColor(CARD_COLOR))
    palette.setColor(QPalette.Text, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Button, QColor(BACKGROUND_COLOR))
    palette.setColor(QPalette.ButtonText, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Link, QColor(SECONDARY_COLOR))
    palette.setColor(QPalette.Highlight, QColor(SECONDARY_COLOR))
    palette.setColor(QPalette.HighlightedText, QColor(CARD_COLOR))
    app.setPalette(palette)

    # Style général en QSS (Qt Style Sheets)
    app.setStyleSheet(f"""
        /* Style général */
        QMainWindow, QDialog {{
            background-color: {BACKGROUND_COLOR};
        }}

        /* Widgets principaux */
        QWidget {{
            color: {TEXT_COLOR};
        }}

        /* Labels */
        QLabel {{
            color: {TEXT_COLOR};
        }}

        /* Boutons standard */
        QPushButton {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-radius: {BORDER_RADIUS}px;
            padding: 6px {PADDING}px;
            min-height: {BUTTON_HEIGHT}px;
            outline: none;
        }}

        QPushButton:hover {{
            background-color: {SECONDARY_COLOR};
            color: white;
            border: 1px solid {SECONDARY_COLOR};
        }}

        QPushButton:pressed {{
            background-color: {PRIMARY_COLOR};
            color: white;
        }}

        QPushButton:disabled {{
            background-color: {BACKGROUND_COLOR};
            color: {LIGHT_TEXT_COLOR};
            border: 1px solid {BORDER_COLOR};
        }}

        /* Boutons d'action positive */
        QPushButton#accent_button {{
            background-color: {ACCENT_COLOR};
            color: white;
            border: none;
        }}

        QPushButton#accent_button:hover {{
            background-color: #16a085;
        }}

        /* Boutons dangereux */
        QPushButton#danger_button {{
            background-color: {DANGER_COLOR};
            color: white;
            border: none;
        }}

        QPushButton#danger_button:hover {{
            background-color: #c0392b;
        }}

        /* Liste et tableaux */
        QListWidget, QTableWidget {{
            background-color: {CARD_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-radius: {BORDER_RADIUS}px;
            outline: none;
        }}

        QListWidget::item {{
            padding: 8px {PADDING}px;
            border-bottom: 1px solid {BORDER_COLOR};
        }}

        QListWidget::item:selected {{
            background-color: {SECONDARY_COLOR};
            color: white;
        }}

        QTableWidget {{
            gridline-color: {BORDER_COLOR};
        }}

        QHeaderView::section {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
            padding: 8px;
            border: none;
            border-bottom: 1px solid {BORDER_COLOR};
        }}

        /* Champs de texte */
        QLineEdit, QTextEdit {{
            background-color: {CARD_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-radius: {BORDER_RADIUS}px;
            padding: 8px;
        }}

        QLineEdit:focus, QTextEdit:focus {{
            border: 1px solid {SECONDARY_COLOR};
        }}

        /* Barres de progression */
        QProgressBar {{
            border: 1px solid {BORDER_COLOR};
            border-radius: {BORDER_RADIUS}px;
            background-color: {BACKGROUND_COLOR};
            padding: 1px;
            text-align: center;
        }}

        QProgressBar::chunk {{
            background-color: {SECONDARY_COLOR};
            border-radius: {BORDER_RADIUS - 1}px;
        }}

        /* Conteneurs de cartes */
        QFrame#card_frame {{
            background-color: {CARD_COLOR};
            border-radius: {BORDER_RADIUS}px;
            border: 1px solid {BORDER_COLOR};
        }}
    """)


def get_style(style_name):
    """Retourne des styles spécifiques pour différents composants."""
    styles = {
        "card_container": f"""
            background-color: {CARD_COLOR};
            border-radius: {BORDER_RADIUS}px;
            border: 1px solid {BORDER_COLOR};
            padding: {PADDING}px;
        """,
        "header_label": f"""
            color: {PRIMARY_COLOR};
            font-size: 18px;
            font-weight: bold;
        """,
        "subheader_label": f"""
            color: {PRIMARY_COLOR};
            font-size: 14px;
            font-weight: bold;
        """,
        "info_label": f"""
            color: {LIGHT_TEXT_COLOR};
            font-size: 12px;
        """,
        "separator": f"""
            background-color: {BORDER_COLOR};
            min-height: 1px;
            max-height: 1px;
        """,
        "correct_button": f"""
            background-color: {ACCENT_COLOR};
            color: white;
            border-radius: {BORDER_RADIUS}px;
            padding: 6px {PADDING}px;
            min-height: {BUTTON_HEIGHT}px;
            font-weight: bold;
        """,
        "incorrect_button": f"""
            background-color: {DANGER_COLOR};
            color: white;
            border-radius: {BORDER_RADIUS}px;
            padding: 6px {PADDING}px;
            min-height: {BUTTON_HEIGHT}px;
            font-weight: bold;
        """,
        "action_button": f"""
            background-color: {SECONDARY_COLOR};
            color: white;
            border-radius: {BORDER_RADIUS}px;
            padding: 6px {PADDING}px;
            min-height: {BUTTON_HEIGHT}px;
        """,
        "card_front": f"""
            font-size: 20px;
            color: {TEXT_COLOR};
            font-weight: bold;
        """,
        "card_back": f"""
            font-size: 18px;
            color: {TEXT_COLOR};
        """,
        "stat_label": f"""
            background-color: {BACKGROUND_COLOR};
            padding: 4px 10px;
            border-radius: {BORDER_RADIUS}px;
            font-size: 12px;
            color: {LIGHT_TEXT_COLOR};
        """,
        "progress_bar": f"""
            QProgressBar {{
                background-color: {BACKGROUND_COLOR};
                border-radius: {BORDER_RADIUS}px;
                text-align: center;
                height: 20px;
            }}
            QProgressBar::chunk {{
                background-color: {SECONDARY_COLOR};
                border-radius: {BORDER_RADIUS - 1}px;
            }}
        """,
        "flashcard": f"""
            background-color: {CARD_COLOR};
            border: 2px solid {SECONDARY_COLOR};
            border-radius: {BORDER_RADIUS * 2}px;
            padding: 20px;
        """,
        "search_box": f"""
            background-color: {CARD_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-radius: {BORDER_RADIUS}px;
            padding: 8px 10px;
            font-size: 13px;
        """,
        "tag_label": f"""
            background-color: {SECONDARY_COLOR};
            color: white;
            border-radius: {BORDER_RADIUS}px;
            padding: 2px 8px;
            font-size: 11px;
        """
    }

    return styles.get(style_name, "")