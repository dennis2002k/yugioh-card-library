# Build Stage
FROM node:20-slim AS build
WORKDIR /
# Copy the frontend files from your computer to the container root
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Serve Stage
FROM nginx:alpine
# Copy the compiled files from the build stage to Nginx
# Since WORKDIR was / above, the path is just /dist
COPY --from=build /dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]