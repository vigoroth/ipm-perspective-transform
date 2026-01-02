# Project 2: Perspective Transformation Deep Dive
## Understanding the Bridge Between 2D Images and 3D World

**Duration:** Week 2 (10-15 hours)
**Difficulty:** ⭐⭐⭐ Medium
**Prerequisites:** Project 1 completed, basic linear algebra, matrix operations
**Goal:** Master coordinate transformations and build intuition for BEV

---

## 🎯 Learning Objectives

By completing this project, you will:
1. Understand homography and perspective transformation mathematics
2. Implement Inverse Perspective Mapping (IPM) from scratch
3. Learn coordinate system conversions (image ↔ world ↔ BEV)
4. Build interactive calibration tools for real-world deployment
5. Recognize when transformations work and when they fail

---

## 📋 Project Structure

Create this directory structure:
```
project-02-perspective-transform/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── homography.py          # Core transformation math
│   ├── ipm.py                  # IPM implementation
│   ├── interactive_tool.py     # GUI calibration tool
│   └── visualizer.py           # Visualization utilities
├── tests/
│   ├── __init__.py
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
│   ├── transformations/
│   └── interactive_demos/
└── docs/
    ├── math_foundations.md
    └── implementation_notes.md
```

---

## 🚀 Step-by-Step Instructions

### **PHASE 1: Mathematical Foundations (2-3 hours)**

#### Step 1.1: Homogeneous Coordinates
**Task:** Understand why homogeneous coordinates are essential

**Instructions:**
1. Study the concept:
   - Cartesian point: (x, y)
   - Homogeneous point: (x, y, w) where x_cart = x/w, y_cart = y/w
   - Why? Allows representing translation as matrix multiplication
2. Work through conversion examples
3. Implement conversion functions

**Theory to Grasp:**
- In Cartesian coordinates, we cannot represent translation as matrix multiplication
- Homogeneous coordinates add an extra dimension (w) to enable this
- Multiple homogeneous points can represent the same Cartesian point
- Points at infinity have w=0

**Exercises:**
1. Convert these points to homogeneous:
   - (5, 10) → (5, 10, 1) or (10, 20, 2) or ...
   - (100, 200) → (100, 200, 1) or ...
2. Convert these to Cartesian:
   - (10, 20, 2) → (5, 10)
   - (50, 100, 5) → (10, 20)
3. What makes (0, 0, 0) special? (Undefined point!)

**Implement:**
```python
def to_homogeneous(points):
    """
    Convert Cartesian coordinates to homogeneous

    Args:
        points: (N, 2) array of 2D points
    Returns:
        (N, 3) array with w=1
    """
    pass  # Your implementation

def from_homogeneous(points):
    """
    Convert homogeneous coordinates to Cartesian

    Args:
        points: (N, 3) array
    Returns:
        (N, 2) array
    """
    pass  # Your implementation
```

**Questions to Answer:**
- Why can't we represent translation with 2x2 matrices?
- How does the extra dimension help?
- What happens if w=0?

**Deliverable:** Working conversion functions with unit tests

---

#### Step 1.2: Homography Matrix Theory
**Task:** Understand what homography represents

**Instructions:**
1. Study the homography equation:
   ```
   [x']   [h11 h12 h13]   [x]
   [y'] = [h21 h22 h23] × [y]
   [w']   [h31 h32 h33]   [1]
   ```
2. Understand degrees of freedom (8 DOF from 9 elements - 1 scale)
3. Learn why we need 4 point correspondences minimum
4. Study the Direct Linear Transform (DLT) algorithm

**Key Concept:** Homography Properties
- 8 degrees of freedom (9 elements, but scale-invariant)
- Preserves straight lines (collinearity)
- Only works for planar surfaces!
- Needs at least 4 point correspondences to solve
- More points = better (overdetermined system with SVD)

**Exercises:**
1. Given 4 source-destination point pairs, what system do we solve?
   - Build 8x9 matrix A
   - Solve Ah = 0 using SVD
2. Why exactly 4 points minimum?
   - Each point gives 2 equations
   - Need 8 equations for 8 unknowns
3. What happens with 3 points? More than 4?
   - 3 points: underdetermined (infinity of solutions)
   - >4 points: overdetermined (least squares solution)

