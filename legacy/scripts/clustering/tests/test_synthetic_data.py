# tests/test_synthetic_data.py
import unittest
import numpy as np
from ConceptX.synthetic_data import generate_synthetic_data, save_synthetic_data

class TestSyntheticData(unittest.TestCase):

    def test_generate_synthetic_data(self):
        points, vocab = generate_synthetic_data(num_points=100, num_dims=5, vocab_size=100)

        # Test shapes
        self.assertEqual(points.shape, (100, 5))
        self.assertEqual(len(vocab), 100)

        # Test vocab format
        self.assertTrue(all([word.startswith('word_') for word in vocab]))

    def test_save_synthetic_data(self):
        points, vocab = generate_synthetic_data(num_points=100, num_dims=5, vocab_size=100)
        save_synthetic_data(points, vocab, point_file='test_points.npy', vocab_file='test_vocab.npy')

        # Load and test saved data
        loaded_points = np.load('test_points.npy')
        loaded_vocab = np.load('test_vocab.npy')

        np.testing.assert_array_equal(points, loaded_points)
        np.testing.assert_array_equal(vocab, loaded_vocab)

if __name__ == '__main__':
    unittest.main()
