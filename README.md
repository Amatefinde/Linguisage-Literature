# Linguisage Literature

One of Linguisage microservices that care about literature management

## What is it?
This microservice encapsulates the logic for processing literature and documents.

It accepts literature in **fb2**, **epub** or **PDF** format. It saves it and returns a unique id. 
Subsequently, you can retrieve, edit, or delete literature by this id. 
When literature in fb2 format is uploaded to the service, 
a background task (by celery) is started to convert it to ePub. 
When a pdf is uploaded, it will be automatically parsed within the 
background task (in case the pdf does not have a text layer) 
(at the moment this functionality has not been implemented yet). 

This microservice will be used by another microservice that will 
use it as a concierge librarian, simply giving it the users' 
literature to hold, leaving all the processing worries to it.

## Deploying
1. Clone repository `git clone https://github.com/iRespectOnlyYen/Linguisage-Literature.git`
2. Rename `.env-example` file to `.env` and fill by your secrets

### Deploying with Docker compose
3. Run `docker compose up`, than you can check that API run on port `9200` successfully


### Manual deploying (Linux)

3. Clone repository `git clone https://github.com/iRespectOnlyYen/Linguisage-Literature.git`, 
then open cloned dir `cd Linguisage-Literature`
4. Create venv `python3.11 -m venv venv`, 
then activate it `source venv/bin/activate`
5. Install poetry if you haven't `pip install poetry`
6. Install requirements `poetry install`
7. Make folder for logs `mkdir logs`
8. Run uvicorn or gunicorn:
    - for debug and development `nohup uvicorn main:app --host 0.0.0.0 --port 9200 --reload --ssl-keyfile /etc/letsencrypt/live/lenya.papiros.volsk.cloudns.biz/privkey.pem --ssl-certfile /etc/letsencrypt/live/lenya.papiros.volsk.cloudns.biz/fullchain.pem > logs/uvicorn.log 2>&1 &`
    - for production `todo`
9. Make sure that redis is installed in your system. 
Then run celery (background tasks): `nohup celery -A src.background_tasks.celery:celery worker --loglevel=INFO -n literature -Q lite_queue > logs/celery.txt 2>&1 &`
10. For monitoring background tasks you can run flower `nohup celery -A src.background_tasks.celery:celery flower > logs/flower.txt 2>&1 &`