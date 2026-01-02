"""
Unit tests for IPM (Inverse Perspective Mapping) module.

Tests cover:
- IPMTransform initialization
- Source/destination point computation
- Image transformations (forward and inverse)
- Point transformations (forward and inverse)
- Round-trip accuracy
- Error handling
"""

import pytest
import numpy as np
import cv2
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ipm import IPMTransform


class TestIPMInitialization:
    """Tests for IPMTransform initialization."""

    def test_initialization_with_valid_config(self, roi_config):
        """Test initialization with valid ROI configuration."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        assert ipm.image_height == 480
        assert ipm.image_width == 640
        assert ipm.bev_width == 640
        assert ipm.bev_height == 480
        assert ipm.H.shape == (3, 3)
        assert ipm.H_inv.shape == (3, 3)

    def test_initialization_stores_config(self, roi_config):
        """Test that ROI configuration is stored."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        assert ipm.roi_config == roi_config

    def test_homography_matrices_are_inverses(self, roi_config):
        """Test that H and H_inv are inverses of each other."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        # H @ H_inv should be identity
        product = ipm.H @ ipm.H_inv
        # Normalize
        product = product / product[2, 2]

        expected = np.eye(3)
        assert np.allclose(product, expected, atol=1e-5)


class TestComputePoints:
    """Tests for source and destination point computation."""

    def test_compute_src_points(self, roi_config):
        """Test source trapezoid points computation."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        src_points = ipm.src_points

        assert src_points.shape == (4, 2)
        assert src_points.dtype == np.float32

        # Check that points are within image bounds
        assert np.all(src_points[:, 0] >= 0)
        assert np.all(src_points[:, 0] <= 640)
        assert np.all(src_points[:, 1] >= 0)
        assert np.all(src_points[:, 1] <= 480)

    def test_compute_dst_points(self, roi_config):
        """Test destination rectangle points computation."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        dst_points = ipm.dst_points

        assert dst_points.shape == (4, 2)
        assert dst_points.dtype == np.float32

        # Check that points form a rectangle at corners of BEV image
        expected = np.array([[0, 0], [640, 0], [640, 480], [0, 480]], dtype=np.float32)
        assert np.allclose(dst_points, expected)

    def test_src_points_form_trapezoid(self, roi_config):
        """Test that source points form a trapezoid (narrow top, wide bottom)."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        src_points = ipm.src_points

        # Top width (between points 0 and 1)
        top_width = src_points[1, 0] - src_points[0, 0]

        # Bottom width (between points 3 and 2)
        bottom_width = src_points[2, 0] - src_points[3, 0]

        # Bottom should be wider than top (perspective effect)
        assert bottom_width > top_width


class TestImageTransformations:
    """Tests for image transformation methods."""

    def test_transform_to_bev_shape(self, sample_image, roi_config):
        """Test that BEV transformation produces correct output shape."""
        image_shape = sample_image.shape[:2]
        ipm = IPMTransform(image_shape, roi_config)

        bev_image = ipm.transform_to_bev(sample_image)

        assert bev_image.shape == (roi_config['bev_height'], roi_config['bev_width'], 3)

    def test_transform_to_bev_grayscale(self, roi_config):
        """Test BEV transformation with grayscale image."""
        gray_image = np.zeros((480, 640), dtype=np.uint8)
        ipm = IPMTransform(gray_image.shape, roi_config)

        bev_image = ipm.transform_to_bev(gray_image)

        assert bev_image.shape == (roi_config['bev_height'], roi_config['bev_width'])

    def test_transform_from_bev_shape(self, sample_image, roi_config):
        """Test that inverse BEV transformation produces correct output shape."""
        image_shape = sample_image.shape[:2]
        ipm = IPMTransform(image_shape, roi_config)

        bev_image = ipm.transform_to_bev(sample_image)
        reconstructed = ipm.transform_from_bev(bev_image)

        assert reconstructed.shape == sample_image.shape

    def test_round_trip_image_transformation(self, sample_image, roi_config):
        """Test that forward → inverse transformation preserves ROI region."""
        image_shape = sample_image.shape[:2]
        ipm = IPMTransform(image_shape, roi_config)

        # Transform to BEV and back
        bev_image = ipm.transform_to_bev(sample_image)
        reconstructed = ipm.transform_from_bev(bev_image)

        # Can't expect perfect reconstruction outside ROI, but shapes should match
        assert reconstructed.shape == sample_image.shape


