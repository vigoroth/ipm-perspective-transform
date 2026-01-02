# Mathematical Foundations for Perspective Transformation

> =→ **Complete mathematical theory for homography-based transformations and Inverse Perspective Mapping (IPM)**

This document provides the mathematical foundations necessary to understand and implement perspective transformations for converting camera images to Bird's Eye View (BEV) representation in autonomous driving applications.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Homogeneous Coordinates](#homogeneous-coordinates)
3. [Homography Matrix Theory](#homography-matrix-theory)
4. [Direct Linear Transformation (DLT) Algorithm](#direct-linear-transformation-dlt-algorithm)
5. [Inverse Perspective Mapping (IPM) Mathematics](#inverse-perspective-mapping-ipm-mathematics)
6. [Camera Models](#camera-models)
7. [Coordinate Systems](#coordinate-systems)
8. [Mathematical Limitations](#mathematical-limitations)
9. [References](#references)

---

## Introduction

### Purpose

Perspective transformations are fundamental to computer vision and autonomous driving. This document covers the mathematical theory behind:

- **Homography:** Planar projective transformations between image planes
- **Inverse Perspective Mapping (IPM):** Converting front-view camera images to Bird's Eye View
- **Camera Models:** Relating 3D world to 2D image coordinates

### Why Perspective Transformation for Autonomous Driving?

In autonomous driving, cameras capture the world in **perspective view**:
- Parallel lines (e.g., lane markings) appear to converge toward a vanishing point
- Objects farther away appear smaller
- Equal distances appear unequal in the image

**Bird's Eye View (BEV)** provides an **orthographic projection**:
- Parallel lines remain parallel
- Uniform metric scale (e.g., 1 pixel = 0.1 meters)
- Simpler geometric relationships for path planning and lane detection

**The Challenge:** Transform between these representations using mathematical mappings.

---

## Homogeneous Coordinates

### Motivation: Why Do We Need Them?

In **Cartesian coordinates**, we represent 2D points as `(x, y)`.

**Problem:** We cannot represent **translation** as a matrix multiplication in 2D:
```
Translation: (x, y) → (x + tx, y + ty)
```

This is an affine operation, not a linear one. We'd need:
```
[x']   [1  0] [x]   [tx]
[y'] = [0  1] [y] + [ty]
```

The `+ [tx, ty]` part prevents us from using a single matrix multiplication.

**Solution:** **Homogeneous coordinates** add an extra dimension to enable **all** transformations (including translation) as matrix multiplications.

### Definition

A 2D Cartesian point `(x, y)` is represented in **homogeneous coordinates** as a 3D vector:
```
(x, y) → (x, →, w) where w ` 0
```

The relationship between Cartesian and homogeneous coordinates is:
```
x = x / w
y = → / w
```

**Key Insight:** Multiple homogeneous representations map to the same Cartesian point:
```
(x, y, 1) a (2x, 2y, 2) a (kx, ky, k) for any k ` 0
```

This is called **projective equivalence**: `(x, →, w) ~ (kx, k→, kw)`.

### Conversion Between Representations

#### Cartesian → Homogeneous

For a 2D point `(x, y)`, the standard homogeneous representation uses `w = 1`:
```
(x, y) → (x, y, 1)
```

**Example:**
```
(5, 10)     → (5, 10, 1)
(100, 200)  → (100, 200, 1)
```

#### Homogeneous → Cartesian

For a homogeneous point `(x, →, w)` with `w ` 0`:
```
(x, →, w) → (x/w, →/w)
```

**Examples:**
```
(10, 20, 2)    → (10/2, 20/2)   = (5, 10)
(50, 100, 5)   → (50/5, 100/5)  = (10, 20)
(6, 9, 3)      → (6/3, 9/3)     = (2, 3)
```

### Special Cases and Properties

#### Points at Infinity

When `w = 0`, the point represents a **direction** or **point at infinity**:
```
(x, →, 0) → (x/0, →/0) = (, ) in direction (x, →)
```

**Geometric Interpretation:**
- Parallel lines in Cartesian space intersect at infinity in projective space
- All parallel lines with the same direction share the same point at infinity

**Example:**
```
(1, 0, 0) = point at infinity in the x-direction
(0, 1, 0) = point at infinity in the y-direction
```

#### Invalid Point

The point `(0, 0, 0)` is **undefined** in homogeneous coordinates (no valid Cartesian equivalent).

### Translation in Homogeneous Coordinates

Now we can represent **translation** as a matrix multiplication:

```
[x']   [1  0  tx] [x]
[y'] = [0  1  ty] [y]
[w']   [0  0  1 ] [w]
```

For `w = 1`:
```
[x']   [1  0  tx] [x]   [x + tx]
[y'] = [0  1  ty] [y] = [y + ty]
[1 ]   [0  0  1 ] [1]   [  1   ]
```

**This unification allows us to represent ALL transformations (rotation, scaling, translation, perspective) as 3→3 matrices!**

### Summary

| Property | Cartesian (2D) | Homogeneous (3D) |
|----------|---------------|------------------|
| Representation | `(x, y)` | `(x, →, w)` with `w ` 0` |
| Equivalence | Unique | `(x, →, w) ~ (kx, k→, kw)` |
| Translation | Requires addition | Matrix multiplication |
| Points at  | Cannot represent | `(x, →, 0)` |
| Dimension | 2D | 3D (projective plane) |

**Key Takeaway:** Homogeneous coordinates enable all geometric transformations as matrix operations, which is essential for perspective transformations and homography.

---

## Homography Matrix Theory

### Definition

A **homography** (also called **projective transformation** or **planar homography**) is a mapping between two **planar** surfaces. It is represented by a 3→3 matrix **H** that transforms homogeneous coordinates:

```
[x']       [x]
[y']  = H  [y]
[w']       [1]
```

Where:
```
     [h11  h12  h13]
H =  [h21  h22  h23]
     [h31  h32  h33]
```

After applying **H**, we convert back to Cartesian coordinates:
```
x' = (h11→x + h12→y + h13) / (h31→x + h32→y + h33)
y' = (h21→x + h22→y + h23) / (h31→x + h32→y + h33)
```

### Degrees of Freedom

The homography matrix has **9 elements**, but only **8 degrees of freedom (DOF)**.

**Why 8 DOF?**
- The matrix is defined up to a scale factor: `H ~ k→H` for any `k ` 0`
- We can normalize one element (typically `h33 = 1`) without loss of generality
- This leaves 8 independent parameters

**Consequence:** We need at least **4 point correspondences** to solve for H:
- Each point correspondence gives 2 equations (one for x, one for y)
- 4 points → 2 equations/point = 8 equations for 8 unknowns

### Homography Properties

#### 1. Preserves Collinearity

**Straight lines remain straight** under homography.

If three points are collinear (lie on a line) in the source plane, their transformed points are also collinear in the destination plane.

**Mathematical Proof:**
A line in homogeneous coordinates: `l^T → p = 0`
After transformation: `l'^T → p' = l'^T → H → p = 0`
The transformed line `l' = H^{-T} → l` is still a line.

#### 2. Preserves Cross-Ratio

The **cross-ratio** of four collinear points is preserved under homography. This is a fundamental projective invariant.

#### 3. Does NOT Preserve

- **Distances:** Equal distances in source ` equal distances in destination
- **Angles:** Right angles may not remain right angles
- **Parallelism:** Parallel lines may not remain parallel (except affine transformations)
- **Areas:** Area ratios change

#### 4. Planar Restriction

**Critical Assumption:** Homography only works for **planar surfaces** or **pure camera rotation**.

If the scene is not planar (e.g., objects at different depths), a single homography cannot correctly map all points.

### Relationship to Other Transformations

Homography is the most general 2D transformation. It includes all simpler transformations as special cases:

| Transformation | DOF | Matrix Form | Properties Preserved |
|---------------|-----|-------------|---------------------|
| **Euclidean** (rotation + translation) | 3 | `h31=h32=0, h33=1, h11=h22=cos(→), h12=-h21=sin(→)` | Distances, angles, parallelism |
| **Similarity** (Euclidean + uniform scale) | 4 | `h31=h32=0, h33=1, isotropic scaling` | Angles, parallelism, shape |
| **Affine** (similarity + non-uniform scale + shear) | 6 | `h31=h32=0, h33=1` | Parallelism, area ratios |
| **Projective** (Homography) | 8 | General 3→3 matrix | Collinearity, cross-ratio |

**Hierarchy:**
```
Euclidean → Similarity → Affine → Projective (Homography)
```

### Mathematical Formulation

Given a set of point correspondences `{(xi, yi) → (x'i, y'i)}`, we want to find **H** such that:

```
[x'i]       [xi]
[y'i]  ~ H  [yi]
[ 1 ]       [ 1]
```

The `~` means **projective equivalence** (equal up to scale).

Expanding:
```
x'i = (h11→xi + h12→yi + h13) / (h31→xi + h32→yi + h33)
y'i = (h21→xi + h22→yi + h23) / (h31→xi + h32→yi + h33)
```

Cross-multiplying to eliminate division:
```
x'i→(h31→xi + h32→yi + h33) = h11→xi + h12→yi + h13
y'i→(h31→xi + h32→yi + h33) = h21→xi + h22→yi + h23
```

Rearranging:
```
h11→xi + h12→yi + h13 - h31→xi→x'i - h32→yi→x'i - h33→x'i = 0
h21→xi + h22→yi + h23 - h31→xi→y'i - h32→yi→y'i - h33→y'i = 0
```

These are **linear equations** in the 9 elements of **H** (treated as a 9→1 vector).

### Example: Identity Homography

The **identity homography** leaves all points unchanged:

```
     [1  0  0]
H =  [0  1  0]
     [0  0  1]
```

**Effect:**
```
[x']   [1  0  0] [x]   [x]
[y'] = [0  1  0] [y] = [y]
[1 ]   [0  0  1] [1]   [1]
```

**Point correspondences:**
```
(0, 0) → (0, 0)
(1, 0) → (1, 0)
(0, 1) → (0, 1)
(1, 1) → (1, 1)
```

### Example: Pure Translation

Translate by `(tx, ty) = (5, 10)`:

```
     [1  0  5]
H =  [0  1 10]
     [0  0  1]
```

**Effect:**
```
[x']   [1  0  5] [x]   [x + 5 ]
[y'] = [0  1 10] [y] = [y + 10]
[1 ]   [0  0  1] [1]   [  1   ]
```

**Point correspondences:**
```
(0, 0) → (5, 10)
(1, 0) → (6, 10)
(0, 1) → (5, 11)
```

### Summary

- **Homography** is a 3→3 matrix representing planar projective transformation
- **8 degrees of freedom** → need **4 point correspondences** minimum
- **Preserves:** straight lines, cross-ratios
- **Does NOT preserve:** distances, angles, parallelism (in general)
- **Only valid for planar scenes** or pure rotation

Next, we'll see how to **compute** the homography matrix from point correspondences using the **Direct Linear Transformation (DLT)** algorithm.

---

## Direct Linear Transformation (DLT) Algorithm

The **Direct Linear Transformation (DLT)** is the standard algorithm for computing a homography matrix **H** from a set of point correspondences.

### Problem Statement

**Given:**
- N e 4 point correspondences: `{(xi, yi) → (x'i, y'i)}` for i = 1, ..., N
- Source points: `(xi, yi)` in the first image/plane
- Destination points: `(x'i, y'i)` in the second image/plane

**Find:**
- The 3→3 homography matrix **H** such that:
  ```
  [x'i]       [xi]
  [y'i]  ~ H  [yi]
  [ 1 ]       [ 1]
  ```

### Mathematical Derivation

#### Step 1: Formulate the Constraint Equations

For each point correspondence `(xi, yi) → (x'i, y'i)`, we have:

```
[x'i]   [h11  h12  h13] [xi]
[y'i] ~ [h21  h22  h23] [yi]
[w'i]   [h31  h32  h33] [ 1]
```

Where:
```
x'i = (h11→xi + h12→yi + h13) / (h31→xi + h32→yi + h33)
y'i = (h21→xi + h22→yi + h23) / (h31→xi + h32→yi + h33)
```

Let `w'i = h31→xi + h32→yi + h33`. Then:
```
x'i → w'i = h11→xi + h12→yi + h13
y'i → w'i = h21→xi + h22→yi + h23
```

Substituting `w'i`:
```
x'i→(h31→xi + h32→yi + h33) = h11→xi + h12→yi + h13
y'i→(h31→xi + h32→yi + h33) = h21→xi + h22→yi + h23
```

#### Step 2: Rearrange into Linear Equations

Rearranging:
```
h11→xi + h12→yi + h13→1 + h21→0 + h22→0 + h23→0 - h31→xi→x'i - h32→yi→x'i - h33→x'i = 0
h11→0 + h12→0 + h13→0 + h21→xi + h22→yi + h23→1 - h31→xi→y'i - h32→yi→y'i - h33→y'i = 0
```

In matrix form, define the vector of unknown homography elements:
```
h = [h11, h12, h13, h21, h22, h23, h31, h32, h33]^T  (9→1 vector)
```

For each point correspondence, we get **two equations**:

**Equation 1 (x-coordinate):**
```
[xi  yi  1   0   0   0  -xi→x'i  -yi→x'i  -x'i] → h = 0
```

**Equation 2 (y-coordinate):**
```
[0   0   0   xi  yi  1  -xi→y'i  -yi→y'i  -y'i] → h = 0
```

#### Step 3: Build the System Matrix A

Stack all constraint equations into a matrix **A**:

For **N point correspondences**, we have **2N equations**:

```
     [x1  y1  1   0   0   0  -x1→x'1  -y1→x'1  -x'1]
     [0   0   0   x1  y1  1  -x1→y'1  -y1→y'1  -y'1]
     [x2  y2  1   0   0   0  -x2→x'2  -y2→x'2  -x'2]
A =  [0   0   0   x2  y2  1  -x2→y'2  -y2→y'2  -y'2]
     [              ...                            ]
     [xN  yN  1   0   0   0  -xN→x'N  -yN→x'N  -x'N]
     [0   0   0   xN  yN  1  -xN→y'N  -yN→y'N  -y'N]
```

Dimensions: **A is (2N → 9)**

The problem becomes: **Find h such that A → h = 0**

#### Step 4: Solve Using SVD

This is a **homogeneous linear system**. The solution lies in the **null space** of **A**.

**Singular Value Decomposition (SVD):**
```
A = U → → → V^T
```

Where:
- **U:** (2N → 2N) orthogonal matrix
- **→:** (2N → 9) diagonal matrix of singular values `→1 e →2 e ... e →9 e 0`
- **V:** (9 → 9) orthogonal matrix

**Solution:**
The vector **h** that minimizes `||A → h||` subject to `||h|| = 1` is the **last column of V** (corresponding to the smallest singular value `→9`).

**Why the last column of V?**
- The columns of **V** are the eigenvectors of **A^T → A**
- The last column corresponds to the smallest eigenvalue (smallest singular value squared)
- This minimizes `||A → h||^2 = h^T → (A^T → A) → h`

**In NumPy:**
```python
U, S, Vt = np.linalg.svd(A)
h = Vt[-1, :]  # Last row of V^T = last column of V
```

#### Step 5: Reshape to 3→3 Matrix

Reshape the 9→1 vector **h** into a 3→3 matrix:

```python
H = h.reshape(3, 3)
```

```
     [h11  h12  h13]
H =  [h21  h22  h23]
     [h31  h32  h33]
```

#### Step 6: Normalization

By convention, we normalize **H** so that `h33 = 1` (or `||H|| = 1`).

**Common normalization:**
```python
H = H / H[2, 2]  # Make h33 = 1
```

This removes the scale ambiguity.

### Algorithm Summary

**Input:** N e 4 point correspondences `{(xi, yi) → (x'i, y'i)}`

**Output:** 3→3 homography matrix **H**

**Steps:**
1. Build the 2N → 9 matrix **A** from point correspondences
2. Compute SVD: `A = U → → → V^T`
3. Extract solution: `h = V[:, -1]` (last column of V)
4. Reshape to 3→3: `H = h.reshape(3, 3)`
5. Normalize: `H = H / H[2, 2]`

### Minimum Number of Points

**Exactly 4 points:**
- 4 points → 2 equations = 8 equations for 8 DOF
- **Determined system** (assuming points are in general position)

**More than 4 points:**
- N > 4 points → 2N > 8 equations
- **Overdetermined system**
- SVD gives the **least-squares solution** that minimizes reprojection error

**Fewer than 4 points:**
- N < 4 → 2N < 8 equations
- **Underdetermined system**
- Infinite solutions (cannot uniquely determine H)

### Degenerate Configurations

**Collinear Points:**
If all points lie on a line, the system is degenerate and has no unique solution.

**Three Points:**
Three non-collinear points define an **affine transformation** (6 DOF), not a full homography (8 DOF).

**Good Practice:**
- Use **N e 4** non-collinear points
- Prefer **N > 4** for robustness (least-squares fitting)
- Ensure points are **well-distributed** (not clustered)

### Numerical Stability Considerations

**Data Normalization:**
For numerical stability, normalize point coordinates before computing homography:

1. **Translate** points so centroid is at origin
2. **Scale** so average distance from origin is 2
3. Compute **H'** from normalized points
4. **Denormalize** to get final **H**

**Why?**
- Large coordinate values can cause numerical instability in SVD
- Normalization improves conditioning of matrix **A**

**Formula:**
```
H = T_dest^{-1} → H' → T_src
```

Where `T_src` and `T_dest` are the normalization transforms for source and destination points.

### Example: Computing Homography for 4 Points

**Source points:**
```
(x1, y1) = (0, 0)
(x2, y2) = (1, 0)
(x3, y3) = (1, 1)
(x4, y4) = (0, 1)
```

**Destination points (2→ scaling):**
```
(x'1, y'1) = (0, 0)
(x'2, y'2) = (2, 0)
(x'3, y'3) = (2, 2)
(x'4, y'4) = (0, 2)
```

**Matrix A:**
```
[0  0  1   0  0  0    0    0    0]   (x-equation for point 1)
[0  0  0   0  0  1    0    0    0]   (y-equation for point 1)
[1  0  1   0  0  0   -2   -0   -2]   (x-equation for point 2)
[0  0  0   1  0  1   -2   -0   -2]   (y-equation for point 2)
[1  1  1   0  0  0   -2   -2   -2]   (x-equation for point 3)
[0  0  0   1  1  1   -2   -2   -2]   (y-equation for point 3)
[0  1  1   0  0  0    0   -2   -2]   (x-equation for point 4)
[0  0  0   0  1  1    0   -2   -2]   (y-equation for point 4)
```

**SVD solution → h:**
```
h H [2, 0, 0, 0, 2, 0, 0, 0, 1]^T
```

**Homography H:**
```
     [2  0  0]
H =  [0  2  0]
     [0  0  1]
```

This is a **2→ uniform scaling** transformation, as expected.

### Summary

- **DLT** solves for homography using SVD of a linear system
- **Build matrix A** from point correspondences (2 rows per point)
- **Solution** is the last column of V in SVD: `A = U → → → V^T`
- **Minimum 4 points** required; more points give least-squares solution
- **Normalization** improves numerical stability

---

## Inverse Perspective Mapping (IPM) Mathematics

**Inverse Perspective Mapping (IPM)** transforms a front-view camera image into a **Bird's Eye View (BEV)** representation. This is a specific application of homography with important geometric assumptions.

### The Perspective Projection Problem

#### Front View (Perspective)

A camera captures a 3D scene as a 2D image through **perspective projection**:
- Objects farther away appear smaller
- Parallel lines (e.g., road lanes) converge toward a vanishing point
- Equal distances on the ground appear unequal in the image

**Example:** Lane markings on a straight road
```
Image plane (front view):
         /\
        /  \
       /    \
      /  ||  \      Lanes converge to vanishing point
     /   ||   \
    /    ||    \
   /__________  \
```

#### Bird's Eye View (Orthographic)

BEV provides an **orthographic projection** from directly above:
- Parallel lines remain parallel
- Equal distances on the ground map to equal distances in BEV
- Uniform metric scale (e.g., 1 pixel = 0.1 meters)

**Same lane markings in BEV:**
```
BEV (top-down view):
   _____________
  |      ||      |
  |      ||      |    Lanes are parallel
  |      ||      |
  |      ||      |
  |_____________|
```

### The Flat Ground Plane Assumption

**Critical Assumption:** IPM assumes all points lie on a **flat ground plane** at `Z = 0` in world coordinates.

**Mathematical Implication:**
- 3D world point: `(X, Y, Z = 0)`
- Under this constraint, the mapping from image to ground plane is a **homography**

**Why?**
- Both the image plane and ground plane are planar surfaces
- Homography maps between two planes
- The transformation is uniquely defined by point correspondences

**Consequence:**
Objects **not** on the ground plane (vehicles, pedestrians, overhead signs) will be **incorrectly transformed** and appear distorted in BEV.

### Defining Source and Destination Regions

#### Source Region: Trapezoid in Front View

In the front-view image, we define a **region of interest (ROI)** as a trapezoid:

```
         (x_tl, y_tl) ________ (x_tr, y_tr)   → Far from camera (small in image)
                      \        /
                       \      /
                        \    /
                         \  /
          (x_bl, y_bl)    \/    (x_br, y_br)   → Close to camera (large in image)
```

**Typical configuration:**
```python
# Image dimensions: width → height
# ROI as ratios of image size

top_left     = (width * 0.4,  height * 0.6)   # Top-left of trapezoid
top_right    = (width * 0.6,  height * 0.6)   # Top-right of trapezoid
bottom_left  = (width * 0.1,  height * 0.95)  # Bottom-left of trapezoid
bottom_right = (width * 0.9,  height * 0.95)  # Bottom-right of trapezoid
```

**Rationale:**
- Top edge (far from camera): narrower width due to perspective
- Bottom edge (close to camera): wider width
- Covers the road region where lanes are visible

#### Destination Region: Rectangle in BEV

In BEV, we define a **rectangular region**:

```
   (0, 0) _______________ (bev_width, 0)
          |               |
          |               |
          |               |    Uniform rectangular grid
          |               |
          |_______________|
  (0, bev_height)    (bev_width, bev_height)
```

**Typical configuration:**
```python
bev_width  = 640   # BEV image width in pixels
bev_height = 480   # BEV image height in pixels

dst_points = [
    [0,         0],            # Top-left
    [bev_width, 0],            # Top-right
    [bev_width, bev_height],   # Bottom-right
    [0,         bev_height]    # Bottom-left
]
```

**Correspondence:**
```
Source (trapezoid)         →    Destination (rectangle)
(x_tl, y_tl)               →    (0, 0)
(x_tr, y_tr)               →    (bev_width, 0)
(x_br, y_br)               →    (bev_width, bev_height)
(x_bl, y_bl)               →    (0, bev_height)
```

### Computing the IPM Homography

Using the **4 point correspondences** between source trapezoid and destination rectangle, we compute the homography **H** using the **DLT algorithm**:

```
H = compute_homography(src_points, dst_points)
```

Where:
```python
src_points = np.array([
    [x_tl, y_tl],
    [x_tr, y_tr],
    [x_br, y_br],
    [x_bl, y_bl]
])

dst_points = np.array([
    [0, 0],
    [bev_width, 0],
    [bev_width, bev_height],
    [0, bev_height]
])
```

**Homography H:**
```
     [h11  h12  h13]
H =  [h21  h22  h23]
     [h31  h32  h33]
```

### Forward Transformation: Image → BEV

To transform the entire image:

```
BEV_image = warpPerspective(front_view_image, H, (bev_width, bev_height))
```

**For individual points:**
```
[x_bev]       [x_img]
[y_bev]  = H  [y_img]
[  w  ]       [  1  ]
```

Then convert from homogeneous:
```
x_bev_cartesian = x_bev / w
y_bev_cartesian = y_bev / w
```

### Inverse Transformation: BEV → Image

To map points from BEV back to the original image:

```
H_inv = inverse(H)
```

**For points:**
```
[x_img]             [x_bev]
[y_img]  = H_inv →  [y_bev]
[  w  ]             [  1  ]
```

**For images:**
```
front_view_image = warpPerspective(BEV_image, H_inv, (img_width, img_height))
```

### Metric BEV: Real-World Scale

To create a **metrically accurate BEV** (e.g., 1 pixel = 0.1 meters), we need camera calibration parameters and ground plane geometry.

**Approach:**
1. Define real-world ground plane coordinates in meters
2. Project world coordinates to image coordinates using camera model
3. Use these correspondences to compute homography

**Example:**
```
World coordinates (meters):          Image coordinates (pixels):
X = -5m, Y = 10m, Z = 0  →  project  →  (u1, v1)
X =  5m, Y = 10m, Z = 0  →  project  →  (u2, v2)
X =  5m, Y = 30m, Z = 0  →  project  →  (u3, v3)
X = -5m, Y = 30m, Z = 0  →  project  →  (u4, v4)
```

Then:
```
BEV coordinates (pixels):
(0, 0), (100, 0), (100, 200), (0, 200)

Homography: src_points (image) → dst_points (BEV pixels)
```

**Benefit:**
- 1 BEV pixel = 0.1 meters in real world
- Enables accurate distance measurements
- Consistent scale across different camera setups

### Mathematical Validation

**Round-Trip Test:**
A point should return to its original location after forward and inverse transformation:

```
p_img → (apply H) → p_bev → (apply H_inv) → p_img'

Ideally: p_img' H p_img  (within numerical precision)
```

**Parallel Line Test:**
Parallel lines on the ground (e.g., lane markings) should remain parallel in BEV.

**Distance Preservation:**
Equal distances on the ground plane should map to approximately equal distances in BEV (depends on calibration quality).

### Summary

- **IPM** uses homography to transform front-view to BEV
- **Assumption:** Flat ground plane (Z = 0)
- **Source:** Trapezoid in front-view image (perspective effect)
- **Destination:** Rectangle in BEV (orthographic view)
- **Homography H** computed from 4 point correspondences
- **Forward:** `BEV = warpPerspective(image, H, size)`
- **Inverse:** `Image = warpPerspective(BEV, H_inv, size)`
- **Metric BEV** requires camera calibration for real-world scale

---

## Camera Models

To fully understand the relationship between 3D world coordinates and 2D image coordinates, we need to model the camera's projection process.

### Pinhole Camera Model

The **pinhole camera** is the fundamental model in computer vision. It describes how a 3D point in the world is projected onto a 2D image plane.

**Geometry:**
```
        3D World Point P = (X, Y, Z)
               |
               | (projection)
               →
         Image Point p = (u, v)
```

**Coordinate Systems:**
1. **World coordinates:** `(X, Y, Z)` in meters
2. **Camera coordinates:** `(Xc, Yc, Zc)` relative to camera center
3. **Image coordinates:** `(u, v)` in pixels

### Intrinsic Parameters

**Intrinsic parameters** describe the camera's **internal geometry**:

1. **Focal length:** `fx`, `fy` (in pixels)
   - Relationship between 3D distance and 2D projection
   - May differ slightly in x and y due to non-square pixels

2. **Principal point:** `(cx, cy)` (in pixels)
   - Center of the image sensor
   - Typically near the image center: `(width/2, height/2)`

3. **Skew coefficient:** `s`
   - Angle between pixel axes (typically 0 for modern cameras)

**Intrinsic Matrix K:**
```
     [fx   s  cx]
K =  [ 0  fy  cy]
     [ 0   0   1]
```

For most cameras, skew `s = 0`:
```
     [fx   0  cx]
K =  [ 0  fy  cy]
     [ 0   0   1]
```

**Typical values:**
```
fx = fy H 500-1000 pixels (for typical cameras)
cx H image_width / 2
cy H image_height / 2
```

### Extrinsic Parameters

**Extrinsic parameters** describe the camera's **position and orientation** in the world:

1. **Rotation:** 3→3 rotation matrix `R`
   - Orientation of camera frame relative to world frame
   - Orthogonal matrix: `R^T → R = I`, `det(R) = 1`

2. **Translation:** 3→1 translation vector `t`
   - Position of camera center in world coordinates
   - Units: meters

**Transformation from World to Camera Coordinates:**
```
[Xc]       [X]
[Yc]  = R  [Y]  + t
[Zc]       [Z]
```

Or in homogeneous coordinates:
```
[Xc]       [X]
[Yc]  = [R | t]  [Y]
[Zc]       [Z]
[ 1]       [1]
```

Where `[R | t]` is a 3→4 matrix.

### Complete Projection: 3D World → 2D Image

**Step 1: World to Camera Coordinates**
```
[Xc]       [X]
[Yc]  = [R | t]  [Y]
[Zc]       [Z]
[ 1]       [1]
```

**Step 2: Perspective Projection**
```
x = Xc / Zc
y = Yc / Zc
```

**Step 3: Apply Intrinsic Parameters**
```
u = fx → x + cx = fx → (Xc / Zc) + cx
v = fy → y + cy = fy → (Yc / Zc) + cy
```

**Combined Projection Matrix:**
```
     [u]       [X]
→ →  [v]  = K → [R | t] → [Y]
     [1]       [Z]
              [1]
```

Where `→ = Zc` is the depth in camera coordinates.

**Projection matrix P:**
```
P = K → [R | t]   (3→4 matrix)
```

**Full equation:**
```
[u → →]       [X]
[v → →]  = P  [Y]
[  →  ]       [Z]
              [1]
```

After projection, divide by `→` to get pixel coordinates `(u, v)`.

### Example: Projection of a 3D Point

**Camera parameters:**
```
K = [800   0  320]    (fx=800, fy=800, cx=320, cy=240)
    [  0 800  240]
    [  0   0    1]

R = I (identity - no rotation)
t = [0, 0, 0]^T (camera at world origin)
```

**3D point:**
```
P = (X, Y, Z) = (1, 2, 5) meters
```

**Projection:**
```
Camera coordinates: (Xc, Yc, Zc) = (1, 2, 5)  (same as world, since R=I, t=0)

Normalized coordinates: x = 1/5 = 0.2,  y = 2/5 = 0.4

Image coordinates:
u = 800 → 0.2 + 320 = 160 + 320 = 480 pixels
v = 800 → 0.4 + 240 = 320 + 240 = 560 pixels
```

**Result:** Point `(1, 2, 5)` projects to pixel `(480, 560)`.

### Backprojection: 2D Image → 3D World (with Constraint)

Recovering 3D from 2D is **ambiguous** without additional information:
- A single image pixel corresponds to a **ray in 3D space**
- Infinite 3D points project to the same 2D pixel (different depths)

**Constraint Needed:** Assume a known depth or known ground plane.

#### Backprojection to Ground Plane (Z = 0)

For IPM, we assume the ground plane at `Z = 0`.

**Given:**
- Image point: `(u, v)`
- Ground plane: `Z = 0`

**Unknown:**
- World coordinates: `(X, Y, 0)`

**Solve:**

From the projection equation:
```
[u → →]       [X]
[v → →]  = P  [Y]
[  →  ]       [0]
              [1]
```

This gives 3 equations for 2 unknowns `(X, Y)` (since `Z = 0` is fixed):
```
u → → = p11 → X + p12 → Y + p14
v → → = p21 → X + p22 → Y + p24
  →   = p31 → X + p32 → Y + p34
```

Substitute the third equation into the first two:
```
u → (p31→X + p32→Y + p34) = p11→X + p12→Y + p14
v → (p31→X + p32→Y + p34) = p21→X + p22→Y + p24
```

This is a **linear system in (X, Y)**:
```
[p11 - u→p31   p12 - u→p32] [X]   [u→p34 - p14]
[p21 - v→p31   p22 - v→p32] [Y] = [v→p34 - p24]
```

**Solve for (X, Y) using matrix inversion or pseudo-inverse.**

**Result:** The 3D ground plane coordinates `(X, Y, 0)` corresponding to image pixel `(u, v)`.

### Camera Calibration

**Calibration** determines the intrinsic `K` and extrinsic `[R | t]` parameters.

**Method:** Use a known calibration pattern (e.g., checkerboard)
1. Capture images of the checkerboard from multiple angles
2. Detect corner points in the images
3. Solve for camera parameters using correspondences
4. Tools: OpenCV `calibrateCamera()` function

**Output:**
- Intrinsic matrix `K`
- Distortion coefficients (lens distortion)
- Extrinsic parameters `[R | t]` for each image

### Summary

- **Pinhole camera model** describes 3D → 2D projection
- **Intrinsic parameters (K):** focal length `(fx, fy)`, principal point `(cx, cy)`
- **Extrinsic parameters:** rotation `R`, translation `t`
- **Projection matrix:** `P = K → [R | t]`
- **Projection:** `(X, Y, Z) → (u, v)` using `P`
- **Backprojection:** `(u, v) → (X, Y, Z)` requires additional constraint (e.g., `Z = 0`)
- **Calibration** determines camera parameters from known patterns

---

## Coordinate Systems

Understanding different coordinate systems is crucial for IPM and autonomous driving applications.

### Overview of Coordinate Systems

Four main coordinate systems are involved:

1. **World Coordinates (3D):** `(X, Y, Z)` in meters
2. **Camera Coordinates (3D):** `(Xc, Yc, Zc)` relative to camera
3. **Image Coordinates (2D):** `(u, v)` in pixels
4. **BEV Coordinates (2D):** `(x_bev, y_bev)` in pixels (top-down view)

### 1. World Coordinate System

**Definition:**
- **Origin:** User-defined reference point (e.g., vehicle center, map origin)
- **Axes:**
  - `X`: Forward direction (typically front of vehicle)
  - `Y`: Left direction (perpendicular to X)
  - `Z`: Upward direction (perpendicular to ground)
- **Units:** Meters

**Usage:** Represents positions in the real world.

**Example:**
```
Vehicle coordinate frame:
    Z (up)
    |
    |
    |_______  X (forward)
   /
  /
 Y (left)
```

### 2. Camera Coordinate System

**Definition:**
- **Origin:** Camera optical center
- **Axes:**
  - `Xc`: Right (perpendicular to optical axis)
  - `Yc`: Down (perpendicular to optical axis)
  - `Zc`: Forward (optical axis, into the scene)
- **Units:** Meters

**Transformation from World:**
```
[Xc]       [X]
[Yc]  = R  [Y]  + t
[Zc]       [Z]
```

Where `R` is rotation matrix, `t` is translation vector.

**Usage:** Intermediate step for camera projection.

### 3. Image Coordinate System

**Definition:**
- **Origin:** Top-left corner of the image (typically)
- **Axes:**
  - `u`: Horizontal (left to right), x-axis
  - `v`: Vertical (top to bottom), y-axis
- **Units:** Pixels

**Transformation from Camera:**
```
u = fx → (Xc / Zc) + cx
v = fy → (Yc / Zc) + cy
```

Where `(fx, fy)` are focal lengths, `(cx, cy)` is principal point.

**Usage:** Pixel coordinates in the captured image.

**Note:** Some conventions use origin at center or bottom-left. OpenCV uses top-left.

### 4. BEV Coordinate System

**Definition:**
- **Origin:** User-defined (e.g., vehicle rear axle projected onto ground)
- **Axes:**
  - `x_bev`: Horizontal in BEV (typically aligned with vehicle lateral direction)
  - `y_bev`: Vertical in BEV (typically aligned with vehicle forward direction)
- **Units:** Pixels (or meters for metric BEV)

**Transformation from Image:**
```
[x_bev]       [u]
[y_bev]  = H  [v]
[  w  ]       [1]
```

Where `H` is the IPM homography matrix.

**Usage:** Top-down view for planning and perception.

### Transformation Pipeline Summary

**3D World → Image:**
```
(X, Y, Z)  →  [extrinsics R, t]  →  (Xc, Yc, Zc)  →  [intrinsics K]  →  (u, v)
```

**Image → BEV:**
```
(u, v)  →  [homography H]  →  (x_bev, y_bev)
```

**Complete Pipeline (World → BEV):**
```
(X, Y, Z=0)  →  [R, t, K]  →  (u, v)  →  [H]  →  (x_bev, y_bev)
```

**Reverse (BEV → World):**
```
(x_bev, y_bev)  →  [H_inv]  →  (u, v)  →  [backproject with Z=0]  →  (X, Y, 0)
```

### Coordinate System Conventions

**Right-Handed vs. Left-Handed:**
Most systems use **right-handed** coordinate systems:
- X → Y = Z (cross product)

**Direction Conventions:**
- **World (vehicle-centric):** X=forward, Y=left, Z=up
- **Camera (computer vision):** Zc=forward (optical axis), Xc=right, Yc=down
- **Image (OpenCV):** u=right, v=down, origin at top-left

**Always verify the coordinate system convention for your specific application!**

### Example: Full Coordinate Transformation

**Setup:**
```
World point: P = (5, 2, 0) meters (5m forward, 2m left, on ground)

Camera extrinsics:
R = I (no rotation)
t = (0, 0, 1.5) (camera 1.5m above ground at vehicle origin)

Camera intrinsics:
fx = fy = 800
cx = 320, cy = 240
```

**Step 1: World → Camera**
```
[Xc]       [5  ]       [5  ]
[Yc]  = I  [2  ] + [0] = [2  ]
[Zc]       [0  ]   [1.5] [1.5]
```

Wait, this is incorrect. The translation `t` represents the camera position in the world. The transformation should be:
```
[Xc]                [X - tx]   [5 - 0  ]   [5  ]
[Yc]  = R^T → ([Y] - [ty]) = I → [2 - 0  ] = [2  ]
[Zc]                [Z]   [tz]   [0 - 1.5]   [-1.5]
```

Actually, for camera coordinates, we need:
```
Pc = R → (Pw - t)
```

But since `R = I`:
```
[Xc]   [5 - 0  ]   [5   ]
[Yc] = [2 - 0  ] = [2   ]
[Zc]   [0 - 1.5]   [-1.5]
```

Hmm, negative `Zc` means the point is behind the camera (not visible). Let me reconsider.

**Correction:** If the camera is at `(0, 0, 1.5)` meters (above ground), and we want to project a ground point `(5, 2, 0)`:

The camera looks in the `+X` direction (forward). The camera frame:
- Origin at `(0, 0, 1.5)`
- `Zc` axis pointing forward (+X in world)
- `Yc` axis pointing down (-Z in world)

For simplicity, assume:
```
R rotates from world to camera:
- World +X → Camera +Zc
- World +Y → Camera -Xc
- World +Z → Camera -Yc

Approximation:
[Xc]   [-2 ]
[Yc] = [1.5]  (point is 5m forward, 2m left → in camera frame)
[Zc]   [5  ]
```

**Step 2: Camera → Image**
```
u = fx → (Xc / Zc) + cx = 800 → (-2 / 5) + 320 = 800 → (-0.4) + 320 = -320 + 320 = 0
v = fy → (Yc / Zc) + cy = 800 → (1.5 / 5) + 240 = 800 → 0.3 + 240 = 240 + 240 = 480
```

**Image coordinates:** `(u, v) H (0, 480)` pixels

**Step 3: Image → BEV**

Assume we have precomputed homography `H` from image to BEV:
```
[x_bev]       [0  ]
[y_bev]  = H  [480]
[  w  ]       [1  ]
```

After division by `w`, we get BEV coordinates.

**This example illustrates the complexity of coordinate transformations - careful bookkeeping is essential!**

### Summary

- **Four coordinate systems:** World (3D), Camera (3D), Image (2D), BEV (2D)
- **World → Camera:** Extrinsic parameters `[R | t]`
- **Camera → Image:** Intrinsic parameters `K`
- **Image → BEV:** Homography `H`
- **Careful attention** to coordinate frame conventions is critical

---

## Mathematical Limitations

Understanding the limitations of homography and IPM is crucial for robust system design.

### 1. Flat Ground Plane Assumption

**Assumption:** All points lie on a plane (Z = 0 in world coordinates).

**Violation:** Non-planar surfaces (hills, slopes, speed bumps).

**Effect:**
- Homography is **exact only for planar scenes**
- Points **not** on the plane will be **incorrectly projected**
- Error increases with distance from the plane

**Mathematical Reason:**
Homography relates two **planes**, not arbitrary 3D surfaces. For a point at height `h` above ground:
```
True world: (X, Y, Z = h)
IPM assumes: (X, Y, Z = 0)
```

The projection will be incorrect by an amount proportional to `h`.

**Example:**
- **Pedestrian (height ~1.8m):** Severely distorted in BEV
- **Vehicle (height ~1.5m):** Appears stretched and displaced
- **Overhead sign:** May appear on the ground

**Mitigation:**
- Restrict IPM to known flat regions (road surface)
- Use semantic segmentation to mask non-ground objects
- Consider multi-plane or 3D reconstruction for non-flat scenes

### 2. Single Homography Limitation

**Assumption:** A **single homography** H applies to the entire ROI.

**Violation:** Curved roads, varying ground plane orientation.

**Effect:**
- On **curved roads**, a single trapezoid cannot accurately capture the road geometry
- Different parts of the scene may require different homographies

**Mathematical Reason:**
A homography is a **global transformation**. For curved surfaces or non-uniform planes, a single homography cannot adapt locally.

**Example:**
- **Curved highway exit ramp:** Lanes appear distorted at the curve
- **Varying pitch (uphill/downhill):** Ground plane changes orientation

**Mitigation:**
- **Piecewise IPM:** Divide image into multiple regions, each with its own homography
- **Polynomial or spline fitting:** Use higher-order transformations
- **Adaptive homography:** Recompute H based on detected road curvature

### 3. Numerical Stability Issues

#### Condition Number

The **condition number** of matrix `A` (in DLT) measures how sensitive the solution is to perturbations:
```
→(A) = →_max / →_min
```

Where `→_max` and `→_min` are the largest and smallest singular values.

**High condition number (→ >> 1):**
- **Ill-conditioned system**
- Small errors in point correspondences → large errors in H
- Unstable solution

**Causes:**
- **Collinear or nearly collinear points**
- **Clustered points** (poor spatial distribution)
- **Large magnitude differences** in coordinates

**Mitigation:**
- **Normalize coordinates** before DLT (shift + scale)
- **Well-distributed points** spanning the entire ROI
- **More than 4 points** for overdetermined least-squares fitting

#### Degenerate Point Configurations

**Collinear Points:**
All points on a single line → Infinite solutions for H.

**3 Points:**
Defines an affine transformation (6 DOF), not a full homography (8 DOF).

**Coincident Points:**
Duplicate points → Rank-deficient matrix A.

**Good Practice:**
- Use **4+ non-collinear points**
- Ensure points span **2D space** (not confined to a line)
- Check matrix rank before solving

### 4. Distortion and Field of View

**Lens Distortion:**
Real cameras have **radial and tangential distortion**:
- Barrel distortion (straight lines appear curved outward)
- Pincushion distortion (straight lines appear curved inward)

**Effect on IPM:**
- Homography assumes a **perfect pinhole camera** (no distortion)
- Distortion causes errors in point correspondences
- BEV will have geometric errors

**Mitigation:**
- **Undistort image** before applying IPM using calibration parameters
- Use OpenCV `undistort()` with camera matrix and distortion coefficients

**Wide Field of View:**
- Extreme wide-angle lenses (fisheye) have severe distortion
- Standard pinhole + distortion model may not suffice
- Consider specialized fisheye models

### 5. Ambiguity in Depth

**Problem:** 2D image → 3D world is **inherently ambiguous**.

**Mathematical:**
```
Image point (u, v) → Ray in 3D space
All points along the ray project to the same pixel
```

**IPM Solution:** Assume `Z = 0` (ground plane).

**Limitation:** Cannot distinguish objects at different heights.

**Effect:**
- All objects mapped to ground plane in BEV
- Occlusions and layering information lost

**Mitigation:**
- Use **stereo cameras** or **LiDAR** for depth information
- Semantic segmentation to identify elevated objects
- Multi-view geometry for 3D reconstruction

### 6. Error Propagation

**Sources of Error:**
1. **Point correspondence errors:** Manual selection, feature detection inaccuracy
2. **Camera calibration errors:** Inaccurate intrinsic/extrinsic parameters
3. **Numerical errors:** Floating-point precision, ill-conditioned matrices
4. **Model errors:** Distortion, ground plane assumption violations

**Propagation:**
Errors compound through the transformation pipeline:
```
World → Camera → Image → BEV
```

Each stage accumulates error, which is amplified by subsequent transformations.

**Quantification:**
- **Reprojection error:** Distance between observed and predicted image points
- **Homography error:** `|| H → src - dst ||` for correspondences
- **BEV error:** Deviation from ground truth measurements

**Mitigation:**
- **High-quality calibration**
- **Robust estimation** (RANSAC for outlier rejection)
- **Validation** with known ground truth
- **Redundancy:** More correspondences than minimum required

### 7. Occlusion and Visibility

**Problem:** Not all ground plane points are visible in the image.

**Causes:**
- **Occlusion** by vehicles, pedestrians, barriers
- **Field of view limits**
- **Image boundaries**

**Effect on IPM:**
- Some BEV pixels have no corresponding image data
- Appears as **black or undefined regions** in BEV

**Mitigation:**
- **Define ROI** to match visible ground plane region
- **Multi-camera fusion** for 360→ coverage
- **Interpolation or inpainting** for missing regions (use with caution)

### Summary of Limitations

| Limitation | Cause | Effect | Mitigation |
|-----------|-------|--------|------------|
| **Non-planar scenes** | Z ` 0 assumption | Distortion of elevated objects | Semantic masking, 3D methods |
| **Curved roads** | Single homography | Geometric distortion | Piecewise IPM, adaptive H |
| **Numerical instability** | Ill-conditioned A | Inaccurate H | Normalization, distributed points |
| **Lens distortion** | Real camera optics | BEV geometric errors | Undistort image first |
| **Depth ambiguity** | 2D → 3D mapping | Cannot resolve height | Stereo, LiDAR, semantic info |
| **Error propagation** | Cascaded transformations | Accumulated inaccuracy | Quality calibration, validation |
| **Occlusion** | Limited FOV, obstacles | Missing BEV regions | Multi-camera, careful ROI |

**Key Insight:** IPM is **powerful but constrained**. Understanding these limitations is essential for:
- **Knowing when IPM is appropriate**
- **Designing robust systems**
- **Validating results**
- **Choosing alternative methods when needed**

---

## References

### Essential Papers

1. **Mallot, H. A., et al. (1991).** "Inverse Perspective Mapping Simplifies Optical Flow Computation and Obstacle Detection." *Biological Cybernetics*, 64(3), 177-185.
   - Original IPM formulation

2. **Bertozzi, M., & Broggi, A. (1998).** "GOLD: A Parallel Real-Time Stereo Vision System for Generic Obstacle and Lane Detection." *IEEE Transactions on Image Processing*, 7(1), 62-81.
   - IPM for lane detection

3. **Hartley, R., & Zisserman, A. (2004).** *Multiple View Geometry in Computer Vision* (2nd ed.). Cambridge University Press.
   - **Chapter 4:** Homography estimation and DLT algorithm
   - **Chapter 2:** Projective geometry and homogeneous coordinates

4. **Zhang, Z. (2000).** "A Flexible New Technique for Camera Calibration." *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 22(11), 1330-1334.
   - Camera calibration method (widely used)

### Books

5. **Szeliski, R. (2022).** *Computer Vision: Algorithms and Applications* (2nd ed.). Springer.
   - **Chapter 2:** Image formation and camera models
   - **Chapter 6:** Feature-based alignment and homographies

6. **Forsyth, D. A., & Ponce, J. (2011).** *Computer Vision: A Modern Approach* (2nd ed.). Pearson.
   - **Chapter 3:** Geometric camera models

### Online Resources

7. **OpenCV Documentation**
   - `cv2.findHomography()`: https://docs.opencv.org/master/d9/d0c/group__calib3d.html
   - `cv2.warpPerspective()`: https://docs.opencv.org/master/da/d54/group__imgproc__transform.html

8. **First Principles of Computer Vision (YouTube)**
   - Shree Nayar's lecture series on homography and projective geometry

9. **Cyrill Stachniss - Photogrammetry Lectures**
   - YouTube series covering DLT, camera models, and transformations

### Advanced Topics

10. **Philion, J., & Fidler, S. (2020).** "Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by Implicitly Unprojecting to 3D." *ECCV 2020*.
    - Modern learned approach to BEV transformation

11. **Li, Z., et al. (2022).** "BEVFormer: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers." *ECCV 2022*.
    - Transformer-based BEV for autonomous driving

---

**End of Mathematical Foundations Document**

This document provides the mathematical theory needed to understand and implement perspective transformations and Inverse Perspective Mapping. For practical implementation details, see `implementation_notes.md`.
