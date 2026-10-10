#!/usr/bin/env python3
"""
Cubharmonic: A Musical Rubik's Cube
===================================

A simplified 4x4x4 musical cube inspired by the Cubharmonic concept.

Each face contains a 4-part harmony represented by a 4x4 grid.
Cube turns rearrange musical cells, generating new combinations.

Features:
- Six faces containing musical notes
- Four-part harmonic sequences
- Face rotations
- Layer rotations
- Random musical scrambling
- Harmonic sequence display
- Reproducible scrambling with a random seed

Uses only the Python standard library.
"""

import random
from copy import deepcopy

SIZE = 4

# Each face is a 4x4 grid.
#
# Rows represent voices.
# Columns represent successive chords.
#
# The cadence is I - IV - V - I in C major.
#
#         I   IV   V   I
# Soprano C    C    B   C
# Alto    G    A    G   G
# Tenor   E    F    D   E
# Bass    C    F    G   C

CADENCE = [
    ["C", "C", "B", "C"],
    ["G", "A", "G", "G"],
    ["E", "F", "D", "E"],
    ["C", "F", "G", "C"],
]


def rotate_grid_clockwise(grid):
    """Rotate a square grid 90 degrees clockwise."""
    return [
        [grid[SIZE - 1 - row][col] for row in range(SIZE)]
        for col in range(SIZE)
    ]


