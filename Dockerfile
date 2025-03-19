FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenSSL for certificate generation
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p app/certificates app/templates app/static

# Generate SSL certificates
RUN chmod +x scripts/generate_certs.sh && \
    ./scripts/generate_certs.sh

# Expose ports
EXPOSE 8000 8001

# Run the application
CMD ["sh", "-c", "python -m app.db.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile ./app/certificates/server.key --ssl-certfile ./app/certificates/server.crt"] 