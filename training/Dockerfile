FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy training scripts and data
COPY train_and_register_intent.py .
COPY intent_data.csv .

# Default command
CMD ["python", "train_and_register_intent.py"]
