# Use the official Python image as a base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV TZ=UTC

# Create and set the working directory
RUN mkdir /webapp
WORKDIR /webapp

# Copy the requirements file and install dependencies
COPY requirements.txt /webapp/
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Start the application

CMD ["gunicorn", "CheckGen.wsgi:application", "--bind", "0.0.0.0:8000"]
