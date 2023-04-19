FROM python:3.10.9-bullseye
ADD requirements.txt . 
RUN pip install -r requirements.txt
CMD ["python", "-V"]
