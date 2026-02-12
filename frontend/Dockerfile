# Build Stage
FROM node:20-slim AS build-stage
WORKDIR /
# Copy the frontend files from your computer to the container root
COPY package*.json ./

# ... (Top of Dockerfile) ...
ARG VITE_API_URL
ARG VITE_S3_URL

# Make them available during the 'npm run build' step
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_S3_URL=$VITE_S3_URL

RUN npm install
COPY . .
RUN npm run build

# Serve Stage
FROM nginx:alpine
# Copy your custom config to the Nginx conf directory
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy your build files
COPY --from=build-stage /dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]