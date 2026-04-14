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

Six profiles were run — three standard, three adversarial edge cases designed to stress-test the scoring logic.

---

### Weight Shift Experiment — Genre ÷2, Energy ×2

**Change applied:** `genre 2.0 → 1.0`, `energy max 1.5 → 3.0` (new max score: 5.5)

The goal was to test whether the original genre weight was creating a 2-point moat that prevented genuinely similar songs from competing. Here's what shifted:

| Profile | Original #1 → #2 gap | Experiment gap | What changed |
|---|---|---|---|
| Deep Intense Rock | 4.49 → 2.46 **(gap: 2.03)** | 4.97 → 3.91 **(gap: 1.06)** | Gap halved — more honest competition |
| High-Energy Lofi (edge) | Lofi dominated easily | Gym Hero (0.93 energy) nearly broke into top 3 | Energy contradiction became *visible* in scores |
| Ghost Genre | Max score 2.47 | Max score 3.94 | System recovered better from missing genre |
| Country + Romantic | Dusty Roads led by 1.45 pts | Dusty Roads led by only 0.41 pts | Velvet Nights (romantic mood match) almost caught up |

**Verdict: more accurate in some cases, just different in others.**

- The Deep Intense Rock gap closing from 2.03 → 1.06 felt *more honest* — a mood-matched pop song shouldn't outscore a sonically similar metal track by that much. Energy carrying more weight reflects that better.
- But the Chill Lofi profile (which was already working well) now produces scores above 5.0 (Library Rain: 5.41) because all four gates fired and energy tripled — making the absolute numbers harder to reason about.
- The original weights were **reverted** as the final design. The experiment confirmed genre dominance is a real tradeoff, not a bug — it's the intended strong prior. The fix for the catalog gap problem is more data, not lower genre weight.

---

---

### Profile 1 — High-Energy Pop

```
========================================================
  High-Energy Pop
  genre=pop  mood=happy  energy=0.9  acoustic=False
========================================================

#1  Sunrise City by Neon Echo
    Score  : 4.38 / 5.00
    Genre  : pop   Mood: happy   Energy: 0.82
    + genre match (+2.0)
    + mood match (+1.0)
    + energy similarity (+1.38)

#2  Gym Hero by Max Pulse
    Score  : 3.46 / 5.00
    Genre  : pop   Mood: intense   Energy: 0.93
    + genre match (+2.0)
    + energy similarity (+1.46)

#3  Rooftop Lights by Indigo Parade
    Score  : 2.29 / 5.00
    Genre  : indie pop   Mood: happy   Energy: 0.76
    + mood match (+1.0)
    + energy similarity (+1.29)

#4  Storm Runner by Voltline
    Score  : 1.49 / 5.00
    Genre  : rock   Mood: intense   Energy: 0.91
    + energy similarity (+1.48)

#5  Pulse Protocol by Grid Nine
    Score  : 1.49 / 5.00
    Genre  : electronic   Mood: energetic   Energy: 0.89
    + energy similarity (+1.48)
```

**What it shows:** Sunrise City wins again but with a slightly lower score than the default profile (4.38 vs 4.47) because energy=0.9 is further from Sunrise City's 0.82 than 0.8 was. Gym Hero climbs from 3.31 → 3.46 since 0.93 is now closer to the target.

---

### Profile 2 — Chill Lofi

```
========================================================
  Chill Lofi
  genre=lofi  mood=chill  energy=0.38  acoustic=True
========================================================

#1  Library Rain by Paper Lanterns
    Score  : 4.96 / 5.00
    Genre  : lofi   Mood: chill   Energy: 0.35
    + genre match (+2.0)
    + mood match (+1.0)
    + energy similarity (+1.46)
    + acoustic bonus (+0.5)

#2  Midnight Coding by LoRoom
    Score  : 4.94 / 5.00
    Genre  : lofi   Mood: chill   Energy: 0.42
    + genre match (+2.0)
    + mood match (+1.0)
    + energy similarity (+1.44)
    + acoustic bonus (+0.5)

#3  Focus Flow by LoRoom
    Score  : 3.97 / 5.00
    Genre  : lofi   Mood: focused   Energy: 0.40
    + genre match (+2.0)
    + energy similarity (+1.47)
    + acoustic bonus (+0.5)

#4  Spacewalk Thoughts by Orbit Bloom
    Score  : 2.85 / 5.00
    Genre  : ambient   Mood: chill   Energy: 0.28
    + mood match (+1.0)
    + energy similarity (+1.35)
    + acoustic bonus (+0.5)

#5  Coffee Shop Stories by Slow Stereo
    Score  : 1.99 / 5.00
    Genre  : jazz   Mood: relaxed   Energy: 0.37
    + energy similarity (+1.48)
    + acoustic bonus (+0.5)
```

**What it shows:** The Chill Lofi profile produced the highest individual score of all six runs (4.96). All four scoring gates fired for Library Rain. The acoustic bonus is doing real work here — it separates acoustic-friendly songs in spots #3–#5 from ones that would otherwise tie on energy alone.

---

### Profile 3 — Deep Intense Rock

```
========================================================
  Deep Intense Rock
  genre=rock  mood=intense  energy=0.9  acoustic=False
========================================================

#1  Storm Runner by Voltline
    Score  : 4.49 / 5.00
    Genre  : rock   Mood: intense   Energy: 0.91
    + genre match (+2.0)
    + mood match (+1.0)
    + energy similarity (+1.48)

#2  Gym Hero by Max Pulse
    Score  : 2.46 / 5.00
    Genre  : pop   Mood: intense   Energy: 0.93
    + mood match (+1.0)
    + energy similarity (+1.46)

#3  Pulse Protocol by Grid Nine
    Score  : 1.49 / 5.00
    Genre  : electronic   Mood: energetic   Energy: 0.89
    + energy similarity (+1.48)

#4  Iron Sermon by Fault Line
    Score  : 1.40 / 5.00
    Genre  : metal   Mood: aggressive   Energy: 0.97
    + energy similarity (+1.40)

#5  Sunrise City by Neon Echo
    Score  : 1.38 / 5.00
    Genre  : pop   Mood: happy   Energy: 0.82
    + energy similarity (+1.38)
```

