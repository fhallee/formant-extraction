import argparse
import numpy as np
import pandas as pd
import parselmouth
import textgrids

def extract_formants_from_file(audio_file_path, textgrid_file_path, phone, desired_formants, points):
    """
    Args:
        audio_file_path (str): Path to the audio file
        textgrid_file_path (str): Path to the TextGrid file
        phone (str): The phone label to extract formants for
        desired_formants (list): A list of integers specifying the formants to extract (e.g., [1, 2])
        points (list): A list of floats representing the time points (as proportions of the interval duration)
                       at which to extract formant values (e.g., [0.2, 0.5, 0.8])

    Returns:
        df: A pandas DataFrame with "speaker", "phone", "point", "interval_start", "interval_end", "formant", and "formant_value" as columns
    """    
    sound = parselmouth.Sound(audio_file_path)
    grid = textgrids.TextGrid(textgrid_file_path)
    formants = sound.to_formant_burg(maximum_formant=5000)

    formant_list = []

    # add argument validation - if desired_formants has anything other than 1-4 or points isnt within 0 and 1 then reject it
    for tier_name, tier in grid.items():
        if "phones" in tier_name:
            speaker_name = tier_name.replace("- phones", "").strip()
            for interval in tier:
                if interval.text == phone:
                    for formant in desired_formants:
                        for point in points:
                            formant_dict = {
                                "speaker": speaker_name,
                                "phone": phone,
                                "point": point,
                                "interval_start": interval.xmin,
                                "interval_end": interval.xmax
                            }
                            formant_index = formant
                            formant_value = formants.get_value_at_time(formant_index, (interval.xmax - interval.xmin)*point)
                            if np.isnan(formant_value):
                                continue
                            formant_dict[f"F{formant}"] = formant_value
                            formant_list.append(formant_dict)

    return pd.DataFrame(formant_list)


    # iterate through tiers of the grid (the keys in a TextGrid dict) and pick out any that have "phones". speaker name is gonna be the name of the tier minus "- phones. be sure to include this in the documentation. note in in the readme.md for now"

def main():
    parser = argparse.ArgumentParser(description="Extracts formants from audio files")
    parser.add_argument(
        "--audio_path",
        type=str,
        required=True,
        help="Path to directory containing audio files"
    )
    parser.add_argument(
        "--textgrids_path",
        type=str,
        required=True,
        help="Path to directory containing Textgrid files"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path and file name for output data"
    )
    parser.add_argument(
        "--phone",
        type=str,
        required=True,
        help="Phone for analysis"
    )
    parser.add_argument(
        "--formants",
        type=str,
        nargs='+',
        choices=["f1", "f2", "f3", "f4"],
        required=True,
        help="Specify which formants to extract (e.g., f1 f2)"
    )
    parser.add_argument(
        "--points",
        type=float,
        nargs='+',
        required=True,
        help="Specify the measurement points as percentages (e.g., 0.2 0.5). Up to 3 points allowed."
    )

    args = parser.parse_args()

    if len(args.points) > 3:
        parser.error("You can specify up to 3 measurement points only.")

if __name__ == "__main__":
    main()