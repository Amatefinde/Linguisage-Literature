#!/bin/sh

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 9200 --ssl-certfile /literature/letsencrypt/live/linguisage.ru/fullchain.pem --ssl-keyfile /literature/letsencrypt/live/linguisage.ru/privkey.pem