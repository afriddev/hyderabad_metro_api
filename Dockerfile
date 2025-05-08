FROM python:3.11

# assumes app.py contains your fastapi app
COPY app.py app.py
# install dependencies
RUN pip install fastapi uvicorn

# this configuration is needed for your app to work, do not change it
ENTRYPOINT ["uvicorn", "app:app", "--host=0.0.0.0", "--port=80"]