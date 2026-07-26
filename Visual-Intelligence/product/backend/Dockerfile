FROM python:3.12-slim

# Security: run as non-root
RUN groupadd -r atelier && useradd -r -g atelier atelier

WORKDIR /app

# Install dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ownership
RUN chown -R atelier:atelier /app
USER atelier

EXPOSE 8000

# Production: uvicorn via Supervisor (see supervisord.conf)
# Dev: override with: docker run ... uvicorn app.main:app --reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
