# modules/nginx_ec2/outputs.tf

output "public_ip" {
  description = "Public IP of the NGINX reverse proxy"
  value       = aws_instance.nginx.public_ip
}

output "private_ip" {
  description = "Private IP of the NGINX reverse proxy"
  value       = aws_instance.nginx.private_ip
}

output "instance_id" {
  description = "Instance ID of the NGINX reverse proxy"
  value       = aws_instance.nginx.id
}

output "nginx_sg_id" {
  description = "Security Group ID of the NGINX reverse proxy"
  value       = aws_security_group.nginx_sg.id
}
