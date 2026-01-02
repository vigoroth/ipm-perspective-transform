# Recommended Books for Project 2: Perspective Transformation & BEV

A curated reading list for mastering homography, camera geometry, and Bird's Eye View transformations.

---

## 📚 Essential Books (Must-Have)

### 1. Multiple View Geometry in Computer Vision (2nd Edition)
**Authors:** Richard Hartley, Andrew Zisserman
**Publisher:** Cambridge University Press
**Edition:** 2nd Edition (2004)
**ISBN-13:** 978-0521540513
**Price:** ~$70-80 (Hardcover), ~$60 (eBook)
**Level:** Intermediate to Advanced

**Why Recommended:**
- **THE** definitive reference for geometric computer vision
- Chapter 2: Projective Geometry - Essential for homogeneous coordinates
- Chapter 4: Estimation - 2D Homographies - Direct coverage of DLT algorithm
- Chapter 8: Camera Models - Complete intrinsic/extrinsic parameters

**Key Chapters for Project 2:**
- **Chapter 2 (pp. 25-78):** Projective geometry, homogeneous coordinates
- **Chapter 3 (pp. 79-120):** Transformations (homographies, affine, projective)
- **Chapter 4 (pp. 121-156):** Homography estimation, DLT algorithm, RANSAC
- **Chapter 6 (pp. 153-190):** Camera models, calibration matrices

**Reading Strategy:**
- Start with Chapter 2 for mathematical foundations
- Chapter 4 before implementing homography solver
- Reference Chapter 6 for camera model integration

**Note:** Dense and mathematical but absolutely worth it. Keep as permanent reference.

---

### 2. Computer Vision: Algorithms and Applications (2nd Edition)
**Authors:** Richard Szeliski
**Publisher:** Springer
**Edition:** 2nd Edition (2022)
**ISBN-13:** 978-3030343712
**Price:** ~$80-90 (Hardcover), **FREE** PDF available from author's website
**Level:** Beginner to Intermediate

**Why Recommended:**
- Modern, comprehensive, and accessible
- Excellent balance of theory and practice
- Up-to-date with recent developments
- Many practical examples and code references

**Key Chapters for Project 2:**
- **Chapter 2 (pp. 37-104):** Image formation, camera models, geometric primitives
- **Chapter 6 (pp. 273-346):** Feature-based alignment, 2D transformations, homographies
- **Chapter 11 (pp. 523-590):** 3D reconstruction basics

**Reading Strategy:**
- Read Chapter 2 for camera fundamentals
- Chapter 6 for transformation theory and applications
- Use as your "friendly" companion to Hartley & Zisserman

**FREE Alternative:** Download PDF from http://szeliski.org/Book/

---

### 3. Computer Vision: A Modern Approach (2nd Edition)
**Authors:** David Forsyth, Jean Ponce
**Publisher:** Pearson
**Edition:** 2nd Edition (2011)
**ISBN-13:** 978-0136085928
**Price:** ~$120-140 (Hardcover)
**Level:** Intermediate

**Why Recommended:**
- Excellent pedagogical approach
- Clear explanations of geometric concepts
- Good problem sets for practice
- Strong on mathematical intuition

**Key Chapters for Project 2:**
- **Chapter 1-2 (pp. 1-60):** Image formation, cameras
- **Chapter 3 (pp. 61-102):** Geometric camera models
- **Chapter 11 (pp. 291-334):** Stereopsis and multi-view geometry

**Reading Strategy:**
- Use for conceptual understanding
- Work through example problems
- Complement with Szeliski for modern perspective

**Note:** Slightly dated but excellent for learning fundamentals.

---

## 📖 Intermediate Books (Deep Dives)

### 4. An Invitation to 3-D Vision: From Images to Geometric Models
**Authors:** Yi Ma, Stefano Soatto, Jana Kosecka, S. Shankar Sastry
**Publisher:** Springer
**Edition:** 1st Edition (2004)
**ISBN-13:** 978-0387008936
**Price:** ~$100-120
**Level:** Advanced

**Why Recommended:**
- Rigorous mathematical treatment
- Unified framework for geometric vision
- Excellent for understanding theory deeply
- Bridge to robotics applications

