FROM python:3.9

#ENV DASH_DEBUG_MODE True
#COPY ./ /app
RUN rm -rf __pycache__
COPY requirements.txt /opt/
RUN pip install -r /opt/requirements.txt
WORKDIR /app
EXPOSE 8050
CMD ["python", "index.py"]