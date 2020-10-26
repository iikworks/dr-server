FROM python:3.8.6
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install
COPY . ./
EXPOSE 80