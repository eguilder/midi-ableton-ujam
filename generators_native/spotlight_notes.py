import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import re

# Create output directory
output_dir = "notes_spotlight"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

notes_data = [
    # Patterns (C1–B1)
    {"file_note": "C1",  "track_name": "Pattern 1 C1"},
    {"file_note": "C#1", "track_name": "Pattern 2 C#1"},
    {"file_note": "D1",  "track_name": "Pattern 3 D1"},
    {"file_note": "D#1", "track_name": "Pattern 4 D#1"},
    {"file_note": "E1",  "track_name": "Pattern 5 E1"},
    {"file_note": "F1",  "track_name": "Pattern 6 F1"},
    {"file_note": "F#1", "track_name": "Pattern 7 F#1"},
    {"file_note": "G1",  "track_name": "Pattern 8 G1"},
    {"file_note": "G#1", "track_name": "Pattern 9 G#1"},
    {"file_note": "A1",  "track_name": "Pattern 10 A1"},
    {"file_note": "A#1", "track_name": "Pattern 11 A#1"},
    {"file_note": "B1",  "track_name": "Pattern 12 B1"},

    # Phrases (C2–B2)
    {"file_note": "C2",  "track_name": "Phrase 1 C2"},
    {"file_note": "C#2", "track_name": "Phrase 2 C#2"},
    {"file_note": "D2",  "track_name": "Phrase 3 D2"},
    {"file_note": "D#2", "track_name": "Phrase 4 D#2"},
    {"file_note": "E2",  "track_name": "Phrase 5 E2"},
    {"file_note": "F2",  "track_name": "Phrase 6 F2"},
    {"file_note": "F#2", "track_name": "Phrase 7 F#2"},
    {"file_note": "G2",  "track_name": "Phrase 8 G2"},
    {"file_note": "G#2", "track_name": "Phrase 9 G#2"},
    {"file_note": "A2",  "track_name": "Phrase 10 A2"},
    {"file_note": "A#2", "track_name": "Phrase 11 A#2"},
    {"file_note": "B2",  "track_name": "Phrase 12 B2"},
]


print("=" * 70)
print("SPOTLIGHT SERIES NOTE GENERATOR WITH TRACK-NAME FILENAMES")
print("=" * 70)
print(f"Generating {len(notes_data)} notes in '{output_dir}' folder")
print("✓ Filenames match Ableton MIDI clip names")
print("✓ Files numbered sequentially from lowest to highest note")
print("✓ Range: C-1 through B-1 in Ableton notation")
print()

# Ableton pitch class order
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# First, calculate MIDI numbers for all notes and sort them
notes_with_midi = []

for note_info in notes_data:
    file_note = note_info["file_note"]
    track_name = note_info["track_name"]

    # ✅ FIXED NOTE PARSING (handles negative octaves correctly)
    match = re.match(r"^([A-G]#?)(-?\d+)$", file_note)
    if not match:
        raise ValueError(f"Invalid note format: {file_note}")

    note_name, octave = match.groups()
    octave = int(octave)

    # Find pitch class index
    note_index = note_names.index(note_name)

    # Ableton MIDI formula: C-2 = 0
    ableton_midi = (octave + 2) * 12 + note_index

    notes_with_midi.append({
        "file_note": file_note,
        "track_name": track_name,
        "midi": ableton_midi,
        "note_name": note_name,
        "octave": octave,
        "note_index": note_index
    })

# Sort by MIDI pitch
notes_with_midi.sort(key=lambda x: x["midi"])

# Change to output directory
original_dir = os.getcwd()
os.chdir(output_dir)

# Generate MIDI files
for file_number, note_info in enumerate(notes_with_midi, start=1):
    file_note = note_info["file_note"]
    track_name = note_info["track_name"]
    ableton_midi = note_info["midi"]

    # Standard notation reference
    standard_octave = (ableton_midi // 12) - 1
    standard_note_index = ableton_midi % 12
    standard_name = f"{note_names[standard_note_index]}{standard_octave}"

    # Frequency
    frequency = 440.0 * (2.0 ** ((ableton_midi - 69) / 12.0))

    # Create MIDI file
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage('track_name', name=track_name, time=0))
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(120), time=0))
    track.append(MetaMessage(
        'time_signature',
        numerator=4,
        denominator=4,
        clocks_per_click=24,
        notated_32nd_notes_per_beat=8,
        time=0
    ))

    track.append(Message('note_on', note=ableton_midi, velocity=64, time=0))
    track.append(Message('note_off', note=ableton_midi, velocity=64, time=1920))
    track.append(MetaMessage('end_of_track', time=0))

    safe_filename = track_name.replace(" ", "_")
    filename = f"{file_number:02d} {safe_filename}.mid"
    mid.save(filename)

    print(f"✓ Created: {filename}")
    print(f"  Note: {file_note}")
    print(f"  MIDI: {ableton_midi}")
    print(f"  Pitch: {standard_name}")
    print(f"  Frequency: {frequency:.2f} Hz\n")

# Change back to original directory
os.chdir(original_dir)

print("=" * 70)
print(f"SUCCESS! Created {len(notes_data)} MIDI files.")
print()
print("FILES CREATED (sequentially numbered with track names):")
print("-" * 70)
print("Filename             | Ableton Track Name | MIDI | Pitch      | Frequency")
print("-" * 70)

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
    safe_filename = track_name.replace(" ", "_")
    display_filename = f"{i:02d} {safe_filename}.mid"
    
    print(f"{display_filename:20} | {track_name:18} | {ableton_midi:4} | {standard_name:10} | {frequency:6.2f} Hz")
