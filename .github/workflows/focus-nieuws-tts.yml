#!/usr/bin/env python3
"""
Process Nieuws Transcript Script
Downloads the newest MP3 from RSS feed and transcribes it using OpenAI Whisper.
"""

import subprocess
import urllib.request
import xml.etree.ElementTree as ET
import os
import sys


def download_rss_mp3(rss_url: str, output_file: str) -> bool:
    """Download the newest MP3 from RSS feed."""
    try:
        print(f"Fetching RSS feed: {rss_url}")
        
        # Download RSS feed
        with urllib.request.urlopen(rss_url) as response:
            rss_content = response.read()
        
        # Parse RSS and extract first item's enclosure URL
        root = ET.fromstring(rss_content)
        
        # Find the first item's enclosure
        for item in root.findall('.//item'):
            enclosure = item.find('enclosure')
            if enclosure is not None:
                audio_url = enclosure.get('url')
                if audio_url:
                    print(f"Nieuwste MP3 URL: {audio_url}")
                    
                    # Download the MP3
                    print(f"Downloading to {output_file}...")
                    urllib.request.urlretrieve(audio_url, output_file)
                    
                    # Check if file was downloaded
                    if os.path.getsize(output_file) > 0:
                        print(f"Successfully downloaded {output_file}")
                        return True
                    else:
                        print("Download mislukt: file is empty")
                        return False
        
        print("Geen MP3 URL gevonden in RSS feed")
        return False
        
    except Exception as e:
        print(f"Fout bij downloaden: {e}")
        return False


def transcribe_audio(audio_file: str, output_file: str) -> bool:
    """Transcribe audio file using Whisper."""
    try:
        print(f"Transcribing {audio_file} with Whisper Medium...")
        
        import whisper
        
        # Load model and transcribe
        model = whisper.load_model("medium")
        result = model.transcribe(audio_file)
        
        # Save transcript
        transcript_text = result.get("text", "").strip()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        
        print(f"Transcript saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Fout bij transcriberen: {e}")
        return False


def commit_to_git(file_to_commit: str, commit_message: str) -> bool:
    """Commit file to git repository."""
    try:
        # Configure git
        subprocess.run(
            ["git", "config", "--global", "user.name", "github-actions[bot]"],
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"],
            check=True,
            capture_output=True
        )
        
        # Add and commit
        subprocess.run(["git", "add", file_to_commit], check=True, capture_output=True)
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"Committed: {commit_message}")
            
            # Push
            subprocess.run(["git", "push"], check=True, capture_output=True)
            print("Pushed to repository")
            return True
        else:
            print("Niets om te committen (geen wijzigingen)")
            return True
            
    except Exception as e:
        print(f"Fout bij git operatie: {e}")
        return False


def main():
    """Main function."""
    rss_url = "https://www.omnycontent.com/d/playlist/8257a063-6be9-42fa-b892-acd4013b1255/84d4de9f-8ca2-40c5-8d33-b0ce00d6f186/e4c79cb6-51a3-4c08-9573-b0ce00d746db/podcast.rss"
    audio_file = "raw_nieuws.mp3"
    transcript_file = "nieuws.txt"
    
    print("=== Processing Nieuws Transcript ===\n")
    
    # Step 1: Download MP3
    if not download_rss_mp3(rss_url, audio_file):
        print("Failed to download MP3")
        sys.exit(1)
    
    # Step 2: Transcribe audio
    if not transcribe_audio(audio_file, transcript_file):
        print("Failed to transcribe audio")
        sys.exit(1)
    
    # Step 3: Commit to git
    if os.path.isfile(transcript_file):
        commit_to_git(transcript_file, "Update transcript nieuws")
        print("\n=== Process completed successfully ===")
    else:
        print(f"Error: {transcript_file} not found")
        sys.exit(1)


if __name__ == "__main__":
    main()
    
