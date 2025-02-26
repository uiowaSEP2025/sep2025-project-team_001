# modules/frontend_ec2/outputs.tf

output "public_ip" {
  description = "Public IP of the frontend EC2 instance"
  value       = aws_instance.frontend_ec2.public_ip
}

output "frontend_sg_id" {
  description = "Security group ID for frontend EC2"
  value       = aws_security_group.frontend_sg.id
}
