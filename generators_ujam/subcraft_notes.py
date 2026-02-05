import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import re

# Create output directory
output_dir = "notes_subcraft"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of notes with their custom track names
notes_data = [
    {"file_note": "C2", "track_name": "Loop 1 C2"},
    {"file_note": "C#2", "track_name": "Loop 2 C#2"},
    {"file_note": "D2", "track_name": "Loop 3 D2"},
    {"file_note": "D#2", "track_name": "Stop D#2"},
    {"file_note": "E2", "track_name": "Loop 4 E2"}
]

print("=" * 70)
print("SUBCRAFT NOTE GENERATOR WITH TRACK-NAME FILENAMES")
print("=" * 70)
print(f"Generating {len(notes_data)} notes in '{output_dir}' folder")
print("✓ Filenames match Ableton MIDI clip names")
print("✓ Files numbered sequentially from lowest to highest note")
print("✓ Range: C2 through E2 in Ableton notation")
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

# Sort by MIDI number (lowest to highest pitch)
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
    
    # Add note (8 bars at 120 BPM = 3840 ticks)
    bars = 8  # Change this to any number of bars
    note_duration = bars * 480  # 480 ticks per bar at 120 BPM

    track.append(Message('note_on', note=ableton_midi, velocity=64, time=0))
    track.append(Message('note_off', note=ableton_midi, velocity=64, time=note_duration))

    track.append(Message('note_on', note=ableton_midi, velocity=64, time=0))
    track.append(Message('note_off', note=ableton_midi, velocity=64, time=note_duration))
    
    # Add end of track
    track.append(MetaMessage('end_of_track', time=0))
    
    # Save file with sequential number and track name (matching Ableton clip name)
    safe_filename = track_name.replace(" ", "_")  # Replace spaces with underscores
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

print()
print("SEQUENTIAL ORDER (by pitch, low to high):")
print("1. Loop 1 C2  - Primary loop pattern (lowest pitch)")
print("2. Loop 2 C#2 - Secondary loop pattern")
print("3. Loop 3 D2  - Tertiary loop pattern")
print("4. Stop D#2   - Break/transition point")
print("5. Loop 4 E2  - Quaternary loop pattern (highest pitch)")
print()
print("IMPORT INTO ABLETON:")
print("1. Go to the 'notes_subcraft' folder")
print("2. Drag and drop MIDI files into Ableton")
print("3. Tracks will be named with loop/stop names (e.g., 'Loop 1 C2')")
print("4. Filenames match track names (with underscores instead of spaces)")
print("5. Files are numbered 01-05 by pitch for easy organization")
print()
print("NOTE RANGE DETAILS:")
print("• Range: C2 to E2 in Ableton notation")
print("• Corresponds to: C3 to E3 in standard notation")
print("• Frequency range: 130.81 Hz to 164.81 Hz")
print("• Perfect range for basslines and rhythmic patterns")
print()
print("SUBCRAFT PATTERN ORGANIZATION:")
print("• Loops 1-4: Progressive loop patterns")
print("• Stop: Designated break or transition point")
print("• Sequential numbering indicates natural pitch progression")
print("• Use patterns in order for evolving sequences")
print()
print("WORKFLOW SUGGESTIONS:")
print("1. Start with Loop 1 for basic foundation")
print("2. Progress through Loops 2-3 for variation")
print("3. Use Stop for dramatic breaks or transitions")
print("4. Finish with Loop 4 for climax sections")
print("5. Combine loops to create dynamic arrangements")
print()
print("PRODUCTION TIPS:")
print("• Loop 1-3: Use for verse sections")
print("• Stop D#2: Perfect for pre-chorus builds")
print("• Loop 4: Ideal for chorus or drop sections")
print("• Combine loops for A/B/C song structures")