# Formant extraction

A Python tool for extracting formant measurements from audio files using TextGrid alignments for sociolinguistic and phonetic analysis.

## Overview

This tool allows you to batch process audio files and extract formant values at specified time points within phone segments. It's particularly useful for sociophonetic research requiring formant analysis across multiple speakers or utterances.

## Features

- Extract multiple formants (F1-F4) from audio files
- Specify measurement points as percentages of phone duration
- Batch process multiple files
- Output results in CSV format for further analysis
- Track phonetic environment (preceding and following phones)

## Requirements

- Python 3.6+
- Pandas
- Parselmouth
- TextGrids

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/formant-extraction.git
   cd formant-extraction
   ```

2. Install required dependencies:
   ```
   pip install pandas praat-parselmouth praat-textgrids
   ```

## Usage

```
python formant_extractor.py --audio_path /path/to/audio/files --textgrids_path /path/to/textgrids --output output_file.csv --phone "æ" --formants 1 2 --points 0.3 0.5 0.7
```

### Arguments

- `--audio_path`: Directory containing WAV audio files
- `--textgrids_path`: Directory containing TextGrid files
- `--output`: Path and filename for the output CSV
- `--phone`: Phone label to extract formants for (e.g., "æ")
- `--formants`: List of formant numbers to extract (e.g., 1 2 for F1 and F2)
- `--points`: Measurement points as proportions of phone duration (e.g., 0.3 0.5 0.7)

### Output Format

The script generates a CSV file with the following columns:

- `speaker`: Speaker identifier (extracted from the TextGrid tier name)
- `phone`: Target phone
- `preceding_phone`: Phone preceding the target
- `following_phone`: Phone following the target
- `point`: Measurement point (as proportion of phone duration)
- `interval_start`: Start time of the phone interval (seconds)
- `interval_end`: End time of the phone interval (seconds)
- `F1`, `F2`, etc.: Formant values at the specified measurement point

## File Matching Logic

The script automatically matches audio files (.wav) with their corresponding TextGrid files (.TextGrid) based on filename. Files must have identical names (excluding extensions) for successful matching.

## TextGrid Structure

The script will only extract formants from tiers that contain "phones" in their name. Tiers without "phones" in their name will be ignored. The tier name must follow the format `speaker - phones`. Ensure your TextGrid files are structured accordingly for the script to work as intended.

## Creating TextGrids

If you only have audio files and transcripts, you can use the [Montreal Forced Aligner (MFA)](https://montreal-forced-aligner.readthedocs.io/en/latest/) to generate TextGrid files with phone-level alignments.

For a detailed guide on using the Montreal Forced Aligner, reference [Eleanor Chodroff's MFA Tutorial.](https://www.eleanorchodroff.com/tutorial/montreal-forced-aligner.html)
