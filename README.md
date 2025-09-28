# Restful Booker API Testing Framework

An effective API testing framework for the Restful Booker API. It automatically finds bugs and creates detailed reports.

## Utility

This framework tests the core features of the Restful Booker API and automatically captures any bugs it finds:

- **Authentication** - login, token handling, invalid credentials
- **Booking Management** - create, read, update, delete bookings  
- **Data Filtering** - search by names, dates, and combinations
- **Concurrent Operations** - multiple users accessing the API simultaneously
- **Health Checks** - making sure the API is available

When tests fail, it automatically creates Excel reports with all the bug details. No manual work needed!

## Quick Start

### Setup
```bash
# Clone the project
git clone <repository-url>
cd restful-booker-test-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

**For bug reporting (recommended):**
```bash
pytest tests/ -v -s -n0
```

**For faster execution:**
```bash
pytest tests/ -v -s -n auto
```

**Run specific test types:**
```bash
pytest -m smoke -v -s -n0          # Critical tests only
pytest -m auth -v -s -n0           # Authentication tests
pytest -m booking -v -s -n0        # Booking management tests
pytest -m concurrent -v -s -n0     # Concurrent operations
```

### Test Reports

After running tests, check the `reports/` folder for:
- **HTML report** - `report.html` (test results overview)
- **Excel bug report** - `enhanced_bug_report_*.xlsx` (detailed bug information)

## Configuration

Copy the example environment file and customize if needed:
```bash
cp .env.example .env
```

Available settings:
- `TEST_ENV` - Which environment to test (prod, dev, staging)
- `API_USERNAME` - API username (default: admin)
- `API_PASSWORD` - API password (default: password123)

### Testing Different Environments

**Local testing:**
```bash
# Test production (default)
pytest tests/ -v -s -n0

# Test development environment
TEST_ENV=dev pytest tests/ -v -s -n0

# Set environment for entire session
export TEST_ENV=dev
pytest tests/ -v -s -n0

# Use .env file for persistent settings
echo "TEST_ENV=dev" > .env
pytest tests/ -v -s -n0
```

**Available environments:**
- `prod` (default) - https://restful-booker.herokuapp.com
- `dev` - https://dev.restful-booker.herokuapp.com  
- `staging` - https://staging.restful-booker.herokuapp.com

## Project Structure

```
restful-booker-test-framework/
├── clients/                    # API client classes
├── config/                     # Environment configuration
├── models/                     # Data models
├── tests/                      # All test files
│   ├── data/                   # Test data generators
│   └── test_*.py              # Individual test suites
├── utils/                      # Helper utilities
├── reports/                    # Generated reports (auto-created)
└── .github/workflows/          # CI/CD automation
```

## Test Categories

- **Smoke Tests** (`-m smoke`) - Essential functionality that must work
- **Authentication** (`-m auth`) - Login and security features
- **Booking Management** (`-m booking`) - Core CRUD operations
- **Concurrent Operations** (`-m concurrent`) - Multi-user scenarios
- **Health Checks** (`-m health`) - API availability

## Automatic Bug Detection

The framework automatically:
- Captures test failures with detailed error messages
- Determines which API area is affected
- Assigns severity levels based on test importance
- Creates Excel reports with all bug information
- Includes environment details and timestamps

## CI/CD Integration

The framework runs automatically on GitHub Actions:
- **Schedule**: Monday to Friday at 12:00 PM UTC
- **Reports**: Uploaded as artifacts for 7 days
- **Python**: Uses Python 3.13 for consistency

## Common Commands

```bash
# Full test suite with bug reporting
pytest tests/ -v -s -n0

# Quick smoke test
pytest -m smoke -v -s

# Test specific functionality
pytest tests/test_booking_crud.py -v -s -n0

# Generate HTML report
pytest tests/ -v -s -n0 --html=reports/my_report.html
```
