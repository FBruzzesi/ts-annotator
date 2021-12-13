# docker build . -t ts-annotator
# docker run -p 8080:8080 ts-annotator:latest
FROM python:3.8-slim

WORKDIR /projects

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --user --no-cache-dir -r requirements.txt \
    && find /root/.local/ -follow -type f  \
    -name '*.a' -name '*.txt' -name '*.md' -name '*.png' \
    -name '*.jpg' -name '*.jpeg' -name '*.js.map' -name '*.pyc' \
    -name '*.c' -name '*.pxc' -name '*.pyd' \
    -delete \
    && find /usr/local/lib/python3.8 -name '__pycache__' | xargs rm -r

COPY app app

EXPOSE 8080
ENTRYPOINT ["python3", "app/index.py"]
