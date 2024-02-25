## Getting Started



### 1. Clone the Repository

First, clone your Flask application repository to your local machine using the following command:

```bash
git clone https://github.com/farseenmanekhan1232/ml-drug-test.git
cd ml-drug-test
```

### 2. Create a Virtual Environment

It is recommended to create a virtual environment for your project to manage dependencies:

- **Windows:**

```bash
python -m venv venv
```

- **macOS/Linux:**

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment with the following command:

- **Windows:**

```bash
.\venv\Scripts\activate
```

- **macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### 5. Set Environment Variables

Before running your Flask application, you need to set the `FLASK_APP` environment variable:

- **Windows:**

```bash
set FLASK_APP=app.py
```

- **macOS/Linux:**

```bash
export FLASK_APP=app.py
```

Replace `app.py` with the entry point of your Flask application.


### 6. Generate Model

```bash
python ./drug_test/generate_model.py
```

### 6. Run the Flask Application

Finally, start your Flask application with:

```bash
flask run
```

Your application will be accessible at `http://127.0.0.1:5000/predict`.
