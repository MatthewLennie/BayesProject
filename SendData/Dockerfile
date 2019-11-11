# From the base build
FROM bayesproject_buildpython:latest

#upload
COPY SendData.py /
COPY code_challenge_data1.csv /
COPY code_challenge_data2.csv /
#Send Data
CMD ["python","SendData.py"]
