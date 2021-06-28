FROM python:3.9-slim

RUN pip install -U poetry

WORKDIR /.fourier

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

COPY . .

EXPOSE 2359

ENTRYPOINT [ "python3" ]
CMD [ "-m", "fourierdb", "run" ]