**Challenge:** Derive the DLT equations manually

**Deliverable:** Written derivation and understanding

---

#### Step 1.3: Homography Solver
**Task:** Implement homography computation from scratch

**Instructions:**
1. Build the DLT matrix A from point correspondences
2. Solve using SVD (Singular Value Decomposition)
3. Reshape solution vector to 3x3 matrix
4. Normalize so H[2,2] = 1

**Implement:**
```python
def compute_homography(src_points, dst_points):
    """
    Compute homography using Direct Linear Transformation

    Args:
        src_points: (N, 2) array - source coordinates (N >= 4)
        dst_points: (N, 2) array - destination coordinates
    Returns:
        H: (3, 3) homography matrix

    Algorithm:
        1. For each correspondence (x,y) -> (x',y'):
           Build two rows of matrix A:
           [-x, -y, -1,  0,  0,  0, x'x, x'y, x']
           [ 0,  0,  0, -x, -y, -1, y'x, y'y, y']
        2. Solve Ah = 0 using SVD: h is last column of V
        3. Reshape h to 3x3 matrix H
        4. Normalize H so H[2,2] = 1
    """
    pass  # Build this from scratch!
```

**Key Concept:** Why SVD?
- SVD finds the null space of A
- Last column of V (smallest singular value) gives solution
- Minimizes ||Ah|| in least-squares sense for overdetermined systems

**Challenge:** Implement without using OpenCV's `findHomography()`

**Test Cases:**
1. Identity test: source = destination → H should be identity
2. Translation test: shift all points → H encodes translation
3. Rotation test: rotate points → H encodes rotation

**Deliverable:** Homography solver with documentation and tests

---

### **PHASE 2: Inverse Perspective Mapping (3-4 hours)**

#### Step 2.1: Understanding IPM
**Task:** Learn why IPM is crucial for lane detection

**Instructions:**
1. Understand the perspective projection problem
2. Study Bird's Eye View (BEV) benefits
3. Identify the key assumption (flat ground plane)
4. Recognize limitations

**Concept Visualization:**
```
Front View (Perspective)    →    Bird's Eye View (Orthographic)
      /\                              ________________
     /  \                            |                |
    /    \                           |                |
   /  ||  \                          |      ||        |
  /   ||   \                         |      ||        |
 /__________\                        |________________|
```

**Key Concept:** Why IPM for Lanes?
- Front view: Parallel lanes converge (perspective)
- BEV: Parallel lanes stay parallel (easier to detect)
- Distance estimation: Uniform scale in BEV
- Lane geometry: Clearer relationships

**Limitations to Understand:**
- Assumes flat ground plane (Z=0)
- Fails for non-planar objects (pedestrians, cars, hills)
- Distorts objects with height
- Only works in defined ROI

**Questions to Answer:**
- Why do parallel lines converge in perspective view?
- What happens to a pedestrian in IPM? (Distorted heavily!)
- When does the flat ground assumption break?
- How does IPM help lane detection algorithms?

**Exercise:** Draw the transformation for a simple road scene

**Deliverable:** Written explanation with diagrams

---

#### Step 2.2: Defining Source and Destination Points
**Task:** Set up the transformation geometry

**Instructions:**
1. Define source points (front view trapezoid):
   - Cover the road region of interest
   - Typically a trapezoid shape
   - Adjust based on camera mounting height/angle
2. Define destination points (BEV rectangle):
   - Rectangular region
   - Represents overhead view of same area
   - Choose appropriate output size

**Typical Configuration:**
```python
# Source points (front view) - trapezoid
src_points = np.float32([
    [width * 0.4,  height * 0.6],   # Top-left
    [width * 0.6,  height * 0.6],   # Top-right
    [width * 0.9,  height * 0.95],  # Bottom-right
    [width * 0.1,  height * 0.95]   # Bottom-left
])

# Destination points (BEV) - rectangle
dst_points = np.float32([
    [0,          0],           # Top-left
    [bev_width,  0],           # Top-right
    [bev_width,  bev_height],  # Bottom-right
    [0,          bev_height]   # Bottom-left
])
```

**Key Concept:** Point Selection Strategy
- Source trapezoid should align with lane boundaries
- Wider bottom = closer to camera (perspective)
- Narrower top = farther from camera
- Destination rectangle = uniform spacing

