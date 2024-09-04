# pic_test

Prerequisites
   
- Docker installed on your machine.
- Knowledge on how to use curl requests
- Or knowledge on how to use Postman, Postman installed in your machine

Getting Started

Follow these steps to get the application up and running with Docker Compose.

1. Ensure in your terminal/command prompt you are inside the `pic_test` directory

2. copy and paste command: `docker compose up --build`
   This will initialise a docker container running a web server linked to the API.
   This will take a few minutes to complete
    
3. once docker compose is complete, you should see the URL to use to interact with the API.
   It will be printed on your screen like this: 'Uvicorn running on http://0.0.0.0:8000
   As a test, please copy and paste http://0.0.0.0:8000 into your browser, you should see
   a welcome message in your browser.

Using The API
    
To interact with the API, we can either use curl requests, or use a tool such as Postman.
Please ensure whilst you are interacting with the API, you do not close/ switch off the docker container.
The container is running the webserver, which was initiated in the 'Getting Started' section.
Also note the URL for the API should always be http://0.0.0.0:8000. This is defined within docker-compose.yaml
    
Using The API: Curl Requests
1. Please open an additional terminal/ command prompt tab.

2. As a test, please run the following command: `curl -X POST -H "Content-Type: application/json" -d '{"description": "first", "time": "2024-01-01", "id": 1}' 'http://0.0.0.0:8000/events'`
   You should see the calendar being returned. This created a calendar

3. If you run: `curl -X GET -H "Content-Type: application/json" 'http://0.0.0.0:8000/events'`
   You will see all existing calendars

4. You can see further examples of curl requests in curl_requests.txt

Using The API: Postman
    
1. Please open Postman application, and import calendar_api.postman_collection.json postman collection

2. You will see already created requests. Feel free to create, then perform different get actions
   on the calendars using the already built requests in the postman collection

Once you have completed running the API, you can close the webserver by going into the tab running the docker container, and pressing `CTRL+C`

You can double check the container has been closed by running docker ps, if you still see it, please run 
`docker rm <container id>` to remove the container



    

    

