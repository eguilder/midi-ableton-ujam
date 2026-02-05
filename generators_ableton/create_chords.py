import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import re

# =============== CONFIGURATION VARIABLES ===============
# Change this value to control note duration
# 1920 ticks = 4 bars at 120 BPM
# 3840 ticks = 8 bars at 120 BPM
NOTE_DURATION_TICKS = 3840  # Set to 8 bars by default
BPM = 120
# =======================================================

# Define key signatures and their chords
KEY_SIGNATURES = {
    # Major keys
    'C Major': {
        'tonality': 'major',
        'chords': ['C Major', 'D Minor', 'E Minor', 'F Major', 'G Major', 'A Minor', 'B Diminished']
    },
    'C# Major': {
        'tonality': 'major', 
        'chords': ['C# Major', 'D# Minor', 'F Minor', 'F# Major', 'G# Major', 'A# Minor', 'C Diminished']
    },
    'D Major': {
        'tonality': 'major',
        'chords': ['D Major', 'E Minor', 'F# Minor', 'G Major', 'A Major', 'B Minor', 'C# Diminished']
    },
    'D# Major': {
        'tonality': 'major',
        'chords': ['D# Major', 'F Minor', 'G Minor', 'G# Major', 'A# Major', 'C Minor', 'D Diminished']
    },
    'E Major': {
        'tonality': 'major',
        'chords': ['E Major', 'F# Minor', 'G# Minor', 'A Major', 'B Major', 'C# Minor', 'D# Diminished']
    },
    'F Major': {
        'tonality': 'major',
        'chords': ['F Major', 'G Minor', 'A Minor', 'A# Major', 'C Major', 'D Minor', 'E Diminished']
    },
    'F# Major': {
        'tonality': 'major',
        'chords': ['F# Major', 'G# Minor', 'A# Minor', 'B Major', 'C# Major', 'D# Minor', 'F Diminished']
    },
    'G Major': {
        'tonality': 'major',
        'chords': ['G Major', 'A Minor', 'B Minor', 'C Major', 'D Major', 'E Minor', 'F# Diminished']
    },
    'G# Major': {
        'tonality': 'major',
        'chords': ['G# Major', 'A# Minor', 'C Minor', 'C# Major', 'D# Major', 'F Minor', 'G Diminished']
    },
    'A Major': {
        'tonality': 'major',
        'chords': ['A Major', 'B Minor', 'C# Minor', 'D Major', 'E Major', 'F# Minor', 'G# Diminished']
    },
    'A# Major': {
        'tonality': 'major',
        'chords': ['A# Major', 'C Minor', 'D Minor', 'D# Major', 'F Major', 'G Minor', 'A Diminished']
    },
    'B Major': {
        'tonality': 'major',
        'chords': ['B Major', 'C# Minor', 'D# Minor', 'E Major', 'F# Major', 'G# Minor', 'A# Diminished']
    },
    
    # Minor keys (natural minor)
    'C Minor': {
        'tonality': 'minor',
        'chords': ['C Minor', 'D Diminished', 'Eb Major', 'F Minor', 'G Minor', 'Ab Major', 'Bb Major']
    },
    'C# Minor': {
        'tonality': 'minor',
        'chords': ['C# Minor', 'D# Diminished', 'E Major', 'F# Minor', 'G# Minor', 'A Major', 'B Major']
    },
    'D Minor': {
        'tonality': 'minor',
        'chords': ['D Minor', 'E Diminished', 'F Major', 'G Minor', 'A Minor', 'Bb Major', 'C Major']
    },
    'D# Minor': {
        'tonality': 'minor',
        'chords': ['D# Minor', 'F Diminished', 'Gb Major', 'G# Minor', 'A# Minor', 'B Major', 'C# Major']
    },
    'E Minor': {
        'tonality': 'minor',
        'chords': ['E Minor', 'F# Diminished', 'G Major', 'A Minor', 'B Minor', 'C Major', 'D Major']
    },
    'F Minor': {
        'tonality': 'minor',
        'chords': ['F Minor', 'G Diminished', 'Ab Major', 'Bb Minor', 'C Minor', 'Db Major', 'Eb Major']
    },
    'F# Minor': {
        'tonality': 'minor',
        'chords': ['F# Minor', 'G# Diminished', 'A Major', 'B Minor', 'C# Minor', 'D Major', 'E Major']
    },
    'G Minor': {
        'tonality': 'minor',
        'chords': ['G Minor', 'A Diminished', 'Bb Major', 'C Minor', 'D Minor', 'Eb Major', 'F Major']
    },
    'G# Minor': {
        'tonality': 'minor',
        'chords': ['G# Minor', 'A# Diminished', 'B Major', 'C# Minor', 'D# Minor', 'E Major', 'F# Major']
    },
    'A Minor': {
        'tonality': 'minor',
        'chords': ['A Minor', 'B Diminished', 'C Major', 'D Minor', 'E Minor', 'F Major', 'G Major']
    },
    'A# Minor': {
        'tonality': 'minor',
        'chords': ['A# Minor', 'C Diminished', 'Db Major', 'Eb Minor', 'F Minor', 'Gb Major', 'Ab Major']
    },
    'B Minor': {
        'tonality': 'minor',
        'chords': ['B Minor', 'C# Diminished', 'D Major', 'E Minor', 'F# Minor', 'G Major', 'A Major']
    }
}

