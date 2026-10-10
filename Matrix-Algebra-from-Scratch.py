#!/usr/bin/env python3
"""
Matrix Algebra from Scratch
===========================

Implements basic matrix operations:

- Matrix creation and validation
- Matrix addition
- Scalar multiplication
- Matrix transposition
- Identity matrices
- Matrix multiplication
- Matrix-vector multiplication
- Equality testing

Matrices are represented as lists of lists.
The implementation uses ordinary Python numbers.
"""

from numbers import Number


class Matrix:
    """A basic matrix class for algebraic operations."""

    def __init__(self, rows):
        if not rows:
            raise ValueError("A matrix must have at least one row.")

        if not rows[0]:
            raise ValueError("A matrix must have at least one column.")

        width = len(rows[0])

        if any(len(row) != width for row in rows):
            raise ValueError("All matrix rows must have equal length.")

        self.rows = [list(row) for row in rows]
        self.m = len(rows)
        self.n = width

    @classmethod
    def zeros(cls, m, n):
        """Create an m-by-n zero matrix."""
        if m < 1 or n < 1:
            raise ValueError("Dimensions must be positive.")

        return cls([[0 for _ in range(n)] for _ in range(m)])

    @classmethod
    def identity(cls, n):
        """Create the n-by-n identity matrix."""
        if n < 1:
            raise ValueError("Dimension must be positive.")

        return cls([
            [1 if i == j else 0 for j in range(n)]
            for i in range(n)
        ])

    @property
    def shape(self):
        """Return the matrix dimensions."""
        return self.m, self.n

    def transpose(self):
        """Return the transposed matrix M^T."""
        return Matrix([
            [self.rows[i][j] for i in range(self.m)]
            for j in range(self.n)
        ])

    @property
    def T(self):
        """Convenient transpose notation: M.T."""
        return self.transpose()

    def __add__(self, other):
        """Add two matrices of the same dimensions."""
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.shape != other.shape:
            raise ValueError(
                f"Cannot add matrices with shapes "
                f"{self.shape} and {other.shape}."
            )

        return Matrix([
            [
                self.rows[i][j] + other.rows[i][j]
                for j in range(self.n)
            ]
            for i in range(self.m)
        ])

    def __neg__(self):
        """Return the additive inverse of a matrix."""
        return Matrix([
            [-value for value in row]
            for row in self.rows
        ])

    def __sub__(self, other):
        """Subtract two matrices."""
        return self + (-other)

    def __mul__(self, scalar):
        """Multiply every entry by a scalar."""
        if not isinstance(scalar, Number):
            return NotImplemented

        return Matrix([
            [scalar * value for value in row]
            for row in self.rows
        ])

    def __rmul__(self, scalar):
        """Allow scalar multiplication from either side."""
        return self * scalar

    def __matmul__(self, other):
        """
        Matrix multiplication.

        For M of shape (m, n) and N of shape (n, p),
        the result has shape (m, p).
        """
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.n != other.m:
            raise ValueError(
                f"Cannot multiply matrices with shapes "
                f"{self.shape} and {other.shape}."
            )

        result = []

        for i in range(self.m):
            row = []

            for j in range(other.n):
                value = sum(
                    self.rows[i][k] * other.rows[k][j]
                    for k in range(self.n)
                )

                row.append(value)

            result.append(row)

        return Matrix(result)

    def __eq__(self, other):
        """Compare matrix dimensions and entries."""
        if not isinstance(other, Matrix):
            return False

        return self.shape == other.shape and self.rows == other.rows

    def __getitem__(self, index):
        """Access a row using zero-based indexing."""
        return self.rows[index]

    def __repr__(self):
        """Display the matrix in readable form."""
        return "\n".join(
            "[ " + "  ".join(map(str, row)) + " ]"
            for row in self.rows
        )


def demonstrate():
    """Demonstrate the matrix operations."""

    M = Matrix([
        [1, 2, 3],
        [4, 5, 6],
    ])

    N = Matrix([
        [7, 8, 9],
        [1, 2, 3],
    ])

    P = Matrix([
        [1, 2],
        [3, 4],
        [5, 6],
    ])

    print("Matrix M:")
    print(M)
    print("Shape:", M.shape)

    print("\nMatrix N:")
    print(N)

    print("\nM + N:")
    print(M + N)

    print("\n3 * M:")
    print(3 * M)

    print("\nTranspose of M:")
    print(M.T)

    print("\nIdentity matrix I3:")
    I3 = Matrix.identity(3)
    print(I3)

    print("\nMatrix multiplication M @ P:")
    print(M @ P)

    print("\nVerify M @ I3 = M:")
    print(M @ I3)
    assert M @ I3 == M

    print("\nVerify (M.T).T = M:")
    assert M.T.T == M
    print("Verified!")

    print("\nAll demonstrations completed successfully.")


if __name__ == "__main__":
    demonstrate()
