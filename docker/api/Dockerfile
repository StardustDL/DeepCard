FROM ubuntu:18.04

RUN apt clean && apt update --fix-missing && apt install -y python3 python3-pip libsm6 libxrender1 libxext-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pip -U

RUN pip install --no-cache-dir numpy opencv-python pillow https://download.pytorch.org/whl/cpu/torch-1.1.0-cp36-cp36m-linux_x86_64.whl https://download.pytorch.org/whl/cpu/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl

WORKDIR /app

COPY ./src/DeepCard.API .

EXPOSE 80

ENTRYPOINT ["python3", "server.py"]