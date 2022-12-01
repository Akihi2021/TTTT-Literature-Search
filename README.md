# Swagger 
Path: 127.0.0.1:5000/v1/swagger

# Docker 
## Workflow 
1. For Developer
- Build 
- Run 
- Push 

2. For User
- Pull
- Run
## Docker Pull
docker pull vinokkk/{VERSION_TAG}

## Docker Build 
docker build -t tttt:{VERSION_TAG} .

## Docker push 
docker push -t vinokkk/tttt:{VERSION_TAG}

## Dokcer Run
- Normal: 
docker run -it -p 5000:5000 tttt:latest 
- For Test:
docker run -it -p 5000:5000 -v {ABSOLUTE_PATH_OF_YOUR_APP}:/app (For Test: No need to build docker file each time when changes applied)
- 
e.g. docker run -it -p -v /Users/kim/Intern/momenta/codes/TTTT-Literature-Search:/app 5000:5000 2f6bcefe2160
