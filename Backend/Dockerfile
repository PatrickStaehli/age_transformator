FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Add modules
ADD scripts scripts 
ADD configs configs
ADD datasets datasets
ADD models models
ADD pretrained_models pretrained_models
ADD utils utils

# Give execution permission
RUN chmod -R 755 .

# Install dblib
RUN yum update -y && \
    yum install build-essential cmake pkg-config -y
RUN yum update -y && yum install -y gcc gcc-c++
RUN pip3 install cmake --target "${LAMBDA_TASK_ROOT}"
RUN yum install boost-devel -y
RUN yum install make -y
RUN yum install libXext libSM libXrender -y
RUN pip3 install dlib --target "${LAMBDA_TASK_ROOT}"

# Install the function's dependencies using file requirements.txt
COPY requirements.txt .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to the handler
CMD [ "app.lambda_handler" ] 