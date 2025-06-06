FROM python:3.11
LABEL authors="Amatefinde"

RUN apt-get update && apt-get install -y libgl1

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \

  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.7.1


RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /literature
COPY poetry.lock pyproject.toml /literature/


RUN poetry install

COPY . .

RUN chmod +x app_entry_point.sh
RUN chmod a+x src/utils/fb2_converter/fb2c

CMD ["/literature/app_entry_point.sh"]