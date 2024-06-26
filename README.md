
# Python Chess Study Tools

A collection of scripts to download, prepare, analyze, and visualize chess games, specifically focusing on opening analysis.

## Step-by-Step Usage

### Step 1: download_games_full.py

Download full game data.

```sh
python download_games_full.py
```

### Step 2: prepare_chessdotcom_export.py

Prepare the downloaded games for analysis.

```sh
python prepare_chessdotcom_export.py
```

### Step 3: analyze_openings.py

Analyze the openings from the prepared data. Note: This step can take a long time. Use filters on the DataFrame to limit the scope of the analysis.

```sh
python analyze_openings.py
```

### Step 4: make_fen_images.py

Generate FEN images from the analyzed game data.

```sh
python make_fen_images.py
```

## Repository Structure

- `download_games_full.py`: Script to download game data.
- `prepare_chessdotcom_export.py`: Script to prepare game data for analysis.
- `analyze_openings.py`: Script to analyze chess openings.
- `make_fen_images.py`: Script to create FEN images from game data.

## Requirements

Ensure you have the required Python packages installed. You can install them using:

```sh
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
