# Use official PostgreSQL image
FROM mysql:latest

# Set environment variables for the default database
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=MenuExtraction123
ENV POSTGRES_DB=menu_db

# Copy the schema to the Docker image
COPY schema.sql /docker-entrypoint-initdb.d/
