# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This simulation builds a lightweight, content-based music recommender that matches songs to a user's current vibe — no listening history required. It scores every song in a small catalog against a user's taste profile using weighted Gaussian proximity on audio features (energy, acousticness, tempo, valence), then applies mood and genre bonuses before surfacing the top matches. The goal is to show how real-world systems like Spotify translate raw audio data into personal recommendations, and to honestly surface where that approach breaks down.

---

## How The System Works

Real-world recommenders like Spotify and Pandora are essentially giant pattern matchers — they watch what millions of people play, skip, and save, then use that collective behavior to guess what any one person might enjoy next. Our version skips the crowd entirely and focuses on something more personal: the actual sound of the music. Instead of asking "what do users like you listen to?", it asks "what does this song *feel* like, and how close is that to what you're in the mood for right now?" Every song gets scored against your taste profile, with genre and mood acting as strong bonus signals and energy acting as a continuous dial. The result is a short, ranked list of songs that should feel right for where you are emotionally, not just what's statistically popular.

### The Algorithm Recipe

Think of the recommender as a judge holding a scorecard. Every song in the catalog walks up and gets evaluated on four questions — and the answers add up to a final score out of 5.0 points:

| Question | Max Points | How it works |
|---|---|---|
| Does the genre match? | +2.0 | Full 2 points for an exact genre match, nothing otherwise |
| Does the mood match? | +1.0 | Full 1 point for an exact mood match, nothing otherwise |
| How close is the energy? | 0 – +1.5 | `1.5 × (1 − │song energy − your target energy│)` — a perfect energy match gives 1.5, a halfway-off match gives 0.75, a complete mismatch gives 0 |
| Is it acoustic (if you care)? | +0.5 | Only kicks in when you prefer acoustic music AND the song scores ≥ 0.6 on acousticness |

Once every song has been judged, they get sorted from highest score to lowest, and the top K are handed back as your recommendations — along with a short explanation of *why* each one scored the way it did.

Here's a quick example of the recipe in action. Say your profile is `genre=pop, mood=happy, energy=0.8`:

- **Sunrise City** (pop, happy, energy 0.82) scores `2.0 + 1.0 + 1.47 = 4.47` — genre and mood both match, and the energy is almost identical.
- **Gym Hero** (pop, intense, energy 0.93) scores `2.0 + 0 + 1.31 = 3.31` — genre matches but the intense mood misses, and the energy is a bit high.
- **Rooftop Lights** (indie pop, happy, energy 0.76) scores `0 + 1.0 + 1.44 = 2.44` — mood hits, energy is close, but "indie pop" isn't "pop" so the genre bonus is lost entirely.

Genre is intentionally the heaviest signal. If two songs are tied on everything else, the one in your preferred genre will always win.

### Potential Biases to Watch For

No algorithm is neutral, and this one has some real blindspots worth acknowledging:

- **Genre rigidity.** Because a genre match is worth twice as much as a mood match, the system can end up recommending a genre-matched song that feels completely wrong emotionally over a mood-matched song from a slightly different genre that would've been a better listen. A chill lofi track and a chill ambient track might feel identical to a human ear, but this system treats them as strangers.

- **Energy tunnel vision.** Energy is the only audio feature being continuously scored. Two songs could be identical in energy but wildly different in tempo, danceability, or emotional tone — and the algorithm wouldn't notice. A 0.8-energy jazz ballad and a 0.8-energy punk track look the same on paper here.

- **Acoustic users get a tiebreaker, not a filter.** The acoustic bonus is small (0.5 points) and optional. If you love acoustic music, you might still get highly-produced electronic tracks at the top of your list if they nail the genre and mood. The bonus nudges the ranking but doesn't protect against it.

- **The catalog is tiny.** With only 18 songs, the "top 5" recommendations might include songs the algorithm scored mediocrely — simply because there aren't enough good matches to fill the list. In a real system, a poor match would just not appear.

### Sample Output

Running the default `pop / happy / energy=0.8` profile produces this terminal output:

```
Loaded songs: 18

====================================================
  Music Recommender — Top 5 Picks
  Profile : genre=pop  mood=happy  energy=0.8
====================================================

#1  Sunrise City by Neon Echo
    Score  : 4.47 / 5.00
    Genre  : pop   Mood: happy   Energy: 0.82
    + genre match (+2.0)
    + mood match (+1.0)
    + energy similarity (+1.47)

#2  Gym Hero by Max Pulse
    Score  : 3.31 / 5.00
    Genre  : pop   Mood: intense   Energy: 0.93
    + genre match (+2.0)
    + energy similarity (+1.30)

#3  Rooftop Lights by Indigo Parade
    Score  : 2.44 / 5.00
    Genre  : indie pop   Mood: happy   Energy: 0.76
    + mood match (+1.0)
    + energy similarity (+1.44)

#4  Night Drive Loop by Neon Echo
    Score  : 1.43 / 5.00
    Genre  : synthwave   Mood: moody   Energy: 0.75
    + energy similarity (+1.42)

#5  Rise Up Sunday by Juno Ray
    Score  : 1.38 / 5.00
    Genre  : soul   Mood: uplifting   Energy: 0.72
    + energy similarity (+1.38)

====================================================
```

**Why these results make sense:**
- **#1 Sunrise City** is the only song that nails all three signals — pop genre, happy mood, and nearly identical energy (0.82 vs 0.80). It's the clear winner at 4.47.
- **#2 Gym Hero** stays at the top because it's still pop, but the intense mood miss costs it the 1.0 mood bonus, dropping it to 3.31.
- **#3 Rooftop Lights** is "indie pop" not "pop" — losing the genre bonus entirely. Mood and close energy earn it 2.44, but genre rigidity keeps it off the podium.
- **#4 and #5** scored only on energy proximity. With 18 songs and only two true pop tracks in the catalog, the tail of the list fills with near-misses.

### Song Features

Each `Song` object carries the following attributes:

| Feature | Type | What it captures |
|---|---|---|
| `id` | Integer | Unique identifier |
| `title` | String | Song name |
| `artist` | String | Artist name |
| `genre` | Categorical | Broad sonic category (lofi, pop, rock, jazz, ambient, synthwave, indie pop) |
| `mood` | Categorical | Emotional tone (chill, happy, intense, relaxed, focused, moody) |
| `energy` | Float 0–1 | Intensity and loudness — the most direct signal of listener intent |
| `tempo_bpm` | Integer | Beats per minute — rhythm feel independent of energy |
| `valence` | Float 0–1 | Musical positiveness; high = uplifting, low = melancholic |
| `danceability` | Float 0–1 | How strongly the rhythm invites movement |
| `acousticness` | Float 0–1 | Organic and acoustic vs. produced and electronic |

### UserProfile Features

Each `UserProfile` stores a personal taste snapshot using the same dimensions as a song, so the two can be directly compared:

| Feature | Type | Purpose |
|---|---|---|
| `name` | String | Identifies the user |
| `preferred_genre` | Categorical | The genre the user gravitates toward |
| `preferred_mood` | Categorical | The emotional context the user is currently in |
| `preferred_energy` | Float 0–1 | How high or low energy the user wants right now |
| `preferred_tempo_bpm` | Integer | The rhythm pace that feels right |
| `preferred_valence` | Float 0–1 | Whether the user wants something uplifting or introspective |
| `preferred_acousticness` | Float 0–1 | Preference for acoustic warmth vs. electronic crispness |

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

