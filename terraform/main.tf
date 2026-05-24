provider "aws" {
  region = var.aws_region
}

# Upload your public SSH key to AWS so you can SSH into the instance
resource "aws_key_pair" "mlops_key" {
  key_name   = "mlops-key"
  public_key = file("~/.ssh/mlops-key.pub")
}

# Security group — controls what traffic is allowed in/out
resource "aws_security_group" "mlops_sg" {
  name        = "mlops-sg"
  description = "Allow SSH and app traffic"

  # Allow SSH from anywhere (you can restrict to your IP later)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow traffic on port 8000 (your FastAPI app)
  ingress {
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# The EC2 instance itself
resource "aws_instance" "mlops_server" {
  ami                    = "ami-0c02fb55956c7d316"  # Amazon Linux 2 us-east-1
  instance_type          = var.instance_type
  key_name               = aws_key_pair.mlops_key.key_name
  vpc_security_group_ids = [aws_security_group.mlops_sg.id]

  # Runs on first boot — installs Docker on the server
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
