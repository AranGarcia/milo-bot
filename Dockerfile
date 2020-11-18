# FROM python:3.6


# COPY requirements.txt .

# # First upgrade pip
# RUN pip install --upgrade pip && \
#     pip install --use-feature=2020-resolver -r requirements.txt

# # Rasa configuration
# ADD rasa .
# RUN rasa train

# # Execute the server
# EXPOSE 5005

# TODO: Delete everything above.

# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:2.0.0

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
# COPY actions/requirements-actions.txt ./

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
# RUN pip install -r requirements-actions.txt

# Copy actions folder to working directory
COPY rasa/actions /app/actions

# By best practices, don't run the code with root user
USER 1001

EXPOSE 5055