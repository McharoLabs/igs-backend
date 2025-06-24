FROM node:20.10.0-alpine

# Install build dependencies required for native modules
RUN apk add --no-cache python3 make g++

WORKDIR /client

# Copy package.json and package-lock.json (if present) for better caching
COPY package.json package-lock.json* ./

# Install node modules
RUN npm install

# Install serve globally to serve production build
RUN npm i -g serve

# Copy rest of the application code
COPY . .

# Build the app for production
RUN npm run build

# Expose port 5173
EXPOSE 5173

# Start the app by serving the build folder
CMD ["serve", "-s", "dist", "-l", "5173"]
