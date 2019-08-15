FROM python
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y    libldap2-dev \
                                            libsasl2-dev
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/