# Client Profitability Genome System

The Client Profitability Genome system creates a 50-dimensional vector representation for each client, enabling advanced AI/ML analysis for profitability optimization, churn prediction, and smart recommendations.

## Overview

The genome system transforms client data into a standardized 50-dimensional vector that captures key aspects of client profitability across five major categories:

1. **Financial Health** (Dimensions 0-9)
2. **Operational Efficiency** (Dimensions 10-19)
3. **Engagement Level** (Dimensions 20-29)
4. **Growth Potential** (Dimensions 30-39)
5. **Risk Factors** (Dimensions 40-49)

## Genome Structure

### Financial Health Dimensions (0-9)
- **0**: Revenue Stability
- **1**: Profit Margin Trend
- **2**: Billing Efficiency
- **3**: Payment Behavior
- **4**: Cost Optimization
- **5**: Financial Growth
- **6**: Contract Value Stability
- **7**: Revenue Diversification
- **8**: Financial Predictability
- **9**: Cash Flow Health

### Operational Efficiency Dimensions (10-19)
- **10**: SLA Compliance
- **11**: Resolution Time
- **12**: Technician Productivity
- **13**: Service Quality
- **14**: Resource Utilization
- **15**: Operational Cost Efficiency
- **16**: Service Consistency
- **17**: Automation Adoption
- **18**: Process Optimization
- **19**: Operational Scalability

### Engagement Level Dimensions (20-29)
- **20**: Login Frequency
- **21**: Feature Usage Depth
- **22**: Support Interaction
- **23**: Communication Responsiveness
- **24**: Feedback Participation
- **25**: Training Adoption
- **26**: Portal Engagement
- **27**: Community Participation
- **28**: Advocacy Indicators
- **29**: Relationship Strength

### Growth Potential Dimensions (30-39)
- **30**: Expansion Opportunity
- **31**: Upsell Readiness
- **32**: Market Position
- **33**: Innovation Adoption
- **34**: Partnership Potential
- **35**: Cross-Selling Opportunities
- **36**: Revenue Growth Trajectory
- **37**: Service Utilization Trends
- **38**: Market Expansion
- **39**: Strategic Alignment

### Risk Factors Dimensions (40-49)
- **40**: Churn Probability
- **41**: Payment Delinquency Risk
- **42**: Contract Expiration Risk
- **43**: Service Quality Risk
- **44**: Competitive Threat
- **45**: Market Volatility Exposure
- **46**: Dependency Risk
- **47**: Compliance Risk
- **48**: Operational Risk
- **49**: Financial Stability Risk

## Core Components

### 1. Genome Creator
Creates 50-dimensional genome vectors from client feature data.

```python
from src.data.preprocessing.client_genome.genome_creator import GenomeCreator

# Create genome creator
creator = GenomeCreator()

# Create genome vector for a client
client_features = {
    'revenue_std': 1000,
    'revenue_mean': 10000,
    'profit_margin_trend': 0.05,
    # ... other features
}

genome_vector = creator.create_genome_vector(client_features)
print(f"Genome vector shape: {genome_vector.shape}")  # (50,)
```

### 2. Similarity Calculator
Calculates similarity between client genome vectors using multiple distance metrics.

```python
from src.data.preprocessing.client_genome.similarity_calculator import SimilarityCalculator

# Create similarity calculator
calculator = SimilarityCalculator()

# Calculate cosine similarity between two clients
similarity = calculator.calculate_cosine_similarity(genome1, genome2)
print(f"Cosine similarity: {similarity}")

# Find most similar clients
similar_clients = calculator.find_most_similar_clients(
    target_genome, client_genomes, top_k=5
)
```

### 3. Clustering Engine
Implements various clustering algorithms for client segmentation.

```python
from src.data.preprocessing.client_genome.clustering_engine import ClientClusteringEngine

# Create clustering engine
engine = ClientClusteringEngine()

# Perform K-means clustering
cluster_assignments = engine.perform_kmeans_clustering(
    client_genomes, n_clusters=5
)

# Perform DBSCAN clustering
cluster_assignments = engine.perform_dbscan_clustering(
    client_genomes, eps=0.5, min_samples=5
)
```

### 4. Comparison Tools
Provides tools for comparing and analyzing client genome vectors.

```python
from src.data.preprocessing.client_genome.comparison_tools import GenomeComparisonTools

# Create comparison tools
tools = GenomeComparisonTools()

# Compare two clients
comparison_result = tools.compare_two_genomes(genome1, genome2, "Client1", "Client2")

# Identify anomalies
anomalies = tools.identify_genome_anomalies(client_genomes)
```

