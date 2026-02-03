# MIDI Generators for Ableton Live

A collection of Python scripts for generating MIDI files specifically designed for Ableton Live, with proper track naming and octave correction.

## Features

- **Ableton-compatible MIDI generation** (corrects for Ableton's octave offset)
- **Track name metadata** (no more "Track 0" in Ableton)
- **Multiple generators for different use cases**
- **Sequentially numbered filenames** (organized by pitch)
- **Descriptive track names** matching filenames

## Generators Included

### 1. Main Ableton Generator (`main_ableton_generator.py`)
Generates any range of notes from C0 to C6 in both Ableton and Standard MIDI notation.

### 2. Beatmaker Generator (`beatmaker_generator.py`)
Generates specific notes for beatmaking with section names:
- C#1 (Intro), D#1 (Fill), F#1 (Verse 1), G#1 (Verse 2), A#1 (Fill)
- C#2 (Chorus 1), D#2 (Chorus 2), F#2 (Break), G#2 (Special), A#2 (Ending)

### 3. Subcraft Generator (`subcraft_generator.py`)
Generates C2 through E2 with loop patterns:
- C2 (Loop 1), C#2 (Loop 2), D2 (Loop 3), D#2 (Stop), E2 (Loop 4)

### 4. USynth Generator (`usynth_generator.py`)
Generates complete octave C1 through B1 with function names:
- Loop patterns, mute, repeat, tempo multipliers (Time x2/x3/x4), stop

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
python main_ableton_generator.py
python beatmaker_generator.py
python subcraft_generator.py
python usynth_generator.py
Each script will create a folder with sequentially numbered MIDI files ready for import into Ableton Live.
```

## How It Works
Octave Correction: Automatically adjusts for Ableton's piano roll display (one octave lower than standard MIDI)
Track Naming: Embeds track names in MIDI metadata (Ableton shows these instead of "Track 0")
Sequential Numbering: Files are numbered 01, 02, 03... from lowest to highest pitch
Descriptive Filenames: Match Ableton track names for easy identification
