FROM jjanzic/docker-python3-opencv
COPY root.py
COPY server server
COPY requirements.txt .
COPY hrnet hrnet
EXPOSE 8008
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r hrnet/requirements_for_docker.txt
CMD ["python", "server/dummy_flask_app.py"]
