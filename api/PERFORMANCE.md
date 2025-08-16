# API Performance and Scalability Guide

## Performance Optimizations

### 1. Database Optimizations

#### Connection Pooling
- **Pool Size**: 20 connections by default
- **Max Overflow**: 30 additional connections
- **Pool Timeout**: 30 seconds
- **Pool Recycle**: 3600 seconds (1 hour)

#### Query Optimizations
- Proper indexing on foreign keys
- Composite indexes for common filter combinations
- Query result caching for expensive operations

#### Recommended Indexes
```sql
-- Stock dimension indexes
CREATE INDEX idx_dim_stock_symbol ON stock_dw.dim_stock (nk_symbol);
CREATE INDEX idx_dim_stock_industry ON stock_dw.dim_stock (industry);

-- Date dimension indexes
CREATE INDEX idx_dim_date_full_date ON stock_dw.dim_date (nk_full_date);
CREATE INDEX idx_dim_date_year ON stock_dw.dim_date (year);

-- OHLCV fact table indexes
CREATE INDEX idx_fact_ohlcv_date_stock ON stock_dw.fact_ohlcv (date_key, stock_key);
CREATE INDEX idx_fact_ohlcv_stock_date ON stock_dw.fact_ohlcv (stock_key, date_key);
CREATE INDEX idx_fact_ohlcv_source ON stock_dw.fact_ohlcv (source_key);

-- Financial fact table indexes
CREATE INDEX idx_fact_balance_sheet_stock_date ON stock_dw.fact_balance_sheet (stock_key, date_key);
CREATE INDEX idx_fact_income_stock_date ON stock_dw.fact_income (stock_key, date_key);
CREATE INDEX idx_fact_cashflow_stock_date ON stock_dw.fact_cashflow (stock_key, date_key);
```

### 2. Caching Strategy

#### Redis Configuration
- **Cache TTL**: Configurable per data type
- **Stock Data**: 5 minutes TTL
- **Financial Data**: 1 hour TTL
- **Reference Data**: 24 hours TTL

#### Cache Patterns
- **Cache-Aside**: Manual cache management
- **Write-Through**: Update cache on write
- **Cache Invalidation**: Pattern-based invalidation

#### Cache Keys Strategy
```
stock:basic:{symbol}
stock:summary:{symbol}
ohlcv:latest:{symbol}
ohlcv:summary:{symbol}:{days}
industries:list
```

### 3. API Performance Features

#### Rate Limiting
- **Default**: 100 requests per minute per IP
- **Burst**: 20 requests allowed in burst
- **Headers**: Rate limit info in response headers

#### Pagination
- **Cursor-based**: For consistent results
- **Page-based**: For simple navigation
- **Default Size**: 50 items
- **Maximum Size**: 1000 items

#### Response Compression
- **Gzip**: Enabled for all responses
- **Types**: JSON, text, CSS, JavaScript

## Scalability Architecture

### 1. Horizontal Scaling

#### Load Balancing
```nginx
upstream api_backend {
    least_conn;
    server api1:8000 weight=3;
    server api2:8000 weight=3;
    server api3:8000 weight=2;
}
```

#### Database Scaling
- **Read Replicas**: For read-heavy workloads
- **Connection Pooling**: PgBouncer for connection management
- **Partitioning**: Time-based partitioning for fact tables

#### Cache Scaling
- **Redis Cluster**: For high availability
- **Sentinel**: For automatic failover
- **Replication**: Master-slave setup

### 2. Microservices Architecture

#### Service Decomposition
```
api-gateway/
├── stock-service/       # Stock management
├── ohlcv-service/       # Price data
├── financial-service/   # Financial statements
├── analytics-service/   # Calculations & ratios
└── notification-service/ # Alerts & updates
```

#### Inter-Service Communication
- **Async**: Message queues (RabbitMQ/Kafka)
- **Sync**: HTTP/gRPC for real-time needs
- **Event-Driven**: Domain events for loose coupling

### 3. Data Pipeline Scaling

#### Stream Processing
```python
# Apache Kafka integration
from kafka import KafkaConsumer, KafkaProducer

# Real-time data ingestion
def process_stock_updates():
    consumer = KafkaConsumer('stock-updates')
    for message in consumer:
        process_stock_data(message.value)
```

#### Batch Processing
```python
# Apache Airflow DAGs
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Daily data processing pipeline
dag = DAG('stock_data_pipeline', schedule_interval='@daily')
```

## Production Deployment

### 1. Container Orchestration

#### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stock-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: stock-api
  template:
    metadata:
      labels:
        app: stock-api
    spec:
      containers:
      - name: api
        image: stock-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

