# Demo Guide for Smart CI/CD Pipeline

This guide walks you through a live demonstration of the smart test selection system.

---

## Pre-Demo Setup

Open a terminal in `c:\Users\rajat\devops` and ensure dependencies are installed:

```cmd
pip install -r requirements.txt
```

---

## Demo Script (Step by Step)

### Step 1: Show the Project Structure
```cmd
dir /b
dir /b app
dir /b tests
```

**Explain:** "We have 4 modules in `app/` (user, payment, order, inventory) and corresponding test files in `tests/`."

---

### Step 2: Run Full Test Suite
```cmd
python -m pytest -v tests/
```

**Expected output:** 20 tests passed (7 user + 7 payment + 2 order + 3 inventory + 1 fixture test)

**Explain:** "This is what a traditional CI pipeline does — runs ALL tests on every commit. It works but wastes time."

---

### Step 3: Run Only Smoke/Regression Tests in Parallel
```cmd
python -m pytest -v -m "smoke or regression" -n auto tests/
```

**Expected output:** 13 tests passed across 8 parallel workers

**Explain:** "We can filter by markers and run tests in parallel with `pytest-xdist`."

---

### Step 4: Demonstrate Smart Test Selection

#### 4a: Change in `app/user.py`
```cmd
python test_selector.py --files "[\"app/user.py\"]"
```

**Expected output:** `["tests/test_user.py"]`

**Explain:** "When we change `user.py`, the selector maps it to only `test_user.py`."

#### 4b: Change in `app/payment.py`
```cmd
python test_selector.py --files "[\"app/payment.py\"]"
```

**Expected output:** `["tests/test_payment.py"]`

#### 4c: Change in `app/order.py`
```cmd
python test_selector.py --files "[\"app/order.py\"]"
```

**Expected output:** `["tests/test_order.py"]`

#### 4d: Change in `app/inventory.py`
```cmd
python test_selector.py --files "[\"app/inventory.py\"]"
```

**Expected output:** `["tests/test_inventory.py"]`

#### 4e: Unknown file (fallback)
```cmd
python test_selector.py --files "[\"app/unknown.py\"]"
```

**Expected output:** `["tests/"]`

**Explain:** "If the selector can't map a file, it safely falls back to running all tests."

---

### Step 5: Run Only Selected Tests

#### 5a: Run only user tests
```cmd
python -m pytest -v tests/test_user.py
```

**Expected output:** 7 tests passed

#### 5b: Run only order tests
```cmd
python -m pytest -v tests/test_order.py
```

**Expected output:** 2 tests passed

**Explain:** "In the CI pipeline, we only run the tests that the selector outputs. This saves time."

---

### Step 6: Show the GitHub Actions Workflow

Open `.github/workflows/ci.yml` in your editor and explain:

1. **Line 29-44:** Detects changed files using `git diff --name-only`
2. **Line 46-51:** Calls `test_selector.py` to map files to tests
3. **Line 53-67:** Runs only the selected tests with pytest
4. **Line 69-78:** Builds Docker image only if tests pass

---

### Step 7: Live Code Change Demo (Optional)

#### 7a: Make a small change to `app/user.py`
```cmd
# Add a comment or whitespace
```

#### 7b: Simulate the CI detection
```cmd
python test_selector.py --files "[\"app/user.py\"]"
python -m pytest -v tests/test_user.py
```

**Explain:** "This is exactly what happens in GitHub Actions when you push a change."

---

## Key Talking Points

1. **Problem:** Traditional CI runs all tests on every commit → slow feedback, wasted compute
2. **Solution:** Smart test selection maps changed files → relevant tests only
3. **Fallback:** Unmapped files trigger full suite → no tests are accidentally skipped
4. **Parallel execution:** `pytest-xdist` runs selected tests across CPU cores
5. **Markers:** `smoke` and `regression` markers add another layer of filtering

---

## Quick Reference Commands

| Command | Purpose |
|---|---|
| `python -m pytest -v tests/` | Run all tests |
| `python -m pytest -v -m "smoke or regression" -n auto tests/` | Run marked tests in parallel |
| `python test_selector.py --files "[\"app/user.py\"]"` | Map file to tests |
| `python -m pytest -v tests/test_user.py` | Run specific test file |
