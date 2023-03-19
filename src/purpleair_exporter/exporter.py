"""
Pulls data from specified PurpleAir air quality monitor and presents as Prometheus metrics
"""
from _socket import gaierror
import json
import os
import sys

import requests
from requests.auth import HTTPDigestAuth
import time
from . import prometheus_metrics
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from socketserver import ForkingMixIn
from prometheus_client import generate_latest, Summary
from urllib.parse import parse_qs
from urllib.parse import urlparse

LOCAL_API="/json?live=true"

def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary(
    'request_processing_seconds', 'Time spent processing request')


class ForkingHTTPServer(ForkingMixIn, HTTPServer):
    max_children = 30
    timeout = 30

class RequestHandler(BaseHTTPRequestHandler):
    """
    Endpoint handler
    """
    def return_error(self):
        self.send_response(500)
        self.end_headers()

    def do_GET(self):
        """
        Process GET request

        :return: Response with Prometheus metrics
        """
        # this will be used to return the total amount of time the request took
        start_time = time.time()
        # get parameters from the URL
        url = urlparse(self.path)
        # following boolean will be passed to True if an error is detected during the argument parsing
        error_detected = False
        query_components = parse_qs(urlparse(self.path).query)

        sensor_host = None
        try:
            sensor_host = query_components['sensor_host'][0]
        except KeyError as e:
            print_err("missing or invalid parameter %s" % e)
            self.return_error()
            error_detected = True

        if url.path == self.server.endpoint and sensor_host is not None:

            sensor_url = "http://{}:{}".format(sensor_host, LOCAL_API)

            response = requests.get(sensor_url)
            if response.status_code != 200:
                print_err("unexpected http return code {} from sensor url {}".format(response.status_code, sensor_url))
                self.return_error()
                error_detected = True

            try:
                data = response.json()
            except ValueError as e:
                print_err("ValueError when parsing json from response: {}".format(e))
                self.return_error()
                error_detected = True

            prometheus_metrics.purpleair_temp_gauge.labels(sensor_host=sensor_host,
                                                           sensor_id=data['SensorId']).set(data['current_temp_f'])

            prometheus_metrics.purpleair_humidity_gauge.labels(sensor_host=sensor_host,
                                                               sensor_id=data['SensorId']).set(data['current_humidity'])

            prometheus_metrics.purpleair_dewpoint_gauge.labels(sensor_host=sensor_host,
                                                               sensor_id=data['SensorId']).set(data['current_dewpoint_f'])

            prometheus_metrics.purpleair_pressure_gauge.labels(sensor_host=sensor_host,
                                                               sensor_id=data['SensorId']).set(data['pressure'])

            prometheus_metrics.purpleair_pm25aqi_gauge.labels(sensor_host=sensor_host,
                                                              sensor_id=data['SensorId']).set(data['pm2.5_aqi'])

            prometheus_metrics.purpleair_httpsuccess_gauge.labels(sensor_host=sensor_host,
                                                                  sensor_id=data['SensorId']).set(data['httpsuccess'])

            prometheus_metrics.purpleair_httpsends_gauge.labels(sensor_host=sensor_host,
                                                                sensor_id=data['SensorId']).set(data['httpsends'])

            # get the amount of time the request took
            REQUEST_TIME.observe(time.time() - start_time)

            # generate and publish metrics
            metrics = generate_latest(prometheus_metrics.registry)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(metrics)

        elif url.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write("""<html>
            <head><title>PurpleAir Air Quality Sensor Exporter</title></head>
            <body>
            <h1>PurpleAir Air Quality Sensor Exporter</h1>
            <p>Visit <a href="/metrics">Metrics</a> to use.</p>
            </body>
            </html>""")

        else:
            if not error_detected:
                self.send_response(404)
                self.end_headers()


class ExporterServer(object):
    """
    Basic server implementation that exposes metrics to Prometheus
    """

    def __init__(self, address='0.0.0.0', port=9312, endpoint="/metrics"):
        self._address = address
        self._port = port
        self.endpoint = endpoint

    def print_info(self):
        print_err("Starting exporter web server on: http://{}:{}{}".format(self._address, self._port, self.endpoint))
        print_err("Press Ctrl+C to quit")

    def run(self):
        self.print_info()

        server = ForkingHTTPServer((self._address, self._port), RequestHandler)
        server.endpoint = self.endpoint

        try:
            while True:
                server.handle_request()
        except KeyboardInterrupt:
            print_err("Killing exporter")
            server.server_close()
