# Git Repo
https://github.com/Akihi2021/TTTT-Literature-Search

# Dockerhub Repo
https://hub.docker.com/repository/docker/vinokkk/tttt/

# Swagger 
http://localhost:5000/v1/swagger

# RUN
When run successfully you should see swagger in the path above

## Run on local machine 
1. clone codes 

`git clone https://github.com/Akihi2021/TTTT-Literature-Search`
3. install requirements 

`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
3. run project 

`python entrypoint.py`
## Run with docker 
1. pull docker image
`docker pull vinokkk/tttt:{VERSION_TAG}`

2. run docker image 
`docker run -it -p 5000:5000 vinokkk/tttt:{VERSION_TAG} `

   
# Docker Related Questions
### Workflow
- For Developer
1. Build
2. Run
3. Push
- For User (Front End Developers)
1. Pull 
2. Run 

### Docker Pull
`docker pull vinokkk/tttt:{VERSION_TAG}`

### Docker Build
NOTE: need to run in the project root path

`docker build -t vinokkk/tttt:{VERSION_TAG} .`

### Docker Push 
`docker push vinokkk/tttt:{VERSION_TAG}`

### Docker Run
`docker run -it -p 5000:5000 vinokkk/tttt:{VERSION_TAG} `

NOTE: 
1. -p flag binds local port 5000 to the docker container port 5000 which allows us to visit our service with URL localhost:5000
2. When run successfully, you should see swagger on localhost:5000/v1/swagger


### Docker Run With Codes Mounted
`docker run -it -p 5000:5000 -v {ABSOLUTE_PATH_OF_YOUR_APP}:/app vinokkk/tttt:{VERSION_TAG}`

e.g. 

`docker run -it -p 5000:5000 -v /Users/kim/Intern/momenta/codes/TTTT-Literature-Search:/app vinokkk/tttt:1.0`

NOTE: 
1. -v flag mount our TTTT project to the /app directory of our container.

2. Since python is a descriptive language, this will allow us to modify our code without having to  build docker image each time, simply restart the container will do.

