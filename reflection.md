# Reflection: Profile Comparisons

This file compares pairs of user profiles and explains — in plain language — why the recommendations changed between them and whether those changes make sense.

---

## Pair 1: High-Energy Pop vs. Deep Intense Rock

Both profiles ask for high energy (0.9) and an intense or happy mood. The difference is genre.

For **High-Energy Pop**, Sunrise City came in first with a score of 4.47. It matched on genre (pop), mood (happy), and energy (0.82 — very close to 0.9). Gym Hero came in second, also a pop song, but with an "intense" mood instead of "happy," so it lost a point there.

For **Deep Intense Rock**, Storm Runner took first place with 4.49. It matched on genre (rock), mood (intense), and energy (0.91). But the gap between first and second was enormous — 4.49 versus 2.46. That's because there is only one rock song in the entire catalog. After Storm Runner, the system had nothing left to offer in that genre, so it started grabbing whatever was energetic, regardless of genre or mood.

**What this tells us:** The genre label is doing most of the heavy lifting. Both profiles asked for something energetic and intense, but the system treats "rock" and "pop" as completely separate worlds. A song like Gym Hero — loud, fast, workout-ready — would feel perfectly at home on a rock fan's playlist, but it scored 2.46 for the rock profile purely because its genre tag says "pop." The system is reading labels, not listening to music.

---

## Pair 2: Chill Lofi vs. High-Energy Lofi (Edge Case)

These two profiles have the same genre (lofi) and the same mood (chill). The only difference is energy — 0.38 for the genuine Chill Lofi listener, and 0.95 for the contradictory edge case.

For the **Chill Lofi** profile, Library Rain scored 4.96 out of 5.5 — the highest score across all six test runs. Every single scoring gate fired: genre matched, mood matched, energy was nearly identical (0.35 vs 0.38), and the song is highly acoustic (0.86), which triggered the acoustic bonus. This was the system working exactly as intended.

For the **High-Energy Lofi** edge case, those same lofi songs still came in first — but their scores dropped noticeably (Midnight Coding fell from 4.94 to 3.71) because their energy of around 0.40 was now far from the target of 0.95. Here is what got interesting: Gym Hero, a pop workout track with energy 0.93, sneaked into the top five with a score of 2.94, almost tying some lofi songs. It had nothing in common with the user's stated genre or mood — it just happened to have the right energy.

**What this tells us:** When you ask for something contradictory — "I want calm, mellow, chill music, but at maximum intensity" — the system does not push back or warn you. It silently tries its best and ends up recommending a mix of songs that satisfy different parts of your request separately, rather than together. The end result would genuinely confuse a real listener.

---

## Pair 3: Ghost Genre (k-pop) vs. Conflicting Genre + Mood (country + romantic)

Both profiles are designed to give the system an impossible task, but in different ways. The Ghost Genre has a preference for a genre that simply does not exist in the catalog. The Conflicting profile has a genre that exists, but no song in that genre has the right mood.

For the **Ghost Genre** profile, the genre bonus never fired for anyone. Every recommendation scored at most 2.47, built entirely from mood similarity and energy proximity. The top result was Sunrise City — a pop song — not because it matched k-pop in any real sense, but because it was happy-mood and high-energy and those were the only signals left.

For the **Conflicting Genre + Mood** profile, the system was forced to choose between two things it could not have at the same time: a country song (only one exists: Dusty Backroads, mood=nostalgic) or a romantic song (only one exists: Velvet Nights, genre=r&b). It chose the country song at 3.92, ahead of the romantic song at 2.47, purely because genre is worth twice as much as mood in the formula.

**What this tells us:** These two edge cases reveal the same underlying problem from different angles. When the user's most important preference cannot be satisfied, the system never says so. The Ghost Genre profile wanted k-pop and got pop as a consolation prize. The Conflicting profile wanted romantic country and got nostalgic country instead — the genre won the tiebreak, but the user asked for both. A real music app would surface this tradeoff and let the user decide which preference matters more to them.

---

## Why Does Gym Hero Keep Showing Up?

Gym Hero (pop, intense, energy=0.93) appeared in the top five results for the High-Energy Pop, Deep Intense Rock, and High-Energy Lofi profiles. For a song about working out, that is a suspiciously wide reach.

The reason is that energy is the only scoring signal that fires for *every single song* in the catalog, every single time, no matter what. Genre and mood are all-or-nothing: you either match or you get zero. But energy similarity always produces a number between 0 and 1.5, even if the song is otherwise completely wrong for you.

Gym Hero has an energy of 0.93 — one of the highest in the catalog. Any profile that sets a high energy target (0.8 or above) will automatically pull Gym Hero toward the top of the list because it keeps earning strong energy similarity points while other songs do not. It is not a recommendation in any meaningful sense. It is a side effect of the formula.

Think of it like a search engine that always surfaces the same popular webpage near the top, not because it is relevant to your question, but because it has been clicked a lot and the algorithm gives it free points every time. Gym Hero is that webpage. The fix is to either lower the energy weight, add a minimum score threshold before a song qualifies as a recommendation, or expand the catalog so there are enough genuinely good matches to push energy-only results out of the top five.
