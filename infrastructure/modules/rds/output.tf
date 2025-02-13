# infrastructure/modules/rds/output.tf

# Output the RDS endpoint for the main PostgreSQL instance
output "rds_endpoint" {
  value       = var.activate_rds ? aws_db_instance.postgres[0].endpoint : ""  # Use [0] to refer to the first instance
  description = "The endpoint for the PostgreSQL database"
}

# Output the RDS DB username
output "db_username" {
  value       = var.activate_rds ? aws_db_instance.postgres[0].username : ""  # Use [0] to refer to the first instance
  description = "The username for the PostgreSQL database"
}

# Output the RDS DB password
output "db_password" {
  value       = var.activate_rds ? aws_db_instance.postgres[0].password : ""  # Use [0] to refer to the first instance
  description = "The password for the PostgreSQL database"
  sensitive   = true
}
