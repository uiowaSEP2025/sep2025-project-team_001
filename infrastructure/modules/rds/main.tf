# modules/rds/main.tf

resource "aws_db_subnet_group" "rds_subnet_group" {
  count      = var.activate_rds ? 1 : 0
  name       = "rds-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "rds-subnet-group"
  }
}

resource "aws_db_instance" "postgres" {
  count                   = var.activate_rds ? 1 : 0
  identifier              = "project-postgres"
  allocated_storage       = 20
  engine                  = "postgres"
  engine_version          = "13.4"
  instance_class          = "db.t3.micro"
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group[0].name
  skip_final_snapshot     = true
  publicly_accessible     = true

  tags = {
    Name = "project-postgres"
  }
}

output "rds_endpoint" {
  value       = var.activate_rds ? aws_db_instance.postgres[0].endpoint : ""
  description = "PostgreSQL Database Endpoint"
}
