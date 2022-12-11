#!/usr/bin/expect

set timeout 30
spawn ssh root@39.101.74.166 docker stop tttt && docker rm tttt && docker pull vinokkk/tttt:latest && docker run -p 5000:5000 -d --name tttt vinokkk/tttt:latest
expect "root@39.101.74.166's password:"
send "Jin196632.\n"

interact
