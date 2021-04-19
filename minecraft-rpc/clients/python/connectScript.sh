#!/bin/bash
#Takes connnection string as args
SERVER=ec2-user@$1
scp -i "~/.ssh/aws_frankfurt.pem" transfer.sh $SERVER:~/transfer.sh
ssh -i "~/.ssh/aws_frankfurt.pem" $SERVER "sudo chmod 755 transfer.sh"
ssh -i "~/.ssh/aws_frankfurt.pem" $SERVER "sudo -s ./transfer.sh"
scp -i "~/.ssh/aws_frankfurt.pem" -r $SERVER:output ./
ssh -i "~/.ssh/aws_frankfurt.pem" $SERVER "sudo rm -r output"