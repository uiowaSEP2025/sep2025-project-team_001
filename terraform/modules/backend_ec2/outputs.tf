# modules/backend_ec2/outputs.tf

output "public_ip" {
  description = "Public IP of the backend EC2 instance"
  value       = aws_instance.backend_ec2.public_ip
}

output "backend_sg_id" {
  description = "Security group ID of the backend EC2 instance"
  value       = aws_security_group.backend_sg.id
}
