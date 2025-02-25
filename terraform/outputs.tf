output "public_subnet_a_id" {
  description = "ID of the newly created public subnet a"
  value       = aws_subnet.public_subnet_a.id
}

output "public_subnet_b_id" {
  description = "ID of the newly created public subnet b"
  value       = aws_subnet.public_subnet_b.id
}

output "rds_endpoint" {
  description = "Endpoint of the RDS instance from the module"
  value       = module.rds.db_endpoint
}

output "backend_ec2_public_ip" {
  value       = module.backend_ec2.public_ip
  description = "Public IP of the backend EC2"
}