**Challenge:** How to choose these points automatically?
- Use lane detection from Project 1
- Fit trapezoid to detected lanes
- Adaptive based on image content

**Deliverable:** Configurable point selection function

---

#### Step 2.3: IPM Class Implementation
**Task:** Build the IPM transformation class

**Instructions:**
1. Create IPM class to encapsulate transformation
2. Compute homography from source/destination points
3. Store both forward (H) and inverse (H_inv) transforms
4. Implement image and point transformation methods

**Implement:**
```python
class IPMTransform:
    def __init__(self, image_shape, roi_config):
        """
        Initialize IPM transformation

        Args:
            image_shape: (height, width) of input image
            roi_config: dict with ROI parameters
        """
        self.image_height = image_shape[0]
        self.image_width = image_shape[1]

        # Compute source and destination points
        self.src_points = self._compute_src_points(roi_config)
        self.dst_points = self._compute_dst_points(roi_config)

        # Compute homography matrices
        self.H = compute_homography(self.src_points, self.dst_points)
        self.H_inv = np.linalg.inv(self.H)

    def _compute_src_points(self, config):
        """Compute source trapezoid vertices"""
        pass  # Implement based on config

    def _compute_dst_points(self, config):
        """Compute destination rectangle vertices"""
        pass  # Implement based on config

    def transform_to_bev(self, image):
        """Transform front-view image to BEV"""
        pass  # Use cv2.warpPerspective

    def transform_from_bev(self, bev_image):
        """Transform BEV back to front-view"""
        pass  # Use H_inv

    def transform_points_to_bev(self, points):
        """Transform points from front-view to BEV"""
        pass  # Apply H to homogeneous points

    def transform_points_from_bev(self, bev_points):
        """Transform points from BEV to front-view"""
        pass  # Apply H_inv
```

**Key Parameters for warpPerspective:**
- dsize: Output image size (bev_width, bev_height)
- flags: Interpolation (cv2.INTER_LINEAR recommended)
- borderMode: cv2.BORDER_CONSTANT
- borderValue: (0, 0, 0) for black borders

**Deliverable:** Complete IPM class with all methods

---

#### Step 2.4: Validation and Testing
**Task:** Verify IPM implementation correctness

**Instructions:**
1. Test point round-trip: front → BEV → front
2. Test image transformation on known patterns
3. Verify parallel lines stay parallel in BEV
4. Measure transformation accuracy

**Test Cases:**
```python
def test_point_roundtrip():
    """Points should return to original after round trip"""
    # Create IPM transform
    # Transform points to BEV
    # Transform back to front view
    # Verify original == result (within tolerance)
    pass

def test_parallel_lines():
    """Parallel lines in world should be parallel in BEV"""
    # Create image with parallel lines
    # Transform to BEV
    # Measure line angles
    # Verify parallelism
    pass
```

**Deliverable:** Complete test suite

---

### **PHASE 3: Interactive Calibration Tool (2-3 hours)**

#### Step 3.1: GUI Framework Setup
**Task:** Build interactive point selection tool

**Instructions:**
1. Choose GUI framework (OpenCV, matplotlib, or PyQt)
2. Set up image display window
3. Implement mouse callback for point selection
4. Display selected points with visual feedback

**Recommended:** Use OpenCV for simplicity
```python
class InteractiveIPM:
    def __init__(self, image):
        self.image = image.copy()
        self.display_image = image.copy()
        self.source_points = []
        self.bev_image = None
        self.window_name = "IPM Calibration"

    def mouse_callback(self, event, x, y, flags, param):
        """
        Handle mouse clicks

        - Left click: Add point
        - Right click: Remove last point
        - When 4 points selected: compute and show BEV
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.source_points) < 4:
                self.source_points.append((x, y))
                self.update_display()

                if len(self.source_points) == 4:
                    self.compute_and_show_bev()

        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.source_points:
                self.source_points.pop()
                self.update_display()
```

**Key Concept:** Interactive Feedback
- Show numbered markers at selected points
- Draw lines connecting points (trapezoid outline)
- Update display in real-time
- Show BEV immediately when 4 points selected

**Deliverable:** Working point selection interface

