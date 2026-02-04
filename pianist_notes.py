import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import re

# Create output directory
output_dir = "notes_pianist"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of notes with their custom track names
notes_data = [
    {"file_note": "C1", "track_name": "Phrase 1 C1"},
    {"file_note": "C#1", "track_name": "Low Chord C#1"},
    {"file_note": "D1", "track_name": "Phrase 2 D1"},
    {"file_note": "D#1", "track_name": "High Chord D#1"},
    {"file_note": "E1", "track_name": "Phrase 3 E1"},
    {"file_note": "F1", "track_name": "Phrase 4 F1"},
    {"file_note": "F#1", "track_name": "Fill 1 F#1"},
    {"file_note": "G1", "track_name": "Phrase 5 G1"},
    {"file_note": "G#1", "track_name": "Fill 2 G#1"},
    {"file_note": "A1", "track_name": "Phrase 6 A1"},
    {"file_note": "A#1", "track_name": "Fill 3 for A#1"},
    {"file_note": "B1", "track_name": "Phrase 7 B1"}
]

print("=" * 70)
print("PIANIST NOTE GENERATOR WITH TRACK-NAME FILENAMES")
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
print("1. Phrase 1 C1  - Primary phrase pattern (lowest pitch)")
print("2. Low Chord C#1 - Low chord progression")
print("3. Phrase 2 D1  - Secondary phrase pattern")
print("4. High Chord D#1 - High chord progression")
print("5. Phrase 3 E1  - Tertiary phrase pattern")
print("6. Phrase 4 F1  - Quaternary phrase pattern")
print("7. Fill 1 F#1   - First fill pattern")
print("8. Phrase 5 G1  - Fifth phrase pattern")
print("9. Fill 2 G#1   - Second fill pattern")
print("10. Phrase 6 A1  - Sixth phrase pattern")
print("11. Fill 3 for A#1 - Third fill pattern")
print("12. Phrase 7 B1  - Seventh phrase pattern (highest pitch)")
print()
print("IMPORT INTO ABLETON:")
print("1. Go to the 'notes_pianist' folder")
print("2. Drag and drop MIDI files into Ableton")
print("3. Tracks will be named with phrase/fill/chord names (e.g., 'Phrase 1 C1')")
print("4. Filenames match track names (with underscores instead of spaces)")
print("5. Files are numbered 01-12 by pitch for easy organization")
print()
print("NOTE RANGE DETAILS:")
print("• Range: C1 to B1 in Ableton notation")
print("• Corresponds to: C2 to B2 in standard notation")
print("• Frequency range: 65.41 Hz to 123.47 Hz")
print("• Perfect range for basslines and rhythmic patterns")
print()
print("PIANIST PATTERN ORGANIZATION:")
print("• Phrases 1-7: Progressive musical phrase patterns")
print("• Fills 1-3: Decorative fill patterns")
print("• Low/High Chords: Chord progressions at different octaves")
print("• Sequential numbering indicates natural pitch progression")
print("• Use patterns in order for evolving sequences")
print()
print("WORKFLOW SUGGESTIONS:")
print("1. Start with Phrase 1 for basic foundation")
print("2. Use Low/High Chords for harmonic progression")
print("3. Insert Fill patterns for transitions and decoration")
print("4. Progress through Phrases 2-7 for variation and development")
print("5. Combine phrases, chords, and fills to create dynamic arrangements")
print()
print("PRODUCTION TIPS:")
print("• Phrases 1-3: Use for verse sections and introductions")
print("• Fill patterns: Perfect for transitions between sections")
print("• Chords: Use for harmonic foundation and emotional impact")
print("• Phrases 4-7: Ideal for chorus, bridge, and climax sections")
print("• Combine elements for A/B/C song structures with harmonic progression")