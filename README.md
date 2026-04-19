# Mangafire Downloader

Download manga from mangafire and save as pdf.

## Requirements

- Python 3.10+

## Setup

1. Download required folders

    ```sh
    pip install -r requirements.txt # using pip (default)
    uv sync # using uv
    ```

2. [Install camoufox by following their guide](https://camoufox.com/python/installation/#download-the-browser):

    ```sh
    python -m camoufox fetch
    ```

3. Run the script:

    ```sh
    python main.py "[url]" "[output_path]"
    ```

    Replace `[url]` with actual url, and `[output_path]` with an actual path.

## Contributions

This script works fine at the time it was published. If you find a better solution or want to update it, fork this repo, make a pull request with your changes. All contributions are welcome.

## License

This project is licensed under MIT License.