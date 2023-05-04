# Use an official Python runtime as a parent image
FROM python:3.10.4
# Set the working directory to /app
WORKDIR /api
# Copy the current directory contents into the container at /app
COPY . .
# Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt
# Make port 80 available to the world outside this container
EXPOSE 5000
# Define environment variable
# ENV NAME World
# RUN pip3 install -r requirements.txt
RUN pip3 install flask
RUN pip3 install pymysql
# RUN pip3 install amqpstorm
# RUN pip3 install -U flask-cors
# RUN pip3 install redis
# RUN pip3 install mysql-connector-python
RUN pip3 install gunicorn
# RUN pip3 install pymongo
# RUN pip3 install flask-compress

# Run appSVC.py when the container launches
CMD gunicorn --workers=5 --threads=2 --log-level INFO --bind 0.0.0.0:5000 --access-logfile - app:app
