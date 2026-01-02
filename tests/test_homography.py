"""
Unit tests for homography module.

Tests cover:
- Coordinate conversions (homogeneous ↔ Cartesian)
- Collinearity detection
- DLT algorithm correctness
- Edge cases and error handling
"""

import pytest
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from homography import (
    to_homogeneous,
    from_homogeneous,
    is_collinear,
    compute_homography
)


class TestCoordinateConversions:
    """Tests for homogeneous ↔ Cartesian coordinate conversions."""

    def test_to_homogeneous_single_point(self):
        """Test converting a single point to homogeneous coordinates."""
        point = np.array([1.0, 2.0])
        result = to_homogeneous(point)

        assert result.shape == (1, 3)
        assert np.allclose(result, [[1.0, 2.0, 1.0]])

    def test_to_homogeneous_multiple_points(self):
        """Test converting multiple points to homogeneous coordinates."""
        points = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        result = to_homogeneous(points)

        assert result.shape == (3, 3)
        expected = np.array([[1.0, 2.0, 1.0],
                            [3.0, 4.0, 1.0],
                            [5.0, 6.0, 1.0]])
        assert np.allclose(result, expected)

    def test_from_homogeneous_standard(self):
        """Test converting standard homogeneous coordinates (w=1)."""
        points_h = np.array([[1.0, 2.0, 1.0],
                            [3.0, 4.0, 1.0]])
        result = from_homogeneous(points_h)

        assert result.shape == (2, 2)
        expected = np.array([[1.0, 2.0],
                            [3.0, 4.0]])
        assert np.allclose(result, expected)

    def test_from_homogeneous_scaled(self):
        """Test converting scaled homogeneous coordinates (w≠1)."""
        points_h = np.array([[4.0, 8.0, 2.0],   # (2, 4) when w=2
                            [6.0, 12.0, 3.0]])  # (2, 4) when w=3
        result = from_homogeneous(points_h)

        assert result.shape == (2, 2)
        expected = np.array([[2.0, 4.0],
                            [2.0, 4.0]])
        assert np.allclose(result, expected)

    def test_round_trip_conversion(self):
        """Test that Cartesian → homogeneous → Cartesian preserves points."""
        original = np.array([[1.5, 2.5], [3.7, 4.9]])
        homogeneous = to_homogeneous(original)
        back = from_homogeneous(homogeneous)

        assert np.allclose(original, back)


class TestCollinearity:
    """Tests for collinearity detection."""

    def test_collinear_points(self):
        """Test that collinear points are detected."""
        points = np.array([[0, 0], [1, 1], [2, 2], [3, 3]], dtype=np.float32)
        assert is_collinear(points)

    def test_non_collinear_points(self):
        """Test that non-collinear points are not flagged."""
        points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=np.float32)
        assert not is_collinear(points)

    def test_collinear_horizontal(self):
        """Test collinearity detection for horizontal line."""
        points = np.array([[0, 5], [1, 5], [2, 5]], dtype=np.float32)
        assert is_collinear(points)

    def test_collinear_vertical(self):
        """Test collinearity detection for vertical line."""
        points = np.array([[3, 0], [3, 1], [3, 2]], dtype=np.float32)
        assert is_collinear(points)

    def test_nearly_collinear_within_tolerance(self):
        """Test that nearly collinear points within tolerance are flagged."""
        points = np.array([[0, 0], [1, 1], [2, 2.0000001]], dtype=np.float32)
        assert is_collinear(points, tolerance=1e-4)

    def test_nearly_collinear_outside_tolerance(self):
        """Test that nearly collinear points outside tolerance are not flagged."""
        points = np.array([[0, 0], [1, 1], [2, 2.1]], dtype=np.float32)
        assert not is_collinear(points, tolerance=1e-6)


