import os
import uuid
import json
from datetime import datetime
import random


class DeckManager:
    """
    Gère le stockage et la manipulation des decks et des cartes de l'application FlashMaster.
    Utilise un fichier JSON pour la persistance des données.
    """

    def __init__(self, data_dir="data"):
        """
        Initialise le gestionnaire de decks.

        Args:
            data_dir: Le répertoire où sont stockés les fichiers de données JSON.
        """
        self.data_dir = data_dir
        self.decks_file = os.path.join(data_dir, "decks.json")
        self.decks = []

        # Création du dossier de données s’il n’existe pas
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Chargement des decks existants à partir du fichier
        self.load_decks()

    def load_decks(self):
        """
        Charge les decks depuis le fichier JSON. Si le fichier est introuvable ou corrompu, initialise une liste vide.
        """
        if os.path.exists(self.decks_file):
            try:
                with open(self.decks_file, 'r', encoding='utf-8') as f:
                    self.decks = json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement des decks: {e}")
                self.decks = []
        else:
            self.decks = []

    def save_decks(self):
        """
        Sauvegarde les decks dans le fichier JSON pour assurer la persistance des données.
        """
        temp_file = self.decks_file + ".tmp"
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.decks, f, ensure_ascii=False, indent=2)

            if os.path.exists(self.decks_file):
                os.remove(self.decks_file)
            os.rename(temp_file, self.decks_file)

        except Exception as e:
            print(f"Erreur critique sauvegarde: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def get_decks(self):
        """
        Retourne tous les decks actuellement chargés en mémoire.
        """
        return self.decks

    def create_deck(self, name, description=""):
        """
        Crée un nouveau deck et l’ajoute à la liste existante.

        Args:
            name: Le nom du deck.
            description: Une description facultative du deck.

        Returns:
            L’ID du nouveau deck créé.
        """
        deck_id = str(uuid.uuid4())
        new_deck = {
            "id": deck_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "last_studied": None,
            "cards": []
        }
        self.decks.append(new_deck)
        self.save_decks()
        return deck_id

    def get_deck(self, deck_id):
        """
        Récupère un deck à partir de son ID.

        Args:
            deck_id: L'identifiant du deck.

        Returns:
            Le dictionnaire du deck ou None s’il n’existe pas.
        """
        for deck in self.decks:
            if deck["id"] == deck_id:
                return deck
        return None

    def update_deck(self, deck_id, name, description):
        """
        Met à jour le nom et la description d’un deck existant.

        Args:
            deck_id: L'identifiant du deck.
            name: Le nouveau nom du deck.
            description: La nouvelle description.

        Returns:
            True si la mise à jour a réussi, False sinon.
        """
        for deck in self.decks:
            if deck["id"] == deck_id:
                deck["name"] = name
                deck["description"] = description
                self.save_decks()
                return True
        return False

    def delete_deck(self, deck_id):
        """
        Supprime un deck de la liste.

        Args:
            deck_id: L'identifiant du deck à supprimer.

        Returns:
            True si la suppression a réussi, False sinon.
        """
        for i, deck in enumerate(self.decks):
            if deck["id"] == deck_id:
                del self.decks[i]
                self.save_decks()
                return True
        return False

    def get_cards(self, deck_id):
        """
        Récupère toutes les cartes associées à un deck.

        Args:
            deck_id: L'identifiant du deck.

        Returns:
            Liste des cartes ou liste vide si le deck n’existe pas.
        """
        deck = self.get_deck(deck_id)
        if deck:
            return deck["cards"]
        return []

    def create_card(self, deck_id, front, back):
        """
        Crée une nouvelle carte dans un deck donné.

        Args:
            deck_id: L'identifiant du deck.
            front: Le texte affiché en recto.
            back: Le texte affiché en verso.

        Returns:
            L’ID de la carte créée ou None si le deck est introuvable.
        """
        deck = self.get_deck(deck_id)
        if not deck:
            return None

        card_id = str(uuid.uuid4())

        new_card = {
            "id": card_id,
            "front": front,
            "back": back,
            "created_at": datetime.now().isoformat(),
            "correct_count": 0,
            "incorrect_count": 0,
            "media": []
        }

        deck["cards"].append(new_card)
        self.save_decks()
        return card_id

    def get_card(self, deck_id, card_id):
        """
        Récupère une carte à partir de son ID dans un deck.

        Args:
            deck_id: L'identifiant du deck.
            card_id: L'identifiant de la carte.

        Returns:
            Le dictionnaire de la carte ou None si introuvable.
        """
        cards = self.get_cards(deck_id)
        for card in cards:
            if card["id"] == card_id:
                return card
        return None

    def update_card(self, deck_id, card_id, front, back):
        """
        Met à jour le recto et le verso d’une carte.

        Args:
            deck_id: L'identifiant du deck.
            card_id: L'identifiant de la carte.
            front: Nouveau texte recto.
            back: Nouveau texte verso.

        Returns:
            True si la mise à jour a réussi, False sinon.
        """
        deck = self.get_deck(deck_id)
        if not deck:
            return False

        for card in deck["cards"]:
            if card["id"] == card_id:
                card["front"] = front
                card["back"] = back
                self.save_decks()
                return True
        return False

    def delete_card(self, deck_id, card_id):
        """
        Supprime une carte d’un deck.

        Args:
            deck_id: L'identifiant du deck.
            card_id: L'identifiant de la carte.

        Returns:
            True si la suppression a réussi, False sinon.
        """
        deck = self.get_deck(deck_id)
        if not deck:
            return False

        for i, card in enumerate(deck["cards"]):
            if card["id"] == card_id:
                del deck["cards"][i]
                self.save_decks()
                return True
        return False

    def get_study_cards(self, deck_id):
        """
        Récupère les cartes d’un deck dans un ordre aléatoire pour une session d’étude.

        Args:
            deck_id: L'identifiant du deck.

        Returns:
            Liste mélangée des cartes du deck.
        """
        cards = self.get_cards(deck_id)
        random.shuffle(cards)
        return cards

    def update_card_result(self, deck_id, card_id, is_correct):
        """
        Met à jour les statistiques de réponse d’une carte après révision.

        Args:
            deck_id: L'identifiant du deck.
            card_id: L'identifiant de la carte.
            is_correct: True si la réponse était correcte, False sinon.

        Returns:
            True si la mise à jour a réussi, False sinon.
        """
        deck = self.get_deck(deck_id)
        if not deck:
            return False

        for card in deck["cards"]:
            if card["id"] == card_id:
                if is_correct:
                    card["correct_count"] = card.get("correct_count", 0) + 1
                else:
                    card["incorrect_count"] = card.get("incorrect_count", 0) + 1

                # Mise à jour de la date de dernière révision du deck
                deck["last_studied"] = datetime.now().isoformat()
                self.save_decks()
                return True

        return False

    def get_card_count(self, deck_id):
        """
        Retourne le nombre de cartes dans un deck donné.

        Args:
            deck_id: L'identifiant du deck.

        Returns:
            Nombre total de cartes ou 0 si le deck est introuvable.
        """
        deck = self.get_deck(deck_id)
        if deck:
            return len(deck["cards"])
        return 0

    def get_deck_stats(self, deck_id):
        """
        Calcule des statistiques globales pour un deck : nombre de réponses correctes/incorrectes et taux de réussite.

        Args:
            deck_id: L'identifiant du deck.

        Returns:
            Dictionnaire des statistiques ou None si le deck est introuvable.
        """
        deck = self.get_deck(deck_id)
        if not deck:
            return None

        total_correct = 0
        total_incorrect = 0

        for card in deck["cards"]:
            total_correct += card.get("correct_count", 0)
            total_incorrect += card.get("incorrect_count", 0)

        total_answers = total_correct + total_incorrect
        success_rate = 0
        if total_answers > 0:
            success_rate = (total_correct / total_answers) * 100

        return {
            "total_cards": len(deck["cards"]),
            "correct_answers": total_correct,
            "incorrect_answers": total_incorrect,
            "success_rate": success_rate
        }

    def add_media_to_card(self, deck_id, card_id, media_type, file_path):
        """
        Associe un média (image, audio, etc.) à une carte.

        Args:
            deck_id: L'identifiant du deck.
            card_id: L'identifiant de la carte.
            media_type: Type du média (ex: 'image', 'audio').
            file_path: Chemin d’accès au fichier média.

        Returns:
            True si le média a été ajouté avec succès, False sinon.
        """
        deck = self.get_deck(deck_id)
        if not deck:
            return False

        for card in deck["cards"]:
            if card["id"] == card_id:
                if "media" not in card:
                    card["media"] = []

                media_id = str(uuid.uuid4())
                media = {
                    "id": media_id,
                    "type": media_type,
                    "path": file_path
                }

                card["media"].append(media)
                self.save_decks()
                return True

        return False