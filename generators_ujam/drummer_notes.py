import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import re

# Create output directory
output_dir = "notes_drummer"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of notes with their custom track names
notes_data = [
    {"file_note": "C3", "track_name": "Verse 1 C3"},
    {"file_note": "C#3", "track_name": "Intro 1 C#3"},
    {"file_note": "D3", "track_name": "Verse 2 D3"},
    {"file_note": "D#3", "track_name": "Intro 2 D#3"},
    {"file_note": "E3", "track_name": "Verse 3 E3"},
    {"file_note": "F3", "track_name": "Verse 4 F3"},
    {"file_note": "F#3", "track_name": "Fill 1 F#3"},
    {"file_note": "G3", "track_name": "Verse 5 G3"},
    {"file_note": "G#3", "track_name": "Fill 2 G#3"},
    {"file_note": "A3", "track_name": "Chorus 1 A3"},
    {"file_note": "A#3", "track_name": "Fill 3 A#3"},
    {"file_note": "B3", "track_name": "Chorus 2 B3"},
    {"file_note": "C4", "track_name": "Chorus 3 C4"},
    {"file_note": "C#4", "track_name": "Ending 1 C#4"},
    {"file_note": "D4", "track_name": "Chorus 4 D4"},
    {"file_note": "D#4", "track_name": "Ending 2 D#4"},
    {"file_note": "E4", "track_name": "Chorus 5 E4"},
    {"file_note": "F4", "track_name": "Special 1 F4"},
    {"file_note": "F#4", "track_name": "Breakdown 1 F#4"},
    {"file_note": "G4", "track_name": "Special 2 G4"},
    {"file_note": "G#4", "track_name": "Breakdown 2 G#4"},
    {"file_note": "A4", "track_name": "Special 3 A4"},
    {"file_note": "A#4", "track_name": "Breakdown 3 A#4"},
    {"file_note": "B4", "track_name": "Stop B4"}
]

print("=" * 70)
print("DRUMMER NOTE GENERATOR WITH TRACK-NAME FILENAMES")
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
print("1. Verse 1 C3     - First verse pattern (lowest pitch)")
print("2. Intro 1 C#3    - First introduction pattern")
print("3. Verse 2 D3     - Second verse pattern")
print("4. Intro 2 D#3    - Second introduction pattern")
print("5. Verse 3 E3     - Third verse pattern")
print("6. Verse 4 F3     - Fourth verse pattern")
print("7. Fill 1 F#3     - First drum fill pattern")
print("8. Verse 5 G3     - Fifth verse pattern")
print("9. Fill 2 G#3     - Second drum fill pattern")
print("10. Chorus 1 A3   - First chorus pattern")
print("11. Fill 3 A#3    - Third drum fill pattern")
print("12. Chorus 2 B3   - Second chorus pattern")
print("13. Chorus 3 C4   - Third chorus pattern")
print("14. Ending 1 C#4  - First ending pattern")
print("15. Chorus 4 D4   - Fourth chorus pattern")
print("16. Ending 2 D#4  - Second ending pattern")
print("17. Chorus 5 E4   - Fifth chorus pattern")
print("18. Special 1 F4  - First special pattern")
print("19. Breakdown 1 F#4 - First breakdown pattern")
print("20. Special 2 G4  - Second special pattern")
print("21. Breakdown 2 G#4 - Second breakdown pattern")
print("22. Special 3 A4  - Third special pattern")
print("23. Breakdown 3 A#4 - Third breakdown pattern")
print("24. Stop B4       - Stop/break pattern (highest pitch)")
print()
print("IMPORT INTO ABLETON:")
print("1. Go to the 'notes_drummer' folder")
print("2. Drag and drop MIDI files into Ableton")
print("3. Tracks will be named with verse/chorus/fill names (e.g., 'Verse 1 C3')")
print("4. Filenames match track names (with underscores instead of spaces)")
print("5. Files are numbered 01-24 by pitch for easy organization")
print()
print("NOTE RANGE DETAILS:")
print("• Range: C3 to B4 in Ableton notation")
print("• Corresponds to: C3 to B4 in standard notation (same)")
print("• Frequency range: 130.81 Hz to 493.88 Hz")
print("• Perfect range for drum patterns and rhythmic elements")
print()
print("DRUMMER PATTERN ORGANIZATION:")
print("• Verses 1-5: Verse drum patterns for main sections")
print("• Choruses 1-5: Chorus drum patterns for impactful sections")
print("• Intros 1-2: Introduction patterns for song openings")
print("• Fills 1-3: Drum fill patterns for transitions")
print("• Endings 1-2: Ending patterns for song conclusions")
print("• Specials 1-3: Special effect drum patterns")
print("• Breakdowns 1-3: Breakdown sections with stripped-down drums")
print("• Stop: Stop/break pattern for dramatic pauses")
print("• Sequential organization follows musical structure progression")
print()
print("WORKFLOW SUGGESTIONS:")
print("1. Start with Intro patterns for song openings")
print("2. Use Verse patterns for main song sections")
print("3. Insert Fill patterns between sections for smooth transitions")
print("4. Switch to Chorus patterns for impactful, energetic sections")
print("5. Use Breakdowns for dynamic contrast and tension building")
print("6. Apply Special patterns for unique musical moments")
print("7. End with Ending patterns for song conclusions")
print("8. Use Stop for dramatic pauses and breaks")
print()
print("PRODUCTION TIPS:")
print("• Intros & Verses: Use for song beginnings and main sections")
print("• Fills: Perfect for transitions between verse and chorus")
print("• Choruses: Use for most energetic and memorable sections")
print("• Breakdowns: Ideal for building tension before drops")
print("• Specials: Add unique character and variation")
print("• Endings: Create satisfying conclusions to songs")
print("• Combine patterns to build complete song arrangements")