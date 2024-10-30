# Use a lightweight Python image
FROM python:3.9-alpine

WORKDIR /app

# Copy frontend script
COPY frontend.py /app/

# Install requests library for HTTP requests
RUN pip install requests

# Run the frontend script
CMD ["python", "frontend.py"]