**Key Chapters for Project 2:**
- **Chapter 2:** Representation of a 3D moving scene
- **Chapter 3:** Image primitives and correspondence
- **Chapter 5:** Reconstruction from multiple views

**Reading Strategy:**
- Read AFTER Hartley & Zisserman Chapter 2-4
- Focus on theoretical foundations
- Good preparation for research

**Note:** Mathematically dense. Have linear algebra background ready.

---

### 5. Introductory Techniques for 3-D Computer Vision
**Authors:** Emanuele Trucco, Alessandro Verri
**Publisher:** Prentice Hall
**Edition:** 1st Edition (1998)
**ISBN-13:** 978-0132611084
**Price:** ~$80-100 (Used copies)
**Level:** Beginner to Intermediate

**Why Recommended:**
- Very accessible introduction
- Step-by-step algorithm descriptions
- Practical focus on implementation
- Good for camera calibration understanding

**Key Chapters for Project 2:**
- **Chapter 2:** Camera models and calibration
- **Chapter 6:** Stereo vision
- **Chapter 9:** 3D vision systems

**Reading Strategy:**
- Start here if new to 3D vision
- Use before tackling Hartley & Zisserman
- Good for practical intuition

**Note:** Older but still excellent for foundational concepts.

---

## 🚀 Advanced/Specialized Books

### 6. Deep Learning for Vision Systems
**Authors:** Mohamed Elgendy
**Publisher:** Manning
**Edition:** 1st Edition (2020)
**ISBN-13:** 978-1617296192
**Price:** ~$50-60
**Level:** Intermediate

**Why Recommended:**
- Bridges classical and modern deep learning approaches
- Covers both geometric and learned BEV methods
- Practical PyTorch implementations
- Relevant for understanding modern lane detection

**Key Chapters for Project 2:**
- **Chapter 2:** Deep learning for image classification (foundations)
- **Chapter 7:** Object detection (relevant for scene understanding)
- Discussion of classical vs. learned feature extraction

**Reading Strategy:**
- Read after completing classical IPM implementation
- Understand how deep learning improves on classical methods
- Preparation for later projects (5-6) on neural approaches

---

### 7. Probabilistic Robotics
**Authors:** Sebastian Thrun, Wolfram Burgard, Dieter Fox
**Publisher:** MIT Press
**Edition:** 1st Edition (2005)
**ISBN-13:** 978-0262201629
**Price:** ~$80-90
**Level:** Advanced

**Why Recommended:**
- Essential for autonomous driving context
- Sensor models and coordinate transformations
- Uncertainty in transformations
- Real-world deployment considerations

**Key Chapters for Project 2:**
- **Chapter 3:** Gaussian filters (relevant for uncertainty)
- **Chapter 5:** Robot motion (coordinate systems)
- **Chapter 6:** Robot perception (sensor models)

**Reading Strategy:**
- Read for broader context of where IPM fits in robotics
- Understand uncertainty and limitations
- Good for Phase 5 (failure mode analysis)

---

## 📐 Supporting Mathematics

### 8. Linear Algebra and Its Applications (6th Edition)
**Authors:** Gilbert Strang
**Publisher:** Cengage Learning
**Edition:** 6th Edition (2022)
**ISBN-13:** 978-1733146678
**Price:** ~$90-100
**Level:** Beginner to Intermediate

**Why Recommended:**
- **THE** linear algebra book
- Clear explanations of SVD, eigenvalues, least squares
- Directly applicable to computer vision
- Author's MIT lectures available free online

**Key Chapters for Project 2:**
- **Chapter 1-2:** Vector spaces, solving linear systems
- **Chapter 6:** Eigenvalues and eigenvectors
- **Chapter 7:** Singular Value Decomposition (SVD) - CRITICAL for DLT
- **Chapter 11:** Least squares

**FREE Alternative:**
- MIT OpenCourseWare: 18.06 Linear Algebra lectures
- Online textbook: https://ocw.mit.edu

**Reading Strategy:**
- Chapter 7 (SVD) is ESSENTIAL before homography implementation
- Review Chapter 11 for understanding least-squares solutions
- Keep as reference for matrix operations

---

