# Virtual Try-On Application

A Streamlit interface application to test the Fashn.ai API and perform virtual clothing try-ons.

## Features

- Upload an image of a person or take a photo with the webcam
- Upload an image of a clothing item or take a photo with the webcam
- Generate a virtual image showing how the garment would look on the person
- Real-time progress tracking during processing
- Download the generated results

## Setup Instructions

1. Clone this repository:
   ```
   git clone <repository-url>
   cd try-similars
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Fashn.ai API key:
   ```
   FASHN_API_KEY=your_api_key_here
   ```

   > You can get an API key by registering at [Fashn.ai](https://fashn.ai/).

4. Run the application:
   ```
   streamlit run app.py
   ```

5. Open the provided URL in your web browser (typically http://localhost:8501).

## Usage

1. Upload a photo of a person using the file selector or take a photo with your webcam.
2. Upload a photo of a clothing item using the file selector or take a photo with your webcam.
3. Select the appropriate clothing category from the dropdown menu (or leave it as "auto").
4. Click the "Generate Try-On" button.
5. Wait for the processing to complete (it may take up to 40 seconds).
6. View the resulting image showing the person wearing the selected garment.
7. Download the resulting image if desired.

## API Information

This application uses the Fashn.ai API, which has the following rate limits:
- `/run` - Up to 50 requests per 60 seconds
- `/status` - Up to 50 requests per 10 seconds

For more information about the API, see the [Fashn.ai API documentation](https://docs.fashn.ai/fashn-api/endpoints).

## Project Structure

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (you must create this file)
- `images/` - Directory for storing sample images and results
  - `samples/` - Sample images for testing
  - `results/` - Results generated by the API

## Troubleshooting

Refer to the [SETUP.md](SETUP.md) file for detailed setup instructions and troubleshooting tips.

## License

[MIT License](LICENSE)
