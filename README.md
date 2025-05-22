# API Gateway with Backend Services

This project consists of three services:
1. API Gateway (port 8000)
2. Backend Service 1 (port 8001)
3. Backend Service 2 (port 8002)

## Features

- API Gateway with authentication and rate limiting
- Two backend services with sample data
- Dockerized services with Docker Compose
- Environment variable configuration

## Setup

1. Make sure you have Docker and Docker Compose installed
2. Clone this repository
3. Create a `.env` file in the api_gateway directory with the following content:
   ```
   API_USERNAME=admin
   API_PASSWORD=admin
   SERVICE1_URL=http://service1:8001
   SERVICE2_URL=http://service2:8002
   ```

## Running the Services

To start all services:

```bash
docker-compose up --build
```

## API Endpoints

### API Gateway (http://localhost:8000)

- GET `/` - Check if API Gateway is running
- GET `/service1/{path}` - Proxy to Service 1
- GET `/service2/{path}` - Proxy to Service 2

### Service 1 (http://localhost:8001)

- GET `/` - Check if Service 1 is running
- GET `/data` - Get sample data from Service 1

### Service 2 (http://localhost:8002)

- GET `/` - Check if Service 2 is running
- GET `/data` - Get sample data from Service 2

## Authentication

The API Gateway uses Basic Authentication. Use the following credentials:
- Username: admin
- Password: admin

## Rate Limiting

The API Gateway implements rate limiting:
- 100 requests per minute per IP address
- Exceeding the limit will result in a 429 Too Many Requests response 