# modules/rds/outputs.tf

output "db_endpoint" {
  description = "The database endpoint without the port"
  value       = aws_db_instance.rds_instance.address
}

output "db_port" {
  description = "The database port"
  value       = aws_db_instance.rds_instance.port
}

output "rds_sg_id" {
  description = "Security group ID for RDS"
  value       = aws_security_group.rds_security_group.id
}
