output "server_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.mlops_server.public_ip
}

output "app_url" {
  description = "URL to access the API"
  value       = "http://${aws_instance.mlops_server.public_ip}:8000"
}
