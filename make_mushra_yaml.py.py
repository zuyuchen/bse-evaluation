import os
import yaml

# List of all volunteer versions you have folders for
versions = ["V1", "V2", "V3", "V4", "V5", "V6", "V7"]

for v_num in versions:
    audio_folder = f"subjective_test_{v_num}_audio"

    # Check if folder exists to avoid errors
    if not os.path.exists(audio_folder):
        print(f"Skipping {v_num}: Folder {audio_folder} not found.")
        continue

    # 1. FIX FILE EXTENSIONS: Ensure we only pick up .wav files
    sample_ids = []
    for f in os.listdir(audio_folder):
        if f.startswith("clean_") and f.endswith(".wav"):
            s_id = f.replace("clean_", "").replace(".wav", "")
            sample_ids.append(s_id)

    sample_ids.sort(key=int)

    # 2. CONFIG SETUP
    config = {
        "testname": f"BSE Evaluation - Set {v_num}",
        "testId": f"BSE_Results_{v_num}",  # This creates /results/bse_results_v1/
        "submissionUrl": "service/write.php",
        "pages": [
            {
                "type": "instructions",
                "id": "intro",
                "content": "<h3>Binaural Speech Enhancement Test</h3><p>Please ensure you are using <b>stereo headphones</b>.</p>"
            },
            {
                "type": "generic",
                "id": "participant_info",
                "name": "Participant Details",
                "content": "Please enter your ID/Name provided by the researcher.",
                "questions": [
                    {"id": "p_name", "text": "Volunteer Name/ID:", "type": "text"}
                ]
            }
        ]
    }

    # 3. ADD TRIALS
    for s_id in sample_ids:
        trial = {
            "type": "mushra",
            "id": f"sample_{s_id}",
            "name": f"Trial {s_id}",
            "reference": f"{audio_folder}/clean_{s_id}.wav",
            "stimuli": {
                "Condition_A": f"{audio_folder}/enhanced_finetuned_A_{s_id}.wav",
                "Condition_B": f"{audio_folder}/enhanced_finetuned_B_{s_id}.wav",
                "Condition_C": f"{audio_folder}/enhanced_finetuned_C_{s_id}.wav",
                "Baseline": f"{audio_folder}/enhanced_baseline_{s_id}.wav",
                "Noisy_Anchor": f"{audio_folder}/noisy_{s_id}.wav",
                "Hidden_Ref": f"{audio_folder}/clean_{s_id}.wav"
            }
        }
        config["pages"].append(trial)

    config["pages"].append({"type": "finish", "id": "end", "content": "All done! Click submit."})

    # 4. SAVE EACH CONFIG
    with open(f"configs/{v_num}.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)

print(f"Successfully generated {len(versions)} configuration files in /configs/")