### 9. Numerical Recipes: The Art of Scientific Computing (3rd Edition)
**Authors:** William H. Press, Saul A. Teukolsky, William T. Vetterling, Brian P. Flannery
**Publisher:** Cambridge University Press
**Edition:** 3rd Edition (2007)
**ISBN-13:** 978-0521880688
**Price:** ~$80-100
**Level:** Intermediate

**Why Recommended:**
- Practical implementation of numerical algorithms
- Chapter on SVD with code
- Covers numerical stability issues
- C++, Fortran, Python examples

**Key Chapters for Project 2:**
- **Chapter 2:** Solution of linear algebraic equations
- **Chapter 15:** Modeling of data (least squares)
- **Section 2.6:** SVD implementation

**Reading Strategy:**
- Reference when implementing homography solver
- Use for understanding numerical issues
- Check code examples for optimization tips

**Note:** Focused on implementation details, not theory.

---

## 💻 Practical/Applied Books

### 10. Learning OpenCV 4 Computer Vision with Python 3 (3rd Edition)
**Authors:** Joe Minichino, Joseph Howse
**Publisher:** Packt
**Edition:** 3rd Edition (2020)
**ISBN-13:** 978-1789531619
**Price:** ~$40-50
**Level:** Beginner to Intermediate

**Why Recommended:**
- Hands-on guide to OpenCV functions
- Covers `warpPerspective`, `findHomography` directly
- Python-focused (relevant for project)
- Practical examples and code

**Key Chapters for Project 2:**
- **Chapter 3:** Image processing basics
- **Chapter 11:** Augmented reality (uses homographies)
- **Chapter 12:** Camera calibration

**Reading Strategy:**
- Use as reference while coding
- Check function signatures and parameters
- Quick lookup for OpenCV-specific issues

**Alternative:** Official OpenCV documentation (free online)

---

### 11. Mastering OpenCV 4 with Python
**Authors:** Alberto Fernández Villán
**Publisher:** Packt
**Edition:** 1st Edition (2019)
**ISBN-13:** 978-1789344912
**Price:** ~$35-45
**Level:** Intermediate

**Why Recommended:**
- More advanced OpenCV topics
- Project-based learning approach
- Covers camera calibration in detail
- Good for interactive tool development

**Key Chapters for Project 2:**
- **Chapter 4:** Camera calibration and 3D reconstruction
- **Chapter 7:** Augmented reality applications
- **Chapter 11:** Deep learning with OpenCV

**Reading Strategy:**
- Use for Phase 3 (interactive tool)
- Reference for GUI development with OpenCV
- Practical examples for calibration workflows

---

## 🎓 Budget-Friendly Options

### Strategy 1: Essential Only (~$220)
**Core Books:**
1. Multiple View Geometry (~$75)
2. Computer Vision: Algorithms and Applications (FREE PDF)
3. Linear Algebra and Its Applications (~$95)
4. Learning OpenCV 4 (~$45)

**Total:** ~$215

**Coverage:** 80% of Project 2 topics

---

### Strategy 2: Comprehensive Collection (~$450)
**Add to Essential:**
- Computer Vision: A Modern Approach (~$130)
- An Invitation to 3-D Vision (~$110)

**Total:** ~$455

**Coverage:** 95% of Project 2 topics + advanced theory

---

### Strategy 3: Complete Library (~$800)
**All Books Listed**

**Total:** ~$800-900

**Coverage:** 100% + preparation for future projects

---

## 🆓 Free Alternatives & Online Resources

### Free Books
1. **Computer Vision: Algorithms and Applications** - Szeliski (FREE PDF)
2. **Deep Learning Book** - Goodfellow et al. (FREE online)
3. **MIT Linear Algebra** - Strang (FREE videos + notes)

### Online Courses (Complementary)
1. **Coursera:** Multiple View Geometry (TUM Munich)
2. **YouTube:** First Principles of Computer Vision (Columbia)
3. **MIT OCW:** Linear Algebra 18.06

### Technical Papers (Free)
1. "Inverse Perspective Mapping: Simplifications and Extensions" (Bertozzi, 2008)
2. "A Versatile Method for Road Detection Based on Dense Stereo Range Images" (2013)

---

## 📖 Reading Order Recommendations

