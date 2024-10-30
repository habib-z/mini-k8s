# Use a lightweight Python image
FROM python:3.9-alpine

WORKDIR /app

# Copy backend script and install dependencies
COPY backend.py /app/
RUN pip install flask

# Expose port used by the Flask app
EXPOSE 5000

# Run the backend
CMD ["python", "backend.py"]
