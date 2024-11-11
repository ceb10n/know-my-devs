FROM python:3.12

RUN mkdir /knowmydevs

WORKDIR /knowmydevs

COPY . .

RUN pip3 install .

CMD [ "uvicorn", "knowmydevs.app:create_app"]