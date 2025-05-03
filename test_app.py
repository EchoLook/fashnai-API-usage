import unittest
from unittest.mock import patch, MagicMock
import os
import json
from PIL import Image
import io
import sys

# Add the current directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import encode_image_to_base64, try_on_clothes, gradio_try_on

class TestVirtualTryOn(unittest.TestCase):
    
    @patch('app.API_KEY', 'fake_api_key')
    def setUp(self):
        # Create a sample test image
        self.test_image = Image.new('RGB', (100, 100), color='red')
        self.test_image_path = 'test_image.jpg'
        self.test_image.save(self.test_image_path)
    
    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        
        # Clean up temporary files that might be created
        for file in ['temp_model.jpg', 'temp_garment.jpg']:
            if os.path.exists(file):
                os.remove(file)
    
    def test_encode_image_to_base64(self):
        """Test that images are properly encoded to base64."""
        encoded = encode_image_to_base64(self.test_image_path)
        self.assertTrue(encoded.startswith('data:image/jpeg;base64,'))
        self.assertTrue(len(encoded) > 30)  # Should be a reasonable length
    
    @patch('requests.post')
    @patch('requests.get')
    def test_try_on_clothes_success(self, mock_get, mock_post):
        """Test successful try-on workflow."""
        # Mock successful job submission
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {'id': 'test_job_id', 'error': None}
        mock_post.return_value = mock_post_response
        
        # Mock successful status check
        mock_get_response = MagicMock()
        mock_get_response.json.return_value = {
            'status': 'completed', 
            'output': ['https://example.com/result.jpg']
        }
        
        # Mock successful image download
        mock_get_content_response = MagicMock()
        mock_get_content_response.content = b'fake_image_data'
        
        # Set up the get method to return different responses for different calls
        mock_get.side_effect = [mock_get_response, mock_get_content_response]
        
        # Call the function
        result = try_on_clothes(self.test_image_path, self.test_image_path, wait=True)
        
        # Verify the result
        self.assertTrue(result.startswith('result_'))
        self.assertTrue(result.endswith('.jpg'))
        
        # Clean up the result file
        if os.path.exists(result):
            os.remove(result)
    
    @patch('requests.post')
    def test_try_on_clothes_api_error(self, mock_post):
        """Test handling of API errors."""
        # Mock API error
        mock_post.side_effect = Exception("API Error")
        
        # Call the function
        result = try_on_clothes(self.test_image_path, self.test_image_path)
        
        # Verify the result
        self.assertTrue(result.startswith('API request error:'))
    
    @patch('app.try_on_clothes')
    def test_gradio_try_on_success(self, mock_try_on):
        """Test the Gradio wrapper function with successful processing."""
        mock_try_on.return_value = 'result_12345.jpg'
        
        image, text = gradio_try_on(self.test_image, self.test_image, 'auto')
        
        self.assertEqual(image, 'result_12345.jpg')
        self.assertEqual(text, 'Processing completed successfully!')
    
    @patch('app.try_on_clothes')
    def test_gradio_try_on_error(self, mock_try_on):
        """Test the Gradio wrapper function with an error."""
        mock_try_on.return_value = 'Error: Something went wrong'
        
        image, text = gradio_try_on(self.test_image, self.test_image, 'auto')
        
        self.assertIsNone(image)
        self.assertEqual(text, 'Error: Something went wrong')

if __name__ == '__main__':
    unittest.main() 