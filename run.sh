#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Load initial data
echo "Loading initial data..."
python manage.py loaddata fixtures/initial_data.json
python manage.py loaddata fixtures/izanami_loop_data.json

# Set up challenges
echo "Setting up challenges..."
python manage.py setup_challenges

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py create_superuser

# Run the development server
echo "Starting development server..."
python manage.py runserver 0.0.0.0:8000
