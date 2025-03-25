# modules/backend_ec2/outputs.tf

output "private_ip" {
  description = "Private IP of the backend EC2 instance"
  value       = aws_instance.backend_ec2.private_ip
}

output "backend_sg_id" {
  description = "Security group ID of the backend EC2 instance"
  value       = aws_security_group.backend_sg.id
}
