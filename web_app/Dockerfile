# Use official Node.js image
FROM node:18
LABEL authors="Cole Arduser"

# Create and set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Expose port 3000 for the React dev server
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
