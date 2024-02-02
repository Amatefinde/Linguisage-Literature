# Linguisage Literature

One of Linguisage microservices that care about literature management

### Manual deploying (Linux)

1. Clone repository `git clone https://github.com/iRespectOnlyYen/Linguisage-Literature.git`, 
then open cloned dir `cd Linguisage-Literature`
2. Create venv `python3.11 -m venv venv`, 
then activate it `source venv/bin/activate`
3. Install poetry if you haven't `pip install poetry`
4. Install requirements `poetry install`
5. Make folder for logs `mkdir logs`
6. Run uvicorn or gunicorn:
    - for debug and development `nohup uvicorn main:app --host 0.0.0.0 --port 9200 --reload --ssl-keyfile /etc/letsencrypt/live/lenya.papiros.volsk.cloudns.biz/privkey.pem --ssl-certfile /etc/letsencrypt/live/lenya.papiros.volsk.cloudns.biz/fullchain.pem > uvicorn.log 2>&1 &`
    - for production `todo`
7. Make sure that redis is installed in your system. 
Then run celery (background tasks): `nohup celery -A src.background_tasks.celery:celery worker --loglevel=INFO -n literature -Q lite_queue > logs/celery.txt 2>&1 &`
8. For monitoring background tasks you can run flower `nohup celery -A src.background_tasks.celery:celery flower > logs/flower.txt 2>&1 &`