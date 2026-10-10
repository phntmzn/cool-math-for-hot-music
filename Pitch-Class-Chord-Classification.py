#!/usr/bin/env python3
"""
Pitch-Class Chord Classification
=================================

Implements the mathematical operations described in
mathematical music theory:

- Pitch-class chords as subsets of Z_12
- Transpositions
- Inversions
- Transposition classes (T-orbits)
- Transposition-inversion classes (TI-orbits)
- Chord complements
- Lexicographically minimal TI representatives
- Compact interval representations

No external dependencies are required.
"""

from itertools import combinations

MODULUS = 12

PITCH_NAMES = (
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#",
    "B",
)


def validate_chord(chord):
    """Validate and normalize a pitch-class chord."""
    result = set()

    for pitch in chord:
        if not isinstance(pitch, int):
            raise TypeError("Pitch classes must be integers.")

        if not 0 <= pitch < MODULUS:
            raise ValueError(
                f"Pitch class {pitch} must be between 0 and 11."
            )

        result.add(pitch)

    return frozenset(result)


def transpose(chord, t):
    """
    Transpose every pitch class by t semitones.

    T_t+(x) = (x + t) mod 12
    """
    chord = validate_chord(chord)
    t %= MODULUS

    return frozenset(
        (pitch + t) % MODULUS
        for pitch in chord
    )


def invert(chord, t=0):
    """
    Invert every pitch class around axis t.

    T_t-(x) = (t - x) mod 12
    """
    chord = validate_chord(chord)
    t %= MODULUS

    return frozenset(
        (t - pitch) % MODULUS
        for pitch in chord
    )


def complement(chord):
    """Return the complement of a chord in Z_12."""
    chord = validate_chord(chord)

    return frozenset(
        pitch
        for pitch in range(MODULUS)
        if pitch not in chord
    )


def chord_vector(chord):
    """
    Represent a chord as a binary sequence of length 12.

    0 means the pitch class is absent.
    1 means the pitch class is present.
    """
    chord = validate_chord(chord)

    return tuple(
        1 if pitch in chord else 0
        for pitch in range(MODULUS)
    )


def format_chord(chord):
    """Format a chord using pitch names."""
    chord = sorted(validate_chord(chord))

    if not chord:
        return "∅"

    return "{" + ", ".join(
        PITCH_NAMES[pitch] for pitch in chord
    ) + "}"


def transposition_orbit(chord):
    """Generate the T-orbit of a chord."""
    chord = validate_chord(chord)

    return {
        transpose(chord, t)
        for t in range(MODULUS)
    }


def transposition_inversion_orbit(chord):
    """Generate the TI-orbit of a chord."""
    chord = validate_chord(chord)

    orbit = set()

    for t in range(MODULUS):
        orbit.add(transpose(chord, t))
        orbit.add(invert(chord, t))

    return orbit


def ti_prime_form(chord):
    """
    Return the lexicographically minimal binary vector
    in the chord's transposition-inversion orbit.

    This follows the binary-vector ordering described
    in the mathematical text.
    """
    orbit = transposition_inversion_orbit(chord)

    representative = min(
        orbit,
        key=chord_vector
    )

    return representative


def interval_class_vector(chord):
    """
    Calculate the interval-class vector.

    Entry i counts unordered pitch pairs at interval
    class i, for i = 1, ..., 6.
    """
    chord = sorted(validate_chord(chord))
    counts = [0] * 6

    for i, p1 in enumerate(chord):
        for p2 in chord[i + 1:]:
            interval = (p2 - p1) % MODULUS
            interval_class = min(
                interval,
                MODULUS - interval
            )

            counts[interval_class - 1] += 1

    return tuple(counts)


def all_chords_of_size(size):
    """Generate every chord containing exactly size pitches."""
    if not 0 <= size <= MODULUS:
        raise ValueError("Chord size must be between 0 and 12.")

    return (
        frozenset(chord)
        for chord in combinations(range(MODULUS), size)
    )


def ti_class_representatives(size):
    """
    Generate one lexicographically minimal representative
    for each TI-class of the specified cardinality.

    The result is sorted by binary-vector ordering.
    """
    representatives = set()

    for chord in all_chords_of_size(size):
        representatives.add(ti_prime_form(chord))

    return sorted(
        representatives,
        key=chord_vector
    )


def demonstrate(chord, name="Chord"):
    """Display the main classifications for a chord."""
    chord = validate_chord(chord)

    print(f"\n{'=' * 50}")
    print(name)
    print(f"{'=' * 50}")

    print("Chord:", format_chord(chord))
    print("Pitch classes:", sorted(chord))
    print("Binary vector:", chord_vector(chord))

    print("\nTransposition by 2:")
    print(format_chord(transpose(chord, 2)))

    print("\nInversion around C:")
    print(format_chord(invert(chord, 0)))

    print("\nComplement:")
    print(format_chord(complement(chord)))

    print("\nT-orbit size:")
    print(len(transposition_orbit(chord)))

    print("\nTI-orbit size:")
    print(len(transposition_inversion_orbit(chord)))

    print("\nTI prime form:")
    print(format_chord(ti_prime_form(chord)))

    print("\nInterval-class vector:")
    print(interval_class_vector(chord))


def main():
    # C-major triad.
    c_major = {0, 4, 7}

    demonstrate(c_major, "C Major Triad")

    # D-major triad.
    d_major = {2, 6, 9}

    demonstrate(d_major, "D Major Triad")

    # Enumerate TI-class representatives for triads.
    print("\n\nTI-Class Representatives for Triads")
    print("=" * 50)

    representatives = ti_class_representatives(3)

    for number, chord in enumerate(representatives, start=1):
        print(
            f"{number:2}. {format_chord(chord):20}"
            f" Binary: {chord_vector(chord)}"
        )

    print(
        f"\nTotal TI classes of three-note chords: "
        f"{len(representatives)}"
    )


if __name__ == "__main__":
    main()
