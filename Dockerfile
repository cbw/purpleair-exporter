FROM python:3-alpine
ADD . /usr/src/purpleair_exporter
RUN pip3 install -e /usr/src/purpleair_exporter
ENTRYPOINT ["purpleair-exporter"]
EXPOSE 9313
