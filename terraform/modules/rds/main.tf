# modules/rds/main.tf

######################################
# Security Group
######################################
resource "aws_security_group" "rds_security_group" {
  name        = "${var.db_identifier}-sg"
  description = "Security group for RDS"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow Postgres from Backend EC2"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [var.backend_sg_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


######################################
# DB Subnet Group
######################################
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "${var.db_identifier}-subnet-group"
  subnet_ids = var.subnet_ids
}

######################################
# RDS Instance
######################################
resource "aws_db_instance" "rds_instance" {
  identifier              = var.db_identifier
  allocated_storage       = var.allocated_storage
  engine                  = var.engine
  engine_version          = var.engine_version
  instance_class          = var.instance_class
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name
  publicly_accessible     = var.publicly_accessible
  skip_final_snapshot     = var.skip_final_snapshot
  vpc_security_group_ids = [aws_security_group.rds_security_group.id]
}
