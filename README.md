# Switch Controller REST API built in Python Flask
### Build and run docker container with Flask RESTful API

Clone repo `git clone https://github.com/richvigorito/switch-api.git`

Change directory `cd switch-api`

Build image `docker build -t switch-api .` 
  
Run container in detached mode and publish port 5000 `docker run -d -p 5000:5000 switch-api`
  
API should be accessible on port 5000 `curl -i localhost:5000/api/v1.0/switches`


... this repo was shamelessly adapted from: https://github.com/gabimelo/flask-boilerplate
