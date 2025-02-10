# EKS IAM Role
resource "aws_iam_role" "eks_cluster_role" {
  count = var.activate_eks ? 1 : 0

  name = "eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

# Attach EKS Policy to Role
resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  count      = var.activate_eks ? 1 : 0
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role[0].name
}

# EKS Cluster
resource "aws_eks_cluster" "project_cluster" {
  count    = var.activate_eks ? 1 : 0
  name     = "project-cluster"
  role_arn = aws_iam_role.eks_cluster_role[0].arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

# Data Source: EKS Cluster Information
data "aws_eks_cluster" "cluster" {
  count = var.activate_eks ? 1 : 0
  name  = aws_eks_cluster.project_cluster[0].name
}

# Data Source: Authentication Token for EKS
data "aws_eks_cluster_auth" "cluster" {
  count = var.activate_eks ? 1 : 0
  name  = aws_eks_cluster.project_cluster[0].name
}

# IAM Role for Worker Nodes
resource "aws_iam_role" "eks_node_role" {
  count = var.activate_eks ? 1 : 0

  name = "eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach policies to the worker node IAM role
resource "aws_iam_role_policy_attachment" "eks_node_policy" {
  count      = var.activate_eks ? 1 : 0
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_role[0].name
}

# EKS Node Group (Scaling with replicas_count)
resource "aws_eks_node_group" "project_node_group" {
  count = var.activate_eks ? 1 : 0

  cluster_name    = aws_eks_cluster.project_cluster[0].name
  node_role_arn   = aws_iam_role.eks_node_role[0].arn
  subnet_ids      = var.subnet_ids
  instance_types  = ["t3.micro"]  # Adjust instance type as needed

  scaling_config {
    desired_size = var.replicas_count     # Set desired_size based on replicas_count
    min_size     = var.replicas_count     # Set min_size based on replicas_count
    max_size     = var.replicas_count * 2 # Allow auto-scaling up to double the number of replicas
  }

  tags = {
    Name = "eks-node-group"
  }

  lifecycle {
    create_before_destroy = true
  }
}
