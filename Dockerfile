FROM python:3.9

WORKDIR /code

RUN git clone https://github.com/dalvarin/slpoc.git /code/ansible --depth 1

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]