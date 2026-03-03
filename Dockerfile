FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for pyarrow
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv

# Create the virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Add the virtual environment's bin directory to PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY extract-load.py .

CMD ["python3", "extract-load.py"]