---

#### Step 3.2: Real-time BEV Computation
**Task:** Compute and display BEV transformation interactively

**Instructions:**
1. When 4 points are selected, compute homography
2. Transform image to BEV
3. Display both front-view and BEV side-by-side
4. Add grid overlay to verify calibration quality

**Implement:**
```python
def compute_and_show_bev(self):
    """Compute homography and display BEV"""
    # Define destination points (rectangle)
    dst_points = np.float32([
        [0, 0],
        [self.bev_width, 0],
        [self.bev_width, self.bev_height],
        [0, self.bev_height]
    ])

    # Compute homography
    src = np.float32(self.source_points)
    H = compute_homography(src, dst_points)

    # Transform image
    self.bev_image = cv2.warpPerspective(
        self.image, H,
        (self.bev_width, self.bev_height)
    )

    # Draw grid and display
    self.draw_verification_grid()
    self.display_results()

def draw_verification_grid(self, spacing=50):
    """Draw grid lines to verify parallelism"""
    for x in range(0, self.bev_width, spacing):
        cv2.line(self.bev_image, (x, 0), (x, self.bev_height), (0, 255, 0), 1)
    for y in range(0, self.bev_height, spacing):
        cv2.line(self.bev_image, (0, y), (self.bev_width, y), (0, 255, 0), 1)
```

**Key Concept:** Verification Grid
- Parallel grid lines should appear parallel in correct BEV
- Lane markings should align with grid
- Equal spacing indicates correct calibration

**Deliverable:** Real-time BEV visualization with grid

---

#### Step 3.3: Calibration Saving and Loading
**Task:** Persist calibration parameters

**Instructions:**
1. Save transformation matrix to file
2. Save source/destination points
3. Load calibration for reuse
4. Support multiple calibration profiles

**Implement:**
```python
def save_calibration(self, filepath):
    """Save calibration to YAML/JSON file"""
    config = {
        'source_points': self.source_points,
        'destination_points': self.destination_points.tolist(),
        'homography_matrix': self.H.tolist(),
        'bev_size': (self.bev_width, self.bev_height),
        'image_size': (self.image_width, self.image_height)
    }
    with open(filepath, 'w') as f:
        yaml.dump(config, f)

def load_calibration(filepath):
    """Load calibration from file"""
    with open(filepath, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config
```

**Deliverable:** Calibration persistence system

---

### **PHASE 4: Advanced Transformations (2-3 hours)**

#### Step 4.1: Camera Model Integration
**Task:** Extend IPM with full camera parameters

**Instructions:**
1. Implement pinhole camera model
2. Add intrinsic parameters (fx, fy, cx, cy)
3. Add extrinsic parameters (rotation, translation)
4. Build complete projection pipeline

**Theory:** Full Camera Model
```
World (X,Y,Z) → Camera (Xc,Yc,Zc) → Image (u,v)

K = [fx  0  cx]    # Intrinsic matrix
    [ 0 fy  cy]
    [ 0  0   1]

P = K[R|t]         # Projection matrix
```

**Implement:**
```python
class CameraModel:
    def __init__(self, intrinsics, extrinsics):
        """
        Full camera projection model

        Args:
            intrinsics: dict with fx, fy, cx, cy
            extrinsics: dict with rotation (3x3), translation (3x1)
        """
        # Build intrinsic matrix K
        self.K = np.array([
            [intrinsics['fx'], 0, intrinsics['cx']],
            [0, intrinsics['fy'], intrinsics['cy']],
            [0, 0, 1]
        ])

        self.R = extrinsics['rotation']
        self.t = extrinsics['translation']

        # Build projection matrix P = K[R|t]
        self.P = self.K @ np.hstack([self.R, self.t])

    def project_3d_to_2d(self, points_3d):
        """Project 3D world points to 2D image"""
        # points_3d: (N, 3)
        # Convert to homogeneous: (N, 4)
        # Apply P: points_2d_h = P @ points_3d_h.T
        # Convert from homogeneous
        pass  # Implement

    def backproject_2d_to_3d(self, points_2d, Z=0):
        """
        Backproject 2D image points to 3D

        Requires assumption: ground plane Z=0
        """
        # Solve for (X,Y) given (u,v) and Z=0
        pass  # Implement using pseudo-inverse
```

