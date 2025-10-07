# infrastructure/main.tf
provider "aws" {
  region = "us-east-1"
}

# Insecure: public S3 bucket (ACL public-read)
resource "aws_s3_bucket" "public_bucket" {
  bucket = "demo-insecure-public-bucket-12345"
  acl    = "public-read"

  versioning {
    enabled = false
  }
}

# Insecure: RDS security group allowing 0.0.0.0/0 on MySQL port (demonstration)
resource "aws_security_group" "open_db_sg" {
  name        = "open-db-sg"
  description = "allows mysql from anywhere (demo insecure)"
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
