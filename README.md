# Swagger 
Path: 127.0.0.1:5000/v1/swagger

# Docker Build 
docker build -t tttt:{VERSION_TAG} .

# Dokcer Run
docker run -it -p 5000:5000 tttt:latest

# Docker Run (For Test: No need to build docker file each time when changes applied)
docker run -it -p 5000:5000 -v {ABSOLUTE_PATH_OF_YOUR_APP}:/app 
e.g. docker run -it -p -v /Users/kim/Intern/momenta/codes/TTTT-Literature-Search:/app 5000:5000 2f6bcefe2160
