# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeMatch 1.0**

A lightweight, rule-based music recommender that matches songs to a listener's current mood, genre preference, and energy level.

---

## 2. Intended Use

**What it's for:**
- Suggesting songs from a small catalog based on how a user feels right now.
- Classroom exploration of how scoring and ranking logic works in real recommender systems.
- Learning how features like energy and mood can be turned into a number that drives decisions.

**What it's NOT for:**
- Real production use. The catalog is 18 songs — it will run out of good matches fast.
- Replacing a streaming app. It has no listening history, no collaborative filtering, and no awareness of what the user has already heard.
- Making decisions for real users. It has no confidence threshold, so it will recommend something even when nothing in the catalog fits.

---

## 3. How the Model Works

When you tell the system your preferred genre, mood, energy level, and whether you like acoustic music, it goes through every song in the catalog one by one and gives each one a score out of 5 points.

Here is how the points work:

- **Genre match** gives 2 points. This is the biggest single signal. If the song's genre tag matches yours exactly, it gets the full 2 points. If not, it gets nothing.
- **Mood match** gives 1 point. Same idea — exact match gets the point, everything else gets zero.
- **Energy similarity** gives up to 1.5 points. This one is a sliding scale, not all-or-nothing. A song with energy very close to your target gets nearly 1.5. A song with the opposite energy gets close to zero. The further away, the less it scores.
- **Acoustic bonus** gives 0.5 points, but only if you said you like acoustic music and the song actually is acoustic. It does not apply otherwise.

After every song gets a score, the system sorts them from highest to lowest and hands back the top 5.

---

## 4. Data

The catalog contains **18 songs** stored in a CSV file. Each song has a title, artist, genre, mood, and several numeric audio features: energy (how loud and intense it feels), tempo in BPM, valence (how positive or sad it sounds), danceability, and acousticness.

There are **14 distinct genres** in the catalog. Most genres have only one song. Lofi has three, pop has two, and everything else — rock, metal, jazz, folk, soul, classical, ambient, country, r&b, synthwave, electronic, hip-hop, and indie pop — has exactly one.

There are **13 distinct moods**. Chill appears three times, happy and intense each appear twice. Every other mood has one song.

**Gaps worth noting:**
- No hip-hop, Latin, reggae, blues, or punk.
- The catalog skews slightly toward Western popular music genres.
- High-energy songs (0.7+) make up 8 of the 18 entries — more than low or mid-energy.
- No data was added or removed from the starter CSV.

---

## 5. Strengths

The system works best when the catalog actually has songs in the user's preferred genre. The Chill Lofi profile is the clearest example — it found three lofi songs, two of which matched on genre, mood, and energy, and the top result scored 4.96 out of 5. That felt genuinely accurate.

It is also good at being transparent. Every recommendation comes with a plain-English explanation: "genre match (+2.0) | mood match (+1.0) | energy similarity (+1.47)." A user can see exactly why a song was chosen, which is something most real recommenders never show you.

The energy similarity score works well for distinguishing between songs in the same genre. When two lofi songs both match the genre and mood, the one with closer energy wins — and that tiebreak felt correct every time it was tested.

---

## 6. Limitations and Bias

**The single-song genre trap** is the most significant weakness uncovered during testing. Twelve out of fourteen genres in the catalog have exactly one representative song — meaning a user who prefers rock, metal, jazz, country, or folk will always get that one song as an automatic winner, not because it genuinely matches their taste, but simply because nothing else can compete for the +2.0 genre bonus. In the Deep Intense Rock experiment, Storm Runner scored 4.49 while #2 only reached 2.46 — a 2-point gap caused by catalog thinness, not scoring quality. The system confidently presents this as a "great match" with no way to signal that it's really just "the only match."

**Energy similarity creates a false floor for bad recommendations.** Every single song in the catalog earns *some* energy similarity points, even when it's a terrible match — because the formula `1.5 × (1 − distance)` never goes negative. This means slots #4 and #5 in almost every profile are filled by songs that share nothing with the user except a vaguely similar energy level. The system outputs five recommendations with the same formatting and confidence regardless of whether it found five good matches or one good match and four accidental ones.

**Users who don't like acoustic music have no voice in the scoring.** The acoustic bonus (+0.5) rewards users who prefer organic, acoustic sounds — but there is no equivalent penalty for users who actively prefer electronic or produced music. A user whose ideal song is something like a synthesizer-heavy electronic track will still see highly acoustic songs score identically to an electronic track on energy similarity, with no downward adjustment. The preference only flows in one direction, which means acoustic-averse users are effectively invisible to part of the algorithm.

---

## 7. Evaluation

Six user profiles were tested — three meant to represent realistic listeners, and three designed to break or stress-test the system on purpose.

