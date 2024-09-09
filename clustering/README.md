# ConceptX Agglomerative Clustering Module

This module is part of the `ConceptX` project and implements agglomerative clustering for unsupervised clustering of high-dimensional data. The module includes standalone functions and a class-based pipeline for more structured usage. It leverages `scikit-learn` and `scipy` for clustering and provides visualization tools like dendrograms and PCA plots.

## Usage

You can use either the standalone functions for simple clustering tasks or the class-based pipeline for structured execution.

### Standalone Function Usage:
To perform agglomerative clustering and generate the linkage matrix:
   ```python
   import numpy as np
   from ConceptX.clustering.agglomerative import perform_agglomerative_clustering, create_linkage_matrix

   points = np.random.rand(100, 5)
   clustering = perform_agglomerative_clustering(points, 5)
   linkage_matrix = create_linkage_matrix(points, './output', 5)
   ```

### Class-Based Pipeline Usage:
To use the pipeline for clustering and visualization:
   ```python
   from ConceptX.clustering.agglomerative import AgglomerativeClusteringPipeline

   pipeline = AgglomerativeClusteringPipeline(output_path='./output', cluster=5)
   pipeline.run_pipeline()
   ```

This will generate synthetic data, perform clustering, create linkage matrices, and plot both the dendrogram and PCA cluster visualization.

## Development

For development, ensure you have `Poetry` installed. After cloning the repository, install the dependencies and make changes as necessary.

### Running the Pipeline:
   ```python
   from ConceptX.clustering.agglomerative import AgglomerativeClusteringPipeline

   pipeline = AgglomerativeClusteringPipeline(output_path='./output', cluster=5)
   pipeline.run_pipeline()
   ```

### Running Tests:
Unit tests are available for the standalone functions. Run tests using `pytest`.

   ```bash
   pytest
   ```

## Dependencies

- `dill`
- `numpy`
- `scikit-learn`
- `scipy`
- `matplotlib`
- `logging`
- `defaultdict`

All dependencies are managed by `Poetry`. For a complete list of packages, see the `pyproject.toml` or `requirements.txt`.

## Contributing

Contributions are welcome! Please fork the repository, submit a pull request with your changes, and update the `README.md` if you add or change functionality.
