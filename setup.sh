#!/bin/bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create settings.json
cat <<EOT > settings.json
{
    "AWS_ACCESS_KEY": ["AWS Access Key", "AKIA[0-9A-Z]{16}"],
    "AWS_SECRET_KEY": ["AWS Secret Key", "[A-Za-z0-9+/]{40}"]
}
EOT

# Run the Python script
python main.py

# Deactivate virtual environment
deactivate
