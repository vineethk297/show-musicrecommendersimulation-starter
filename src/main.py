"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # --- Header ---
    print("\n" + "=" * 52)
    print("  Music Recommender — Top 5 Picks")
    print(f"  Profile : genre={user_prefs['genre']}  "
          f"mood={user_prefs['mood']}  "
          f"energy={user_prefs['energy']}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score  : {score:.2f} / 5.00")
        print(f"    Genre  : {song['genre']}   Mood: {song['mood']}   Energy: {song['energy']:.2f}")
        reasons = explanation.split(" | ")
        for reason in reasons:
            print(f"    + {reason}")

    print("\n" + "=" * 52)


if __name__ == "__main__":
    main()
