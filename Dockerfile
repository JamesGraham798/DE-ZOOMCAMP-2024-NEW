#defines the base image used
FROM python:3.9

#gives specifications on what to run when opening the container
RUN pip install pandas

#will create a directory in the container and will cd into it when container is started
WORKDIR /app

# copy pipeline file, first is the name of it at the source then the name of the pipeline in the new destination
COPY pipeline.py pipeline.py

#want to use bash when opening the container as opposed to python at the start
## ENTRYPOINT [ "bash" ]

#want to have python and file ready when opening container
ENTRYPOINT [ "python", "pipeline.py" ]

#to run dockerfile after buidling do something like docker run -it test:pandas 2021-01-15 (you can put any date there)