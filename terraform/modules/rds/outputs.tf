# modules/rds/outputs.tf

output "db_endpoint" {
  description = "The database endpoint without the port"
  value       = aws_db_instance.rds_instance.address
}

output "db_port" {
  description = "The database port"
  value       = aws_db_instance.rds_instance.port
}
