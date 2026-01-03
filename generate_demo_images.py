#!/usr/bin/env python3
"""
Generate demo images for README.md

Creates 4 demonstration images showing IPM transformation:
1. demo_front_view.png - Original KITTI road image with ROI overlay
2. demo_bev.png - Bird's Eye View transformation
3. demo_point_transform.png - Point transformation visualization
4. demo_grid_overlay.png - Grid overlay showing parallel lines
"""

import cv2
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, 'src')
from ipm import IPMTransform

# Configuration
KITTI_IMAGE_PATH = '/home/vigoroth/mst_research/temporal 3D detection  BEV/data/KITTI.v2i.yolov12/test/images/000243_png.rf.0ec750f675d3bc21a5319bea8c2d2dbd.jpg'
OUTPUT_DIR = Path('results')
ROI_CONFIG = {
    'top_left_ratio': (0.4, 0.6),
    'top_right_ratio': (0.6, 0.6),
    'bottom_right_ratio': (0.9, 0.95),
    'bottom_left_ratio': (0.1, 0.95),
    'bev_width': 640,
    'bev_height': 480
}


def draw_roi_trapezoid(image, roi_config):
    """Draw trapezoid ROI overlay on image."""
    h, w = image.shape[:2]

    # Compute corner points
    pts = np.array([
        [roi_config['top_left_ratio'][0] * w, roi_config['top_left_ratio'][1] * h],
        [roi_config['top_right_ratio'][0] * w, roi_config['top_right_ratio'][1] * h],
        [roi_config['bottom_right_ratio'][0] * w, roi_config['bottom_right_ratio'][1] * h],
        [roi_config['bottom_left_ratio'][0] * w, roi_config['bottom_left_ratio'][1] * h]
    ], dtype=np.int32)

    # Draw polygon (green, semi-transparent overlay)
    overlay = image.copy()
    cv2.polylines(overlay, [pts], True, (0, 255, 0), 3)
    cv2.fillPoly(overlay, [pts], (0, 255, 0))

    # Blend with original
    output = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)

    # Add labels
    cv2.putText(output, 'ROI for BEV Transform', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return output


def draw_grid_overlay(bev_image, spacing=50):
    """Draw grid overlay showing parallel lines in BEV."""
    output = bev_image.copy()
    h, w = output.shape[:2]

    # Draw vertical lines (parallel to road direction)
    for x in range(0, w, spacing):
        cv2.line(output, (x, 0), (x, h), (0, 255, 255), 1)

    # Draw horizontal lines (across road)
    for y in range(0, h, spacing):
        cv2.line(output, (0, y), (w, y), (0, 255, 255), 1)

    # Add label
    cv2.putText(output, 'Grid: Parallel Lines Remain Parallel', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    return output


def create_point_transformation_viz(ipm, front_image, bev_image):
    """Create side-by-side with point correspondences."""
    # Sample points along center line of road
    h, w = front_image.shape[:2]
    sample_points = np.array([
        [w//2, int(h * 0.65)],  # Near
        [w//2, int(h * 0.75)],  # Middle
        [w//2, int(h * 0.85)],  # Far
    ], dtype=np.float32)

    # Transform points to BEV
    bev_points = ipm.transform_points_to_bev(sample_points)

    # Draw points on front image
    front_viz = front_image.copy()
    for i, pt in enumerate(sample_points):
        color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)][i]
        cv2.circle(front_viz, tuple(pt.astype(int)), 8, color, -1)
        cv2.putText(front_viz, f'P{i+1}', tuple((pt + [15, 0]).astype(int)),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Draw points on BEV
    bev_viz = bev_image.copy()
    for i, pt in enumerate(bev_points):
        color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)][i]
        cv2.circle(bev_viz, tuple(pt.astype(int)), 8, color, -1)
        cv2.putText(bev_viz, f'P{i+1}', tuple((pt + [15, 0]).astype(int)),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Create side-by-side
    # Resize to same height if needed
    h_front, w_front = front_viz.shape[:2]
    h_bev, w_bev = bev_viz.shape[:2]

    # Use the smaller height for consistency
    target_height = min(h_front, h_bev)

    if h_front != target_height:
        front_viz = cv2.resize(front_viz, (int(w_front * target_height / h_front), target_height))
    if h_bev != target_height:
        bev_viz = cv2.resize(bev_viz, (int(w_bev * target_height / h_bev), target_height))

    combined = np.hstack([front_viz, bev_viz])

    return combined


def save_image(image, filename):
    """Save image with confirmation message."""
    output_path = OUTPUT_DIR / filename
    success = cv2.imwrite(str(output_path), image)
    if success:
        print(f"✓ Saved: {output_path}")
    else:
        print(f"✗ Failed to save: {output_path}")
    return success


def main():
    """Generate all 4 demo images."""
    print("Generating demo images...")
    print()

    # 1. Load KITTI image
    print(f"Loading KITTI image from: {KITTI_IMAGE_PATH}")
    image = cv2.imread(KITTI_IMAGE_PATH)

    if image is None:
        print(f"✗ Error: Could not load image from {KITTI_IMAGE_PATH}")
        return 1

    print(f"✓ Loaded KITTI image: {image.shape}")
    print()

    # 2. Create IPM transformer
    print("Creating IPM transformer...")
    ipm = IPMTransform(image.shape[:2], ROI_CONFIG)
    print(f"✓ Created IPM transformer (BEV size: {ROI_CONFIG['bev_width']}x{ROI_CONFIG['bev_height']})")
    print()

    # 3. Generate demo_front_view.png
    print("Generating demo_front_view.png...")
    front_with_roi = draw_roi_trapezoid(image.copy(), ROI_CONFIG)
    save_image(front_with_roi, 'demo_front_view.png')
    print()

    # 4. Generate demo_bev.png
    print("Generating demo_bev.png...")
    bev_image = ipm.transform_to_bev(image)
    save_image(bev_image, 'demo_bev.png')
    print()

    # 5. Generate demo_grid_overlay.png
    print("Generating demo_grid_overlay.png...")
    bev_with_grid = draw_grid_overlay(bev_image.copy(), spacing=50)
    save_image(bev_with_grid, 'demo_grid_overlay.png')
    print()

    # 6. Generate demo_point_transform.png
    print("Generating demo_point_transform.png...")
    point_viz = create_point_transformation_viz(ipm, image, bev_image)
    save_image(point_viz, 'demo_point_transform.png')
    print()

    print("=" * 50)
    print("All 4 demo images generated successfully!")
    print("=" * 50)
    print()
    print("Demo images saved to:")
    print(f"  - {OUTPUT_DIR}/demo_front_view.png")
    print(f"  - {OUTPUT_DIR}/demo_bev.png")
    print(f"  - {OUTPUT_DIR}/demo_grid_overlay.png")
    print(f"  - {OUTPUT_DIR}/demo_point_transform.png")

    return 0


if __name__ == '__main__':
    sys.exit(main())
