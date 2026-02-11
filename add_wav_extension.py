"""
Add .wav extension to audio files in subjective test folders
"""
import os
from pathlib import Path

def add_wav_extensions(audio_folder):
    """
    Add .wav extension to all files that don't have it but should be WAV files.
    
    Args:
        audio_folder: Path to the audio folder
    """
    audio_path = Path(audio_folder)
    
    if not audio_path.exists():
        print(f"❌ Folder not found: {audio_folder}")
        return
    
    # Find all files without .wav extension
    files_to_rename = []
    for file in audio_path.iterdir():
        if file.is_file() and not file.suffix == '.wav':
            files_to_rename.append(file)
    
    if not files_to_rename:
        print(f"✅ All files in {audio_folder} already have .wav extension")
        return
    
    print(f"\n📁 Processing folder: {audio_folder}")
    print(f"   Found {len(files_to_rename)} files without .wav extension")
    
    renamed_count = 0
    for file in files_to_rename:
        new_name = file.parent / f"{file.name}.wav"
        
        if new_name.exists():
            print(f"  ⚠️  Skipping {file.name} - {new_name.name} already exists")
            continue
        
        try:
            file.rename(new_name)
            renamed_count += 1
            print(f"  ✓ Renamed: {file.name} → {new_name.name}")
        except Exception as e:
            print(f"  ❌ Error renaming {file.name}: {e}")
    
    print(f"\n✅ Renamed {renamed_count} files")


def main():
    """Process all volunteer audio folders"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Add .wav extension to audio files in subjective test folders'
    )
    parser.add_argument(
        'folder',
        type=str,
        help='Path to the audio folder (e.g., subjective_test_V1_audio)'
    )
    
    args = parser.parse_args()
    
    add_wav_extensions(args.folder)


if __name__ == '__main__':
    main()
