FROM openjdk:11-jdk-slim

# Install Git
RUN apt-get update && apt-get install -y git

# Install Python 3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install Jinja
RUN pip3 install jinja2

CMD ["/bin/bash"]
