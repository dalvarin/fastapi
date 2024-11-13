FROM python:3.9

WORKDIR /code

RUN git clone https://github.com/dalvarin/slpoc.git /code/ansible --depth 1

#TODO add checkout to specific branch/tag/commit or Refspec

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#TODO ansible-galaxy installation of required roles and/or collections

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
