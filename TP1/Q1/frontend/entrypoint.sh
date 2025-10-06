#!/bin/sh

# Replace the placeholder with the actual API URL from environment variable
sed -i "s|__API_URL__|${API_URL}|g" /usr/share/nginx/html/script.js

# Start nginx
exec "$@"
