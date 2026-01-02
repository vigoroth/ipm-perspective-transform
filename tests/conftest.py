"""Shared test fixtures for IPM tests."""
import pytest
import numpy as np
import cv2


@pytest.fixture
def sample_image():
    """
    Create sample road image for testing.

    Returns:
        np.ndarray: Synthetic road image (480x640x3) with converging lane lines
    """
    height, width = 480, 640
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = (100, 120, 140)  # Gray background

    # Draw converging lane lines (perspective effect)
    vp_x, vp_y = width // 2, height // 3  # Vanishing point

    # Left lane line
    cv2.line(image, (100, height), (vp_x - 50, vp_y), (255, 255, 255), 3)

    # Right lane line
    cv2.line(image, (width - 100, height), (vp_x + 50, vp_y), (255, 255, 255), 3)

    return image


@pytest.fixture
def roi_config():
    """
    Standard ROI configuration for IPM testing.

    Returns:
        dict: ROI configuration with trapezoid ratios and BEV dimensions
    """
    return {
        'top_left_ratio': (0.4, 0.6),
        'top_right_ratio': (0.6, 0.6),
        'bottom_right_ratio': (0.9, 0.95),
        'bottom_left_ratio': (0.1, 0.95),
        'bev_width': 640,
        'bev_height': 480
    }


@pytest.fixture
def test_points():
    """
    Sample point correspondences for homography testing.

    Returns:
        dict: Dictionary with 'src' and 'dst' point arrays
    """
    return {
        'src': np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32),
        'dst': np.array([[0, 0], [2, 0], [2, 2], [0, 2]], dtype=np.float32)
    }


@pytest.fixture
def identity_points():
    """
    Point correspondences for identity transformation.

    Returns:
        dict: Dictionary with identical 'src' and 'dst' point arrays
    """
    points = np.array([[0, 0], [10, 0], [10, 10], [0, 10]], dtype=np.float32)
    return {
        'src': points.copy(),
        'dst': points.copy()
    }


@pytest.fixture
def translation_points():
    """
    Point correspondences for translation transformation.

    Returns:
        dict: Dictionary with 'src' and 'dst' arrays (translation by [5, 3])
    """
    return {
        'src': np.array([[0, 0], [10, 0], [10, 10], [0, 10]], dtype=np.float32),
        'dst': np.array([[5, 3], [15, 3], [15, 13], [5, 13]], dtype=np.float32)
    }


@pytest.fixture
def collinear_points():
    """
    Collinear points that should fail homography computation.

    Returns:
        dict: Dictionary with collinear 'src' and 'dst' point arrays
    """
    return {
        'src': np.array([[0, 0], [1, 1], [2, 2], [3, 3]], dtype=np.float32),
        'dst': np.array([[0, 0], [1, 0], [2, 0], [3, 0]], dtype=np.float32)
    }


@pytest.fixture
def perspective_points():
    """
    Point correspondences for perspective transformation.

    Returns:
        dict: Dictionary with perspective-distorted point arrays
    """
    return {
        'src': np.array([[0, 0], [100, 0], [100, 100], [0, 100]], dtype=np.float32),
        'dst': np.array([[20, 10], [80, 10], [100, 100], [0, 100]], dtype=np.float32)
    }
