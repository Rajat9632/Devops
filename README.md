# Smart CI/CD Pipeline with Test Optimization

A minimal, working Python project that demonstrates a **smart test-selection** strategy inside a GitHub Actions CI/CD pipeline. Only tests relevant to the changed files are executed, cutting down feedback time while still guaranteeing quality.

---

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── user.py          # User management module
│   └── payment.py       # Payment processing module
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Pytest fixtures
│   ├── test_user.py     # Tests for user.py
│   └── test_payment.py  # Tests for payment.py
├── test_selector.py     # Maps changed files -> test files
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container image definition
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions pipeline
└── README.md            # This file
```

---

## How the System Works

1. **Code Change Detection** — On every `push` or `pull_request`, the CI job uses `git diff --name-only` to list files that changed compared to the previous commit (or PR base).
2. **Smart Test Mapping** — `test_selector.py` receives the JSON list of changed files, looks them up in a configurable `FILE_TO_TEST_MAP`, and returns only the matching test files.
3. **Targeted Test Execution** — The workflow feeds the selected paths to `pytest` (with parallel execution via `pytest-xdist`). If the selector cannot map any file, it safely falls back to running the full `tests/` directory.
4. **Gated Docker Build** — If (and only if) all selected tests pass, the pipeline builds the Docker image and runs a quick container smoke test.

---

## Advantages

- **Faster feedback loops** — Small PRs that touch a single module run a fraction of the full suite.
- **Reduced CI costs** — Less runner time spent on irrelevant tests.
- **Fail-safe defaults** — Unknown or unmapped files trigger the full suite, so nothing is accidentally skipped.
- **Parallel execution** — `pytest-xdist` runs tests across multiple CPU cores.
- **Markers** — `smoke` and `regression` markers let you layer additional filtering inside the pipeline.

---

## Limitations & Future Improvements

| Limitation | Improvement Idea |
|------------|------------------|
| Static file mapping only | Use AST parsing or dependency graphs to detect downstream consumers automatically |
| No cross-module impact analysis | Introduce a coverage / import-graph tool (e.g., `import_deps`) |
| Single runner only | Shard selected tests across multiple jobs using a dynamic matrix |
| No test-result caching | Persist test outcomes and skip previously passed unchanged tests |
| Simple module boundaries | For monorepos, map directories to separate workflows or composite actions |

---

## Local Development

### 1. Install dependencies

```bash
cd C:\Users\rajat\devops
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run all tests

```bash
pytest -v
```

### 3. Run only smoke tests in parallel

```bash
pytest -v -m smoke -n auto
```

### 4. Test the smart selector locally

```bash
# Simulate a change in user.py
python test_selector.py --files '["app/user.py"]'
# Expected output: ["tests/test_user.py"]

# Simulate a change in payment.py
python test_selector.py --files '["app/payment.py"]'
# Expected output: ["tests/test_payment.py"]

# Simulate an unknown file (falls back to all tests)
python test_selector.py --files '["app/unknown.py"]'
# Expected output: ["tests/"]
```

### 5. Build and run the Docker image locally

```bash
docker build -t smart-ci-cd-app:latest .
docker run --rm smart-ci-cd-app:latest
```

---

## Push to GitHub & Trigger the Pipeline

1. **Create a repository** on GitHub (e.g., `my-org/smart-ci-cd`).
2. **Push this project**:

```bash
git init
git add .
git commit -m "Initial commit: Smart CI/CD pipeline with test optimization"
git branch -M main
git remote add origin https://github.com/<USER>/<REPO>.git
git push -u origin main
```

3. **Trigger a run** by pushing a change to `app/user.py` or `app/payment.py`. Open the **Actions** tab to watch:
   - changed-files step listing the diff
   - select-tests step emitting `tests/test_user.py` (or `test_payment.py`)
   - pytest running only those tests
   - Docker image building only after green tests

---

## Expected Output Examples

### Example 1 — Changed file: `app/user.py`

```
Changed files: ["app/user.py"]
Selected tests: ["tests/test_user.py"]
============================= test session starts =============================
collected 7 items
tests/test_user.py::test_user_creation PASSED                           [ 14%]
tests/test_user.py::test_user_deactivate PASSED                         [ 28%]
tests/test_user.py::test_user_update_email PASSED                       [ 42%]
tests/test_user.py::test_user_update_email_invalid PASSED               [ 57%]
tests/test_user.py::test_validate_user_name PASSED                      [ 71%]
tests/test_user.py::test_create_user_success PASSED                    [ 85%]
tests/test_user.py::test_create_user_invalid_name PASSED                [100%]
============================== 7 passed in 0.05s ==============================
Docker image built successfully.
```

### Example 2 — Changed file: `app/payment.py`

```
Changed files: ["app/payment.py"]
Selected tests: ["tests/test_payment.py"]
============================= test session starts =============================
collected 7 items
tests/test_payment.py::test_payment_creation PASSED                     [ 14%]
tests/test_payment.py::test_payment_process PASSED                      [ 28%]
tests/test_payment.py::test_payment_refund PASSED                       [ 42%]
tests/test_payment.py::test_payment_refund_not_completed PASSED         [ 57%]
tests/test_payment.py::test_payment_negative_amount PASSED              [ 71%]
tests/test_payment.py::test_calculate_tax PASSED                        [ 85%]
tests/test_payment.py::test_calculate_total PASSED                     [100%]
============================== 7 passed in 0.05s ==============================
Docker image built successfully.
```

### Example 3 — Unknown file (fallback)

```
Changed files: ["app/unknown.py"]
Selected tests: ["tests/"]
============================= test session starts =============================
collected 14 items
tests/test_user.py  ......                                               [ 50%]
tests/test_payment.py ........                                           [100%]
============================== 14 passed in 0.10s ==============================
```

---

## License

MIT
