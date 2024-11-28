# Knajping demo django application

This is a Django application to manage restaurants by owners and review them by users

## Requirements

- **Python**: 3.12
- **Django**: 5.1
- **PostgreSQL**: 16 or higher

## Getting Started

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/maciejbentkowski/knajping-demo-django.git

cd knajping-demo-django
```

2. **Create a virtual environment and activate it**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** in .env file in the root directory of the project:
```bash
SECRET_KEY=your-secret-key
```


## Running the App


Docker required:

  ```
  docker-compose up -d 
  ```
   
Then, visit http://localhost:8000 in your browser.
## Testing

This app is set up with RSpec for testing. Run all tests with:

```bash
pytest
```
in app container