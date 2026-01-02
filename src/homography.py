"""
Homography computation using Direct Linear Transformation (DLT).

This module provides functions for computing homography matrices from point correspondences
using the Direct Linear Transformation (DLT) algorithm with Singular Value Decomposition (SVD).

Functions:
    to_homogeneous: Convert Cartesian coordinates to homogeneous coordinates
    from_homogeneous: Convert homogeneous coordinates to Cartesian coordinates
    is_collinear: Check if points are collinear
    compute_homography: Compute homography matrix using DLT algorithm
"""

import numpy as np
from typing import Union


def to_homogeneous(points: np.ndarray) -> np.ndarray:
    """
    Convert Cartesian coordinates to homogeneous coordinates.

    Homogeneous coordinates add an extra dimension (w) to enable representing
    all 2D transformations (including translation) as matrix multiplication.

    Args:
        points: np.ndarray of shape (N, 2) - Cartesian coordinates (x, y)

    Returns:
        np.ndarray of shape (N, 3) - Homogeneous coordinates (x, y, w) with w=1

    Example:
        >>> pts = np.array([[1, 2], [3, 4]])
        >>> to_homogeneous(pts)
        array([[1., 2., 1.],
               [3., 4., 1.]])
    """
    points = np.asarray(points, dtype=np.float32)
    if points.ndim == 1:
        points = points.reshape(1, -1)

    N = points.shape[0]
    ones = np.ones((N, 1))
    return np.hstack([points, ones])


def from_homogeneous(points_h: np.ndarray) -> np.ndarray:
    """
    Convert homogeneous coordinates to Cartesian coordinates.

    Converts from homogeneous representation (x, y, w) back to Cartesian (x/w, y/w).
    Handles scale invariance: (x, y, w) and (kx, ky, kw) represent the same point.

    Args:
        points_h: np.ndarray of shape (N, 3) - Homogeneous coordinates

    Returns:
        np.ndarray of shape (N, 2) - Cartesian coordinates

    Example:
        >>> pts_h = np.array([[4, 8, 2], [6, 12, 3]])
        >>> from_homogeneous(pts_h)
        array([[2., 4.],
               [2., 4.]])
    """
    points_h = np.asarray(points_h, dtype=np.float32)
    if points_h.ndim == 1:
        points_h = points_h.reshape(1, -1)

    # Divide x and y by w
    w = points_h[:, 2:3]  # Keep as column vector
    xy = points_h[:, :2]

    return xy / w


def is_collinear(points: np.ndarray, tolerance: float = 1e-6) -> bool:
    """
    Check if points are collinear using cross product.

    Collinear points cannot define a unique homography because they don't
    span 2D space. This function checks if the first 3 points are collinear.

    Args:
        points: np.ndarray of shape (N, 2) where N >= 3
        tolerance: float, threshold for considering points collinear

    Returns:
        bool: True if points are collinear, False otherwise

    Example:
        >>> pts = np.array([[0, 0], [1, 1], [2, 2]])  # Collinear
        >>> is_collinear(pts)
        True
        >>> pts = np.array([[0, 0], [1, 0], [0, 1]])  # Not collinear
        >>> is_collinear(pts)
        False
    """
    if len(points) < 3:
        return False

    # Use first 3 points
    p1, p2, p3 = points[:3]

    # Compute cross product magnitude: (p2-p1) × (p3-p1)
    v1 = p2 - p1
    v2 = p3 - p1
    cross = v1[0] * v2[1] - v1[1] * v2[0]

    return abs(cross) < tolerance


def compute_homography(src_points: np.ndarray, dst_points: np.ndarray) -> np.ndarray:
    """
    Compute homography matrix using Direct Linear Transformation (DLT).

    A homography H is a 3×3 matrix that maps points from one plane to another:
        dst_point ~ H @ src_point (in homogeneous coordinates)

    The DLT algorithm:
    1. Build constraint matrix A from point correspondences (2N × 9)
    2. Solve Ah = 0 using SVD (Singular Value Decomposition)
    3. Solution is the last column of V (smallest singular value)
    4. Reshape to 3×3 matrix and normalize so H[2,2] = 1

    Args:
        src_points: np.ndarray of shape (N, 2), where N >= 4
                   Source points in the first plane
        dst_points: np.ndarray of shape (N, 2)
                   Destination points in the second plane

    Returns:
        H: np.ndarray of shape (3, 3)
           Homography matrix normalized so H[2,2] = 1

    Raises:
        ValueError: If fewer than 4 points provided or points are invalid

    Example:
        >>> src = np.array([[0,0], [1,0], [1,1], [0,1]], dtype=np.float32)
        >>> dst = np.array([[0,0], [2,0], [2,2], [0,2]], dtype=np.float32)  # 2x scaling
        >>> H = compute_homography(src, dst)
        >>> # H should be approximately [[2,0,0], [0,2,0], [0,0,1]]

    Notes:
        - Homography has 8 degrees of freedom (9 elements but scale-invariant)
        - Minimum 4 points needed (each gives 2 equations, need 8 for 8 unknowns)
        - For >4 points, SVD finds least-squares solution
        - Points must not be collinear
    """
    # Convert to numpy arrays
    src = np.asarray(src_points, dtype=np.float32)
    dst = np.asarray(dst_points, dtype=np.float32)

    # Validate shapes
    if src.shape != dst.shape:
        raise ValueError(f"Source and destination shapes must match: {src.shape} != {dst.shape}")

    if len(src.shape) != 2 or src.shape[1] != 2:
        raise ValueError(f"Points must be Nx2 array, got shape {src.shape}")

    n_points = src.shape[0]
    if n_points < 4:
        raise ValueError(f"Need at least 4 points to compute homography, got {n_points}")

    # Check for collinearity (optional but recommended)
    if is_collinear(src):
        raise ValueError("Source points are collinear - cannot compute unique homography")
    if is_collinear(dst):
        raise ValueError("Destination points are collinear - cannot compute unique homography")

    # Build constraint matrix A (2N × 9)
    # For each correspondence (x,y) -> (x',y'), we get two equations:
    # -x  -y  -1   0   0   0  x'x x'y x'  | h1
    #  0   0   0  -x  -y  -1  y'x y'y y'  | h2
    A = np.zeros((2 * n_points, 9))

    for i in range(n_points):
        x, y = src[i]
        xp, yp = dst[i]

        # First equation (x-coordinate)
        A[2*i] = [-x, -y, -1, 0, 0, 0, xp*x, xp*y, xp]

        # Second equation (y-coordinate)
        A[2*i + 1] = [0, 0, 0, -x, -y, -1, yp*x, yp*y, yp]

    # Solve using SVD: A = U @ S @ Vt
    # Solution to Ah = 0 is last column of V (smallest singular value)
    U, S, Vt = np.linalg.svd(A)

    # Solution is last column of V (last row of Vt)
    h = Vt[-1, :]

    # Reshape to 3×3 matrix
    H = h.reshape(3, 3)

    # Normalize so H[2,2] = 1 (standard convention)
    H = H / H[2, 2]

    return H
