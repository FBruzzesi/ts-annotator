# docker build . -t ts-annotator
# docker run -p 8088:8088 ts-annotator
FROM python:3.8-slim

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt \
    && find /root/.local/ -follow -type f  \
    -name '*.a' -name '*.txt' -name '*.md' -name '*.png' \
    -name '*.jpg' -name '*.jpeg' -name '*.js.map' -name '*.pyc' \
    -name '*.c' -name '*.pxc' -name '*.pyd' \    
    -delete \ 
    && find /usr/local/lib/python3.8 -name '__pycache__' | xargs rm -r

COPY app app
WORKDIR /app

EXPOSE 8088
ENTRYPOINT ["python3", "index.py"]
