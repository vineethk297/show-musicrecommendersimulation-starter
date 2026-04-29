# Music Recommender — Final Project Extension

## What this project is
A content-based music recommender that scores songs against a user taste profile 
(genre, mood, energy, acousticness) and returns top-K ranked recommendations with explanations.

## Current state
- `src/recommender.py`: has working functional code (`load_songs`, `score_song`, `recommend_songs`) 
  but the OOP `Recommender` class stubs (`recommend`, `explain_recommendation`) are NOT implemented yet
- `src/main.py`: CLI runner with 6 user profiles including 3 adversarial/edge-case profiles
- `data/songs.csv`: 18-song catalog with audio features
- `tests/test_recommender.py`: 2 tests that use the OOP class (currently failing)
- `model_card.md` and `reflection.md` exist but need updating after extensions

## What needs to be built (in order)
1. **Wire up Recommender class** — move score_song logic into `recommend()` and `explain_recommendation()` so tests pass
2. **RAG-style knowledge base** — create `data/genre_knowledge.json` with genre/mood descriptions, retrieve relevant entries in `explain_recommendation()` to enrich explanations
3. **Confidence threshold** — if top recommendation scores below 2.5/5.0, flag as low confidence in output
4. **Evaluation tests** — add 3-4 tests in `tests/test_recommender.py`: genre dominance check, diversity check, low-confidence detection for ghost genre, acoustic bonus verification
5. **Update model_card.md** — document decision process, biases, guardrails

## Scoring formula (max 5.0)
- Genre match: +2.0 (exact match only)
- Mood match: +1.0 (exact match only)  
- Energy similarity: 0 to +1.5 (`1.5 * (1 - abs(song_energy - target_energy))`)
- Acoustic bonus: +0.5 (if user likes acoustic AND song acousticness >= 0.6)

## Rules
- Python only, no external APIs or LLMs needed
- Keep it simple — template-based retrieval, not vector search
- All new code goes in existing files, no new modules unless necessary
- Run tests with: `pytest tests/ -v` from project root