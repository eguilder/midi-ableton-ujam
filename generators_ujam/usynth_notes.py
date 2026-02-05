import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import re

# Create output directory
output_dir = "notes_usynth"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of notes with their custom track names (C1 through B1)
notes_data = [
    {"file_note": "C1", "track_name": "Loop 1 C1"},
    {"file_note": "C#1", "track_name": "Mute C#1"},
    {"file_note": "D1", "track_name": "Loop 2 D1"},
    {"file_note": "D#1", "track_name": "Repeat D#1"},
    {"file_note": "E1", "track_name": "Loop 3 E1"},
    {"file_note": "F1", "track_name": "Loop 4 F1"},
    {"file_note": "F#1", "track_name": "Time x2 F#1"},
    {"file_note": "G1", "track_name": "Loop 5 G1"},
    {"file_note": "G#1", "track_name": "Time x3 G#1"},
    {"file_note": "A1", "track_name": "Loop 6 A1"},
    {"file_note": "A#1", "track_name": "Time x4 A#1"},
    {"file_note": "B1", "track_name": "Stop B1"}
]

print("=" * 80)
print("USYNTH NOTE GENERATOR FOR ABLETON LIVE")
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
    bars = 8  # Change this to any number of bars
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

print()
print("SEQUENTIAL ORDER & FUNCTIONS (by pitch, low to high):")
print("-" * 80)
print("01. C1   - Loop 1 (basic pattern)")
print("02. C#1  - Mute (silence/volume control)")
print("03. D1   - Loop 2 (secondary pattern)")
print("04. D#1  - Repeat (loop current pattern)")
print("05. E1   - Loop 3 (tertiary pattern)")
print("06. F1   - Loop 4 (quaternary pattern)")
print("07. F#1  - Time x2 (double tempo)")
print("08. G1   - Loop 5 (quinary pattern)")
print("09. G#1  - Time x3 (triple tempo)")
print("10. A1   - Loop 6 (senary pattern)")
print("11. A#1  - Time x4 (quadruple tempo)")
print("12. B1   - Stop (end sequence)")
print()
print("IMPORT INTO ABLETON:")
print("1. Go to the 'notes_usynth' folder")
print("2. Drag and drop MIDI files into Ableton")
print("3. Tracks will be named with function names (e.g., 'Loop 1 C1', 'Time x2 F#1')")
print("4. Files are numbered 01-12 by pitch for easy organization")
print("5. Filenames match track names (with underscores for spaces)")
print()
print("NOTE RANGE DETAILS:")
print("• Complete octave: C1 through B1 in Ableton notation")
print("• Corresponds to: C2 through B2 in standard notation")
print("• Frequency range: 65.41 Hz to 123.47 Hz")
print("• Ideal bass/sub-bass range for synth patterns")
print()
print("USYNTH FUNCTION MAPPING:")
print("• Loops 1-6: Different pattern variations")
print("• Mute: Silence or volume drop")
print("• Repeat: Loop current pattern")
print("• Time x2/x3/x4: Tempo multipliers (double, triple, quadruple time)")
print("• Stop: End sequence or pattern")
print()
print("APPLICATION IDEAS:")
print("• Create evolving synth sequences with tempo changes")
print("• Use for generative/algorithmic music patterns")
print("• Perfect for ambient, techno, or experimental music")
print("• Map to a MIDI controller for live performance")
print("• Use Mute for dynamic volume control")
print("• Use Time multipliers for rhythmic variations")
print()
print("PERFORMANCE TIPS:")
print("1. Start with Loop 1-3 for basic patterns")
print("2. Use Repeat to extend interesting patterns")
print("3. Apply Time multipliers for rhythmic complexity")
print("4. Use Mute for dynamic contrast")
print("5. End with Stop for clean transitions")