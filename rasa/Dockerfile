FROM rasa/rasa-sdk:2.0.0

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY requirements.txt ./

# Change back to root user to install dependencies
USER root

# Install system dependencies
RUN apt update -y && \
    apt upgrade -y && \
    apt install gcc libpq-dev -y 

# Installing python requirements and dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download es_core_news_lg

# Copy actions folder to working directory
COPY rasa/actions /app/actions
COPY docs /app/docs
COPY lib /app/lib

# Change time zone
ENV TZ=America/Mexico_City
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# By best practices, don't run the code with root user
USER 1001

EXPOSE 5055
