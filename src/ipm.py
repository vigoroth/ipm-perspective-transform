"""
Inverse Perspective Mapping (IPM) for Bird's Eye View (BEV) transformation.

This module provides the IPMTransform class for converting front-view camera images
to Bird's Eye View (BEV) representation using homography-based transformation.

Classes:
    IPMTransform: Complete IPM transformation with forward/inverse image and point transforms
"""

import numpy as np
import cv2
from typing import Tuple, Dict

# Handle both relative and absolute imports
try:
    from .homography import compute_homography, to_homogeneous, from_homogeneous
except ImportError:
    from homography import compute_homography, to_homogeneous, from_homogeneous


class IPMTransform:
    """
    Inverse Perspective Mapping (IPM) transformation for Bird's Eye View (BEV).

    Transforms front-view images to overhead (BEV) representation using homography.
    Assumes flat ground plane (Z=0).

    This class provides:
    - Forward and inverse image transformations (front ↔ BEV)
    - Forward and inverse point transformations (front ↔ BEV)
    - Precomputed homography matrices for efficiency

    Attributes:
        image_height (int): Input image height in pixels
        image_width (int): Input image width in pixels
        bev_height (int): BEV output height in pixels
        bev_width (int): BEV output width in pixels
        src_points (np.ndarray): Source trapezoid points (4, 2)
        dst_points (np.ndarray): Destination rectangle points (4, 2)
        H (np.ndarray): Forward homography matrix (3, 3) for front → BEV
        H_inv (np.ndarray): Inverse homography matrix (3, 3) for BEV → front

    Example:
        >>> config = {
        ...     'top_left_ratio': (0.4, 0.6),
        ...     'top_right_ratio': (0.6, 0.6),
        ...     'bottom_right_ratio': (0.9, 0.95),
        ...     'bottom_left_ratio': (0.1, 0.95),
        ...     'bev_width': 640,
        ...     'bev_height': 480
        ... }
        >>> ipm = IPMTransform((720, 1280), config)
        >>> bev_image = ipm.transform_to_bev(front_image)
    """

    def __init__(self, image_shape: Tuple[int, int], roi_config: Dict):
        """
        Initialize IPM transformation.

        Args:
            image_shape: tuple (height, width) of input image
            roi_config: dict with keys:
                - top_left_ratio: (x_ratio, y_ratio) for top-left corner of trapezoid
                - top_right_ratio: (x_ratio, y_ratio) for top-right corner
                - bottom_right_ratio: (x_ratio, y_ratio) for bottom-right corner
                - bottom_left_ratio: (x_ratio, y_ratio) for bottom-left corner
                - bev_width: output BEV width in pixels
                - bev_height: output BEV height in pixels

        Ratios are fractions of image dimensions (0.0 to 1.0).
        The trapezoid defined by the ratios should cover the road region of interest.

        Example config:
            {
                'top_left_ratio': (0.4, 0.6),      # Narrower top (farther)
                'top_right_ratio': (0.6, 0.6),
                'bottom_right_ratio': (0.9, 0.95),  # Wider bottom (closer)
                'bottom_left_ratio': (0.1, 0.95),
                'bev_width': 640,
                'bev_height': 480
            }
        """
        self.image_height = image_shape[0]
        self.image_width = image_shape[1]
        self.roi_config = roi_config

        # Compute source and destination points
        self.src_points = self._compute_src_points(roi_config)
        self.dst_points = self._compute_dst_points(roi_config)

        # Compute forward and inverse homography matrices
        # H: front-view → BEV
        # H_inv: BEV → front-view
        self.H = compute_homography(self.src_points, self.dst_points)
        self.H_inv = np.linalg.inv(self.H)

        self.bev_width = roi_config['bev_width']
        self.bev_height = roi_config['bev_height']

    def _compute_src_points(self, config: Dict) -> np.ndarray:
        """
        Compute source trapezoid vertices from ratio configuration.

        The trapezoid in the front-view image represents the road region.
        Narrower at top (far from camera) and wider at bottom (close to camera)
        due to perspective projection.

        Args:
            config: ROI configuration dict with ratio keys

        Returns:
            np.ndarray: (4, 2) array of corner points in order:
                       [top-left, top-right, bottom-right, bottom-left]
        """
        src_points = np.array([
            [config['top_left_ratio'][0] * self.image_width,
             config['top_left_ratio'][1] * self.image_height],
            [config['top_right_ratio'][0] * self.image_width,
             config['top_right_ratio'][1] * self.image_height],
            [config['bottom_right_ratio'][0] * self.image_width,
             config['bottom_right_ratio'][1] * self.image_height],
            [config['bottom_left_ratio'][0] * self.image_width,
             config['bottom_left_ratio'][1] * self.image_height]
        ], dtype=np.float32)

        return src_points

    def _compute_dst_points(self, config: Dict) -> np.ndarray:
        """
        Compute destination rectangle vertices for BEV.

        In BEV, we want a rectangle (parallel sides) since parallel lines
        in the world should appear parallel in the overhead view.

        Args:
            config: ROI configuration dict with bev_width, bev_height

        Returns:
            np.ndarray: (4, 2) array of corner points forming a rectangle
                       [top-left, top-right, bottom-right, bottom-left]
        """
        bev_w = config['bev_width']
        bev_h = config['bev_height']

        dst_points = np.array([
            [0, 0],                # top-left
            [bev_w, 0],            # top-right
            [bev_w, bev_h],        # bottom-right
            [0, bev_h]             # bottom-left
        ], dtype=np.float32)

        return dst_points

    def transform_to_bev(self, image: np.ndarray) -> np.ndarray:
        """
        Transform front-view image to Bird's Eye View.

        Uses cv2.warpPerspective with the precomputed homography matrix.

        Args:
            image: np.ndarray of shape (H, W, 3) or (H, W)
                  Front-view image (color or grayscale)

        Returns:
            np.ndarray: BEV image of shape (bev_height, bev_width, 3) or (bev_height, bev_width)

        Example:
            >>> bev_image = ipm.transform_to_bev(front_image)
        """
        bev_image = cv2.warpPerspective(
            image,
            self.H,
            (self.bev_width, self.bev_height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0) if len(image.shape) == 3 else 0
        )

        return bev_image

    def transform_from_bev(self, bev_image: np.ndarray) -> np.ndarray:
        """
        Transform BEV image back to front-view (inverse transformation).

        Uses the inverse homography matrix H_inv.

        Args:
            bev_image: np.ndarray of shape (bev_height, bev_width, 3) or (bev_height, bev_width)
                      BEV image (color or grayscale)

        Returns:
            np.ndarray: Front-view image of shape (image_height, image_width, 3)
                       or (image_height, image_width)

        Example:
            >>> front_reconstructed = ipm.transform_from_bev(bev_image)
        """
        front_image = cv2.warpPerspective(
            bev_image,
            self.H_inv,
            (self.image_width, self.image_height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0) if len(bev_image.shape) == 3 else 0
        )

        return front_image

    def transform_points_to_bev(self, points: np.ndarray) -> np.ndarray:
        """
        Transform points from front-view to BEV (vectorized).

        This is useful for transforming detected lane points, object positions,
        or any other coordinates from the front-view image to BEV space.

        Args:
            points: np.ndarray of shape (N, 2) - points in front-view image coordinates (x, y)

        Returns:
            np.ndarray of shape (N, 2) - points in BEV coordinates (x', y')

        Example:
            >>> front_points = np.array([[320, 400], [320, 500]])
            >>> bev_points = ipm.transform_points_to_bev(front_points)
        """
        points = np.asarray(points, dtype=np.float32)
        if points.ndim == 1:
            points = points.reshape(1, -1)

        # Convert to homogeneous coordinates
        points_h = to_homogeneous(points)

        # Apply homography
        transformed_h = (self.H @ points_h.T).T

        # Convert back to Cartesian coordinates
        transformed = from_homogeneous(transformed_h)

        return transformed

    def transform_points_from_bev(self, bev_points: np.ndarray) -> np.ndarray:
        """
        Transform points from BEV to front-view (inverse point transformation).

        This is the inverse of transform_points_to_bev().

        Args:
            bev_points: np.ndarray of shape (N, 2) - points in BEV coordinates (x', y')

        Returns:
            np.ndarray of shape (N, 2) - points in front-view image coordinates (x, y)

        Example:
            >>> bev_points = np.array([[320, 240], [320, 360]])
            >>> front_points = ipm.transform_points_from_bev(bev_points)
        """
        bev_points = np.asarray(bev_points, dtype=np.float32)
        if bev_points.ndim == 1:
            bev_points = bev_points.reshape(1, -1)

        # Convert to homogeneous coordinates
        points_h = to_homogeneous(bev_points)

        # Apply inverse homography
        transformed_h = (self.H_inv @ points_h.T).T

        # Convert back to Cartesian coordinates
        transformed = from_homogeneous(transformed_h)

        return transformed
