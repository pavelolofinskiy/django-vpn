# Django VPN Service

This repository contains a Django project for a VPN service.

## Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/django-vpn-service.git

2. Navigate to the project directory:

   ```bash
   cd django-vpn-service

3. Build and run the Docker containers using Docker Compose:
    ```bash
    docker-compose up --build

4. Access the Django application:
   Open a web browser and navigate to http://localhost:8000/

5. To stop the application, press Ctrl + C in the terminal where Docker Compose is running, and then run:
   ```bash
   docker-compose down

## Notes 
    The Django application will be available at http://localhost:8000/
    Ensure port 8000 is available and not used by any other service on your machine.
    For production deployment, additional configuration and security measures are recommended.
    