**Key Concept:** Camera Calibration
- Intrinsics: Camera-specific (focal length, principal point)
- Extrinsics: Installation-specific (position, orientation)
- Can be obtained from calibration patterns (checkerboard)

**Deliverable:** Complete camera model class

---

#### Step 4.2: Metric BEV Generation
**Task:** Create BEV with real-world scale

**Instructions:**
1. Define meters-per-pixel scale for BEV
2. Create world coordinate grid
3. Project grid to image coordinates
4. Sample colors from original image to build BEV

**Goal:** 1 pixel in BEV = 0.1 meters in world

**Implement:**
```python
def create_metric_bev(image, camera_model, meters_per_pixel=0.1,
                     x_range=(-10, 10), y_range=(0, 50)):
    """
    Create metrically accurate BEV

    Args:
        image: Front-view image
        camera_model: CameraModel with calibration
        meters_per_pixel: Real-world scale
        x_range: (x_min, x_max) in meters
        y_range: (y_min, y_max) in meters (forward distance)
    Returns:
        bev_image: BEV image
        transform_info: Metadata
    """
    # Create grid of world coordinates
    # All points on ground plane (Z=0)
    # Project to image coordinates
    # Sample colors and build BEV
    pass  # Implement
```

**Key Concept:** Why Metric BEV?
- Enables distance measurements in meters
- Consistent scale for different cameras
- Required for multi-camera fusion
- Important for downstream algorithms

**Challenge:** How far forward should BEV extend?
- Limited by image resolution
- Limited by camera pitch angle
- Trade-off: coverage vs. resolution

**Deliverable:** Metric BEV generator

---

### **PHASE 5: Failure Mode Analysis (1-2 hours)**

#### Step 5.1: Systematic Failure Testing
**Task:** Identify and document when IPM fails

**Experiments to Conduct:**

1. **Hills and Slopes:**
   - Test on inclined roads
   - Observe distortion patterns
   - Measure error magnitude

2. **Speed Bumps:**
   - Local height variations
   - Object distortion in BEV
   - Recovery strategies

3. **Overpasses and Bridges:**
   - Non-ground-plane objects
   - Where do they appear?
   - Phantom projections

4. **Curved Roads:**
   - Does single homography work?
   - Local vs. global transformation
   - Piecewise IPM approach

**For Each Scenario:**
1. Capture or create test image
2. Apply IPM transformation
3. Document distortions with screenshots
4. Explain mathematical reason for failure
5. Propose mitigation strategies

**Deliverable:** Failure mode documentation with images and explanations

---

#### Step 5.2: Limitations Summary Table
**Task:** Create comprehensive limitations reference

**Create Table:**
| Scenario | IPM Works? | Reason | Impact | Alternative |
|----------|------------|--------|--------|-------------|
| Flat highway | ✅ Yes | Ground plane valid | None | - |
| Hilly road | ❌ No | Non-planar surface | Severe distortion | 3D reconstruction |
| Curved road | ⚠️ Partial | Local approximation | Minor distortion | Spline fitting |
| Parking lot | ✅ Yes | Flat surface | None | - |
| With pedestrians | ❌ No | Height objects | Object distortion | Semantic filtering |
| Tunnels | ✅ Yes | Flat floor | None | - |
| Intersections | ⚠️ Partial | Multiple planes | Edge distortion | Adaptive ROI |

**Key Insight:** Know Your Assumptions
- IPM is powerful but limited
- Violations of flat-ground assumption = failures
- Always validate assumptions in deployment
- Consider when to disable IPM

**Deliverable:** Comprehensive limitations documentation

---

### **PHASE 6: Validation & Benchmarking (1-2 hours)**

#### Step 6.1: Accuracy Validation
**Task:** Quantitatively measure transformation accuracy

**Method:**
1. Create synthetic calibration pattern (checkerboard)
2. Transform to BEV
3. Measure distances and angles
4. Compare with ground truth
5. Compute error metrics

