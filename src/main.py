"""
Example usage of IPMTransform for converting front-view road images to Bird's Eye View (BEV).

This script demonstrates:
1. Loading a road image from the KITTI dataset
2. Creating an IPMTransform instance with ROI configuration
3. Transforming the image to BEV
4. Displaying the results
"""

from ipm import IPMTransform
import cv2
import numpy as np

# Load road image from KITTI dataset
image_path = '/home/vigoroth/mst_research/temporal 3D detection  BEV/data/KITTI.v2i.yolov12/test/images/000243_png.rf.0ec750f675d3bc21a5319bea8c2d2dbd.jpg'

print(f"Loading image from: {image_path}")
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Could not load image from {image_path}")
    print("Using synthetic example image instead...")

    # Create synthetic road image for demonstration
    height, width = 480, 640
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = (100, 120, 140)  # Gray background

    # Draw converging lane lines (perspective)
    vp_x, vp_y = width//2, height//3  # Vanishing point
    # Left lane
    cv2.line(image, (100, height), (vp_x - 50, vp_y), (255, 255, 255), 3)
    # Right lane
    cv2.line(image, (width - 100, height), (vp_x + 50, vp_y), (255, 255, 255), 3)

    print(f"Created synthetic image: {image.shape}")
else:
    print(f"Image loaded successfully: {image.shape}")

# Define ROI configuration
# The trapezoid ratios define the region of interest in the front-view image
roi_config = {
    'top_left_ratio': (0.4, 0.6),      # Top-left corner (narrower, farther)
    'top_right_ratio': (0.6, 0.6),     # Top-right corner
    'bottom_right_ratio': (0.9, 0.95),  # Bottom-right corner (wider, closer)
    'bottom_left_ratio': (0.1, 0.95),   # Bottom-left corner
    'bev_width': 640,                   # BEV output width in pixels
    'bev_height': 480                   # BEV output height in pixels
}

print("\nROI Configuration:")
print(f"  Trapezoid (front-view): top=({roi_config['top_left_ratio']}, {roi_config['top_right_ratio']})")
print(f"                         bottom=({roi_config['bottom_left_ratio']}, {roi_config['bottom_right_ratio']})")
print(f"  BEV output size: {roi_config['bev_width']}x{roi_config['bev_height']}")

# Create IPM transform
print("\nInitializing IPMTransform...")
ipm = IPMTransform(image.shape[:2], roi_config)
print(f"  Homography matrix H:")
print(f"{ipm.H}")

# Transform to BEV
print("\nTransforming image to Bird's Eye View...")
bev_image = ipm.transform_to_bev(image)
print(f"  BEV image shape: {bev_image.shape}")

# Display results
print("\nDisplaying results (press any key to close)...")
cv2.imshow('Front-View (Original)', image)
cv2.imshow('Bird\'s Eye View (BEV)', bev_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("\n✓ IPM transformation complete!")
print("\nNext steps:")
print("  - Adjust ROI ratios in roi_config to better fit your road images")
print("  - Use ipm.transform_points_to_bev() to transform detected lane points")
print("  - Explore Notebook 1 & 2 to understand the mathematics behind IPM")
print("  - See how BEV makes lane detection easier (parallel lines stay parallel!)")