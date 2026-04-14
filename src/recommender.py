from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects ranked by score for the given UserProfile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended to a user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a songs CSV and return a list of dicts with numeric fields pre-converted."""
    import csv

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]               = int(row["id"])
            row["energy"]           = float(row["energy"])
            row["tempo_bpm"]        = float(row["tempo_bpm"])
            row["valence"]          = float(row["valence"])
            row["danceability"]     = float(row["danceability"])
            row["acousticness"]     = float(row["acousticness"])
            row["instrumentalness"] = float(row["instrumentalness"])
            row["speechiness"]      = float(row["speechiness"])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return (total_score, reasons) where max score is 5.0."""
    score: float = 0.0
    reasons: List[str] = []

    # --- Genre match (+2.0) ---
    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # --- Mood match (+1.0) ---
    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # --- Energy similarity (0 to +1.5) ---
    target_energy = float(user_prefs.get("energy", 0.5))
    energy_points = 1.5 * (1.0 - abs(song["energy"] - target_energy))
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    # --- Acoustic bonus (+0.5) ---
    if user_prefs.get("likes_acoustic", False) and song["acousticness"] >= 0.6:
        score += 0.5
        reasons.append(f"acoustic bonus (+0.5)")

    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    scored = [
        (song, total_score, " | ".join(reasons))
        for song in songs
        for total_score, reasons in (score_song(user_prefs, song),)
    ]

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
