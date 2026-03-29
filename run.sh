#!/bin/bash

echo "Starting Trader Analytics..."

# Check if the .env file exists (crucial for API keys)
if [ ! -f .env ]; then
    echo "⚠️  WARNING: .env file not found in the root directory!"
    echo "Make sure your API keys (e.g., GROQ_API_KEY) are set before analyzing."
    echo ""
fi

# Run the Streamlit application
streamlit run app/main.py