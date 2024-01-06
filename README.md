
# Documentation

## Installation Process

### Clone the Project

To get the source code, you can clone the project repository from the Git repository:

``` git clone git@github.com:chetangartoula/Navya_task.git ```

### Manual Setup

#### 1. Create a Simple .env File

Copy the sample \`.env\` file to create a new one:

``` cp sample.env .env ```

#### 2. Create a Database in Postgres

Run the following command to access the Postgres database:

``` psql -U postgres ```

Inside the Postgres shell, create the database:

``` sql CREATE DATABASE navya_db; ```

#### 3. Setup Redis

Ensure that Redis is installed and working correctly. Set the Redis host and port in the \`.env\` file.

#### 4. Create Virtual Environment

Create a virtual environment for the project:

``` python -m venv venv ```

Activate the virtual environment:

```
source venv/bin/activate  # On Linux/Mac
venv\\Scripts\\activate  # On Windows
```

#### 5. Install Dependencies

Install the required packages for the project:

``` pip install -r requirements.txt ```

### Run the Project

After completing the setup, you can run the following commands:

1.  **Start the Server:**

``` python manage.py runserver ```

2.  **Run Celery Worker:**

``` celery -A navya_project worker --loglevel=info ```

3.  **Run Celery Beat:**

``` celery -A navya_project beat --loglevel=info ```

### Docker Installation

For Docker installation, ensure that all environment variables are set as per Docker requirements. Then run the following command:

```docker-compose up ```
