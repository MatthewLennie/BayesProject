#Build on top of the buildpython image. 
FROM bayesproject_buildpython:latest


COPY ConsumePredict.py /
#COPY template.html /templates/
#COPY main.css /static/css/
COPY code_challenge_model.p /
COPY code_challenge_base_predictor.py /
#Run the ConsumePredict 
CMD ["python","ConsumePredict.py"]
#CMD ["FLASK_APP=hello.py", "flask", "run"]