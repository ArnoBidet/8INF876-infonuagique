FROM nginx:alpine

# Copy the entrypoint script first
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Remove default nginx files and copy our frontend files
RUN rm -rf /usr/share/nginx/html/*
COPY ./src /usr/share/nginx/html

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command to run nginx
CMD ["nginx", "-g", "daemon off;"]