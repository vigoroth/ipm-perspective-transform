# Contributing to IPM Perspective Transform

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Inverse Perspective Mapping (IPM) for Bird's Eye View Transformation project.

## Table of Contents

- [How to Report Issues](#how-to-report-issues)
- [How to Suggest Enhancements](#how-to-suggest-enhancements)
- [Pull Request Process](#pull-request-process)
- [Development Guidelines](#development-guidelines)
- [Testing Requirements](#testing-requirements)
- [Code of Conduct](#code-of-conduct)

## How to Report Issues

### Bug Reports

If you find a bug, please create an issue with the following information:

**Title**: Brief, descriptive title of the bug

**Description**:
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Steps to reproduce**: Minimal steps to reproduce the issue
- **Environment**:
  - Python version
  - Operating system
  - Relevant dependency versions (numpy, opencv-python, etc.)
- **Code snippet**: Minimal code that reproduces the issue
- **Error message**: Full error traceback if applicable

**Example**:
```
Title: Homography computation fails with 5 collinear points

Description:
Expected: ValueError with message "Points are collinear"
Actual: System hangs indefinitely

Steps to reproduce:
1. Create 5 collinear points
2. Call compute_homography(src, dst)
3. System hangs

Environment:
- Python 3.9.7
- Ubuntu 20.04
- numpy 1.21.0

Code snippet:
import numpy as np
from src.homography import compute_homography

src = np.array([[0,0], [1,1], [2,2], [3,3], [4,4]], dtype=np.float32)
dst = np.array([[0,0], [1,0], [2,0], [3,0], [4,0]], dtype=np.float32)
H = compute_homography(src, dst)  # Hangs here
```

### Enhancement Suggestions

If you have ideas for new features or improvements:

- **Describe the enhancement**: What functionality would you like to see?
- **Use case**: Why is this enhancement valuable?
- **Proposed implementation**: (Optional) How might this be implemented?
- **Alternatives considered**: What other approaches did you consider?

### Questions about IPM/Homography

If you have questions about the mathematics, implementation, or usage:

- Check the [documentation](docs/PROJECT_02_PERSPECTIVE_TRANSFORM.md) first
- Review the [educational notebooks](notebooks/) for in-depth explanations
- Search existing issues to see if your question was already answered
- Open a new issue with the "question" label

## How to Suggest Enhancements

We welcome suggestions for:

- **New features**: Additional transformation methods, calibration tools, etc.
- **Performance improvements**: Faster algorithms, optimized code
- **Documentation improvements**: Better explanations, more examples
- **Educational enhancements**: Additional notebooks, visualizations, tutorials

Please open an issue with:
1. Clear description of the enhancement
2. Rationale for why it's valuable
3. (Optional) Proposed implementation approach

## Pull Request Process

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/ipm-perspective-transform.git
cd ipm-perspective-transform

# Add upstream remote
git remote add upstream https://github.com/originalowner/ipm-perspective-transform.git
```

### 2. Create a Feature Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create a new branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch naming conventions**:
- `feature/` - New features (e.g., `feature/add-calibration-tool`)
- `fix/` - Bug fixes (e.g., `fix/homography-collinearity-check`)
- `docs/` - Documentation updates (e.g., `docs/improve-api-reference`)
- `test/` - Test additions/fixes (e.g., `test/add-ipm-edge-cases`)

### 3. Make Changes

- Write clear, readable code following PEP 8 style
- Add/update tests for your changes
- Update documentation (docstrings, README, etc.)
- Keep commits atomic and focused
- Write descriptive commit messages

**Commit message format**:
```
Short summary (50 chars or less)

More detailed explanation if needed (wrap at 72 characters).
Explain the problem this commit solves and why you chose this approach.

- Bullet points are okay
- Reference issues like #123
```

### 4. Run Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term

# Run specific test file
pytest tests/test_homography.py -v

# Check code style (optional but recommended)
flake8 src/ tests/
```

Ensure all tests pass before submitting your PR.

### 5. Update Documentation

- Update docstrings for any new/modified functions
- Update README.md if you added new features
- Add examples in `docs/` if applicable
- Update type hints for all function parameters and returns

### 6. Submit Pull Request

```bash
# Push your branch to your fork
git push origin feature/your-feature-name

# Go to GitHub and create a pull request
```

**Pull request description should include**:
- **Summary**: Brief description of what this PR does
- **Motivation**: Why is this change needed?
- **Changes**: Detailed list of changes made
- **Testing**: How did you test this? What edge cases did you consider?
- **Screenshots/Output**: (If applicable) Visual results or terminal output
- **Related issues**: Closes #123, Relates to #456

**Example PR description**:
```markdown
## Summary
Add round-trip error measurement to IPMTransform class

## Motivation
Users need to quantify transformation accuracy for their specific ROI configurations.
This PR adds a method to compute pixel error after front → BEV → front transformation.

## Changes
- Added `compute_round_trip_error()` method to IPMTransform class
- Added unit tests in `test_ipm.py`
- Updated API documentation in `docs/README.md`
- Added usage example in README.md

## Testing
- Tested with KITTI dataset images: round-trip error < 0.5 pixels
- Added 3 unit tests covering normal case, edge points, and invalid inputs
- All existing tests still pass

## Related Issues
Closes #42
```

### 7. Address Review Feedback

- Respond to all comments from reviewers
- Make requested changes in new commits (don't force push)
- Re-request review after making changes

### 8. Merge

Once approved, a maintainer will merge your PR. Thank you for your contribution!

## Development Guidelines

### Code Style

- **Follow PEP 8**: Use consistent Python style
  - 4 spaces for indentation (no tabs)
  - Max line length: 100 characters (docstrings: 79)
  - Two blank lines between top-level functions/classes
  - One blank line between methods

- **Naming conventions**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods: `_leading_underscore`

- **Type hints**: Add type hints to all functions
  ```python
  def compute_homography(src_points: np.ndarray, dst_points: np.ndarray) -> np.ndarray:
      ...
  ```

- **Docstrings**: Use Google-style docstrings
  ```python
  def transform_to_bev(self, image: np.ndarray) -> np.ndarray:
      """
      Transform front-view image to Bird's Eye View.

      Args:
          image: np.ndarray of shape (H, W, 3) or (H, W)
                Front-view image (color or grayscale)

      Returns:
          np.ndarray: BEV image of shape (bev_height, bev_width, 3)
                      or (bev_height, bev_width)

      Example:
          >>> bev_image = ipm.transform_to_bev(front_image)
      """
  ```

### Writing Tests

- **Test file structure**: Match source file names
  - `src/homography.py` → `tests/test_homography.py`
  - `src/ipm.py` → `tests/test_ipm.py`

- **Test function naming**: `test_<function_name>_<scenario>`
  ```python
  def test_compute_homography_identity():
      """Test homography with identity transformation."""
      ...

  def test_compute_homography_collinear_points():
      """Test that collinear points raise ValueError."""
      ...
  ```

- **Test both success and failure cases**:
  - Valid inputs with expected outputs
  - Edge cases (boundary conditions, empty inputs)
  - Invalid inputs (wrong types, shapes, collinearity)

- **Use fixtures**: Define reusable test data in `tests/conftest.py`
  ```python
  @pytest.fixture
  def sample_image():
      """Create sample road image for testing."""
      ...
  ```

- **Assert with clear messages**:
  ```python
  assert result.shape == expected_shape, \
      f"Expected shape {expected_shape}, got {result.shape}"
  ```

### Documentation Standards

- **Every public function/class needs a docstring**
- **Include type hints in function signatures**
- **Provide usage examples in docstrings**
- **Update README.md for user-facing changes**
- **Keep docs/ up to date with implementation**

### Keep It Simple

- **Avoid over-engineering**: Don't add features that aren't needed
- **Prefer clarity over cleverness**: Readable code > clever code
- **One feature per PR**: Don't combine multiple unrelated changes
- **Backwards compatibility**: Don't break existing APIs without good reason

## Testing Requirements

### All Tests Must Pass

Before submitting a PR:

```bash
pytest tests/ -v --cov=src
```

All tests must pass with no errors or failures.

### Coverage Should Not Decrease

- Current coverage: ~85%
- New code should include tests
- Aim for >80% coverage on new code

Check coverage:
```bash
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Test Both Success and Error Cases

For every function, test:
1. **Normal operation**: Valid inputs, expected outputs
2. **Edge cases**: Boundary values, empty inputs, special cases
3. **Error handling**: Invalid inputs, expected exceptions

Example:
```python
def test_compute_homography_success():
    """Test homography with valid inputs."""
    src = np.array([[0,0], [1,0], [1,1], [0,1]], dtype=np.float32)
    dst = np.array([[0,0], [2,0], [2,2], [0,2]], dtype=np.float32)
    H = compute_homography(src, dst)
    assert H.shape == (3, 3)

def test_compute_homography_collinear():
    """Test that collinear points raise ValueError."""
    src = np.array([[0,0], [1,1], [2,2], [3,3]], dtype=np.float32)
    dst = np.array([[0,0], [1,0], [2,0], [3,0]], dtype=np.float32)
    with pytest.raises(ValueError, match="collinear"):
        compute_homography(src, dst)
```

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Background
- Identity

### Expected Behavior

- Be respectful and considerate in all interactions
- Provide constructive feedback
- Accept feedback gracefully
- Focus on what is best for the project and community

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling, insulting, or derogatory remarks
- Publishing private information without permission
- Any conduct that would be inappropriate in a professional setting

### Enforcement

Violations of the code of conduct should be reported to the project maintainers. All reports will be reviewed and investigated promptly and fairly.

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Review existing issues and pull requests
- Check the [documentation](docs/PROJECT_02_PERSPECTIVE_TRANSFORM.md)

## Thank You!

Your contributions make this project better. Whether you're fixing a typo, reporting a bug, or implementing a major feature, we appreciate your effort and time.

Happy coding!
