import argparse
import os
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

    # TODO: add argument validation - if desired_formants has anything other than 1-4 or points isnt within 0 and 1 then reject it
    # TODO: add file name in formant_dict
    for tier_name, tier in grid.items():
        if "phones" in tier_name:
            speaker_name = tier_name.replace("- phones", "").strip()
            for i, interval in enumerate(tier):
                if interval.text == phone:
                    for formant_number in desired_formants:
                        for point in points:
                            formant_dict = {
                                "speaker": speaker_name,
                                "phone": phone,
                                "preceding_phone": tier[i-1].text if i > 0 else None,
                                "following_phone": tier[i+1].text if i < len(tier) - 1 else None,
                                "point": point,
                                "interval_start": interval.xmin,
                                "interval_end": interval.xmax
                            }
                            formant_value = formants.get_value_at_time(int(formant_number), (interval.xmax - interval.xmin)*point)
                            formant_dict[f"F{formant_number}"] = formant_value
                            formant_list.append(formant_dict)

    # TODO : add print statement that the file has been processed
    # TODO : return list and have it converted to DF in 
    return pd.DataFrame(formant_list)

# TODO: add "normalize" function w/ command line option

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
        type=int,
        nargs='+',
        choices=[1, 2, 3, 4],
        required=True,
        help="Specify which formants to extract (e.g., 1 2)"
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

    # TODO : add handling if one file doesnt match but the rest do
    audio_files = {os.path.splitext(f)[0]: os.path.join(args.audio_path, f) for f in os.listdir(args.audio_path) if f.endswith(".wav")}
    textgrid_files = {os.path.splitext(f)[0]: os.path.join(args.textgrids_path, f) for f in os.listdir(args.textgrids_path) if f.endswith(".TextGrid")}

    matched_files = set(audio_files.keys()) & set(textgrid_files.keys())
    if not matched_files:
        raise ValueError("No matching audio and TextGrid files found in the provided directories.")

    all_formant_data = []
    for file_name in matched_files:
        audio_file_path = audio_files[file_name]
        textgrid_file_path = textgrid_files[file_name]
        df = extract_formants_from_file(
            audio_file_path=audio_file_path,
            textgrid_file_path=textgrid_file_path,
            phone=args.phone,
            desired_formants=args.formants,
            points=args.points
        )
        all_formant_data.append(df)

    final_df = pd.concat(all_formant_data, ignore_index=True)

    final_df.to_csv(args.output, index=False)
    print(f"Formant data saved to {args.output}")

if __name__ == "__main__":
    main()