#### Service and Ingress
```yaml
apiVersion: v1
kind: Service
metadata:
  name: stock-api-service
spec:
  selector:
    app: stock-api
  ports:
  - port: 80
    targetPort: 8000
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: stock-api-ingress
spec:
  rules:
  - host: api.stockdata.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: stock-api-service
            port:
              number: 80
```

### 2. Infrastructure as Code

#### Terraform Configuration
```hcl
# EKS Cluster
resource "aws_eks_cluster" "stock_api_cluster" {
  name     = "stock-api"
  role_arn = aws_iam_role.eks_cluster_role.arn
  
  vpc_config {
    subnet_ids = aws_subnet.cluster_subnets[*].id
  }
}

# RDS Database
resource "aws_db_instance" "stock_db" {
  identifier = "stock-database"
  engine     = "postgres"
  engine_version = "15.4"
  instance_class = "db.r5.xlarge"
  allocated_storage = 1000
  storage_encrypted = true
  
  db_name  = "indian_sm_dw"
  username = var.db_username
  password = var.db_password
  
  backup_retention_period = 7
  backup_window = "03:00-04:00"
  maintenance_window = "sun:04:00-sun:05:00"
}

# ElastiCache Redis
resource "aws_elasticache_replication_group" "stock_cache" {
  replication_group_id = "stock-cache"
  description = "Redis cluster for stock API"
  
  node_type = "cache.r5.large"
  port = 6379
  parameter_group_name = "default.redis7"
  
  num_cache_clusters = 3
  automatic_failover_enabled = true
  multi_az_enabled = true
}
```

## Monitoring and Observability

### 1. Metrics Collection

#### Prometheus Metrics
- **Request Metrics**: Count, duration, errors
- **Database Metrics**: Connection pool, query time
- **Cache Metrics**: Hit/miss ratio, memory usage
- **System Metrics**: CPU, memory, disk usage

#### Custom Metrics
```python
from prometheus_client import Counter, Histogram, Gauge

# Custom business metrics
api_requests_total = Counter('api_requests_total', 'Total API requests', ['endpoint', 'method'])
query_duration = Histogram('db_query_duration_seconds', 'Database query duration')
active_users = Gauge('active_users', 'Number of active users')
```

### 2. Logging Strategy

#### Structured Logging
```python
import structlog

logger = structlog.get_logger()

# Correlated logs
logger.info("User request", 
           user_id=user_id, 
           request_id=request_id,
           endpoint=endpoint,
           duration=duration)
```

#### Log Aggregation
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Fluentd**: Log collection and forwarding
- **Grafana**: Visualization and alerting

### 3. Distributed Tracing

#### Jaeger Integration
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
```

## Security Considerations

### 1. Authentication & Authorization

#### JWT Implementation
```python
# Enhanced JWT with refresh tokens
def create_token_pair(user_id: str):
    access_token = create_access_token(user_id, expires_delta=timedelta(minutes=15))
    refresh_token = create_refresh_token(user_id, expires_delta=timedelta(days=7))
    return {"access_token": access_token, "refresh_token": refresh_token}
```

#### API Key Management
```python
# API key with rate limiting tiers
class APIKey(BaseModel):
    key: str
    tier: str  # free, premium, enterprise
    rate_limit: int
    expires_at: datetime
```

### 2. Data Protection

#### Encryption
- **Data at Rest**: Database encryption (TDE)
- **Data in Transit**: TLS 1.3 for all connections
- **Sensitive Fields**: Application-level encryption

#### Data Masking
```python
# PII data masking
def mask_sensitive_data(data):
    if 'email' in data:
        data['email'] = mask_email(data['email'])
    if 'phone' in data:
        data['phone'] = mask_phone(data['phone'])
    return data
```

### 3. Network Security

#### WAF Rules
```nginx
# Rate limiting and DDoS protection
limit_req_zone $binary_remote_addr zone=api:10m rate=1r/s;
limit_req_status 429;

# Block malicious patterns
if ($request_uri ~* "(union|select|insert|delete|drop|create|update|exec)") {
    return 403;
}
```

## Cost Optimization

### 1. Resource Management

#### Auto-scaling
```yaml
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: stock-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: stock-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

#### Database Optimization
- **Connection Pooling**: Reduce connection overhead
- **Query Optimization**: Reduce compute costs
- **Storage Optimization**: Compression and archiving

### 2. Cloud Cost Management

#### Reserved Instances
- **RDS**: 1-3 year reservations for steady workloads
- **ElastiCache**: Reserved nodes for cache clusters
- **EC2**: Reserved instances for predictable usage

#### Spot Instances
```yaml
# Spot instances for batch processing
nodeSelector:
  kubernetes.io/instance-type: spot
tolerations:
- key: "spot"
  operator: "Equal"
  value: "true"
  effect: "NoSchedule"
```

This comprehensive API provides enterprise-grade features including high performance, scalability, security, and monitoring capabilities suitable for large-scale deployment in production environments.
