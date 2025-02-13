# infrastructure/modules/django/main.tf

# Create the ECR repository for Django
resource "aws_ecr_repository" "django_api_repo" {
  name                 = "django-api-repo"
  image_tag_mutability = "MUTABLE"

  tags = {
    Name        = "django-api-repo"
    Environment = "development"
  }
}

# Kubernetes Deployment for Django API
resource "kubernetes_deployment" "django_api" {
  metadata {
    name = "django-api-deployment"
    labels = {
      app = "django-api"
    }
  }

  spec {
    replicas = var.replicas_count
    selector {
      match_labels = {
        app = "django-api"
      }
    }
    template {
      metadata {
        labels = {
          app = "django-api"
        }
      }
      spec {
        container {
          name  = "django-api"
          image = var.image_url
          port {
            container_port = 8000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "django_service" {
  metadata {
    name = "django-api-service"
  }
  spec {
    selector = {
      app = kubernetes_deployment.django_api.metadata[0].labels.app
    }
    port {
      port        = 80
      target_port = 8000
    }
    type = "LoadBalancer"
  }
}