The **realistic profiles** were High-Energy Pop (genre=pop, mood=happy, energy=0.9), Chill Lofi (genre=lofi, mood=chill, energy=0.38, likes_acoustic=True), and Deep Intense Rock (genre=rock, mood=intense, energy=0.9). For each one, the goal was to check whether the top result felt like something a real person would actually want to hear. For the most part it did — Storm Runner was the obvious pick for a rock fan, and Library Rain felt exactly right for someone who wanted quiet, acoustic background music to study to.

The **edge-case profiles** were designed to expose cracks. A "High-Energy Lofi" profile deliberately asked for things that contradict each other — lofi music is by nature slow and soft, but the energy target was set to 0.95. A "Ghost Genre" profile asked for k-pop, which doesn't exist in the catalog at all. A "Conflicting Genre + Mood" profile asked for country music with a romantic mood, even though the only country song in the catalog has a nostalgic mood, not a romantic one.

**What surprised me most** was how confidently the system behaved even when it had nothing good to offer. When the Ghost Genre profile ran, the top result scored only 2.47 out of 5.0 — barely half marks — but the output looked identical to a strong recommendation. There was no warning, no asterisk, no "we couldn't find a great match." The system just quietly handed over whatever came closest. In a real app, a user would have no idea they were getting a consolation prize.

A second surprise was how often **Gym Hero kept appearing** for profiles it had no business serving. It showed up in the High-Energy Pop, Deep Intense Rock, and even the High-Energy Lofi edge case. The reason is simple: Gym Hero has a very high energy value (0.93), and energy similarity is the only signal that fires for *every* song no matter what. So whenever a user wants high energy and nothing else matches well, Gym Hero floats up by default. It is not a recommendation — it is an energy-proximity accident.

---

## 8. Future Work

**Add a minimum score threshold.** Right now the system always returns exactly k results, even if the best match is weak. A simple fix would be to only show songs that scored above, say, 2.5 out of 5.0 — and tell the user honestly when fewer than k songs cleared the bar. That alone would eliminate the "consolation prize" problem.

**Score more audio features continuously.** Energy is the only numeric feature being scored on a sliding scale. Valence (how happy vs. sad a song sounds) and acousticness would both improve results if scored the same way. A user who wants something melancholic would benefit from a valence proximity score, not just a mood label match.

**Expand the catalog.** Most improvements to the weights and formula are limited by having only one or two songs per genre. Adding 5–10 songs per genre would let the scoring algorithm do real work instead of defaulting to the only available option. More data is the highest-leverage change.

---

## 9. Personal Reflection

**My biggest learning moment** was realizing that the hardest part of this project wasn't writing the code — it was deciding what the numbers should mean. Choosing to give genre 2.0 points and mood only 1.0 felt arbitrary at first, like I was just making things up. But then I ran the Deep Intense Rock profile and saw a 2-point gap between first and second place, entirely because there was only one rock song in the catalog. That moment made the weight choice feel real and consequential. I wasn't just typing numbers into a formula — I was making a design decision that quietly shaped what every single user would see. That's a different kind of responsibility than getting the syntax right.

**Using AI tools helped a lot, but I had to stay in the driver's seat.** The AI was fast at helping structure the scoring function, suggesting the `sorted()` vs `.sort()` distinction, and drafting sections of the model card. But there were moments where I had to slow down and verify. Early on, a suggested implementation would have worked syntactically but silently returned the wrong data type — strings instead of floats — which would have broken the math later. I only caught it because I checked the CSV against what the code was actually doing. The AI gave me a solid first draft almost every time, but "looks right" and "is right" are not the same thing. The tool is most useful when you already understand what you're trying to build well enough to recognize when something is off.

**What surprised me most** was how easily a handful of arithmetic rules could produce output that feels like a real recommendation. When Sunrise City came back as the top pick for the happy/pop/0.8 profile with a score of 4.47, it genuinely felt correct — like the system understood something. But it didn't understand anything. It just multiplied and subtracted. That gap between "feels intelligent" and "is actually intelligent" is something I'll think about every time I see a "recommended for you" section anywhere. The algorithm doesn't know music. It knows numbers that happen to describe music. The feeling of a good recommendation is partly an illusion created by good labeling and enough data.

**If I extended this project**, the first thing I'd try is scoring valence — the happy-vs-sad dimension — the same way energy is currently scored, as a sliding scale instead of a mood label. Right now two songs can both have the mood tag "chill" but one might sound gloomy and the other breezy; the system can't tell the difference. Adding a `target_valence` field to the user profile and scoring it continuously would make the recommendations feel more emotionally accurate. After that, I'd add a minimum score cutoff so the system stops pretending it found five good matches when it really only found two. And eventually, I'd want to try a genre similarity map — so that "metal" and "rock" are treated as neighbors rather than strangers, and a metal song could earn partial genre credit for a rock user instead of zero.
