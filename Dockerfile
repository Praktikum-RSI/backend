FROM python:3.14-alpine

WORKDIR /app

RUN apk update && apk add --no-cache curl

RUN adduser -u 1000 -D appuser

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false

RUN poetry install --without dev --no-interaction --no-ansi --no-root

COPY --chown=appuser:appuser --chmod=700  . .

USER appuser

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