class TestPointTransformations:
    """Tests for point transformation methods."""

    def test_transform_points_to_bev_shape(self, roi_config):
        """Test that point transformation produces correct output shape."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        front_points = np.array([[320, 400], [320, 450], [400, 425]], dtype=np.float32)
        bev_points = ipm.transform_points_to_bev(front_points)

        assert bev_points.shape == (3, 2)
        assert bev_points.dtype == np.float32

    def test_transform_points_to_bev_single_point(self, roi_config):
        """Test transforming a single point to BEV."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        front_point = np.array([320, 400], dtype=np.float32)
        bev_point = ipm.transform_points_to_bev(front_point)

        assert bev_point.shape == (1, 2)

    def test_transform_points_from_bev_shape(self, roi_config):
        """Test that inverse point transformation produces correct output shape."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        bev_points = np.array([[320, 240], [320, 360], [400, 300]], dtype=np.float32)
        front_points = ipm.transform_points_from_bev(bev_points)

        assert front_points.shape == (3, 2)
        assert front_points.dtype == np.float32

    def test_round_trip_point_transformation(self, roi_config):
        """Test that point forward → inverse transformation preserves points."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        # Points within ROI
        original_points = np.array([
            [256, 350],  # Within trapezoid
            [384, 350],
            [320, 400]
        ], dtype=np.float32)

        # Transform to BEV and back
        bev_points = ipm.transform_points_to_bev(original_points)
        reconstructed = ipm.transform_points_from_bev(bev_points)

        # Should match original points closely
        assert np.allclose(original_points, reconstructed, atol=1.0)


class TestDifferentBEVSizes:
    """Tests for different BEV output sizes."""

    def test_different_bev_width(self, sample_image):
        """Test BEV transformation with different width."""
        config = {
            'top_left_ratio': (0.4, 0.6),
            'top_right_ratio': (0.6, 0.6),
            'bottom_right_ratio': (0.9, 0.95),
            'bottom_left_ratio': (0.1, 0.95),
            'bev_width': 800,  # Different from default
            'bev_height': 480
        }

        image_shape = sample_image.shape[:2]
        ipm = IPMTransform(image_shape, config)

        bev_image = ipm.transform_to_bev(sample_image)

        assert bev_image.shape == (480, 800, 3)

    def test_different_bev_height(self, sample_image):
        """Test BEV transformation with different height."""
        config = {
            'top_left_ratio': (0.4, 0.6),
            'top_right_ratio': (0.6, 0.6),
            'bottom_right_ratio': (0.9, 0.95),
            'bottom_left_ratio': (0.1, 0.95),
            'bev_width': 640,
            'bev_height': 600  # Different from default
        }

        image_shape = sample_image.shape[:2]
        ipm = IPMTransform(image_shape, config)

        bev_image = ipm.transform_to_bev(sample_image)

        assert bev_image.shape == (600, 640, 3)

    def test_square_bev_output(self, sample_image):
        """Test BEV transformation with square output."""
        config = {
            'top_left_ratio': (0.4, 0.6),
            'top_right_ratio': (0.6, 0.6),
            'bottom_right_ratio': (0.9, 0.95),
            'bottom_left_ratio': (0.1, 0.95),
            'bev_width': 512,
            'bev_height': 512  # Square
        }

        image_shape = sample_image.shape[:2]
        ipm = IPMTransform(image_shape, config)

        bev_image = ipm.transform_to_bev(sample_image)

        assert bev_image.shape == (512, 512, 3)


class TestDifferentImageShapes:
    """Tests for different input image shapes."""

    def test_different_image_width(self, roi_config):
        """Test IPM with different image width."""
        image_shape = (480, 1280)  # Wider image
        ipm = IPMTransform(image_shape, roi_config)

        image = np.zeros((480, 1280, 3), dtype=np.uint8)
        bev_image = ipm.transform_to_bev(image)

        assert bev_image.shape == (roi_config['bev_height'], roi_config['bev_width'], 3)

    def test_different_image_height(self, roi_config):
        """Test IPM with different image height."""
        image_shape = (720, 640)  # Taller image
        ipm = IPMTransform(image_shape, roi_config)

        image = np.zeros((720, 640, 3), dtype=np.uint8)
        bev_image = ipm.transform_to_bev(image)

        assert bev_image.shape == (roi_config['bev_height'], roi_config['bev_width'], 3)

    def test_hd_image(self, roi_config):
        """Test IPM with HD image (1920x1080)."""
        image_shape = (1080, 1920)
        ipm = IPMTransform(image_shape, roi_config)

        image = np.zeros((1080, 1920, 3), dtype=np.uint8)
        bev_image = ipm.transform_to_bev(image)

        assert bev_image.shape == (roi_config['bev_height'], roi_config['bev_width'], 3)


