# Use the official Python image for ARM architecture
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy your code into the container
COPY . .

# Install dependencies
RUN pip3 install -r requirements.txt

# Start the bot
CMD ["python", "kindleThis.py"]
