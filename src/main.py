"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

# --- Standard profiles ---
HIGH_ENERGY_POP = {
    "label":         "High-Energy Pop",
    "genre":         "pop",
    "mood":          "happy",
    "energy":        0.9,
    "likes_acoustic": False,
}

CHILL_LOFI = {
    "label":         "Chill Lofi",
    "genre":         "lofi",
    "mood":          "chill",
    "energy":        0.38,
    "likes_acoustic": True,
}

DEEP_INTENSE_ROCK = {
    "label":         "Deep Intense Rock",
    "genre":         "rock",
    "mood":          "intense",
    "energy":        0.9,
    "likes_acoustic": False,
}

# --- Adversarial / edge-case profiles ---

# Energy contradicts genre: lofi is inherently low-energy, but this user wants 0.95
ENERGY_CONTRADICTION = {
    "label":         "EDGE — High-Energy Lofi (contradiction)",
    "genre":         "lofi",
    "mood":          "chill",
    "energy":        0.95,
    "likes_acoustic": False,
}

# Genre doesn't exist in the catalog at all — pure energy/mood fallback
GHOST_GENRE = {
    "label":         "EDGE — Ghost Genre (not in catalog)",
    "genre":         "k-pop",
    "mood":          "happy",
    "energy":        0.8,
    "likes_acoustic": False,
}

# Mood and genre point to different songs — no song satisfies both
CONFLICTING_PREFS = {
    "label":         "EDGE — Conflicting Genre + Mood (country + romantic)",
    "genre":         "country",
    "mood":          "romantic",
    "energy":        0.5,
    "likes_acoustic": True,
}


PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    ENERGY_CONTRADICTION,
    GHOST_GENRE,
    CONFLICTING_PREFS,
]


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_recommendations(label: str, user_prefs: dict, recommendations: list) -> None:
    """Print a formatted recommendation block for one user profile."""
    print("\n" + "=" * 56)
    print(f"  {label}")
    print(f"  genre={user_prefs['genre']}  mood={user_prefs['mood']}"
          f"  energy={user_prefs['energy']}  acoustic={user_prefs.get('likes_acoustic', False)}")
    print("=" * 56)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score  : {score:.2f} / 5.00")
        print(f"    Genre  : {song['genre']}   Mood: {song['mood']}   Energy: {song['energy']:.2f}")
        for reason in explanation.split(" | "):
            print(f"    + {reason}")

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        user_prefs = {k: v for k, v in profile.items() if k != "label"}
        recs = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile["label"], user_prefs, recs)


if __name__ == "__main__":
    main()
