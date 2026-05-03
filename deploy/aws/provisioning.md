# AWS base provisioning (EC2 + RDS + ECR)

Este guia cria a base de infraestrutura para deploy com EC2 e Docker Compose.

## 1) Variaveis

```bash
export AWS_REGION=us-east-1
export APP_NAME=energy-solar
export VPC_ID=vpc-xxxxxxxx
export SUBNET_ID=subnet-xxxxxxxx
```

## 2) ECR

```bash
aws ecr create-repository \
  --repository-name ${APP_NAME} \
  --image-scanning-configuration scanOnPush=true \
  --region ${AWS_REGION}
```

## 3) Security groups

```bash
EC2_SG_ID=$(aws ec2 create-security-group \
  --group-name ${APP_NAME}-ec2-sg \
  --description "EC2 SG for ${APP_NAME}" \
  --vpc-id ${VPC_ID} \
  --query GroupId --output text --region ${AWS_REGION})

RDS_SG_ID=$(aws ec2 create-security-group \
  --group-name ${APP_NAME}-rds-sg \
  --description "RDS SG for ${APP_NAME}" \
  --vpc-id ${VPC_ID} \
  --query GroupId --output text --region ${AWS_REGION})
```

Regras de entrada EC2:

```bash
aws ec2 authorize-security-group-ingress --group-id ${EC2_SG_ID} --protocol tcp --port 22 --cidr x.x.x.x/32 --region ${AWS_REGION}
aws ec2 authorize-security-group-ingress --group-id ${EC2_SG_ID} --protocol tcp --port 80 --cidr 0.0.0.0/0 --region ${AWS_REGION}
aws ec2 authorize-security-group-ingress --group-id ${EC2_SG_ID} --protocol tcp --port 443 --cidr 0.0.0.0/0 --region ${AWS_REGION}
```

Liberar acesso ao RDS somente da EC2:

```bash
aws ec2 authorize-security-group-ingress \
  --group-id ${RDS_SG_ID} \
  --protocol tcp --port 5432 \
  --source-group ${EC2_SG_ID} \
  --region ${AWS_REGION}
```

## 4) RDS PostgreSQL

```bash
aws rds create-db-subnet-group \
  --db-subnet-group-name ${APP_NAME}-db-subnets \
  --db-subnet-group-description "Subnets for ${APP_NAME}" \
  --subnet-ids ${SUBNET_ID} \
  --region ${AWS_REGION}

aws rds create-db-instance \
  --db-instance-identifier ${APP_NAME}-db \
  --db-instance-class db.t4g.micro \
  --engine postgres \
  --engine-version 16.3 \
  --master-username energy_user \
  --master-user-password 'CHANGE_ME_STRONG_PASSWORD' \
  --allocated-storage 20 \
  --backup-retention-period 7 \
  --no-publicly-accessible \
  --vpc-security-group-ids ${RDS_SG_ID} \
  --db-subnet-group-name ${APP_NAME}-db-subnets \
  --region ${AWS_REGION}
```

## 5) EC2

```bash
aws ec2 run-instances \
  --image-id ami-xxxxxxxx \
  --instance-type t3.small \
  --key-name your-keypair \
  --security-group-ids ${EC2_SG_ID} \
  --subnet-id ${SUBNET_ID} \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=${APP_NAME}-web}]" \
  --region ${AWS_REGION}
```

Depois de subir a EC2:

1. Copie e execute `deploy/aws/ec2-bootstrap.sh`.
2. Configure `.env.prod` no servidor.
3. Configure Nginx/TLS e pipeline de deploy.
