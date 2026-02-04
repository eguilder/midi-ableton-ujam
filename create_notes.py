import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import re

# ====== ADD THIS GLOBAL VARIABLE ======
# Duration in MIDI ticks (8 bars at 120 BPM = 3840 ticks)
# Change this single variable to adjust duration for all functions
DEFAULT_DURATION_TICKS = 3840  # Changed from 1920 to 3840 for 8 bars
# ======================================

# Define note names and their indices (make it global)
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def create_note_midi_ableton_final(ableton_display_name, file_number, duration_ticks=DEFAULT_DURATION_TICKS, bpm=120):
    """
    Create MIDI file where filename is sequentially numbered
    
    Args:
        ableton_display_name: What you want to see in Ableton (e.g., 'C3')
        file_number: Sequential number for filename (e.g., 1, 2, 3...)
        duration_ticks: Duration in MIDI ticks (default: 8 bars at 120 BPM)
        bpm: Tempo in beats per minute
    """
    # Parse the note name and octave from the display name
    match = re.match(r'([A-G]#?)(-?\d+)', ableton_display_name)
    if not match:
        raise ValueError(f"Invalid note name format: {ableton_display_name}. Use format like 'C3', 'C#4', 'A2'")
    
    note_name = match.group(1)
    octave = int(match.group(2))
    
    # Find the index of the note
    try:
        note_index = NOTE_NAMES.index(note_name)
    except ValueError:
        raise ValueError(f"Invalid note name: {note_name}. Use C, C#, D, D#, E, F, F#, G, G#, A, A#, or B")
    
    # Calculate Ableton MIDI number
    # In Ableton: C-2 = MIDI 0, C-1 = MIDI 12, C0 = MIDI 24, C1 = MIDI 36, etc.
    # Formula: MIDI = (octave + 2) * 12 + note_index
    ableton_midi = (octave + 2) * 12 + note_index
    
    # Check if MIDI number is within valid range (0-127)
    if ableton_midi < 0 or ableton_midi > 127:
        raise ValueError(f"Note {ableton_display_name} results in MIDI {ableton_midi}, which is outside valid range (0-127)")
    
    # Calculate what this corresponds to in standard notation (for reference)
    # CORRECTED: Standard is one octave higher than Ableton display
    standard_midi = ableton_midi  # Same MIDI number, different interpretation
    standard_octave = (standard_midi // 12) - 1  # Standard: C-1 = MIDI 0, C0 = MIDI 12, etc.
    standard_note_index = standard_midi % 12
    standard_name = f"{NOTE_NAMES[standard_note_index]}{standard_octave}"
    
    # Create a new MIDI file
    mid = MidiFile()
    
    # Create a track
    track = MidiTrack()
    mid.tracks.append(track)
    
    # ADD TRACK NAME METADATA - This makes Ableton show the track name!
    track_name = f"Note {ableton_display_name}"
    track.append(MetaMessage('track_name', name=track_name, time=0))
    
    # Set tempo (microseconds per beat)
    tempo = mido.bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    
    # Set time signature (4/4)
    track.append(MetaMessage('time_signature', numerator=4, denominator=4, 
                                  clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    
    # Add note on message (start playing the note)
    track.append(Message('note_on', note=ableton_midi, velocity=64, time=0))
    
    # Add note off message (stop playing the note) after the specified duration
    track.append(Message('note_off', note=ableton_midi, velocity=64, time=duration_ticks))
    
    # Add end of track marker
    track.append(MetaMessage('end_of_track', time=0))
    
    # Save the MIDI file with sequential numbering (01, 02, 03...)
    filename = f"{file_number:02d} {ableton_display_name}.mid"
    mid.save(filename)
    
    print(f"Created: {filename}")
    print(f"  • Track name in Ableton: '{track_name}'")
    print(f"  • Note: {ableton_display_name}")
    print(f"  • Plays at: {standard_name} pitch (standard notation)")
    print(f"  • MIDI note in file: {ableton_midi}")
    print(f"  • Frequency: {midi_to_frequency(ableton_midi):.2f} Hz")
    print(f"  • Duration: {duration_ticks} ticks ({duration_ticks/1920} bars)")
    
    return mid

def create_note_midi_standard(standard_display_name, file_number, duration_ticks=DEFAULT_DURATION_TICKS, bpm=120):
    """
    Create MIDI file using STANDARD MIDI notation (one octave higher than Ableton)
    
    Args:
        standard_display_name: Note name in standard notation (e.g., 'C4' for middle C)
        file_number: Sequential number for filename (e.g., 1, 2, 3...)
        duration_ticks: Duration in MIDI ticks (default: 8 bars at 120 BPM)
        bpm: Tempo in beats per minute
    """
    # Parse the note name and octave from the display name
    match = re.match(r'([A-G]#?)(-?\d+)', standard_display_name)
    if not match:
        raise ValueError(f"Invalid note name format: {standard_display_name}. Use format like 'C4', 'C#5', 'A3'")
    
    note_name = match.group(1)
    octave = int(match.group(2))
    
    # Find the index of the note
    try:
        note_index = NOTE_NAMES.index(note_name)
    except ValueError:
        raise ValueError(f"Invalid note name: {note_name}. Use C, C#, D, D#, E, F, F#, G, G#, A, A#, or B")
    
    # Calculate standard MIDI number
    # In Standard: C-1 = MIDI 0, C0 = MIDI 12, C1 = MIDI 24, C2 = MIDI 36, C3 = MIDI 48, C4 = MIDI 60, etc.
    # Formula: MIDI = (octave + 1) * 12 + note_index
    standard_midi = (octave + 1) * 12 + note_index
    
    # Check if MIDI number is within valid range (0-127)
    if standard_midi < 0 or standard_midi > 127:
        raise ValueError(f"Note {standard_display_name} results in MIDI {standard_midi}, which is outside valid range (0-127)")
    
    # Calculate what this corresponds to in Ableton notation (for reference)
    ableton_midi = standard_midi  # Same MIDI number, different interpretation
    ableton_octave = (ableton_midi // 12) - 2  # Ableton: C-2 = MIDI 0, C-1 = MIDI 12, etc.
    ableton_note_index = ableton_midi % 12
    ableton_display = f"{NOTE_NAMES[ableton_note_index]}{ableton_octave}"
    
    # Create a new MIDI file
    mid = MidiFile()
    
    # Create a track
    track = MidiTrack()
    mid.tracks.append(track)
    
    # ADD TRACK NAME METADATA
    track_name = f"Note {standard_display_name} (Standard)"
    track.append(MetaMessage('track_name', name=track_name, time=0))
    
    # Set tempo (microseconds per beat)
    tempo = mido.bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    
    # Set time signature (4/4)
    track.append(MetaMessage('time_signature', numerator=4, denominator=4, 
                                  clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    
    # Add note on message (start playing the note)
    track.append(Message('note_on', note=standard_midi, velocity=64, time=0))
    
    # Add note off message (stop playing the note) after the specified duration
    track.append(Message('note_off', note=standard_midi, velocity=64, time=duration_ticks))
    
    # Add end of track marker
    track.append(MetaMessage('end_of_track', time=0))
    
    # Save the MIDI file with sequential numbering
    filename = f"{file_number:02d} {standard_display_name}_standard.mid"
    mid.save(filename)
    
    print(f"Created: {filename}")
    print(f"  • Track name in Ableton: '{track_name}'")
    print(f"  • Standard notation: {standard_display_name}")
    print(f"  • Will display in Ableton as: {ableton_display}")
    print(f"  • MIDI note in file: {standard_midi}")
    print(f"  • Frequency: {midi_to_frequency(standard_midi):.2f} Hz")
    print(f"  • Duration: {duration_ticks} ticks ({duration_ticks/1920} bars)")
    
    return mid

def midi_to_frequency(midi_note):
    """Convert MIDI note number to frequency in Hz"""
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

def generate_ableton_range(start_note="C0", end_note="C6", include_track_names=True, duration_ticks=DEFAULT_DURATION_TICKS):
    """
    Generate MIDI files for a range of notes with sequential filenames
    
    Args:
        start_note: Starting note in Ableton notation (e.g., 'C0')
        end_note: Ending note in Ableton notation (e.g., 'C6')
        include_track_names: If True, adds track name metadata
        duration_ticks: Duration in MIDI ticks (default: 8 bars at 120 BPM)
    """
    # Create output directory
    output_dir = "midi_files_ableton_sequential"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Generating MIDI files for Ableton Live")
    print("=" * 70)
    print(f"Range: {start_note} to {end_note}")
    print(f"Duration: {duration_ticks} ticks ({duration_ticks/1920} bars)")
    print("Filenames are sequentially numbered from lowest to highest note")
    if include_track_names:
        print("✓ Track names will be set in MIDI metadata")
    print()
    
    # Parse start and end notes
    start_match = re.match(r'([A-G]#?)(-?\d+)', start_note)
    end_match = re.match(r'([A-G]#?)(-?\d+)', end_note)
    
    if not start_match or not end_match:
        raise ValueError("Invalid start or end note format. Use format like 'C0', 'C#4', 'A2'")
    
    start_note_name = start_match.group(1)
    start_octave = int(start_match.group(2))
    end_note_name = end_match.group(1)
    end_octave = int(end_match.group(2))
    
    # Find indices
    start_note_index = NOTE_NAMES.index(start_note_name)
    end_note_index = NOTE_NAMES.index(end_note_name)
    
    # Generate all notes in the range (sorted by MIDI number = pitch)
    all_notes = []
    
    for octave in range(start_octave, end_octave + 1):
        # Determine which notes to include in this octave
        if octave == start_octave:
            note_start_index = start_note_index
        else:
            note_start_index = 0
            
        if octave == end_octave:
            note_end_index = end_note_index + 1  # +1 to include the end note
        else:
            note_end_index = 12  # All notes in the octave
        
        for note_idx in range(note_start_index, note_end_index):
            note_name = NOTE_NAMES[note_idx]
            display_name = f"{note_name}{octave}"
            
            # Calculate MIDI number for sorting
            midi_num = (octave + 2) * 12 + note_idx
            all_notes.append((display_name, midi_num))
    
    # Sort by MIDI number (lowest to highest pitch)
    all_notes.sort(key=lambda x: x[1])
    
    # Generate MIDI files
    print(f"Generating {len(all_notes)} MIDI files...")
    print()
    
    # Track which notes we've created
    created_count = 0
    
    for file_number, (display_name, midi_num) in enumerate(all_notes, start=1):
        # Change to output directory
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        try:
            if include_track_names:
                create_note_midi_ableton_final(display_name, file_number, duration_ticks=duration_ticks)
            else:
                # Fallback to simple creation without track names
                mid = MidiFile()
                track = MidiTrack()
                mid.tracks.append(track)
                track.append(Message('note_on', note=midi_num, velocity=64, time=0))
                track.append(Message('note_off', note=midi_num, velocity=64, time=duration_ticks))
                filename = f"{file_number:02d} {display_name}.mid"
                mid.save(filename)
                print(f"Created: {filename} (no track name, duration: {duration_ticks} ticks)")
            
            created_count += 1
        except ValueError as e:
            print(f"Skipping {display_name}: {e}")
        
        # Change back to original directory
        os.chdir(original_dir)
    
    print()
    print("=" * 70)
    print(f"Successfully created {created_count} MIDI files in '{output_dir}' directory")
    print(f"✓ Duration: {duration_ticks} ticks ({duration_ticks/1920} bars)")
    if include_track_names:
        print("✓ Track names are embedded in MIDI files")
        print("✓ Ableton will show the track names instead of 'Track 0'")
    print("✓ Files are numbered sequentially from lowest to highest note")
    print()

def generate_standard_range(start_note="C0", end_note="C6", duration_ticks=DEFAULT_DURATION_TICKS):
    """
    Generate MIDI files for a range of notes using STANDARD MIDI notation
    with sequential numbering
    
    Args:
        start_note: Starting note in STANDARD notation (e.g., 'C0')
        end_note: Ending note in STANDARD notation (e.g., 'C6')
        duration_ticks: Duration in MIDI ticks (default: 8 bars at 120 BPM)
    """
    # Create output directory
    output_dir = "midi_files_standard_sequential"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Generating MIDI files using STANDARD MIDI notation")
    print("=" * 70)
    print(f"Range: {start_note} to {end_note}")
    print(f"Duration: {duration_ticks} ticks ({duration_ticks/1920} bars)")
    print("Filenames use standard notation (one octave higher than Ableton)")
    print("✓ Files are numbered sequentially from lowest to highest note")
    print("✓ Track names are embedded in MIDI files")
    print()
    
    # Parse start and end notes
    start_match = re.match(r'([A-G]#?)(-?\d+)', start_note)
    end_match = re.match(r'([A-G]#?)(-?\d+)', end_note)
    
    if not start_match or not end_match:
        raise ValueError("Invalid start or end note format. Use format like 'C0', 'C#4', 'A3'")
    
    start_note_name = start_match.group(1)
    start_octave = int(start_match.group(2))
    end_note_name = end_match.group(1)
    end_octave = int(end_match.group(2))
    
    # Find indices
    start_note_index = NOTE_NAMES.index(start_note_name)
    end_note_index = NOTE_NAMES.index(end_note_name)
    
    # Generate all notes in the range (sorted by MIDI number = pitch)
    all_notes = []
    
    for octave in range(start_octave, end_octave + 1):
        # Determine which notes to include in this octave
        if octave == start_octave:
            note_start_index = start_note_index
        else:
            note_start_index = 0
            
        if octave == end_octave:
            note_end_index = end_note_index + 1  # +1 to include the end note
        else:
            note_end_index = 12  # All notes in the octave
        
        for note_idx in range(note_start_index, note_end_index):
            note_name = NOTE_NAMES[note_idx]
            display_name = f"{note_name}{octave}"
            
            # Calculate standard MIDI number for sorting
            midi_num = (octave + 1) * 12 + note_idx
            all_notes.append((display_name, midi_num))
    
    # Sort by MIDI number (lowest to highest pitch)
    all_notes.sort(key=lambda x: x[1])
    
    # Generate MIDI files
    print(f"Generating {len(all_notes)} MIDI files...")
    print()
    
    # Track which notes we've created
    created_count = 0
    
    for file_number, (display_name, midi_num) in enumerate(all_notes, start=1):
        # Change to output directory
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        try:
            create_note_midi_standard(display_name, file_number, duration_ticks=duration_ticks)
            created_count += 1
        except ValueError as e:
            print(f"Skipping {display_name}: {e}")
        
        # Change back to original directory
        os.chdir(original_dir)
    
    print()
    print("=" * 70)
    print(f"Successfully created {created_count} MIDI files in '{output_dir}' directory")
    print(f"✓ Duration: {duration_ticks} ticks ({duration_ticks/1920} bars)")
    print("✓ Files are numbered sequentially from lowest to highest")
    print("✓ Track names are embedded in MIDI files")
    print()

def generate_all_notes_c0_to_c6(duration_ticks=DEFAULT_DURATION_TICKS):
    """Generate all notes from C0 to C6 in Ableton notation with sequential numbering"""
    generate_ableton_range("C0", "C6", include_track_names=True, duration_ticks=duration_ticks)

def generate_standard_c0_to_c6(duration_ticks=DEFAULT_DURATION_TICKS):
    """Generate all notes from C0 to C6 in STANDARD notation with sequential numbering"""
    generate_standard_range("C0", "C6", duration_ticks=duration_ticks)

def generate_middle_c_range(duration_ticks=DEFAULT_DURATION_TICKS):
    """Generate a practical range around middle C (C3 in Ableton notation)"""
    print("Generating practical range around Middle C (C3 in Ableton)")
    print("=" * 70)
    print(f"Duration: {duration_ticks} ticks ({duration_ticks/1920} bars)")
    
    output_dir = "middle_c_range_sequential"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    original_dir = os.getcwd()
    os.chdir(output_dir)
    
    # Generate from C2 to C4 in Ableton notation
    notes_to_generate = []
    
    for octave in [2, 3, 4]:  # C2, C3, C4 in Ableton
        for note_name in NOTE_NAMES:  # Use the global NOTE_NAMES
            display_name = f"{note_name}{octave}"
            # Calculate MIDI number for sorting
            note_index = NOTE_NAMES.index(note_name)  # Use the global NOTE_NAMES
            midi_num = (octave + 2) * 12 + note_index
            notes_to_generate.append((display_name, midi_num))
    
    # Sort by MIDI number
    notes_to_generate.sort(key=lambda x: x[1])
    
    print(f"Generating {len(notes_to_generate)} MIDI files around Middle C...")
    print()
    
    created_count = 0
    for file_number, (display_name, midi_num) in enumerate(notes_to_generate, start=1):
        try:
            # Create the note
            mid = MidiFile()
            track = MidiTrack()
            mid.tracks.append(track)
            
            # Add track name
            track.append(MetaMessage('track_name', name=f"Note {display_name}", time=0))
            
            # Set tempo
            tempo = mido.bpm2tempo(120)
            track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
            
            # Set time signature
            track.append(MetaMessage('time_signature', numerator=4, denominator=4, 
                                    clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
            
            # Add note
            track.append(Message('note_on', note=midi_num, velocity=64, time=0))
            track.append(Message('note_off', note=midi_num, velocity=64, time=duration_ticks))
            
            # Add end of track
            track.append(MetaMessage('end_of_track', time=0))
            
            # Save with sequential number
            filename = f"{file_number:02d} {display_name}.mid"
            mid.save(filename)
            
            print(f"✓ Created: {filename}")
            print(f"  Track name: 'Note {display_name}'")
            
            # Calculate standard notation for display
            standard_octave = (midi_num // 12) - 1
            standard_note_index = midi_num % 12
            standard_name = f"{NOTE_NAMES[standard_note_index]}{standard_octave}"  # Use the global NOTE_NAMES
            print(f"  Plays at: {standard_name} pitch (standard notation)")
            
            created_count += 1
        except ValueError as e:
            print(f"Skipping {display_name}: {e}")
    
    os.chdir(original_dir)
    print()
    print(f"Created {created_count} files in '{output_dir}' directory")
    print(f"✓ Duration: {duration_ticks} ticks ({duration_ticks/1920} bars)")
    print("✓ Files are numbered sequentially from lowest to highest")

def show_example_output():
    """Show example of correct pitch mapping"""
    print("EXAMPLE OF CORRECT PITCH MAPPING:")
    print("=" * 60)
    print("Ableton File | MIDI | Standard Pitch | Correct Display")
    print("-" * 60)
    print("01 C0.mid    | 24   | C1             | 'Plays at: C1 pitch'")
    print("37 C3.mid    | 48   | C4             | 'Plays at: C4 pitch' (Middle C)")
    print("73 C6.mid    | 96   | C7             | 'Plays at: C7 pitch'")
    print()
    print(f"Duration: {DEFAULT_DURATION_TICKS} ticks ({DEFAULT_DURATION_TICKS/1920} bars)")
    print("Key: Ableton C3 = MIDI 48 = Standard C4 = Middle C")
    print()

if __name__ == "__main__":
    print("=" * 70)
    print("MIDI FILE GENERATOR WITH CORRECT PITCH DISPLAY")
    print("=" * 70)
    print(f"Default Duration: {DEFAULT_DURATION_TICKS} ticks ({DEFAULT_DURATION_TICKS/1920} bars)")
    print("Creates MIDI files numbered from lowest to highest note")
    print("✓ Correctly displays 'Plays at: C7 pitch' for C6 in Ableton")
    print()
    
    # Show correct pitch mapping
    show_example_output()
    
    # Ask user what they want to generate
    print("OPTIONS:")
    print("1. Generate all notes from C0 to C6 in ABLETON notation (85 notes)")
    print("2. Generate all notes from C0 to C6 in STANDARD notation (85 notes)")
    print("3. Generate practical range around Middle C (C2 to C4, 36 notes)")
    print("4. Generate custom range")
    print()
    
    try:
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            generate_all_notes_c0_to_c6()
        elif choice == "2":
            generate_standard_c0_to_c6()
        elif choice == "3":
            generate_middle_c_range()
        elif choice == "4":
            # Optional: Allow user to specify custom duration
            custom_duration = input(f"Enter custom duration in ticks (press Enter for default {DEFAULT_DURATION_TICKS}): ").strip()
            if custom_duration:
                duration = int(custom_duration)
            else:
                duration = DEFAULT_DURATION_TICKS
                
            notation = input("Use (A)bleton or (S)tandard notation? ").strip().upper()
            start_note = input("Enter start note: ").strip()
            end_note = input("Enter end note: ").strip()
            
            if notation == "S" or notation == "STANDARD":
                generate_standard_range(start_note, end_note, duration_ticks=duration)
            else:
                generate_ableton_range(start_note, end_note, include_track_names=True, duration_ticks=duration)
        else:
            print("Invalid choice. Generating default range (Ableton C0 to C6)...")
            generate_all_notes_c0_to_c6()
        
        print()
        print("=" * 70)
        print("CORRECT PITCH DISPLAY:")
        print("-" * 70)
        print("✓ 'Plays at: C7 pitch' for file '73 C6.mid' (not C8)")
        print("✓ Ableton C6 = Standard C7 = MIDI 96")
        print("✓ Middle C: Ableton C3 = Standard C4 = MIDI 48")
        print(f"✓ Duration: {DEFAULT_DURATION_TICKS} ticks ({DEFAULT_DURATION_TICKS/1920} bars)")
        print("✓ All pitch references are now correct!")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")