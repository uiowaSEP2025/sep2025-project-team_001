resource "aws_db_subnet_group" "rds_subnet_group" {
  count      = var.activate_rds ? 1 : 0
  name       = "rds-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "rds-subnet-group"
  }
}

# Main PostgreSQL instance
resource "aws_db_instance" "postgres" {
  count                   = var.activate_rds ? 1 : 0
  identifier              = "project-postgres"
  allocated_storage       = 20
  engine                  = "postgres"
  engine_version          = "13"
  instance_class          = "db.t3.micro"
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group[0].name
  skip_final_snapshot     = true
  publicly_accessible     = true
  multi_az                = var.replicas_count > 1  # Enable Multi-AZ if needed

  tags = {
    Name = "project-postgres"
  }
}

# Read replicas for PostgreSQL (if replicas_count > 1)
resource "aws_db_instance" "postgres_replica" {
  count                   = var.replicas_count > 1 ? var.replicas_count - 1 : 0  # Create replicas if replicas_count > 1
  identifier              = "project-postgres-replica-${count.index}"
  engine                  = "postgres"
  instance_class          = "db.t3.micro"
  publicly_accessible     = true
  replicate_source_db     = aws_db_instance.postgres[0].id  # Reference to the source PostgreSQL DB instance for read replica

  tags = {
    Name = "project-postgres-replica-${count.index}"
  }
}

# Output the RDS endpoint for the main PostgreSQL instance
output "rds_endpoint" {
  value       = var.activate_rds ? aws_db_instance.postgres[0].endpoint : ""
  description = "PostgreSQL Database Endpoint"
}
