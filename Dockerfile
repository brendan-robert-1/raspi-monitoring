FROM arm32v7/python:3.6-buster
RUN pip install psutil pyembedded paho-mqtt
COPY embedded-raspi-monitoring.py ./
ADD setup.sh /
RUN chmod +x /setup.sh
CMD ["/setup.sh"]