### 5. Genome Orchestrator
Coordinates all components of the Client Profitability Genome system.

```python
from src.data.preprocessing.client_genome.genome_orchestrator import GenomeOrchestrator

# Create orchestrator
orchestrator = GenomeOrchestrator()

# Process client data through complete pipeline
client_genomes = orchestrator.process_client_data(clients_data)

# Analyze client similarity
similarity_analysis = orchestrator.analyze_client_similarity("client_1", "client_2")

# Cluster clients
cluster_assignments = orchestrator.cluster_clients(method="kmeans", n_clusters=5)
```

## Usage Examples

### Complete Genome Analysis Pipeline

```python
import pandas as pd
import numpy as np
from src.data.preprocessing.client_genome.genome_orchestrator import GenomeOrchestrator

# Create sample client data
client_data = pd.DataFrame({
    'client_id': ['client_1', 'client_2', 'client_3'],
    'revenue_std': [1000, 1500, 800],
    'revenue_mean': [10000, 12000, 8000],
    'profit_margin_trend': [0.05, 0.03, 0.07],
    # ... add all required features
})

# Create orchestrator and process data
orchestrator = GenomeOrchestrator()
client_genomes = orchestrator.process_client_data(client_data)

# Cluster clients
cluster_assignments = orchestrator.cluster_clients(method="kmeans", n_clusters=2)

# Find similar clients to client_1
similar_clients = orchestrator.find_similar_clients("client_1", top_k=2)

# Generate client profile
profile = orchestrator.generate_client_profile("client_1")
print(f"Client profile: {profile}")
```

## Integration with Feature Engineering

The genome system integrates with the existing feature engineering pipeline:

```python
# First, create features using the feature engineering system
from src.data.preprocessing.feature_engineering import FeatureEngineeringOrchestrator

# Then, use those features to create genome vectors
from src.data.preprocessing.client_genome.genome_creator import GenomeCreator

# Process data through feature engineering
fe_orchestrator = FeatureEngineeringOrchestrator()
processed_data = fe_orchestrator.process_data(raw_data)

# Create genome vectors from processed features
genome_creator = GenomeCreator()
client_genomes = genome_creator.create_genomes_for_clients(processed_data)
```

## API Reference

### GenomeCreator
- `create_genome_vector(client_features)`: Create a single genome vector
- `create_genomes_for_clients(clients_data)`: Create genome vectors for multiple clients
- `get_genome_history(client_id)`: Get historical genome data for a client

### SimilarityCalculator
- `calculate_cosine_similarity(genome1, genome2)`: Calculate cosine similarity
- `calculate_euclidean_distance(genome1, genome2)`: Calculate Euclidean distance
- `calculate_manhattan_distance(genome1, genome2)`: Calculate Manhattan distance
- `find_most_similar_clients(target_genome, client_genomes, top_k)`: Find most similar clients

### ClientClusteringEngine
- `perform_kmeans_clustering(client_genomes, n_clusters)`: K-means clustering
- `perform_dbscan_clustering(client_genomes, eps, min_samples)`: DBSCAN clustering
- `perform_hierarchical_clustering(client_genomes, n_clusters)`: Hierarchical clustering

### GenomeComparisonTools
- `compare_two_genomes(genome1, genome2, client1_id, client2_id)`: Compare two genomes
- `identify_genome_anomalies(client_genomes, threshold)`: Identify anomalous genomes

### GenomeOrchestrator
- `process_client_data(clients_data)`: Process client data through complete pipeline
- `analyze_client_similarity(client_id1, client_id2)`: Analyze similarity between clients
- `cluster_clients(method, **kwargs)`: Cluster all clients
- `find_similar_clients(target_client_id, top_k)`: Find similar clients

## Best Practices

1. **Data Quality**: Ensure high-quality input features for accurate genome vectors
2. **Normalization**: All genome dimensions are normalized to 0-1 range
3. **Regular Updates**: Update genome vectors as new client data becomes available
4. **Validation**: Validate genome results against known client characteristics
5. **Privacy**: Ensure client data privacy and compliance with regulations

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all required dependencies are installed
2. **Memory Issues**: For large datasets, process clients in batches
3. **Performance**: Use appropriate clustering algorithms for your data size

### Debugging Tips

1. Check that all required client features are provided
2. Verify that genome vectors have the expected shape (50 dimensions)
3. Ensure client IDs are consistent across all components