**Metrics to Compute:**
```python
def validate_ipm(ipm_transform, test_points, ground_truth):
    """
    Compute validation metrics

    Returns:
        metrics: {
            'point_reprojection_error_px': mean absolute error,
            'distance_preservation_error_pct': relative error,
            'angle_preservation_error_deg': angular error,
            'max_error_px': worst-case error
        }
    """
    # Transform test points
    transformed = ipm_transform.transform_points_to_bev(test_points)

    # Compute errors
    # ...

    return metrics
```

**Acceptance Criteria:**
- Point reprojection error < 2 pixels
- Distance preservation < 5% error
- Angle preservation < 2 degrees

**Deliverable:** Validation report with metrics

---

#### Step 6.2: Performance Benchmarking
**Task:** Measure computational performance

**Benchmarks:**
1. Image transformation time (various sizes)
2. Point transformation time (various counts)
3. Homography computation time
4. Memory usage

**Test Conditions:**
```python
def benchmark_ipm():
    """Run performance benchmarks"""
    image_sizes = [(640, 480), (1280, 720), (1920, 1080)]
    point_counts = [10, 100, 1000, 10000]

    results = {}

    for size in image_sizes:
        # Time image transformation
        # Time homography computation
        pass

    for n_points in point_counts:
        # Time point transformation
        pass

    return results
```

**Expected Performance (approximate):**
- 1280x720 image transformation: < 10ms
- 1000 points transformation: < 1ms
- Homography computation: < 1ms

**Deliverable:** Performance benchmark report

---

### **PHASE 7: Integration & Documentation (1-2 hours)**

#### Step 7.1: Create Educational Notebooks
**Task:** Build Jupyter notebooks for learning

**Notebook 1: Understanding Homography (01_understanding_homography.ipynb)**
- Theory explanation with equations
- Interactive visualizations of transformations
- Step-by-step DLT algorithm walkthrough
- Visual comparison of different transformations

**Notebook 2: IPM Experiments (02_ipm_experiments.ipynb)**
- Load and display test images
- Apply IPM with different configurations
- Visualize results side-by-side
- Experiment with parameter variations

**Notebook 3: Failure Modes (03_failure_modes.ipynb)**
- Demonstrate each failure case
- Visual comparison of distortions
- Explanation of underlying causes
- Discussion of alternative approaches

**Deliverable:** 3 comprehensive educational notebooks

---

#### Step 7.2: API Documentation
**Task:** Document all classes and functions

**Documentation Requirements:**
1. Docstrings for all public methods
2. Type hints for parameters and returns
3. Usage examples in docstrings
4. API reference document

**Example Docstring:**
```python
def compute_homography(src_points, dst_points):
    """
    Compute homography matrix using Direct Linear Transformation (DLT).

    The homography H maps points from source plane to destination plane:
    dst = H @ src (in homogeneous coordinates)

    Args:
        src_points (np.ndarray): Source points, shape (N, 2) where N >= 4
        dst_points (np.ndarray): Destination points, shape (N, 2)

    Returns:
        np.ndarray: Homography matrix H, shape (3, 3)

    Raises:
        ValueError: If fewer than 4 points provided

    Example:
        >>> src = np.array([[0,0], [1,0], [1,1], [0,1]])
        >>> dst = np.array([[0,0], [2,0], [2,2], [0,2]])  # 2x scaling
        >>> H = compute_homography(src, dst)
        >>> # H should be approximately [[2,0,0], [0,2,0], [0,0,1]]
    """
```

**Deliverable:** Complete API documentation

---

## 📊 Evaluation Rubric

### **Mathematical Understanding (30%)**
- [ ] Correctly explains homogeneous coordinates and their purpose
- [ ] Understands homography degrees of freedom (8 DOF) and constraints
- [ ] Can derive transformation matrices from point correspondences
- [ ] Recognizes when flat-ground assumption breaks
- [ ] Understands the relationship between IPM and camera geometry

### **Implementation Quality (30%)**
- [ ] Homography solver implemented correctly from scratch
- [ ] IPM transformation produces accurate results
- [ ] Interactive calibration tool is functional and user-friendly
- [ ] Code is modular, well-organized, and reusable
- [ ] Proper error handling and input validation

### **Analysis & Validation (20%)**
- [ ] Comprehensive failure mode analysis conducted
- [ ] Quantitative validation performed with metrics
- [ ] Performance benchmarked across conditions
- [ ] Limitations clearly documented with examples
- [ ] Appropriate test coverage

