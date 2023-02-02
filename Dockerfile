FROM python:3.10.6
ENV PYTHONUNBUFFERED 1
COPY . $DockerHOME
RUN pip3 install -r requirements.txt
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]