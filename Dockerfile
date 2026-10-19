FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN pip install --no-cache-dir flask playwright
RUN playwright install chromium --with-deps

WORKDIR /app
COPY app.py .

EXPOSE 8080
CMD ["python", "app.py"]
