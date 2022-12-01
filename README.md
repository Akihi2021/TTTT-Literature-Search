# Git Repo
https://github.com/Akihi2021/TTTT-Literature-Search

# Dockerhub Repo
https://hub.docker.com/repository/docker/vinokkk/tttt/

# Swagger 
Path: localhost:5000/v1/swagger

# Docker Commands
## Workflow
- For Developer
1. Build
2. Run
3. Push
- For User (Front End Developers)
1. Pull 
2. Run 

## Docker Pull
`docker pull vinokkk/{VERSION_TAG}`

## Docker Build
NOTE: need to run in the project root path

`docker build -t tttt:{VERSION_TAG} .`

## Docker push 
`docker push vinokkk/tttt:{VERSION_TAG}`

## Docker Run
`docker run -it -p 5000:5000 tttt:{VERSION_TAG} `

NOTE: 
1. -p flag binds local port 5000 to the docker container port 5000 which allows us to visit our service with URL localhost:5000
2. When run successfully, you should see swagger on localhost:5000/v1/swagger




## Docker Run With Codes Mounted
`docker run -it -p 5000:5000 -v {ABSOLUTE_PATH_OF_YOUR_APP}:/app `

e.g. 

`docker run -it -p 5000:5000 -v /Users/kim/Intern/momenta/codes/TTTT-Literature-Search:/app tttt:1.0`

NOTE: 
1. -v flag mount our TTTT project to the /app directory of our container.

2. Since python is a descriptive language, this will allow us to modify our code without having to  build docker image each time, simply restart the container will do.