class TestComputeHomography:
    """Tests for homography computation using DLT."""

    def test_identity_transformation(self, identity_points):
        """Test homography for identity transformation."""
        H = compute_homography(identity_points['src'], identity_points['dst'])

        # Should be identity matrix
        expected = np.eye(3)
        assert np.allclose(H, expected, atol=1e-6)

    def test_translation_transformation(self, translation_points):
        """Test homography for pure translation."""
        H = compute_homography(translation_points['src'], translation_points['dst'])

        # Apply to source points
        src_h = to_homogeneous(translation_points['src'])
        transformed_h = (H @ src_h.T).T
        transformed = from_homogeneous(transformed_h)

        # Should match destination points
        assert np.allclose(transformed, translation_points['dst'], atol=1e-5)

    def test_scaling_transformation(self, test_points):
        """Test homography for scaling (2x)."""
        H = compute_homography(test_points['src'], test_points['dst'])

        # Apply to source points
        src_h = to_homogeneous(test_points['src'])
        transformed_h = (H @ src_h.T).T
        transformed = from_homogeneous(transformed_h)

        # Should match destination points
        assert np.allclose(transformed, test_points['dst'], atol=1e-5)

    def test_perspective_transformation(self, perspective_points):
        """Test homography for perspective transformation."""
        H = compute_homography(perspective_points['src'], perspective_points['dst'])

        # Apply to source points
        src_h = to_homogeneous(perspective_points['src'])
        transformed_h = (H @ src_h.T).T
        transformed = from_homogeneous(transformed_h)

        # Should match destination points
        assert np.allclose(transformed, perspective_points['dst'], atol=1e-5)

    def test_overdetermined_system_5_points(self):
        """Test homography with 5 points (overdetermined system)."""
        src = np.array([[0, 0], [10, 0], [10, 10], [0, 10], [5, 5]], dtype=np.float32)
        dst = np.array([[0, 0], [20, 0], [20, 20], [0, 20], [10, 10]], dtype=np.float32)

        H = compute_homography(src, dst)

        # Apply to source points
        src_h = to_homogeneous(src)
        transformed_h = (H @ src_h.T).T
        transformed = from_homogeneous(transformed_h)

        # Should closely match destination points (least squares solution)
        assert np.allclose(transformed, dst, atol=1e-4)

    def test_homography_round_trip(self, test_points):
        """Test that forward and inverse homographies are inverses."""
        H = compute_homography(test_points['src'], test_points['dst'])
        H_inv = compute_homography(test_points['dst'], test_points['src'])

        # H @ H_inv should be identity
        product = H @ H_inv
        # Normalize
        product = product / product[2, 2]

        expected = np.eye(3)
        assert np.allclose(product, expected, atol=1e-5)


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_insufficient_points(self):
        """Test that fewer than 4 points raises ValueError."""
        src = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.float32)
        dst = np.array([[0, 0], [2, 0], [2, 2]], dtype=np.float32)

        with pytest.raises(ValueError, match="at least 4 points"):
            compute_homography(src, dst)

    def test_collinear_source_points(self, collinear_points):
        """Test that collinear source points raise ValueError."""
        with pytest.raises(ValueError, match="collinear"):
            compute_homography(collinear_points['src'], collinear_points['dst'])

    def test_collinear_destination_points(self, collinear_points):
        """Test that collinear destination points raise ValueError."""
        # Non-collinear source, collinear destination
        src = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=np.float32)
        dst = collinear_points['src']  # Use collinear points

        with pytest.raises(ValueError, match="collinear"):
            compute_homography(src, dst)

    def test_shape_mismatch(self):
        """Test that mismatched source/destination shapes raise ValueError."""
        src = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32)
        dst = np.array([[0, 0], [2, 0], [2, 2]], dtype=np.float32)  # Only 3 points

        with pytest.raises(ValueError, match="shapes must match"):
            compute_homography(src, dst)

    def test_invalid_shape_1d(self):
        """Test that 1D array raises ValueError."""
        src = np.array([0, 1, 2, 3], dtype=np.float32)  # 1D
        dst = np.array([0, 2, 4, 6], dtype=np.float32)  # 1D

        with pytest.raises(ValueError, match="Nx2 array"):
            compute_homography(src, dst)

    def test_invalid_shape_3d(self):
        """Test that wrong dimensionality raises ValueError."""
        src = np.array([[[0, 0], [1, 0]], [[1, 1], [0, 1]]], dtype=np.float32)  # 3D
        dst = src.copy()

        with pytest.raises(ValueError, match="Nx2 array"):
            compute_homography(src, dst)

    def test_normalized_output(self, test_points):
        """Test that homography matrix is normalized (H[2,2] = 1)."""
        H = compute_homography(test_points['src'], test_points['dst'])

        assert np.isclose(H[2, 2], 1.0)

    def test_homography_shape(self, test_points):
        """Test that homography matrix has correct shape."""
        H = compute_homography(test_points['src'], test_points['dst'])

        assert H.shape == (3, 3)


class TestNumericalStability:
    """Tests for numerical stability and edge cases."""

    def test_large_coordinates(self):
        """Test homography with large coordinate values."""
        src = np.array([[0, 0], [1000, 0], [1000, 1000], [0, 1000]], dtype=np.float32)
        dst = np.array([[100, 100], [1100, 100], [1100, 1100], [100, 1100]], dtype=np.float32)

        H = compute_homography(src, dst)

        # Verify transformation
        src_h = to_homogeneous(src)
        transformed_h = (H @ src_h.T).T
        transformed = from_homogeneous(transformed_h)

        assert np.allclose(transformed, dst, atol=1e-3)

    def test_small_coordinates(self):
        """Test homography with small coordinate values."""
        src = np.array([[0, 0], [0.01, 0], [0.01, 0.01], [0, 0.01]], dtype=np.float32)
        dst = np.array([[0, 0], [0.02, 0], [0.02, 0.02], [0, 0.02]], dtype=np.float32)

        H = compute_homography(src, dst)

        # Verify transformation
        src_h = to_homogeneous(src)
        transformed_h = (H @ src_h.T).T
        transformed = from_homogeneous(transformed_h)

        assert np.allclose(transformed, dst, atol=1e-6)