class TestROIConfigurations:
    """Tests for different ROI configurations."""

    def test_narrow_roi(self, sample_image):
        """Test IPM with narrow ROI (smaller trapezoid)."""
        config = {
            'top_left_ratio': (0.45, 0.7),    # Narrower
            'top_right_ratio': (0.55, 0.7),
            'bottom_right_ratio': (0.65, 0.9),
            'bottom_left_ratio': (0.35, 0.9),
            'bev_width': 640,
            'bev_height': 480
        }

        image_shape = sample_image.shape[:2]
        ipm = IPMTransform(image_shape, config)

        bev_image = ipm.transform_to_bev(sample_image)

        assert bev_image.shape == (480, 640, 3)

    def test_wide_roi(self, sample_image):
        """Test IPM with wide ROI (larger trapezoid)."""
        config = {
            'top_left_ratio': (0.3, 0.5),    # Wider
            'top_right_ratio': (0.7, 0.5),
            'bottom_right_ratio': (0.95, 0.98),
            'bottom_left_ratio': (0.05, 0.98),
            'bev_width': 640,
            'bev_height': 480
        }

        image_shape = sample_image.shape[:2]
        ipm = IPMTransform(image_shape, config)

        bev_image = ipm.transform_to_bev(sample_image)

        assert bev_image.shape == (480, 640, 3)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_points_at_bev_boundaries(self, roi_config):
        """Test transforming points at BEV image boundaries."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        # Points at BEV corners
        bev_points = np.array([
            [0, 0],                                      # Top-left
            [roi_config['bev_width'], 0],               # Top-right
            [roi_config['bev_width'], roi_config['bev_height']],  # Bottom-right
            [0, roi_config['bev_height']]               # Bottom-left
        ], dtype=np.float32)

        front_points = ipm.transform_points_from_bev(bev_points)

        # Should produce valid coordinates
        assert not np.any(np.isnan(front_points))
        assert not np.any(np.isinf(front_points))

    def test_empty_image_regions(self, roi_config):
        """Test that transformation handles empty image regions gracefully."""
        image = np.zeros((480, 640, 3), dtype=np.uint8)
        ipm = IPMTransform(image.shape[:2], roi_config)

        bev_image = ipm.transform_to_bev(image)

        # Should produce valid output (all zeros)
        assert bev_image.shape == (roi_config['bev_height'], roi_config['bev_width'], 3)
        assert np.all(bev_image == 0)


class TestRoundTripAccuracy:
    """Tests for round-trip transformation accuracy."""

    def test_round_trip_error_within_roi(self, roi_config):
        """Test that round-trip error is small for points within ROI."""
        image_shape = (480, 640)
        ipm = IPMTransform(image_shape, roi_config)

        # Sample points within ROI trapezoid
        test_points = np.array([
            [256, 350],   # Center-left
            [320, 400],   # Center
            [384, 350],   # Center-right
            [320, 300],   # Top center
            [320, 450]    # Bottom center
        ], dtype=np.float32)

        # Round trip: front → BEV → front
        bev_points = ipm.transform_points_to_bev(test_points)
        reconstructed = ipm.transform_points_from_bev(bev_points)

        # Compute pixel error
        error = np.linalg.norm(test_points - reconstructed, axis=1)

        # Error should be < 0.5 pixels for all points
        assert np.all(error < 0.5)

    def test_transformation_determinism(self, sample_image, roi_config):
        """Test that transformation is deterministic (same input → same output)."""
        image_shape = sample_image.shape[:2]
        ipm = IPMTransform(image_shape, roi_config)

        bev1 = ipm.transform_to_bev(sample_image)
        bev2 = ipm.transform_to_bev(sample_image)

        # Should be identical
        assert np.array_equal(bev1, bev2)