def create_chord_triad_midi(root_note, triad_type, file_number, duration_ticks=NOTE_DURATION_TICKS, bpm=BPM):
    """
    Create MIDI file with a chord triad for Ableton Live
    
    Args:
        root_note: Root note in Ableton notation (e.g., 'C3')
        triad_type: Type of triad ('Major', 'Minor', 'Diminished', 'Augmented')
        file_number: Sequential number for filename (e.g., 001, 002, 003...)
        duration_ticks: Duration in MIDI ticks (default: 8 bars at 120 BPM)
        bpm: Tempo in beats per minute
    """
    # Parse the note name and octave from the root note
    match = re.match(r'([A-G]#?)(-?\d+)', root_note)
    if not match:
        raise ValueError(f"Invalid note name format: {root_note}. Use format like 'C3', 'C#4', 'A2'")
    
    note_name = match.group(1)
    octave = int(match.group(2))
    
    # Define note names and their indices
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Find the index of the root note
    try:
        root_index = note_names.index(note_name)
    except ValueError:
        raise ValueError(f"Invalid note name: {note_name}. Use C, C#, D, D#, E, F, F#, G, G#, A, A#, or B")
    
    # FIXED: Correct MIDI note calculation for Ableton Live
    # In Ableton Live, C3 = MIDI 60 (not 48)
    # Standard MIDI: C-2 = 0, C-1 = 12, C0 = 24, C1 = 36, C2 = 48, C3 = 60, C4 = 72, C5 = 84
    # So the formula is: MIDI = (octave + 2) * 12 + note_index
    # Where C3 = (3 + 2) * 12 + 0 = 5 * 12 = 60
    root_midi = (octave + 2) * 12 + root_index
    
    # Calculate the third and fifth based on triad type
    if triad_type.lower() == 'major':
        # Major: root, major third (4 semitones), perfect fifth (7 semitones)
        third_midi = root_midi + 4
        fifth_midi = root_midi + 7
    elif triad_type.lower() == 'minor':
        # Minor: root, minor third (3 semitones), perfect fifth (7 semitones)
        third_midi = root_midi + 3
        fifth_midi = root_midi + 7
    elif triad_type.lower() == 'diminished':
        # Diminished: root, minor third (3 semitones), diminished fifth (6 semitones)
        third_midi = root_midi + 3
        fifth_midi = root_midi + 6
    elif triad_type.lower() == 'augmented':
        # Augmented: root, major third (4 semitones), augmented fifth (8 semitones)
        third_midi = root_midi + 4
        fifth_midi = root_midi + 8
    else:
        raise ValueError(f"Invalid triad type: {triad_type}. Use Major, Minor, Diminished, or Augmented")
    
    # Check if all MIDI numbers are within valid range (0-127)
    chord_notes = [root_midi, third_midi, fifth_midi]
    for note in chord_notes:
        if note < 0 or note > 127:
            raise ValueError(f"Note {midi_to_note_name(note)} is outside valid range (0-127)")
    
    # Get standard notation names for display (what will show in piano roll)
    standard_root = midi_to_standard_notation(root_midi)
    standard_third = midi_to_standard_notation(third_midi)
    standard_fifth = midi_to_standard_notation(fifth_midi)
    
    # Get Ableton notation for reference
    ableton_root = midi_to_ableton_notation(root_midi)
    ableton_third = midi_to_ableton_notation(third_midi)
    ableton_fifth = midi_to_ableton_notation(fifth_midi)
    
    # Create a new MIDI file
    mid = MidiFile()
    
    # Create a track
    track = MidiTrack()
    mid.tracks.append(track)
    
    # ADD TRACK NAME METADATA - Use the requested Ableton notation in track name
    track_name = f"{root_note} {triad_type}"
    track.append(MetaMessage('track_name', name=track_name, time=0))
    
    # Set tempo (microseconds per beat)
    tempo = mido.bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    
    # Set time signature (4/4)
    track.append(MetaMessage('time_signature', numerator=4, denominator=4, 
                             clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    
    # Add note on messages for all three notes of the chord (simultaneous)
    # All notes start at time=0
    track.append(Message('note_on', note=root_midi, velocity=64, time=0))
    track.append(Message('note_on', note=third_midi, velocity=60, time=0))
    track.append(Message('note_on', note=fifth_midi, velocity=56, time=0))
    
    # Add note off messages after the specified duration
    # All notes end at the same time
    track.append(Message('note_off', note=root_midi, velocity=64, time=duration_ticks))
    track.append(Message('note_off', note=third_midi, velocity=60, time=0))
    track.append(Message('note_off', note=fifth_midi, velocity=56, time=0))
    
    # Add end of track marker
    track.append(MetaMessage('end_of_track', time=0))
    
    # Save the MIDI file with 3-digit sequential numbering
    filename = f"{file_number:03d} {root_note} {triad_type}.mid"
    mid.save(filename)
    
    # Calculate duration in bars and seconds for display
    bars = duration_ticks / 480  # 480 ticks per bar at 4/4
    seconds = (duration_ticks * 60) / (bpm * 480)  # Convert ticks to seconds
    
    print(f"Created: {filename}")
    print(f"  • Track name in Ableton: '{track_name}'")
    print(f"  • MIDI notes in file: {root_midi} ({standard_root}), {third_midi} ({standard_third}), {fifth_midi} ({standard_fifth})")
    print(f"  • Will display in piano roll as: {standard_root}, {standard_third}, {standard_fifth}")
    print(f"  • Corresponds to Ableton UI as: {ableton_root}, {ableton_third}, {ableton_fifth}")
    print(f"  • Duration: {bars:.1f} bars ({seconds:.1f} seconds at {bpm} BPM)")
    print(f"  • Intervals: {get_intervals_description(triad_type)}")
    print()
    
    return mid

def midi_to_ableton_notation(midi_note):
    """Convert MIDI note number to Ableton UI notation"""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_index = midi_note % 12
    # FIXED: Correct conversion for Ableton UI
    # In Ableton UI: C3 = MIDI 60, C4 = MIDI 72
    # So: octave = (midi_note // 12) - 1
    octave = (midi_note // 12) - 1  # Ableton UI: C3 = MIDI 60
    return f"{note_names[note_index]}{octave}"

def midi_to_standard_notation(midi_note):
    """Convert MIDI note number to standard notation (what displays in piano roll)"""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_index = midi_note % 12
    # FIXED: This should match what Ableton shows in piano roll
    # Standard MIDI: C-1 = 0, C0 = 12, C1 = 24, C2 = 36, C3 = 48, C4 = 60, C5 = 72
    # But Ableton shows: C3 = MIDI 60, C4 = MIDI 72, C5 = MIDI 84
    # So we need: octave = (midi_note // 12) - 2 for standard notation
    octave = (midi_note // 12) - 2  # Standard: C3 = MIDI 48, but Ableton shows C3 = MIDI 60
    return f"{note_names[note_index]}{octave}"

def midi_to_note_name(midi_note):
    """Convert MIDI note to readable name"""
    return midi_to_standard_notation(midi_note)

def get_intervals_description(triad_type):
    """Get interval description for triad type"""
    intervals = {
        'major': "Root, Major 3rd (4 semitones), Perfect 5th (7 semitones)",
        'minor': "Root, Minor 3rd (3 semitones), Perfect 5th (7 semitones)",
        'diminished': "Root, Minor 3rd (3 semitones), Diminished 5th (6 semitones)",
        'augmented': "Root, Major 3rd (4 semitones), Augmented 5th (8 semitones)"
    }
    return intervals.get(triad_type.lower(), "Unknown intervals")

def generate_chord_triads_range(start_note="C3", end_note="C5"):
    """
    Generate MIDI files for all chord triads in the specified range
    
    Args:
        start_note: Starting root note in Ableton notation (e.g., 'C3')
        end_note: Ending root note in Ableton notation (e.g., 'C5')
    """
    # Create main output directory
    main_output_dir = "midi_files_ableton_triads"
    if not os.path.exists(main_output_dir):
        os.makedirs(main_output_dir)
    
    # Create range-specific subdirectory
    safe_range_name = f"range_{start_note}_to_{end_note}".replace("#", "sharp")
    output_dir = os.path.join(main_output_dir, safe_range_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("=" * 70)
    print("GENERATING CHORD TRIADS FOR ABLETON LIVE")
    print("=" * 70)
    print(f"Range: {start_note} to {end_note} (Ableton notation)")
    print(f"Note duration: {NOTE_DURATION_TICKS} ticks ({NOTE_DURATION_TICKS/480:.1f} bars at {BPM} BPM)")
    print("Chord types: Major, Minor, Diminished, Augmented")
    print(f"Output folder: '{output_dir}'")
    print("Order: Key first, then type (001 C3 Major, 002 C3 Minor, etc.)")
    print("IMPORTANT: Using corrected MIDI mapping for Ableton Live")
    print("  • 'C3' in filename = C3 in Ableton piano roll = MIDI 60")
    print()
    
    # Parse start and end notes (in Ableton notation)
    start_match = re.match(r'([A-G]#?)(-?\d+)', start_note)
    end_match = re.match(r'([A-G]#?)(-?\d+)', end_note)
    
    if not start_match or not end_match:
        raise ValueError("Invalid start or end note format. Use format like 'C3', 'C#4', 'A2'")
    
    start_note_name = start_match.group(1)
    start_octave = int(start_match.group(2))
    end_note_name = end_match.group(1)
    end_octave = int(end_match.group(2))
    
    # Define note names and their indices
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Find indices
    start_note_index = note_names.index(start_note_name)
    end_note_index = note_names.index(end_note_name)
    
    # Define triad types in the order they should appear
    triad_types = ['Major', 'Minor', 'Diminished', 'Augmented']
    
    # Generate all root notes in the range (sorted by MIDI number = pitch)
    all_root_notes = []
    
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
            note_name = note_names[note_idx]
            display_name = f"{note_name}{octave}"  # Ableton notation for filename/track name
            
            # FIXED: Calculate MIDI number using corrected formula
            # C3 = (3 + 2) * 12 + 0 = 60
            midi_num = (octave + 2) * 12 + note_idx
            all_root_notes.append((display_name, midi_num))
    
    # Sort by MIDI number (lowest to highest pitch)
    all_root_notes.sort(key=lambda x: x[1])
    
    # Generate all chord combinations (root × type)
    all_chords = []
    file_counter = 1
    
    for root_note_ableton, root_midi in all_root_notes:
        for triad_type in triad_types:
            all_chords.append((file_counter, root_note_ableton, triad_type, root_midi))
            file_counter += 1
    
    # Generate MIDI files
    print(f"Generating {len(all_chords)} chord triad MIDI files...")
    print()
    
    # Track which chords we've created
    created_count = 0
    
    for file_number, root_note_ableton, triad_type, root_midi in all_chords:
        # Change to output directory
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        try:
            # Pass the Ableton notation for the filename/track name
            create_chord_triad_midi(root_note_ableton, triad_type, file_number, 
                                    duration_ticks=NOTE_DURATION_TICKS, bpm=BPM)
            created_count += 1
        except ValueError as e:
            print(f"Skipping {root_note_ableton} {triad_type}: {e}")
        
        # Change back to original directory
        os.chdir(original_dir)
    
    print()
    print("=" * 70)
    print(f"SUCCESSFULLY CREATED {created_count} CHORD TRIAD MIDI FILES")
    print("=" * 70)
    print(f"Location: '{output_dir}' directory")
    print(f"Range: {start_note} to {end_note} (Ableton notation in filenames)")
    print(f"Triad types: {', '.join(triad_types)}")
    print(f"Note duration: {NOTE_DURATION_TICKS} ticks ({NOTE_DURATION_TICKS/480:.1f} bars at {BPM} BPM)")
    print("✓ Files numbered with 3 digits: 001, 002, ..., 100")
    print("✓ Track names use Ableton notation")
    print("✓ MIDI notes use corrected mapping for Ableton piano roll")
    print("✓ All chords contain root, third, and fifth")
    print()
    
    # Calculate total duration in bars and seconds
    total_bars = NOTE_DURATION_TICKS / 480
    total_seconds = (NOTE_DURATION_TICKS * 60) / (BPM * 480)
    
    # Show example of the first few files
    print("EXAMPLE FILE NAMES (first 8 and last 4):")
    print("-" * 50)
    for i, (file_num, root, ttype, midi) in enumerate(all_chords[:8]):
        standard_root = midi_to_standard_notation(midi)
        print(f"{file_num:03d} {root} {ttype}.mid")
        print(f"    • Piano roll: {standard_root} chord ({total_bars:.1f} bars, {total_seconds:.1f}s)")
        print(f"    • MIDI notes: {midi}, {midi+4 if ttype.lower() in ['major', 'augmented'] else midi+3}, {midi+7 if ttype.lower() in ['major', 'minor'] else (midi+6 if ttype.lower() == 'diminished' else midi+8)}")
    print("...")
    for i, (file_num, root, ttype, midi) in enumerate(all_chords[-4:], start=len(all_chords)-4):
        standard_root = midi_to_standard_notation(midi)
        print(f"{file_num:03d} {root} {ttype}.mid")
        print(f"    • Piano roll: {standard_root} chord ({total_bars:.1f} bars, {total_seconds:.1f}s)")
        print(f"    • MIDI notes: {midi}, {midi+4 if ttype.lower() in ['major', 'augmented'] else midi+3}, {midi+7 if ttype.lower() in ['major', 'minor'] else (midi+6 if ttype.lower() == 'diminished' else midi+8)}")
    
    return all_chords

def generate_key_chords(key_signature, octaves=2):
    """
    Generate all chords for a specific key signature across multiple octaves
    
    Args:
        key_signature: Key signature name (e.g., 'C Major', 'A Minor')
        octaves: Number of octaves to generate (default: 2)
    """
    if key_signature not in KEY_SIGNATURES:
        raise ValueError(f"Invalid key signature: {key_signature}. Available: {', '.join(sorted(KEY_SIGNATURES.keys()))}")
    
    key_data = KEY_SIGNATURES[key_signature]
    chords = key_data['chords']
    tonality = key_data['tonality']
    
    # Create main output directory if it doesn't exist
    main_output_dir = "midi_files_ableton_triads"
    if not os.path.exists(main_output_dir):
        os.makedirs(main_output_dir)
    
    # Create key-specific subdirectory inside main directory
    safe_key_name = key_signature.replace(" ", "_").replace("#", "sharp")
    output_dir = os.path.join(main_output_dir, f"key_{safe_key_name}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("=" * 70)
    print(f"GENERATING CHORDS FOR {key_signature.upper()}")
    print("=" * 70)
    print(f"Tonality: {tonality.title()}")
    print(f"Number of chords in key: {len(chords)}")
    print(f"Octaves: {octaves}")
    print(f"Note duration: {NOTE_DURATION_TICKS} ticks ({NOTE_DURATION_TICKS/480:.1f} bars at {BPM} BPM)")
    print(f"Output folder: '{output_dir}'")
    print("IMPORTANT: Using corrected MIDI mapping for Ableton Live")
    print("  • 'C3' in filename = C3 in Ableton piano roll = MIDI 60")
    print()
    
    # Parse chords to get root notes and triad types
    chord_data = []
    for chord in chords:
        # Parse chord notation (e.g., "C Major", "D Minor", "B Diminished")
        # Handle chords like "Ab Major", "Eb Major", "Gb Major"
        if chord.startswith("Ab"):
            root_note_name = "G#"
            triad_type = chord[3:]
        elif chord.startswith("Bb"):
            root_note_name = "A#"
            triad_type = chord[3:]
        elif chord.startswith("Db"):
            root_note_name = "C#"
            triad_type = chord[3:]
        elif chord.startswith("Eb"):
            root_note_name = "D#"
            triad_type = chord[3:]
        elif chord.startswith("Gb"):
            root_note_name = "F#"
            triad_type = chord[3:]
        else:
            # Regular chords like "C Major", "D# Minor"
            # Find where the note name ends (before the space)
            for i in range(len(chord)):
                if chord[i] == ' ':
                    root_note_name = chord[:i]
                    triad_type = chord[i+1:]
                    break
    
        chord_data.append((root_note_name, triad_type))
    
    # Generate chords for each octave
    all_chords = []
    file_counter = 1
    
    # Determine starting octave based on key
    if key_signature in ['C Major', 'C Minor', 'A Minor']:
        start_octave = 3
    else:
        start_octave = 3  # Default to C3 octave
    
    for octave in range(start_octave, start_octave + octaves):
        for root_note_name, triad_type in chord_data:
            # Create note in Ableton notation
            root_note_ableton = f"{root_note_name}{octave}"
            
            # Calculate MIDI number for reference
            note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            try:
                root_index = note_names.index(root_note_name)
            except ValueError:
                # Try alternative names
                alt_names = {'Ab': 'G#', 'Bb': 'A#', 'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#'}
                if root_note_name in alt_names:
                    root_index = note_names.index(alt_names[root_note_name])
                else:
                    raise ValueError(f"Invalid note name in chord: {root_note_name}")
            
            # FIXED: Calculate MIDI number using corrected formula
            # C3 = (3 + 2) * 12 + 0 = 60
            root_midi = (octave + 2) * 12 + root_index
            all_chords.append((file_counter, root_note_ableton, triad_type, root_midi, octave))
            file_counter += 1
    
    print(f"Generating {len(all_chords)} MIDI files for {key_signature}...")
    print()
    
    # Track which chords we've created
    created_count = 0
    
    for file_number, root_note_ableton, triad_type, root_midi, octave in all_chords:
        # Change to output directory
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        try:
            create_chord_triad_midi(root_note_ableton, triad_type, file_number, 
                                    duration_ticks=NOTE_DURATION_TICKS, bpm=BPM)
            created_count += 1
        except ValueError as e:
            print(f"Skipping {root_note_ableton} {triad_type}: {e}")
        
        # Change back to original directory
        os.chdir(original_dir)
    
    print()
    print("=" * 70)
    print(f"SUCCESSFULLY CREATED {created_count} MIDI FILES FOR {key_signature.upper()}")
    print("=" * 70)
    print(f"Location: '{output_dir}' directory")
    print(f"Key: {key_signature}")
    print(f"Tonality: {tonality.title()}")
    print(f"Chords in key: {', '.join(chords)}")
    print(f"Octaves generated: {octaves} (C{start_octave} to C{start_octave + octaves - 1})")
    print(f"Note duration: {NOTE_DURATION_TICKS} ticks ({NOTE_DURATION_TICKS/480:.1f} bars at {BPM} BPM)")
    print("✓ Files numbered with 3 digits")
    print("✓ Track names use Ableton notation")
    print("✓ MIDI notes use corrected mapping for Ableton piano roll")
    print("✓ All chords contain root, third, and fifth")
    print()
    
    # Display chord progression for this key
    print(f"CHORD PROGRESSION FOR {key_signature}:")
    print("-" * 40)
    roman_numerals = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°'] if tonality == 'major' else ['i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII']
    for i, (chord, roman) in enumerate(zip(chords, roman_numerals)):
        print(f"  {roman}: {chord}")
    
    return all_chords

def generate_all_key_chords(octaves=2):
    """Generate chords for all available key signatures"""
    print("=" * 70)
    print("GENERATING CHORDS FOR ALL KEY SIGNATURES")
    print("=" * 70)
    
    all_results = {}
    for key_signature in sorted(KEY_SIGNATURES.keys()):
        print(f"\nProcessing {key_signature}...")
        try:
            chords = generate_key_chords(key_signature, octaves)
            all_results[key_signature] = chords
        except Exception as e:
            print(f"Failed to generate {key_signature}: {e}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Generated chords for {len(all_results)} key signatures:")
    for key_signature in sorted(all_results.keys()):
        chords = all_results[key_signature]
        safe_key_name = key_signature.replace(" ", "_").replace("#", "sharp")
        print(f"  • {key_signature}: {len(chords)} files in 'midi_files_ableton_triads/key_{safe_key_name}'")
    
    return all_results

def generate_C3_to_C5_triads():
    """Generate all chord triads from C3 to C5 (100 files total)"""
    return generate_chord_triads_range("C3", "C5")

def show_key_signature_menu():
    """Display a menu of available key signatures"""
    print("=" * 70)
    print("AVAILABLE KEY SIGNATURES")
    print("=" * 70)
    
    print("\nMAJOR KEYS:")
    print("-" * 40)
    major_keys = [k for k in KEY_SIGNATURES.keys() if KEY_SIGNATURES[k]['tonality'] == 'major']
    for i, key in enumerate(sorted(major_keys), 1):
        chords = KEY_SIGNATURES[key]['chords']
        print(f"  {key:12} → {', '.join(chords[:3])}...")
    
    print("\nMINOR KEYS (Natural Minor):")
    print("-" * 40)
    minor_keys = [k for k in KEY_SIGNATURES.keys() if KEY_SIGNATURES[k]['tonality'] == 'minor']
    for i, key in enumerate(sorted(minor_keys), 1):
        chords = KEY_SIGNATURES[key]['chords']
        print(f"  {key:12} → {', '.join(chords[:3])}...")
    
    print("\n" + "=" * 70)

def show_configuration_summary():
    """Show the current configuration settings"""
    print("=" * 70)
    print("CURRENT CONFIGURATION")
    print("=" * 70)
    print(f"Note Duration: {NOTE_DURATION_TICKS} ticks")
    print(f"  • Equivalent to: {NOTE_DURATION_TICKS/480:.1f} bars at {BPM} BPM")
    print(f"  • Equivalent to: {(NOTE_DURATION_TICKS * 60)/(BPM * 480):.1f} seconds at {BPM} BPM")
    print()
    print(f"BPM: {BPM}")
    print(f"Octave Range: C3 to C5 (2 octaves)")
    print(f"Main Output Folder: 'midi_files_ableton_triads'")
    print()
    print("CORRECTED MIDI MAPPING FOR ABLETON LIVE:")
    print("  • 'C3' in filename = C3 in Ableton piano roll = MIDI 60")
    print("  • 'C4' in filename = C4 in Ableton piano roll = MIDI 72")
    print("  • 'C5' in filename = C5 in Ableton piano roll = MIDI 84")
    print()
    print("To change duration, modify the NOTE_DURATION_TICKS variable at the top of the script.")
    print("Common values:")
    print("  • 480 ticks = 1 bar")
    print("  • 960 ticks = 2 bars")
    print("  • 1920 ticks = 4 bars")
    print("  • 3840 ticks = 8 bars (current)")
    print("  • 7680 ticks = 16 bars")
    print("=" * 70)
    print()

if __name__ == "__main__":
    print("=" * 70)
    print("ABLETON CHORD TRIAD MIDI GENERATOR (FIXED OCTAVE)")
    print("=" * 70)
    print("Creates MIDI files with chord triads for Ableton Live")
    print("Two generation modes available:")
    print("  1. Full range: All chords from C3 to C5 (100 files)")
    print("  2. Key-based: Chords harmonically related to a specific key")
    print("  3. All keys: Generate chords for all 24 keys")
    print()
    print("FIXED: Now uses correct MIDI mapping for Ableton Live")
    print("  • 'C3' in filename = C3 in Ableton piano roll = MIDI 60")
    print()
    print("All files are organized under 'midi_files_ableton_triads' folder")
    print()
    
    # Show configuration summary
    show_configuration_summary()
    
    # Show key signature menu
    show_key_signature_menu()
    
    print("\nSELECT GENERATION MODE:")
    print("1. Generate all chords from C3 to C5 (100 files)")
    print("2. Generate chords for a specific key")
    print("3. Generate chords for all keys (creates multiple folders)")
    
    try:
        mode = int(input("\nEnter choice (1-3): ").strip())
    except ValueError:
        mode = 1  # Default to mode 1
    
    if mode == 1:
        # Generate full range C3 to C5
        try:
            chords = generate_chord_triads_range("C3", "C5")
            
            print()
            print("=" * 70)
            print("IMPORTANT NOTES FOR ABLETON:")
            print("=" * 70)
            print(f"1. Each MIDI file contains a single chord triad ({NOTE_DURATION_TICKS/480:.1f} bars)")
            print("2. All three notes (root, third, fifth) play simultaneously")
            print("3. Track names use Ableton notation for easy identification")
            print("4. Piano roll displays correct notes (C3 = MIDI 60)")
            print("5. Files are numbered 001-100 for easy browsing")
            print(f"6. Files saved in: 'midi_files_ableton_triads/range_C3_to_C5/'")
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            print(f"\nError: {e}")
    
    elif mode == 2:
        # Generate for specific key
        print("\nEnter key signature (e.g., 'C Major', 'A Minor', 'F# Major'):")
        print("Or press Enter for default (C Major)")
        key_input = input("Key: ").strip()
        
        if not key_input:
            key_input = "C Major"
        
        if key_input not in KEY_SIGNATURES:
            print(f"\nWarning: '{key_input}' not found in key signatures.")
            print(f"Defaulting to 'C Major'")
            key_input = "C Major"
        
        print(f"\nNumber of octaves to generate (default: 2):")
        try:
            octaves_input = input("Octaves: ").strip()
            octaves = int(octaves_input) if octaves_input else 2
        except ValueError:
            octaves = 2
        
        try:
            chords = generate_key_chords(key_input, octaves)
            
            print()
            print("=" * 70)
            print("IMPORTANT NOTES FOR ABLETON:")
            print("=" * 70)
            print(f"1. Key: {key_input}")
            print(f"2. Chords follow {key_input} harmony")
            print(f"3. Each chord plays for {NOTE_DURATION_TICKS/480:.1f} bars")
            safe_key_name = key_input.replace(" ", "_").replace("#", "sharp")
            print(f"4. Files saved in: 'midi_files_ableton_triads/key_{safe_key_name}/'")
            print(f"5. Use these chords to create progressions in the key of {key_input}")
            print(f"6. Correct MIDI mapping: 'C3' = C3 in piano roll = MIDI 60")
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            print(f"\nError: {e}")
    
    elif mode == 3:
        # Generate for all keys
        print("\nNumber of octaves to generate for each key (default: 2):")
        try:
            octaves_input = input("Octaves: ").strip()
            octaves = int(octaves_input) if octaves_input else 2
        except ValueError:
            octaves = 2
        
        try:
            all_results = generate_all_key_chords(octaves)
            
            print()
            print("=" * 70)
            print("SUMMARY:")
            print("=" * 70)
            print(f"Created folders for {len(all_results)} key signatures:")
            print("All files are organized under 'midi_files_ableton_triads/' folder:")
            for key in sorted(all_results.keys()):
                chords = all_results[key]
                safe_key_name = key.replace(" ", "_").replace("#", "sharp")
                print(f"  • {key}: {len(chords)} files in 'key_{safe_key_name}'")
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            print(f"\nError: {e}")
    
    else:
        print(f"\nInvalid choice: {mode}. Defaulting to mode 1.")
        try:
            chords = generate_chord_triads_range("C3", "C5")
        except Exception as e:
            print(f"\nError: {e}")