# infrastructure/modules/ecr/main.tf

# Create the ECR repository for Django
resource "aws_ecr_repository" "django_api_repo" {
  name                 = "django-api-repo"
  image_tag_mutability = "MUTABLE"

  tags = {
    Name        = "django-api-repo"
    Environment = "development"
  }
}

output "repository_url" {
  value       = aws_ecr_repository.django_api_repo.repository_url
  description = "URL of the ECR repository for Django API"
}