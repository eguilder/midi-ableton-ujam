# MIDI Generators for Ableton Live

A collection of Python scripts for generating MIDI files specifically designed to control Ujam sequencers in Ableton Live, with proper MIDI clip track naming and octave correction. The notes are already created in this repo and can be used directly in Ableton Live.

## Features

- **Ableton-compatible MIDI generation** (corrects for Ableton's octave offset)
- **Track name metadata** (no more "Track 0" in Ableton)
- **Multiple generators for different use cases**
- **Sequentially numbered filenames** (organized by pitch)
- **Descriptive track names** matching filenames

## Generators Included

### 1. Main Ableton Generator (`create_notes.py`)
Generates any range of notes from C0 to C6 in both Ableton and Standard MIDI notation.

### 2. Beatmaker Generator (`beatmaker_notes.py`)
Generates specific notes for beatmaking with section names:
- C#1 (Intro), D#1 (Fill), F#1 (Verse 1), G#1 (Verse 2), A#1 (Fill)
- C#2 (Chorus 1), D#2 (Chorus 2), F#2 (Break), G#2 (Special), A#2 (Ending)

### 3. Subcraft Generator (`subcraft_notes.py`)
Generates C2 through E2 with loop patterns:
- C2 (Loop 1), C#2 (Loop 2), D2 (Loop 3), D#2 (Stop), E2 (Loop 4)

### 4. USynth Generator (`usynth_notes.py`)
Generates complete octave C1 through B1 with function names:
- Loop patterns, mute, repeat, tempo multipliers (Time x2/x3/x4), stop

### 5. V-Drummer Generator (`drummer_notes.py`)
Generates comprehensive drum patterns across multiple octaves:
- **C3-G3**: Verse 1-5 patterns
- **C#3, D#3**: Intro 1-2 patterns
- **F#3, G#3, A#3**: Fill 1-3 patterns
- **A3-E4**: Chorus 1-5 patterns
- **C#4, D#4**: Ending 1-2 patterns
- **F4, G4, A4**: Special 1-3 patterns
- **F#4, G#4, A#4**: Breakdown 1-3 patterns
- **B4**: Stop pattern

### 6. V-Bassist Generator (`vbassist_notes.py`)
Generates bass patterns with phrases, styles, and transitions:
- **C0**: Silence pattern
- **C#0-B1**: Phrases 1-18 with Intros and Fills
- **C2-A#2**: Styles 1-6 with Style Intros and Style Fills
- **B2**: Stop pattern

### 7. V-Pianist Generator (`pianist_notes.py`)
Generates piano phrases and chord progressions:
- **C1-B1**: Phrases 1-7 with Fills
- **C#1, D#1**: Low Chord and High Chord progressions

### 8. V-Guitarist Generator (`vguitarist_notes.py`)
Generates guitar patterns across multiple ranges:
- **C0**: Silence pattern
- **C#0-B1**: Phrases 1-23
- **C2-A#2**: Styles 1-11
- **B2**: Stop pattern

### 9. Chord Generator (`create_chords.py`)
Generates chord triads organized by key and tonality for use with sequencers like V-Bassist and V-Guitarist:
- **Major and minor triads** for all 12 keys
- **Chord progressions** in common patterns (I-IV-V, ii-V-I, etc.)
- **Multiple voicings** (root position, first inversion, second inversion)
- **Key-specific organization** with Roman numeral notation
- **Export formats** suitable for chord progressions and arpeggiation patterns

## Installation

1. Install Python 3.6 or higher
2. Install required packages:
```bash
pip install -r requirements.txt
```
## Usage
Run any generator script:

bash
```python
python create_notes.py
python beatmaker_notes.py
python subcraft_notes.py
python usynth_notes.py
python drummer_notes.py
python vbassist_notes.py
python pianist_notes.py
python vguitarist_notes.py
python create_chords.py
```
Each script will create a folder with sequentially numbered MIDI files ready for import into Ableton Live.


## How It Works
- Octave Correction: Automatically adjusts for Ableton's piano roll display (one octave lower than standard MIDI)
- Track Naming: Embeds track names in MIDI metadata (Ableton shows these instead of "Track 0")
- Sequential Numbering: Files are numbered 01, 02, 03... from lowest to highest pitch
- Descriptive Filenames: Match Ableton track names for easy identification
