FROM python:3.6


COPY requirements.txt .

# First upgrade pip
RUN pip install --upgrade pip && \
    pip install --use-feature=2020-resolver -r requirements.txt

# Rasa configuration
ADD rasa .
RUN rasa train

# Execute the server
EXPOSE 5005