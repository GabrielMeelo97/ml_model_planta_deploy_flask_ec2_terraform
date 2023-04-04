provider "aws" {
  region = "us-east-1"
}

resource "aws_key_pair" "app_key_pair" {
  key_name   = "gabrielssh2"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC5rgglXio0k6DF//ADBJPO7sWoBA3JrB1LP9k7bCgkW85DpAGwlUO7n5o27cgT2XwudTL+8MKyMipMm7jeW+W2FJ8SgUIB84zf8E/cmkccd4WwErHEvzLHuZJZtP3GFVFJOfMgAn2osenk3M9s1+cC6NgxUNV+XloTa0gcOLURASk9ECFPI/mjgkEtq02IlJK2yhkjUSa5nnGRvHrfA1QzjnAwiDBNENc/PGiIWfHpLp0fzva47XZ1DGxsC1u9zllYsVWyE2YaGkO4XmZfvZb1RjZ+ojZFsyR4+IMmZOXTsDy4eAYYepQynOZUNwmxYswxj23qQm7bbky1OH8huSExCgAbncuAB8AuGf5s90jRywuYcne2fAC4aK2sZpat39kveIBhSRy/v7ty5CxWRzhzPy3wwytgvsc3gntidu0bgbqkkvz83L5u91aX7Tw2PeersO8eAre8svE+o1m7L75C2MsQq9W3n1BSxN5wc4Qo0WcZE926lcq9fF+lwkcrVW0= gabriel@gabriel-VirtualBox"
}

resource "aws_security_group" "app_security_group" {
  name_prefix = "app_security_group"
  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 5000
    to_port   = 5000
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_instance" {
  ami = "ami-0c94855ba95c71c99" # AMI da região us-east-1
  instance_type = "t2.micro"
  key_name = aws_key_pair.app_key_pair.key_name
  vpc_security_group_ids = [aws_security_group.app_security_group.id]
  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install -y python3-pip
              sudo pip3 install flask
              git clone <seu_repositorio_do_git>
              cd <diretorio_do_app>
              nohup python3 app.py &
              EOF
  tags = {
    Name = "app_instance"
  }
}