import numpy as np

def generate_synthetic_data(num_points=100, num_dims=5):
    """Generate synthetic data for testing."""
    # Generate random points with num_points rows and num_dims dimensions
    points = np.random.rand(num_points, num_dims)

    # Generate a simple vocabulary array
    vocab = np.array([f"word_{i}" for i in range(num_points)])

    return points, vocab

def save_synthetic_data(points, vocab, point_file='synthetic_points.npy', vocab_file='synthetic_vocab.npy'):
    """Save synthetic data to files."""
    np.save(point_file, points)
    np.save(vocab_file, vocab)
