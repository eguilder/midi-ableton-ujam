import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import re

# Create output directory
output_dir = "notes_v-guitarist"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of notes with their custom track names
notes_data = [
    # C0 - Silence
    {"file_note": "C0", "track_name": "Silence C0"},
    
    # C#0 through B1 - Phrases (sequential numbering)
    # C#0 to B0
    {"file_note": "C#0", "track_name": "Phrase 1 C#0"},
    {"file_note": "D0", "track_name": "Phrase 2 D0"},
    {"file_note": "D#0", "track_name": "Phrase 3 D#0"},
    {"file_note": "E0", "track_name": "Phrase 4 E0"},
    {"file_note": "F0", "track_name": "Phrase 5 F0"},
    {"file_note": "F#0", "track_name": "Phrase 6 F#0"},
    {"file_note": "G0", "track_name": "Phrase 7 G0"},
    {"file_note": "G#0", "track_name": "Phrase 8 G#0"},
    {"file_note": "A0", "track_name": "Phrase 9 A0"},
    {"file_note": "A#0", "track_name": "Phrase 10 A#0"},
    {"file_note": "B0", "track_name": "Phrase 11 B0"},
    
    # C1 to B1
    {"file_note": "C1", "track_name": "Phrase 12 C1"},
    {"file_note": "C#1", "track_name": "Phrase 13 C#1"},
    {"file_note": "D1", "track_name": "Phrase 14 D1"},
    {"file_note": "D#1", "track_name": "Phrase 15 D#1"},
    {"file_note": "E1", "track_name": "Phrase 16 E1"},
    {"file_note": "F1", "track_name": "Phrase 17 F1"},
    {"file_note": "F#1", "track_name": "Phrase 18 F#1"},
    {"file_note": "G1", "track_name": "Phrase 19 G1"},
    {"file_note": "G#1", "track_name": "Phrase 20 G#1"},
    {"file_note": "A1", "track_name": "Phrase 21 A1"},
    {"file_note": "A#1", "track_name": "Phrase 22 A#1"},
    {"file_note": "B1", "track_name": "Phrase 23 B1"},
    
    # C2 through A#2 - Styles (sequential numbering)
    {"file_note": "C2", "track_name": "Style 1 C2"},
    {"file_note": "C#2", "track_name": "Style 2 C#2"},
    {"file_note": "D2", "track_name": "Style 3 D2"},
    {"file_note": "D#2", "track_name": "Style 4 D#2"},
    {"file_note": "E2", "track_name": "Style 5 E2"},
    {"file_note": "F2", "track_name": "Style 6 F2"},
    {"file_note": "F#2", "track_name": "Style 7 F#2"},
    {"file_note": "G2", "track_name": "Style 8 G2"},
    {"file_note": "G#2", "track_name": "Style 9 G#2"},
    {"file_note": "A2", "track_name": "Style 10 A2"},
    {"file_note": "A#2", "track_name": "Style 11 A#2"},
    
    # B2 - Stop
    {"file_note": "B2", "track_name": "Stop B2"}
]

