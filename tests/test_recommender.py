import pytest
from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# ---------------------------------------------------------------------------
# Evaluation tests
# ---------------------------------------------------------------------------

def test_genre_dominance():
    """Genre match (+2.0) must be strong enough to push the matching song to rank #1."""
    songs = [
        Song(id=1, title="Pop Track", artist="A", genre="pop", mood="chill",
             energy=0.5, tempo_bpm=120, valence=0.7, danceability=0.7, acousticness=0.2),
        Song(id=2, title="Rock Track", artist="B", genre="rock", mood="happy",
             energy=0.9, tempo_bpm=150, valence=0.5, danceability=0.5, acousticness=0.1),
    ]
    # pop: genre (+2.0) + energy exact (1.5) = 3.5
    # rock: mood (+1.0) + energy sim 1.5*(1-0.4)=0.9 = 1.9
    rec = Recommender(songs)
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.5, likes_acoustic=False)
    results = rec.recommend(user, k=2)

    assert results[0].genre == "pop", "Genre-matching song should rank first"


def test_no_genre_match_results_are_diverse():
    """When the user's genre is absent from the catalog, top-k results should span multiple genres."""
    songs = [
        Song(id=1, title="Pop Track", artist="A", genre="pop", mood="happy",
             energy=0.8, tempo_bpm=120, valence=0.8, danceability=0.8, acousticness=0.2),
        Song(id=2, title="Rock Track", artist="B", genre="rock", mood="happy",
             energy=0.7, tempo_bpm=130, valence=0.5, danceability=0.6, acousticness=0.1),
        Song(id=3, title="Jazz Track", artist="C", genre="jazz", mood="chill",
             energy=0.4, tempo_bpm=90, valence=0.6, danceability=0.5, acousticness=0.7),
    ]
    # k-pop not in catalog → no genre bonus; scoring differences come from mood/energy only
    rec = Recommender(songs)
    user = UserProfile(favorite_genre="k-pop", favorite_mood="happy", target_energy=0.75, likes_acoustic=False)
    results = rec.recommend(user, k=3)

    genres_returned = {s.genre for s in results}
    assert len(genres_returned) > 1, "Results should include songs from more than one genre"


def test_low_confidence_for_ghost_genre():
    """is_low_confidence must be True when the user's genre isn't in the catalog."""
    songs = [
        Song(id=1, title="Pop Track", artist="A", genre="pop", mood="happy",
             energy=0.8, tempo_bpm=120, valence=0.8, danceability=0.8, acousticness=0.2),
    ]
    rec = Recommender(songs)

    ghost = UserProfile(favorite_genre="k-pop", favorite_mood="chill", target_energy=0.5, likes_acoustic=False)
    # best score: no genre, no mood, energy sim = 1.5*(1-0.3) = 1.05 → below 2.5
    assert rec.is_low_confidence(ghost) is True

    normal = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    # best score: genre (+2.0) + mood (+1.0) + energy sim (1.5) = 4.5 → above 2.5
    assert rec.is_low_confidence(normal) is False


def test_acoustic_bonus_adds_half_point():
    """A song with acousticness >= 0.6 must score exactly 0.5 more for a user who likes acoustic."""
    acoustic = Song(id=1, title="Acoustic Track", artist="A", genre="folk", mood="chill",
                    energy=0.5, tempo_bpm=80, valence=0.6, danceability=0.4, acousticness=0.8)
    non_acoustic = Song(id=2, title="Electric Track", artist="B", genre="folk", mood="chill",
                        energy=0.5, tempo_bpm=80, valence=0.6, danceability=0.4, acousticness=0.2)

    rec = Recommender([acoustic, non_acoustic])
    user = UserProfile(favorite_genre="folk", favorite_mood="chill", target_energy=0.5, likes_acoustic=True)

    score_a, _ = rec._score(user, acoustic)
    score_b, _ = rec._score(user, non_acoustic)

    assert score_a - score_b == pytest.approx(0.5), "Acoustic bonus should be exactly +0.5"
    assert rec.recommend(user, k=1)[0].title == "Acoustic Track", "Acoustic song should rank first"
