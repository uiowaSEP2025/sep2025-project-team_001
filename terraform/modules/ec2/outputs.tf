output "public_ip" {
  description = "Public IP of the backend EC2 instance"
  value       = aws_instance.backend_ec2.public_ip
}