print("=" * 70)
print("V-GUITARIST NOTE GENERATOR WITH TRACK-NAME FILENAMES")
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
    
    # Add note (4 bars at 120 BPM = 1920 ticks)
    track.append(Message('note_on', note=ableton_midi, velocity=64, time=0))
    track.append(Message('note_off', note=ableton_midi, velocity=64, time=1920))
    
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
print("1. Silence C0        - Silent/rest pattern (lowest pitch)")
print("2. Phrase 1 C#0      - First guitar phrase pattern")
print("3. Phrase 2 D0       - Second guitar phrase pattern")
print("4. Phrase 3 D#0      - Third guitar phrase pattern")
print("5. Phrase 4 E0       - Fourth guitar phrase pattern")
print("6. Phrase 5 F0       - Fifth guitar phrase pattern")
print("7. Phrase 6 F#0      - Sixth guitar phrase pattern")
print("8. Phrase 7 G0       - Seventh guitar phrase pattern")
print("9. Phrase 8 G#0      - Eighth guitar phrase pattern")
print("10. Phrase 9 A0      - Ninth guitar phrase pattern")
print("11. Phrase 10 A#0    - Tenth guitar phrase pattern")
print("12. Phrase 11 B0     - Eleventh guitar phrase pattern")
print("13. Phrase 12 C1     - Twelfth guitar phrase pattern")
print("14. Phrase 13 C#1    - Thirteenth guitar phrase pattern")
print("15. Phrase 14 D1     - Fourteenth guitar phrase pattern")
print("16. Phrase 15 D#1    - Fifteenth guitar phrase pattern")
print("17. Phrase 16 E1     - Sixteenth guitar phrase pattern")
print("18. Phrase 17 F1     - Seventeenth guitar phrase pattern")
print("19. Phrase 18 F#1    - Eighteenth guitar phrase pattern")
print("20. Phrase 19 G1     - Nineteenth guitar phrase pattern")
print("21. Phrase 20 G#1    - Twentieth guitar phrase pattern")
print("22. Phrase 21 A1     - Twenty-first guitar phrase pattern")
print("23. Phrase 22 A#1    - Twenty-second guitar phrase pattern")
print("24. Phrase 23 B1     - Twenty-third guitar phrase pattern")
print("25. Style 1 C2       - First guitar style pattern")
print("26. Style 2 C#2      - Second guitar style pattern")
print("27. Style 3 D2       - Third guitar style pattern")
print("28. Style 4 D#2      - Fourth guitar style pattern")
print("29. Style 5 E2       - Fifth guitar style pattern")
print("30. Style 6 F2       - Sixth guitar style pattern")
print("31. Style 7 F#2      - Seventh guitar style pattern")
print("32. Style 8 G2       - Eighth guitar style pattern")
print("33. Style 9 G#2      - Ninth guitar style pattern")
print("34. Style 10 A2      - Tenth guitar style pattern")
print("35. Style 11 A#2     - Eleventh guitar style pattern")
print("36. Stop B2          - Stop/break pattern (highest pitch)")
print()
print("IMPORT INTO ABLETON:")
print("1. Go to the 'notes_v-guitarist' folder")
print("2. Drag and drop MIDI files into Ableton")
print("3. Tracks will be named with phrase/style names (e.g., 'Phrase 1 C#0')")
print("4. Filenames match track names (with underscores instead of spaces)")
print("5. Files are numbered 01-36 by pitch for easy organization")
print()
print("NOTE RANGE DETAILS:")
print("• Range: C0 to B2 in Ableton notation")
print("• Corresponds to: C0 to B2 in standard notation (same)")
print("• Frequency range: 16.35 Hz to 123.47 Hz")
print("• Perfect range for guitar patterns and chord progressions")
print()
print("V-GUITARIST PATTERN ORGANIZATION:")
print("• Silence C0: Silent/rest pattern for pauses")
print("• Phrases 1-23: Progressive guitar phrase patterns (C#0-B1)")
print("• Styles 1-11: Different guitar playing style patterns (C2-A#2)")
print("• Stop B2: Stop/break pattern for dramatic pauses")
print("• Covers 3 full octaves of guitar-friendly range")
print("• Sequential numbering within each category (Phrases & Styles)")
print()
print("WORKFLOW SUGGESTIONS:")
print("1. Start with Silence or Phrase 1 for clean beginnings")
print("2. Use Phrases 1-11 for deep, atmospheric guitar textures")
print("3. Progress through Phrases 12-23 for standard rhythm guitar range")
print("4. Switch to Style patterns for different guitar techniques and moods")
print("5. End with Stop pattern for dramatic conclusions")
print("6. Combine phrase and style patterns for complex guitar arrangements")
print()
print("PRODUCTION TIPS:")
print("• Phrases 1-11 (C#0-B0): Use for deep ambient guitar pads and drones")
print("• Phrases 12-23 (C1-B1): Use for rhythm guitar, chords, and arpeggios")
print("• Styles 1-11 (C2-A#2): Use for lead guitar, solos, and melodic lines")
print("• Silence: Use for dramatic pauses and rhythmic spacing")
print("• Stop: Create hard breaks and dramatic pauses")
print("• Layer phrases and styles for rich, textured guitar arrangements")