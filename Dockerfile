# Step 1: Use an official Python
FROM python:3.9-slim

# Step 2: Set the working directory in the container to /app
WORKDIR /app

# Step 3: Copy the contents into the container at /app
COPY . .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port the app runs on
EXPOSE 8000

# Step 6: Define the command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]