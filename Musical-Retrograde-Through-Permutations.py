#!/usr/bin/env python3
"""
Musical Retrograde Through Permutations
=======================================

Demonstrates how a melody's retrograde can be constructed
through successive transpositions (i, 10).

The melody's notes are numbered 1 through 10 according
to their onset order.

Each transposition swaps two note positions.
"""

from math import factorial


def swap_positions(permutation, i, j):
    """Swap two positions in a permutation."""
    result = list(permutation)

    # Convert mathematical positions (1-based) to Python indices.
    result[i - 1], result[j - 1] = (
        result[j - 1],
        result[i - 1],
    )

    return result


def retrograde(permutation):
    """Return the retrograde permutation."""
    return list(reversed(permutation))


def inversion_decomposition(n):
    """
    Construct the transposition decomposition of the
    reversal permutation using swaps with position n.

    The decomposition is obtained by sorting the target
    reversal permutation into the identity permutation.
    The resulting swaps are then reversed.
    """
    target = list(range(n, 0, -1))
    current = target.copy()
    swaps = []

    # Sort the target into the identity by swapping
    # positions i and n.
    for i in range(1, n):
        if current[i - 1] != i:
            j = current.index(i) + 1

            if j != n:
                raise ValueError(
                    "Unexpected permutation structure."
                )

            current = swap_positions(current, i, n)
            swaps.append((i, n))

    # Sorting swaps transform retrograde into original.
    # Reverse them to construct retrograde from original.
    return list(reversed(swaps))


def apply_transposition_sequence(melody, swaps):
    """Yield every intermediate melody after each swap."""
    current = list(melody)

    yield current.copy()

    for i, j in swaps:
        current = swap_positions(current, i, j)
        yield current.copy()


def cycle_decomposition(permutation):
    """
    Express a permutation as disjoint cycles.

    A permutation is represented as a list of images:
    permutation[i - 1] is the image of i.
    """
    n = len(permutation)
    visited = [False] * n
    cycles = []

    for start in range(1, n + 1):
        if visited[start - 1]:
            continue

        cycle = []
        current = start

        while not visited[current - 1]:
            visited[current - 1] = True
            cycle.append(current)
            current = permutation[current - 1]

        if len(cycle) > 1:
            cycles.append(cycle)

    return cycles


def format_cycles(cycles):
    """Format cycles using standard mathematical notation."""
    if not cycles:
        return "()"

    return "".join(
        "(" + " ".join(map(str, cycle)) + ")"
        for cycle in cycles
    )


def main():
    # The original melody is represented by note labels.
    melody = list(range(1, 11))
    n = len(melody)

    # The retrograde reverses the onset order.
    target = retrograde(melody)

    # Find swaps that produce the retrograde.
    swaps = inversion_decomposition(n)

    # Display the original and target.
    print("Original:  ", melody)
    print("Retrograde:", target)

    print("\nTransposition decomposition:")

    for i, (left, right) in enumerate(swaps, start=1):
        print(f"{i:2}. ({left},{right})")

    print(f"\nNumber of transpositions: {len(swaps)}")

    # Display all intermediate melodies.
    print("\nIntermediate melodies:")

    for step, version in enumerate(
        apply_transposition_sequence(melody, swaps)
    ):
        if step == 0:
            label = "Original"
        elif step == len(swaps):
            label = "Retrograde"
        else:
            label = f"Step {step}"

        print(f"{label:12}: {version}")

    # Display the cycle representation.
    cycles = cycle_decomposition(target)

    print("\nRetrograde permutation in cycle notation:")
    print(format_cycles(cycles))

    # Verify the result.
    assert list(
        apply_transposition_sequence(melody, swaps)
    )[-1] == target

    print("\nVerification successful!")


if __name__ == "__main__":
    main()
