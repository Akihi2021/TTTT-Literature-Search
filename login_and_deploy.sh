#!/usr/bin/expect

set timeout 30
spawn ssh root@39.101.74.166 "./deploy.sh"
expect "root@39.101.74.166's password:"
send "Jin196632.\n"

interact


