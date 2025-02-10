# modules/django/main.tf

resource "kubernetes_deployment" "django_api" {
  metadata {
    name = "django-api-deployment"
    labels = {
      app = "django-api"
    }
  }

  spec {
    replicas = 2
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
          image = var.image_url  # Pass the ECR image URL via variables
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
