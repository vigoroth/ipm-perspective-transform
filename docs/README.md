# Project 02: Perspective Transformation & BEV - Technical Documentation

> 📘 **For project overview and quick start guide, see the [main README](../README.md)**

This document provides detailed technical documentation for the perspective transformation implementation.

## Overview
Geometric transformation system implementing homography-based Inverse Perspective Mapping (IPM) to convert front-view camera images to Bird's Eye View (BEV) representation for improved lane detection and spatial reasoning.

## Objectives
- Implement homography computation using Direct Linear Transformation
- Build Inverse Perspective Mapping system
- Create interactive calibration tool
- Transform images to BEV representation
- Understand transformation limitations and failure modes

## Timeline
- **Duration:** 10-15 hours
- **Difficulty:** ⭐⭐⭐ Medium

## Prerequisites
- Project 01 completed
- Linear algebra (matrices, transformations)
- Basic camera geometry understanding
- NumPy and OpenCV proficiency

## Setup
```bash
pip install -r requirements.txt
```

## Project Structure
```
project-02-perspective-transform/
├── src/
│   ├── homography.py          # DLT homography solver
│   ├── ipm.py                  # IPM transformation class
│   ├── interactive_tool.py     # Calibration GUI
│   └── visualizer.py           # Visualization utilities
├── tests/
│   ├── test_homography.py
│   └── test_ipm.py
├── notebooks/
│   ├── 01_understanding_homography.ipynb
│   ├── 02_ipm_experiments.ipynb
│   └── 03_failure_modes.ipynb
├── data/
│   ├── calibration/
│   └── test_images/
├── results/
│   └── transformations/
└── docs/
```

## Detailed Instructions
See `PROJECT_02_PERSPECTIVE_TRANSFORM.md` for complete implementation guide.

## Usage

### Running IPM Transformation

```bash
# Interactive calibration tool
python src/interactive_tool.py --image data/test_images/road.jpg

# Transform single image to BEV
python src/main.py --image data/test_images/road.jpg --output results/

# Use saved calibration
python src/main.py --image data/test_images/road.jpg --calibration config/calibration.yaml
```

### Using the IPM Class

```python
from ipm import IPMTransform
import cv2

# Load image
image = cv2.imread('data/test_images/road.jpg')

# Create IPM transform with ROI configuration
roi_config = {
    'top_left_ratio': (0.4, 0.6),
    'top_right_ratio': (0.6, 0.6),
    'bottom_left_ratio': (0.1, 0.95),
    'bottom_right_ratio': (0.9, 0.95),
    'bev_width': 640,
    'bev_height': 480
}

ipm = IPMTransform(image.shape[:2], roi_config)

# Transform to BEV
bev_image = ipm.transform_to_bev(image)

# Transform points
points = np.array([[320, 400], [400, 400]])  # Image coordinates
bev_points = ipm.transform_points_to_bev(points)
```

## Testing

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run tests with coverage report
python -m pytest tests/ --cov=src --cov-report=term --cov-report=html

# View HTML coverage report
# Open htmlcov/index.html in browser
```

### Run Specific Test Modules

```bash
# Test homography solver only
pytest tests/test_homography.py -v

# Test IPM transformation only
pytest tests/test_ipm.py -v

# Test interactive tool only
pytest tests/test_interactive.py -v
```

### Test Coverage

Current test suite:
- **Unit tests** for homography computation (DLT algorithm)
- **Integration tests** for IPM transformation pipeline
- **Validation tests** for accuracy metrics
- **Performance tests** for benchmarking

## Validation

### Accuracy Metrics

Validate IPM transformation accuracy:

```bash
python src/validation/validate_ipm.py \
    --calibration config/calibration.yaml \
    --test-pattern data/calibration/checkerboard.jpg \
    --output results/validation_report.md
```

**Validation Metrics:**
- Point reprojection error (pixels)
- Distance preservation error (%)
- Angle preservation error (degrees)
- Homography condition number

### Performance Benchmarks

Benchmark transformation performance:

```bash
python src/validation/benchmark_ipm.py \
    --sizes 640x480 1280x720 1920x1080 \
    --output results/performance_report.md
```

**Performance Metrics:**
- Image transformation time
- Point transformation time
- Homography computation time
- Memory usage

## Project Results

**Implementation Status:**
- Homography solver: Direct Linear Transformation (DLT)
- IPM class: Forward and inverse transformations
- Interactive tool: Point-based calibration
- Camera model: Pinhole projection (optional)

**Validation Results:**
- Point reprojection error: < 2 pixels (target)
- Transformation time (1280x720): ~5-10ms
- Homography computation: < 1ms

## Success Criteria

- [x] Homography computation correct
- [x] IPM transformation accurate
- [x] Interactive calibration tool functional
- [x] BEV visualization clear
- [x] Failure modes documented
- [x] Validation metrics computed
- [x] Performance benchmarked
- [x] Comprehensive documentation

## Key Concepts

**Homogeneous Coordinates:**
- Represent 2D points in 3D space: (x, y, 1)
- Enable matrix representation of translations
- Essential for projective transformations

**Homography:**
- 3x3 matrix mapping between planar surfaces
- 8 degrees of freedom
- Requires 4 point correspondences minimum
- Solved using SVD (Singular Value Decomposition)

**IPM Assumptions:**
- Flat ground plane (Z = 0)
- Fixed camera calibration
- Planar transformation region only
- Known source and destination correspondence

**Limitations:**
- Fails on non-planar surfaces (hills, slopes)
- Distorts objects with height (vehicles, pedestrians)
- Requires careful calibration
- Single homography unsuitable for curved roads

## Resources

### Core Documentation
- OpenCV: warpPerspective, getPerspectiveTransform
- PROJECT_02_PERSPECTIVE_TRANSFORM.md (detailed guide)
- Jupyter notebooks in notebooks/

### Recommended Reading
- Multiple View Geometry (Hartley & Zisserman): Chapter 2
- "Inverse Perspective Mapping" (Bertozzi et al., 2008)
- "Lift, Splat, Shoot" (Philion & Fidler, 2020) - Modern learned approach

### Video Lectures
- First Principles of Computer Vision: "Homography"
- Cyrill Stachniss: "Projective Geometry"

---
*Part of 12-project learning path for 3D Lane Detection thesis*
