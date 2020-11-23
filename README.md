# Django Project to get Meta data about Metar codes and display information.   

## Requirements

This Project is developed using **Django** and **Redis** . Additional requirements are included in **requirement.txt** file for interaction with *https://tgftp.nws.noaa.gov/data/observations/metar/stations/* website. <br />
<br/>Also change the **Redis_HOST** and **Redis_PORT** in the **settings.py** if deploying on any other server. 
<br /> The Project uses Redis, Web Drivers, Selenium and such libraries to develop the application.
 
 
This application is developed and tested well in Windows Environment. While instaling or running the app locally, if there occurs any error because of versioning, feel free to ping me on 
 **vivannathani99@gmail.com**
 

## How to run project locally

Clone repository and got to project's root directory afterwards follow steps:

1. Activate python virtual environment <br />
`source /path/to/local/env`

2. Install requirements <br />
`pip install -r requirements.txt`

3. Run Redis server <br />
    Dowload it from the **https://redis.io/** based on your system requirements <br />
 Refer to **https://redis.io/topics/quickstart** for installation guide.
 
 Once the redis file has be installed extract it and open the terminal and run the following command to run server
 `redis-server`
 
 To check if it responds to client open a new terminal and run 
  `redis client ping` this command returns "Pong".
  
**Congratulations! Your redis server has been served**

4. Now, Run server <br />
`python manage.py runserver`


### GET /

Has the frontend of the search. The button in the header part checks Status of Redis Server.

### GET /metar/ping

This checks if the Redis server is live or not,If not, it returns **Connection refused** else returns 

```json
{
    "data": "Pong"
}
```

### GET /metar/info?scode=<text>

Fetches metar code from the url and checks if the metar code exists, if not it returns 
**"Metar Code Dosen't Exsits"**

On re-visiting the same code again, the data is fetched from the Redis-cache for lower latency and faster loading process.

<br />

**Currently the Cache Time to Leave for the code/view to be deleted is set to be 5 minutes, mentioned in settings.py file.**

##For Instance look at the images below for better Visualization and Understanding

![Alt-Text](/Screenshots/code-not-exsits.JPG)

<br />

![Alt-Text](/Screenshots/code-exsists.JPG)



