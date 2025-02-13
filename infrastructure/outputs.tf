# infrastructure/outputs.tf

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "db_username" {
  value = aws_db_instance.postgres.username
}

output "db_password" {
  value = aws_db_instance.postgres.password
}

output "ecr_repository_url" {
  value = aws_ecr_repository.django_api_repo.repository_url
}