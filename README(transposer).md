# 🎵 Your_Transposer

A simple Python CLI tool for musicians to discover family chords and transpose chord progressions.

## Features

- Input any musical key (C, F#, Bb, etc.)
- Choose major or minor scale
- Instantly see the 7 family chords (diatonic chords) for that key
- Use the family chords **or** enter your own progression
- Transpose from **-14 to +14 semitones**

## How to Run

```bash
python your_transposer.py
```

No external dependencies — pure Python 3.

## Example Session

```
=================================================
         🎵  YOUR TRANSPOSER  🎵
=================================================

  Step 1: What key is the song in?
  Enter the key of the song (e.g. C, F#, Bb): G

  Step 2: Is it major or minor?
  Is the key major or minor? (major/minor): major

  Family chords for G major:
  Degree  Chord     Type
  ----------------------------
  I       G         (maj)
  II      Amin      (min)
  III     Bmin      (min)
  IV      C         (maj)
  V       D         (maj)
  VI      Emin      (min)
  VII     F#dim     (dim)

  Step 4: Would you like to use these family chords,
          or enter your own chord progression?
  Options:
  [1] Use the family chords above
  [2] Enter my own chord progression

  Your choice: 2
  Enter your chords: G, Em, C, D

  Step 5: How many semitones do you want to transpose?
  Enter semitones to transpose: -2

  Original   → G - Em - C - D
  Transposed (-2 semitones) → F - Dm - A# - C
```

## Notes

- Supports sharps (`C#`, `F#`) and flats (`Bb`, `Eb`)
- Handles enharmonic equivalents automatically
- Works with any chord suffix: `m`, `min`, `maj`, `dim`, `7`, `sus2`, etc.

## Requirements

- Python 3.10+

## License

MIT