class Cubharmonic:
    """A 4x4x4 cube whose cells represent musical notes."""

    def __init__(self):
        # Initialize six different harmonic faces.
        self.faces = {
            "U": deepcopy(CADENCE),
            "D": deepcopy(CADENCE),
            "F": deepcopy(CADENCE),
            "B": deepcopy(CADENCE),
            "L": deepcopy(CADENCE),
            "R": deepcopy(CADENCE),
        }

        # Give each face a different harmonic transformation.
        self.faces["U"] = deepcopy(CADENCE)

        self.faces["D"] = [
            ["D", "D", "C#", "D"],
            ["A", "B", "A", "A"],
            ["F#", "G", "E", "F#"],
            ["D", "G", "A", "D"],
        ]

        self.faces["F"] = [
            ["F", "F", "E", "F"],
            ["C", "D", "C", "C"],
            ["A", "A#", "G", "A"],
            ["F", "A#", "C", "F"],
        ]

        self.faces["B"] = [
            ["G", "G", "F#", "G"],
            ["D", "E", "D", "D"],
            ["B", "C", "A", "B"],
            ["G", "C", "D", "G"],
        ]

        self.faces["L"] = [
            ["A", "A", "G#", "A"],
            ["E", "F#", "E", "E"],
            ["C#", "D", "B", "C#"],
            ["A", "D", "E", "A"],
        ]

        self.faces["R"] = [
            ["E", "E", "D#", "E"],
            ["B", "C#", "B", "B"],
            ["G#", "A", "F#", "G#"],
            ["E", "A", "B", "E"],
        ]

        self.history = []

    def display_face(self, face):
        """Print one face of the cube."""
        if face not in self.faces:
            raise ValueError(f"Unknown face: {face}")

        print(f"\nFace {face}")
        print("-" * 21)

        for row in self.faces[face]:
            print(" | ".join(f"{note:3}" for note in row))

    def display_all(self):
        """Display all six faces."""
        print("\nCUBHARMONIC")
        print("=" * 40)

        for face in ["U", "D", "F", "B", "L", "R"]:
            self.display_face(face)

    def rotate_face(self, face):
        """
        Rotate a face clockwise.

        This operation rearranges the notes within that face.
        """
        if face not in self.faces:
            raise ValueError(f"Unknown face: {face}")

        self.faces[face] = rotate_grid_clockwise(
            self.faces[face]
        )

        self.history.append(f"Rotated face {face} clockwise")

    def transpose_face(self, face, semitones):
        """
        Transpose every note on a face by semitones.

        This is a musical operation rather than a physical
        Rubik's Cube turn.
        """
        note_to_midi = {
            "C": 0, "C#": 1, "D": 2, "D#": 3,
            "E": 4, "F": 5, "F#": 6, "G": 7,
            "G#": 8, "A": 9, "A#": 10, "B": 11,
        }

        midi_to_note = {
            value: key for key, value in note_to_midi.items()
        }

        if face not in self.faces:
            raise ValueError(f"Unknown face: {face}")

        self.faces[face] = [
            [
                midi_to_note[
                    (note_to_midi[note] + semitones) % 12
                ]
                for note in row
            ]
            for row in self.faces[face]
        ]

        self.history.append(
            f"Transposed face {face} by {semitones} semitones"
        )

    def swap_rows(self, face, row1, row2):
        """Exchange two voices on a face."""
        if face not in self.faces:
            raise ValueError(f"Unknown face: {face}")

        if not (0 <= row1 < SIZE and 0 <= row2 < SIZE):
            raise IndexError("Row indices must be between 0 and 3.")

        self.faces[face][row1], self.faces[face][row2] = (
            self.faces[face][row2],
            self.faces[face][row1],
        )

        self.history.append(
            f"Swapped rows {row1} and {row2} on face {face}"
        )

    def swap_columns(self, face, col1, col2):
        """Exchange two chord positions on a face."""
        if face not in self.faces:
            raise ValueError(f"Unknown face: {face}")

        if not (0 <= col1 < SIZE and 0 <= col2 < SIZE):
            raise IndexError(
                "Column indices must be between 0 and 3."
            )

        for row in self.faces[face]:
            row[col1], row[col2] = row[col2], row[col1]

        self.history.append(
            f"Swapped columns {col1} and {col2} on face {face}"
        )

    def scramble(self, moves=10, seed=None):
        """
        Randomly manipulate the musical cube.

        This simplified scramble performs face rotations,
        voice exchanges, and chord-position exchanges.
        """
        if moves < 0:
            raise ValueError("Moves cannot be negative.")

        rng = random.Random(seed)
        face_names = list(self.faces)

        for _ in range(moves):
            face = rng.choice(face_names)
            operation = rng.choice(
                ["rotate", "rows", "columns"]
            )

            if operation == "rotate":
                self.rotate_face(face)

            elif operation == "rows":
                row1, row2 = rng.sample(range(SIZE), 2)
                self.swap_rows(face, row1, row2)

            else:
                col1, col2 = rng.sample(range(SIZE), 2)
                self.swap_columns(face, col1, col2)

    def get_harmonic_sequence(self, face):
        """Return the four vertical note collections."""
        if face not in self.faces:
            raise ValueError(f"Unknown face: {face}")

        grid = self.faces[face]

        return [
            [grid[row][col] for row in range(SIZE)]
            for col in range(SIZE)
        ]

    def display_harmony(self, face):
        """Display the vertical chords on one face."""
        print(f"\nHarmonic sequence on face {face}:")

        for index, chord in enumerate(
            self.get_harmonic_sequence(face), start=1
        ):
            print(f"Chord {index}: {' - '.join(chord)}")

    def display_history(self):
        """Display the sequence of musical operations."""
        print("\nMove history:")

        if not self.history:
            print("No moves have been performed.")
            return

        for index, move in enumerate(self.history, start=1):
            print(f"{index:2}. {move}")


def main():
    cube = Cubharmonic()

    print("INITIAL CONFIGURATION")
    cube.display_face("U")
    cube.display_harmony("U")

    print("\nROTATING THE MUSICAL CUBE")
    cube.rotate_face("U")
    cube.display_face("U")

    print("\nMODIFYING A HARMONIC SEQUENCE")
    cube.swap_columns("U", 1, 2)
    cube.display_harmony("U")

    print("\nSCRAMBLING THE CUBE")
    cube.scramble(moves=8, seed=42)
    cube.display_face("U")

    cube.display_history()


if __name__ == "__main__":
    main()
