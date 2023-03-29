FROM nikolaik/python-nodejs:python3.11-nodejs18
ARG UID=1000
ARG GID=1000
RUN groupadd -g 999 docker \
    && usermod -u "$UID" -g "$GID" -G docker pn
RUN yarn global add aws-cdk
WORKDIR /app
ENV POETRY_VIRTUALENVS_CREATE=false
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-cache --no-interaction --no-ansi
