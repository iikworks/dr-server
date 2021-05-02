FROM python:3.9.4
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install
COPY . ./
EXPOSE 80
