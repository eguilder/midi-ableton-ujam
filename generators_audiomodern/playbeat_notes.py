import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import re

# Create output directory
output_dir = "notes_playbeat"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of notes with their custom track names (C1 through B1)
notes_data = [
    {"file_note": "C3",  "track_name": "Original C3"},

    {"file_note": "C#3", "track_name": "Remix 1 C#3"},
    {"file_note": "D3",  "track_name": "Remix 2 D3"},
    {"file_note": "D#3", "track_name": "Remix 3 D#3"},
    {"file_note": "E3",  "track_name": "Remix 4 E3"},
    {"file_note": "F3",  "track_name": "Remix 5 F3"},
    {"file_note": "F#3", "track_name": "Remix 6 F#3"},
    {"file_note": "G3",  "track_name": "Remix 7 G3"},
    {"file_note": "G#3", "track_name": "Remix 8 G#3"},
    {"file_note": "A3",  "track_name": "Remix 9 A3"},
    {"file_note": "A#3", "track_name": "Remix 10 A#3"},
    {"file_note": "B3",  "track_name": "Remix 11 B3"},

    {"file_note": "C4",  "track_name": "Remix 12 C4"},
    {"file_note": "C#4", "track_name": "Remix 13 C#4"},
    {"file_note": "D4",  "track_name": "Remix 14 D4"},
    {"file_note": "D#4", "track_name": "Remix 15 D#4"},
    {"file_note": "E4",  "track_name": "Remix 16 E4"},
    {"file_note": "F4",  "track_name": "Remix 17 F4"},
    {"file_note": "F#4", "track_name": "Remix 18 F#4"},
    {"file_note": "G4",  "track_name": "Remix 19 G4"},
    {"file_note": "G#4", "track_name": "Remix 20 G#4"},
    {"file_note": "A4",  "track_name": "Remix 21 A4"},
    {"file_note": "A#4", "track_name": "Remix 22 A#4"},
    {"file_note": "B4",  "track_name": "Remix 23 B4"},
]

print("=" * 80)
print("PLAYBEAT REMIX NOTE GENERATOR FOR ABLETON LIVE")
print("=" * 80)
print(f"Generating {len(notes_data)} notes in '{output_dir}' folder")
print("✓ Complete octave: C1 through B1 in Ableton notation")
print("✓ Files numbered sequentially from lowest to highest note")
print()

# Note mapping for Ableton
# In Ableton: C-2 = MIDI 0, C-1 = MIDI 12, C0 = MIDI 24, C1 = MIDI 36, etc.
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# First, calculate MIDI numbers for all notes and sort them
notes_with_midi = []
for note_info in notes_data:
    file_note = note_info["file_note"]
    track_name = note_info["track_name"]
    
    # Parse the note name and octave
    note_name = file_note[:-1]  # Remove last character (octave)
    octave = int(file_note[-1])  # Get octave number
    
    # Find the index of the note
    note_index = note_names.index(note_name)
    
    # Calculate MIDI number for Ableton
    # Formula: MIDI = (octave + 2) * 12 + note_index
    ableton_midi = (octave + 2) * 12 + note_index
    
    notes_with_midi.append({
        "file_note": file_note,
        "track_name": track_name,
        "midi": ableton_midi,
        "note_name": note_name,
        "octave": octave,
        "note_index": note_index
    })

# Sort by MIDI number (lowest to highest pitch) - already in order for full octave
notes_with_midi.sort(key=lambda x: x["midi"])

# Change to output directory
original_dir = os.getcwd()
os.chdir(output_dir)

# Generate each note with sequential numbering
for file_number, note_info in enumerate(notes_with_midi, start=1):
    file_note = note_info["file_note"]
    track_name = note_info["track_name"]
    ableton_midi = note_info["midi"]
    note_name = note_info["note_name"]
    octave = note_info["octave"]
    note_index = note_info["note_index"]
    
    # Calculate what this is in standard notation (for reference)
    standard_octave = (ableton_midi // 12) - 1  # Standard: C-1 = MIDI 0, C0 = MIDI 12
    standard_note_index = ableton_midi % 12
    standard_name = f"{note_names[standard_note_index]}{standard_octave}"
    
    # Calculate frequency
    frequency = 440.0 * (2.0 ** ((ableton_midi - 69) / 12.0))
    
    # Create MIDI file
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Set track name (this is what Ableton will display)
    track.append(MetaMessage('track_name', name=track_name, time=0))
    
    # Set tempo (120 BPM)
    tempo = mido.bpm2tempo(120)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    
    # Set time signature (4/4)
    track.append(MetaMessage('time_signature', numerator=4, denominator=4, 
                            clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    
    # Add note (8 bars at 120 BPM = 1920 ticks)
    bars = 16  # Change this to any number of bars
    note_duration = bars * 480  # 480 ticks per bar at 120 BPM

    track.append(Message('note_on', note=ableton_midi, velocity=64, time=0))
    track.append(Message('note_off', note=ableton_midi, velocity=64, time=note_duration))
    
    # Add end of track
    track.append(MetaMessage('end_of_track', time=0))
    
    # Save file with sequential number
    # Use track name for filename (as requested)
    safe_filename = track_name.replace(" ", "_").replace("x", "x")  # Keep x for multiplication
    filename = f"{file_number:02d} {safe_filename}.mid"
    mid.save(filename)
    
    print(f"✓ Created: {filename}")
    print(f"  Track name in Ableton: '{track_name}'")
    print(f"  Note: {file_note}")
    print(f"  MIDI note: {ableton_midi}")
    print(f"  Plays at: {standard_name} pitch (standard notation)")
    print(f"  Frequency: {frequency:.2f} Hz")
    print()

# Change back to original directory
os.chdir(original_dir)

print("=" * 80)
print(f"SUCCESS! Created {len(notes_data)} MIDI files.")
print()
print("FILES CREATED (sequentially numbered with function names):")
print("-" * 80)
print("Filename                   | Ableton Track Name | MIDI | Pitch      | Frequency")
print("-" * 80)

# Display in the order they were created (sorted by pitch)
for i, note_info in enumerate(notes_with_midi, start=1):
    file_note = note_info["file_note"]
    track_name = note_info["track_name"]
    ableton_midi = note_info["midi"]
    
    # Calculate standard pitch
    standard_octave = (ableton_midi // 12) - 1
    standard_note_index = ableton_midi % 12
    standard_name = f"{note_names[standard_note_index]}{standard_octave}"
    
    # Calculate frequency
    frequency = 440.0 * (2.0 ** ((ableton_midi - 69) / 12.0))
    
    # Create filename for display
    safe_filename = track_name.replace(" ", "_").replace("x", "x")
    display_filename = f"{i:02d} {safe_filename}.mid"
    
    print(f"{display_filename:25} | {track_name:18} | {ableton_midi:4} | {standard_name:10} | {frequency:6.2f} Hz")

