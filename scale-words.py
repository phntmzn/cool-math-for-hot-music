#!/usr/bin/env python3
"""
Musical Scale Words
===================

Represent musical scales as words over the alphabet A = {a, b}.

a = 1 semitone
b = 2 semitones

Generate pitch classes, repeat scale words, and explore
octave-compatible and non-octave-compatible scales.
"""

from itertools import accumulate

# Pitch names using sharps.
PITCH_NAMES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]

# Map letters to semitone intervals.
INTERVALS = {
    "a": 1,
    "b": 2,
}


def validate_word(word):
    """Ensure the word contains only valid alphabet letters."""
    word = word.lower()

    if not word:
        raise ValueError("The scale word cannot be empty.")

    invalid = set(word) - set(INTERVALS)

    if invalid:
        raise ValueError(
            f"Invalid letters: {invalid}. Use only 'a' and 'b'."
        )

    return word


def word_to_intervals(word):
    """Convert a word into a sequence of semitone intervals."""
    word = validate_word(word)
    return [INTERVALS[letter] for letter in word]


def repeat_word(word, repetitions):
    """Repeat a scale word a specified number of times."""
    word = validate_word(word)

    if repetitions < 1:
        raise ValueError("Repetitions must be at least 1.")

    return word * repetitions


def generate_pitch_classes(word, repetitions=1, start=0):
    """
    Generate pitches modulo 12.

    The starting pitch is included.
    The final pitch after all intervals is also included.
    """
    repeated = repeat_word(word, repetitions)
    intervals = word_to_intervals(repeated)

    pitches = [start % 12]
    current = start

    for interval in intervals:
        current += interval
        pitches.append(current % 12)

    return pitches


def generate_absolute_pitches(word, repetitions=1, start=0):
    """
    Generate pitches without reducing modulo 12.

    This allows pitches to continue across octave boundaries.
    C4 is represented by 0, C#4 by 1, and C5 by 12.
    """
    repeated = repeat_word(word, repetitions)
    intervals = word_to_intervals(repeated)

    pitches = [start]
    current = start

    for interval in intervals:
        current += interval
        pitches.append(current)

    return pitches


def pitch_name(pitch):
    """Convert a pitch number to a pitch name."""
    return PITCH_NAMES[pitch % 12]


def format_pitches(pitches):
    """Format a list of pitches as readable pitch names."""
    return " ".join(pitch_name(pitch) for pitch in pitches)


def scale_information(word):
    """Display the interval and octave properties of a word."""
    word = validate_word(word)
    intervals = word_to_intervals(word)
    total = sum(intervals)

    print(f"Word: {word}")
    print(f"Intervals: {intervals}")
    print(f"Total interval: {total} semitones")
    print(f"Octave-compatible: {total % 12 == 0}")


def demonstrate(title, word, repetitions=1):
    """Print a scale-word demonstration."""
    print(f"\n--- {title} ---")

    scale_information(word)

    pitches = generate_pitch_classes(word, repetitions)
    print("Pitch classes:", format_pitches(pitches))

    absolute = generate_absolute_pitches(word, repetitions)
    print("Absolute pitches:", format_pitches(absolute))


def main():
    # D major: whole, whole, half, whole, whole, whole, half.
    d_major = "bbabbba"

    # The interval pattern given in the passage for D minor.
    d_minor = "babbbba"

    demonstrate("D Major", d_major)
    demonstrate("D Minor (as given in the passage)", d_minor)

    # First Messiaen scale: whole-tone scale.
    demonstrate("First Messiaen Scale", "b", repetitions=6)

    # Second Messiaen scale.
    demonstrate("Second Messiaen Scale", "ba", repetitions=4)

    # Third Messiaen scale.
    demonstrate("Third Messiaen Scale", "aab", repetitions=3)

    # Non-octave-compatible word.
    demonstrate("Non-Octave Word: bba", "bba", repetitions=5)


if __name__ == "__main__":
    main()
