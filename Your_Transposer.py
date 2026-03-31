"""
Your_Transposer
A CLI tool to recommend family chords and transpose them to any key.

"""

CHROMATIC = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

ENHARMONIC = {"DB": "C#", "EB": "D#", "FB": "E", "GB": "F#","AB": "G#", "BB": "A#", "CB": "B","E#": "F", "B#": "C",}


MAJOR_INTERVALS   = [0, 2, 4, 5, 7, 9, 11]
MINOR_INTERVALS   = [0, 2, 3, 5, 7, 8, 10]

MAJOR_CHORD_TYPES = ["maj", "min", "min", "maj", "maj", "min", "dim"]
MINOR_CHORD_TYPES = ["min", "dim", "maj", "min", "min", "maj", "maj"]

DEGREE_NAMES_MAJOR = ["I",  "II",  "III",  "IV",  "V",  "VI",  "VII"]
DEGREE_NAMES_MINOR = ["i",  "ii°", "III",  "iv",  "v",  "VI",  "VII"]


def normalize_note(note: str) -> str | None:
    note = note.strip().upper()
    note = note.replace("♭", "B").replace("♯", "#")
    if note in ENHARMONIC:
        note = ENHARMONIC[note]
    if note in CHROMATIC:
        return note
    return None


def get_family_chords(root: str, scale: str) -> list[tuple[str, str, str]]:
    root_idx = CHROMATIC.index(root)
    intervals   = MAJOR_INTERVALS   if scale == "major" else MINOR_INTERVALS
    chord_types = MAJOR_CHORD_TYPES if scale == "major" else MINOR_CHORD_TYPES
    degrees     = DEGREE_NAMES_MAJOR if scale == "major" else DEGREE_NAMES_MINOR

    chords = []
    for i, (interval, ctype, degree) in enumerate(zip(intervals, chord_types, degrees)):
        note = CHROMATIC[(root_idx + interval) % 12]
        chords.append((degree, note, ctype))
    return chords


def transpose_note(note: str, semitones: int) -> str:
    idx = CHROMATIC.index(note)
    return CHROMATIC[(idx + semitones) % 12]


def parse_chord(chord_str: str) -> tuple[str, str] | None:
    """Parse a chord string like 'Cm', 'F#maj', 'Bb', 'Ddim' into (root, suffix)."""
    chord_str = chord_str.strip().upper().replace("♭", "B").replace("♯", "#")
    if len(chord_str) == 0:
        return None

    # Extract root (1 or 2 chars)
    if len(chord_str) >= 2 and chord_str[1] in ("#", "B"):
        root_raw = chord_str[:2]
        suffix   = chord_str[2:]
    else:
        root_raw = chord_str[:1]
        suffix   = chord_str[1:]

    if root_raw in ENHARMONIC:
        root_raw = ENHARMONIC[root_raw]

    if root_raw not in CHROMATIC:
        return None

    return root_raw, suffix.lower()


def transpose_chord(chord_str: str, semitones: int) -> str:
    parsed = parse_chord(chord_str)
    if parsed is None:
        return chord_str  # return as-is if unrecognised
    root, suffix = parsed
    new_root = transpose_note(root, semitones)
    return new_root + suffix


def print_header():
    print("\n" + "=" * 50)
    print("         🎵  YOUR TRANSPOSER  🎵")
    print("=" * 50 + "\n")


def print_family_table(chords: list[tuple[str, str, str]]):
    print("\n  Family chords:\n")
    print(f"  {'Degree':<6}  {'Chord':<8}  {'Type'}")
    print("  " + "-" * 28)
    for degree, note, ctype in chords:
        chord_name = note + ("" if ctype == "maj" else ctype)
        print(f"  {degree:<6}  {chord_name:<8}  ({ctype})")
    print()


def get_key_input() -> str:
    while True:
        raw = input("  Enter the key of the song (e.g. C, F#, Bb): ").strip()
        note = normalize_note(raw)
        if note:
            return note
        print(f"  ✗  '{raw}' is not a valid note. Try again (e.g. C, D, E, F, G, A, B, C#, Bb).\n")


def get_scale_input() -> str:
    while True:
        raw = input("  Is the key major or minor? (major/minor): ").strip().lower()
        if raw in ("major", "minor", "maj", "min"):
            return "major" if raw in ("major", "maj") else "minor"
        print("  ✗  Please type 'major' or 'minor'.\n")


def get_chord_choice(family_chords: list[tuple[str, str, str]]) -> list[str]:
    print("  Options:")
    print("  [1] Use the family chords above")
    print("  [2] Enter my own chord progression\n")
    while True:
        choice = input("  Your choice (1 or 2): ").strip()
        if choice == "1":
            again = input("  Transpose again? (y/n): ").strip().lower()
            if again in ("y", "yes"):
                main()
            else:
                print("\n  Thanks for using Your_Transposer! \n")
                print("\n Happy Music bye bye....swagieee!!!")
        if choice == "2":
            raw = input("\n  Enter your chords separated by commas (e.g. C, Am, F, G): ")
            chords = [c.strip() for c in raw.split(",") if c.strip()]
            if chords:
                return chords
            print("  ✗  No chords detected. Try again.\n")
        else:
             print("  ✗  Please enter 1 or 2.\n")


def get_semitones() -> int:
    print("\n  Transpose range: -14 to +14 semitones")
    print("  (negative = lower, positive = higher, 0 = no change)\n")
    while True:
        raw = input("  Enter semitones to transpose: ").strip()
        try:
            val = int(raw)
            if -14 <= val <= 14:
                return val
            print("  ✗  Please enter a number between -14 and +14.\n")
        except ValueError:
            print("  ✗  Please enter a whole number.\n")


def print_transposed(original: list[str], semitones: int):
    transposed = [transpose_chord(c, semitones) for c in original]
    direction  = f"+{semitones}" if semitones >= 0 else str(semitones)

    print("\n" + "-" * 50)
    print(f"  Original   → {' - '.join(original)}")
    print(f"  Transposed ({direction} semitones) → {' - '.join(transposed)}")
    print("-" * 50 + "\n")


def main():
    print_header()

    # Step 1 – key
    print("  Step 1: What key is the song in?")
    root = get_key_input()

    # Step 2 – major / minor
    print("\n  Step 2: Is it major or minor?")
    scale = get_scale_input()

    # Step 3 – show family chords
    family = get_family_chords(root, scale)
    print(f"\n  Family chords for {root} {scale}:")
    print_family_table(family)

    # Step 4 – choose chords
    print("  Step 4: Would you like to use these family chords,")
    print("          or enter your own chord progression?")
    chords = get_chord_choice(family)

    print(f"\n  Chords selected: {' - '.join(chords)}")

    # Step 5 – transpose
    print("\n  Step 5: How many semitones do you want to transpose?")
    semitones = get_semitones()

    if semitones == 0:
        print("\n  No transposition applied — chords stay the same.\n")
        print(f"  Chords: {' - '.join(chords)}\n")
    else:
        print_transposed(chords, semitones)

    # Loop option
    again = input("  Transpose again? (y/n): ").strip().lower()
    if again in ("y", "yes"):
        main()
    else:
        print("\n  Thanks for using Your_Transposer! \n")
        print("\n  Happy Music swagieee!!!")




if __name__ == "__main__":
    main()