**What it shows:** Storm Runner is the only rock song in the catalog, so it wins easily. The big gap between #1 (4.49) and #2 (2.46) reveals a catalog blind spot — there's essentially no competition in the rock genre. Iron Sermon (metal) scores only 1.40 despite being sonically close, because genre and mood both miss.

---

### Edge Case 1 — High-Energy Lofi (self-contradicting profile)

```
========================================================
  EDGE — High-Energy Lofi (contradiction)
  genre=lofi  mood=chill  energy=0.95  acoustic=False
========================================================

#1  Midnight Coding by LoRoom
    Score  : 3.71 / 5.00
    Genre  : lofi   Mood: chill   Energy: 0.42
    + genre match (+2.0)
    + mood match (+1.0)
    + energy similarity (+0.70)

#2  Library Rain by Paper Lanterns
    Score  : 3.60 / 5.00
    Genre  : lofi   Mood: chill   Energy: 0.35
    + genre match (+2.0)
    + mood match (+1.0)
    + energy similarity (+0.60)

#3  Focus Flow by LoRoom
    Score  : 2.67 / 5.00
    Genre  : lofi   Mood: focused   Energy: 0.40
    + genre match (+2.0)
    + energy similarity (+0.68)

#4  Spacewalk Thoughts by Orbit Bloom
    Score  : 1.50 / 5.00
    Genre  : ambient   Mood: chill   Energy: 0.28
    + mood match (+1.0)
    + energy similarity (+0.50)

#5  Gym Hero by Max Pulse
    Score  : 1.47 / 5.00
    Genre  : electronic   Mood: energetic   Energy: 0.89
    + energy similarity (+1.47)
```

**What it shows:** The algorithm doesn't crash — it just rewards genre+mood and ignores the contradiction. Lofi songs still dominate because genre (2.0) + mood (1.0) outweigh the energy penalty. A human would say "that's not a real preference," but the system silently accepts it. This exposes the lack of preference validation.

---

### Edge Case 2 — Ghost Genre (genre not in catalog)

```
========================================================
  EDGE — Ghost Genre (not in catalog)
  genre=k-pop  mood=happy  energy=0.8  acoustic=False
========================================================

#1  Sunrise City by Neon Echo
    Score  : 2.47 / 5.00
    Genre  : pop   Mood: happy   Energy: 0.82
    + mood match (+1.0)
    + energy similarity (+1.47)

#2  Rooftop Lights by Indigo Parade
    Score  : 2.44 / 5.00
    Genre  : indie pop   Mood: happy   Energy: 0.76
    + mood match (+1.0)
    + energy similarity (+1.44)

#3  Night Drive Loop by Neon Echo
    Score  : 1.43 / 5.00
    Genre  : synthwave   Mood: moody   Energy: 0.75
    + energy similarity (+1.42)

#4  Rise Up Sunday by Juno Ray
    Score  : 1.38 / 5.00
    Genre  : soul   Mood: uplifting   Energy: 0.72
    + energy similarity (+1.38)

#5  Pulse Protocol by Grid Nine
    Score  : 1.36 / 5.00
    Genre  : electronic   Mood: energetic   Energy: 0.89
    + energy similarity (+1.36)
```

**What it shows:** When the genre doesn't exist in the catalog, no song ever earns the +2.0 genre bonus. The top score drops from ~4.5 to just 2.47 — the recommender still works but confidence collapses. Every result is a weak match. A real system would warn the user that their preferred genre isn't available.

---

### Edge Case 3 — Conflicting Genre + Mood (no song satisfies both)

```
========================================================
  EDGE — Conflicting Genre + Mood (country + romantic)
  genre=country  mood=romantic  energy=0.5  acoustic=True
========================================================

#1  Dusty Backroads by Wren Hollis
    Score  : 3.92 / 5.00
    Genre  : country   Mood: nostalgic   Energy: 0.55
    + genre match (+2.0)
    + energy similarity (+1.42)
    + acoustic bonus (+0.5)

#2  Velvet Nights by Sable June
    Score  : 2.47 / 5.00
    Genre  : r&b   Mood: romantic   Energy: 0.52
    + mood match (+1.0)
    + energy similarity (+1.47)

#3  Midnight Coding by LoRoom
    Score  : 1.88 / 5.00
    Genre  : lofi   Mood: chill   Energy: 0.42
    + energy similarity (+1.38)
    + acoustic bonus (+0.5)

#4  Focus Flow by LoRoom
    Score  : 1.85 / 5.00
    Genre  : lofi   Mood: focused   Energy: 0.40
    + energy similarity (+1.35)
    + acoustic bonus (+0.5)

#5  Coffee Shop Stories by Slow Stereo
    Score  : 1.80 / 5.00
    Genre  : jazz   Mood: relaxed   Energy: 0.37
    + energy similarity (+1.30)
    + acoustic bonus (+0.5)
```

**What it shows:** No song in the catalog is both `country` and `romantic` — the genre only appears with `nostalgic` mood. The system is forced to choose: genre match wins (#1 Dusty Backroads, 3.92) over mood match (#2 Velvet Nights, 2.47), purely because genre is worth 2x more. The user wanted a romantic country song and got a nostalgic one instead — a real system would surface this tradeoff to the user.

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