### **Documentation (20%)**
- [ ] Clear mathematical explanations in docs
- [ ] Jupyter notebooks are educational and well-structured
- [ ] API documentation complete with examples
- [ ] Usage instructions clear and accurate
- [ ] Code comments explain "why" not just "what"

---

## 🎓 Key Takeaways

After completing this project, you should understand:

1. **Geometric Transformations:**
   - Why homogeneous coordinates are essential for projective geometry
   - How homography matrices encode planar transformations
   - When coordinate transformations are valid and when they break

2. **IPM for Autonomous Driving:**
   - Benefits of Bird's Eye View for lane detection and path planning
   - Critical importance of the flat-ground assumption
   - How calibration affects transformation quality
   - Trade-offs between coverage and accuracy

3. **Foundations for Modern Methods:**
   - BEV representation is standard in modern 3D perception
   - Deep learning can learn transformations (LSS, BEVFormer)
   - Classical IPM provides geometric intuition
   - Understanding limitations guides when to use learned vs. geometric approaches

4. **Practical Engineering:**
   - Implementing mathematical concepts in code
   - Building interactive tools for real-world deployment
   - Validating computer vision algorithms systematically
   - Documenting limitations for production systems

---

## 📚 Recommended Reading

**Before Starting:**
- Multiple View Geometry (Hartley & Zisserman): Chapter 2 (Projective Geometry)
- Computer Vision: A Modern Approach (Forsyth): Chapter 6 (Geometry)

**While Working:**
- "Inverse Perspective Mapping: Simplifications and Extensions" (Bertozzi, 2008)
- "A Versatile Method for Road Detection" (Danescu, 2013)
- OpenCV documentation: warpPerspective, findHomography

**After Completing:**
- "Lift, Splat, Shoot" (Philion & Fidler, 2020) - Modern learned BEV
- "BEVFormer" (Li et al., 2022) - Transformer-based BEV
- Compare classical IPM with learned approaches

**Video Lectures:**
- Cyrill Stachniss: "Photogrammetry I - 06 - Projective Geometry"
- First Principles of Computer Vision: "Homography and Image Mosaics"

---

## 💡 Debugging Tips

**Homography not working?**
- Check point correspondences are correct
- Verify points are in correct order (clockwise/counterclockwise)
- Ensure at least 4 non-collinear points
- Print intermediate DLT matrix to check for numerical issues

**BEV looks distorted?**
- Verify source points define valid trapezoid
- Check destination points form rectangle
- Ensure points are in same coordinate system
- Visualize selected points before computing homography

**Lanes not parallel in BEV?**
- Recheck calibration points (should be on lane boundaries)
- Ensure points are equidistant along lanes
- Try different vertical positions in image
- Check if road is truly flat

**Transformation too slow?**
- Reduce BEV output size
- Use INTER_LINEAR instead of INTER_CUBIC
- Pre-compute homography matrix
- Consider using GPU (cv2.cuda module)

**Interactive tool not responding?**
- Check if cv2.waitKey() is called in loop
- Verify mouse callback is registered correctly
- Add print statements to debug event handling
- Test with simple opencv mouse example first

---

## 🚀 Next Steps

After completing Project 2:
1. Review your failure mode analysis
2. Commit code to GitHub with clear documentation
3. Reflect on limitations of classical geometric approaches
4. Move to Project 3: Full 3D Coordinate Systems
5. Think ahead: How can neural networks learn these transformations?

---

## 📝 Submission Checklist

Before moving to the next project:
- [ ] Homography solver implemented and tested
- [ ] IPM class functional with forward/inverse transforms
- [ ] Interactive calibration tool working
- [ ] Camera model integrated (optional but recommended)
- [ ] Failure mode analysis documented with examples
- [ ] Validation metrics computed and recorded
- [ ] Three Jupyter notebooks completed
- [ ] API documentation written
- [ ] README with usage examples
- [ ] Test suite passing
- [ ] GitHub repository organized and pushed
- [ ] Personal understanding of concepts solid

---

**Remember:** This project bridges classical CV and modern deep learning. Understanding IPM deeply will help you appreciate why methods like LSS and BEVFormer are revolutionary. Take time to experiment and visualize! Good luck! 🎓
