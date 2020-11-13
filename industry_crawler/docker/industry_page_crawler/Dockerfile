FROM python:3.7

COPY /requirements.txt /

RUN pip3 install -U pip && \
    pip3 install --no-cache-dir -r /requirements.txt && rm /requirements.txt

COPY /industry_page_crawler /app/

COPY settings.py /app/

WORKDIR /app/

CMD ["/app/entrypoint.sh"]
