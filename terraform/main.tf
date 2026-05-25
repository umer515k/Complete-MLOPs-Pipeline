provider "aws" {
  region = var.aws_region
}

resource "aws_key_pair" "mlops_key" {
  key_name   = "mlops-key"
  public_key = file("~/.ssh/mlops-key.pub")
}

resource "aws_security_group" "mlops_sg" {
  name        = "mlops-sg"
  description = "Allow SSH and app traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "mlops_server" {
  ami                    = "ami-0c02fb55956c7d316"
  instance_type          = var.instance_type
  key_name               = aws_key_pair.mlops_key.key_name
  vpc_security_group_ids = [aws_security_group.mlops_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ec2-user
  EOF

  tags = {
    Name    = "mlops-pipeline-server"
    Project = "mlops-pipeline"
  }
}