### Path 1: Theory First (Academic Approach)
1. **Start:** Linear Algebra (Strang) - Ch 6-7 (SVD)
2. **Core:** Multiple View Geometry - Ch 2-4
3. **Applied:** Computer Vision: Algorithms and Applications - Ch 2, 6
4. **Practical:** Learning OpenCV 4 - Ch 11-12
5. **Advanced:** An Invitation to 3-D Vision (optional)

**Timeline:** 4-6 weeks of parallel reading with project implementation

---

### Path 2: Practice First (Hands-On Approach)
1. **Start:** Learning OpenCV 4 - Ch 11-12 (get hands dirty)
2. **Concepts:** Computer Vision: Algorithms and Applications - Ch 2, 6
3. **Theory:** Multiple View Geometry - Ch 2-4
4. **Math:** Linear Algebra (Strang) - Ch 7 (as needed)
5. **Advanced:** Probabilistic Robotics (for context)

**Timeline:** 3-4 weeks alongside project work

---

### Path 3: Just-In-Time Learning (Project-Driven)
**Phase 1 (Math Foundations):**
- Linear Algebra Ch 7 (SVD)
- MVG Ch 2 (Homogeneous coordinates)

**Phase 2 (IPM Implementation):**
- MVG Ch 4 (Homography estimation)
- Szeliski Ch 6 (Transformations)

**Phase 3 (Interactive Tool):**
- Learning OpenCV 4 Ch 11-12
- Mastering OpenCV 4 Ch 4

**Phase 4-5 (Advanced Topics):**
- Probabilistic Robotics Ch 5-6
- An Invitation to 3-D Vision Ch 2-3

---

## 🔗 Chapter-to-Project Phase Mapping

| Project Phase | Essential Chapters | Time |
|---------------|-------------------|------|
| **Phase 1: Math Foundations** | Strang Ch 7, MVG Ch 2-3 | 1-2 weeks |
| **Phase 2: IPM** | MVG Ch 4, Szeliski Ch 6 | 1 week |
| **Phase 3: Interactive Tool** | Learning OpenCV Ch 11-12 | 3-4 days |
| **Phase 4: Advanced Transform** | MVG Ch 6, Forsyth Ch 3 | 1 week |
| **Phase 5: Failure Analysis** | Prob. Robotics Ch 6 | 2-3 days |
| **Phase 6: Validation** | Numerical Recipes Ch 2 | 2-3 days |

---

## 💰 Total Investment Summary

| Strategy | Books | Cost | Coverage |
|----------|-------|------|----------|
| **Minimal** | 2-3 books + FREE resources | ~$150 | 70% |
| **Recommended** | 5-6 books | ~$350 | 90% |
| **Complete** | 8-10 books | ~$700 | 100% |
| **Ultimate** | All 11 books | ~$900 | 100% + future prep |

---

## 📌 Final Recommendations

### If You Can Only Buy 3 Books:
1. **Multiple View Geometry** (Hartley & Zisserman) - Core theory
2. **Computer Vision: Algorithms and Applications** (Szeliski) - FREE PDF!
3. **Linear Algebra and Its Applications** (Strang) - Math foundation

**Total:** ~$170 + invaluable knowledge

### Library Checkout Strategy:
- Borrow: Computer Vision: A Modern Approach (Forsyth) - read once
- Borrow: Numerical Recipes - reference as needed
- Borrow: Introductory Techniques - if new to 3D vision

### E-Book vs Physical:
- **E-Book:** Szeliski, Deep Learning for Vision Systems (searchable)
- **Physical:** Multiple View Geometry, Strang (frequent reference)
- **Either:** Learning OpenCV 4, Forsyth & Ponce

---

## 🎯 Success Criteria Checklist

After acquiring and reading recommended sections:
- [ ] Understand homogeneous coordinates (MVG Ch 2)
- [ ] Can derive DLT algorithm (MVG Ch 4)
- [ ] Understand SVD mathematically (Strang Ch 7)
- [ ] Know camera models (Szeliski Ch 2, MVG Ch 6)
- [ ] Familiar with OpenCV functions (Learning OpenCV)
- [ ] Understand IPM limitations (Prob. Robotics)

---

**Note:** All prices are approximate USD as of 2024. Check current prices on Amazon, Springer, or publisher websites. Student discounts often available through university bookstores.

**Last Updated:** November 2024
