FROM jjanzic/docker-python3-opencv:opencv-4.0.1
COPY root.py .
COPY server server
COPY requirements_docker.txt .
COPY hrnet hrnet
EXPOSE 8009
RUN python -m pip install --no-cache-dir -r requirements_docker.txt
RUN python -m pip install --no-cache-dir torch==1.6.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN python -m pip install --no-cache-dir torchvision==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN python -m pip install --no-cache-dir -r hrnet/requirements.txt
CMD ["python", "server/dummy_flask_app.py"]
