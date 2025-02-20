output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.docker_ec2.public_ip
}

output "ec2_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.docker_ec2.id
}