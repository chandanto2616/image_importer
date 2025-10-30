# -----------------------------------------------
# 1️⃣ Base image
# -----------------------------------------------
FROM python:3.11-slim

# -----------------------------------------------
# 2️⃣ Install system dependencies
# -----------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------------------------
# 3️⃣ Set working directory inside container
# -----------------------------------------------
WORKDIR /app

# -----------------------------------------------
# 4️⃣ Copy dependency file and install Python packages
# -----------------------------------------------
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# -----------------------------------------------
# 5️⃣ Copy the backend FastAPI app
# -----------------------------------------------
COPY backend/app /app/app

# -----------------------------------------------
# 6️⃣ Copy the frontend static files (optional, if backend serves static)
# -----------------------------------------------
COPY frontend /app/frontend

# -----------------------------------------------
# 7️⃣ Copy entrypoint script and make it executable
# -----------------------------------------------
COPY backend/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# -----------------------------------------------
# 8️⃣ Expose port
# -----------------------------------------------
EXPOSE 8000

# -----------------------------------------------
# 9️⃣ Set entrypoint
# -----------------------------------------------
ENTRYPOINT ["/app/entrypoint.sh"]
backend/Dockerfile
# FROM python:3.11-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
