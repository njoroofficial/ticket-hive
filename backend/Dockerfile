# 1. Base Image: Start with a lightweight Linux version that has Python 3.10 installed
FROM python:3.10-slim

# 2. Work Directory: Create a folder inside the container to hold our app
WORKDIR /app

# 3. Dependencies: Copy requirements first!
# Docker caches layers. If requirements.txt hasn't changed, 
# it won't re-run the expensive pip install step.
COPY requirements.txt .

# 4. Install: Install the Python packages inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Application Code: Copy the rest of your backend code into the container
COPY . .

# 6. Command: Tell the container how to run the app when it starts
# host 0.0.0.0 is crucial for Docker networking
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]