import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from pydub import AudioSegment  # Still used for handling audio conversions, if needed
import pygame  # New addition for MIDI playback
import os
from tkinterdnd2 import TkinterDnD, DND_FILES  # Import TkinterDnD and DND_FILES
from mido import MidiFile, MidiTrack, Message  # Import required for MIDI file generation
from midi2audio import FluidSynth


# Initialize Pygame for MIDI playback
pygame.mixer.init()

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure necessary directory
PROGRESSIONS_FOLDER = os.path.join(current_dir, "Chord Progressions")
os.makedirs(PROGRESSIONS_FOLDER, exist_ok=True)

# Path to the SoundFont file in the same directory
SOUNDFONT_PATH = os.path.join(current_dir, "Piano_Sample_Soundfont.sf2")

# Define chord mappings and their MIDI notes
KEYS = {
    'C major': {'C': [60, 64, 67], 'Dm': [62, 65, 69], 'Em': [64, 67, 71], 
                'F': [65, 69, 72], 'G': [67, 71, 74], 'Am': [69, 72, 76], 'Bdim': [71, 74, 77]},
    'G major': {'G': [67, 71, 74], 'Am': [69, 72, 76], 'Bm': [71, 74, 78], 
                'C': [60, 64, 67], 'D': [62, 66, 69], 'Em': [64, 67, 71], 'F#dim': [66, 69, 73]},
    'A minor': {'Am': [69, 72, 76], 'Bdim': [71, 74, 77], 'C': [60, 64, 67], 
                'Dm': [62, 65, 69], 'Em': [64, 67, 71], 'F': [65, 69, 72], 'G': [67, 71, 74]},
    'E minor': {'Em': [64, 67, 71], 'F#dim': [66, 69, 73], 'G': [67, 71, 74], 
                'Am': [69, 72, 76], 'Bm': [71, 74, 78], 'C': [60, 64, 67], 'D': [62, 66, 69]}
}



def generate_midi_file(progression):
    """Generate a MIDI file for the given chord progression and save it."""
    midi = MidiFile() #not defined?
    track = MidiTrack() #not defined?
    midi.tracks.append(track)
    

    # Get the volume value from the slider
    volume = volume_slider.get()


    for chord in progression:
        notes = KEYS[selected_key.get()][chord]
        for note in notes:
            track.append(Message('note_on', note=note, velocity=volume, time=0))
        for note in notes:
            track.append(Message('note_off', note=note, velocity=volume, time=480))
    
    # Save with sequential numbering
    existing_files = os.listdir(PROGRESSIONS_FOLDER)
    next_number = len(existing_files) + 1
    filename = f"{PROGRESSIONS_FOLDER}/chord_progression_{next_number}.mid"
    midi.save(filename)
    update_progression_list()
    print(f"MIDI file '{filename}' downloaded successfully!")

def update_progression_list():
    """Update the list of saved chord progressions."""
    progression_listbox.delete(0, tk.END)
    files = sorted(os.listdir(PROGRESSIONS_FOLDER))
    for file in files:
        if file.endswith(".mid"):
            progression_listbox.insert(tk.END, file)

def on_select_key(event):
    """Update the chord listbox based on the selected key and clear the progression."""
    selected = selected_key.get()
    chords_listbox.delete(0, tk.END)
    progression_bar.delete(0, tk.END)  # Clear the progression bar
    for chord, notes in KEYS[selected].items():
        chord_name = f"{chord} ({', '.join(map(str, notes))})"
        chords_listbox.insert(tk.END, chord_name)

def on_chord_click(event):
    """Add the clicked chord to the progression bar."""
    selected_chord = chords_listbox.get(tk.ACTIVE).split(' ')[0]
    progression_bar.insert(tk.END, selected_chord)

def on_clear_progression():
    """Clear the progression bar."""
    progression_bar.delete(0, tk.END)

def on_download_midi():
    """Download the MIDI file for the current progression."""
    progression = progression_bar.get(0, tk.END)
    if progression:
        generate_midi_file(progression)

def delete_selected_progression():
    """Delete the selected MIDI file from the list and the folder."""
    selected = progression_listbox.get(tk.ACTIVE)
    if selected:
        os.remove(os.path.join(PROGRESSIONS_FOLDER, selected))
        update_progression_list()
        print(f"Deleted '{selected}'.")


def play_selected_progression():
    """Play the selected MIDI file using FluidSynth."""
    selected = progression_listbox.get(tk.ACTIVE)
    if selected:
        midi_path = os.path.abspath(os.path.join(PROGRESSIONS_FOLDER, selected))

        # Debug prints
        print(f"Selected MIDI file: {midi_path}")
        print(f"SoundFont path: {SOUNDFONT_PATH}")

        # Ensure MIDI file and SoundFont file exist
        if not os.path.exists(midi_path):
            print(f"Error: MIDI file '{midi_path}' not found.")
            return

        if not os.path.exists(SOUNDFONT_PATH):
            print(f"Error: SoundFont file '{SOUNDFONT_PATH}' not found.")
            return
        
        try:
            # Initialize FluidSynth once
            if not hasattr(play_selected_progression, "fs"):
                play_selected_progression.fs = FluidSynth(sound_font=SOUNDFONT_PATH, sample_rate=22050)
                print("FluidSynth initialized successfully.")
            
            # Load and play the MIDI file using FluidSynth
            play_selected_progression.fs.play_midi(midi_path)
            print(f"Playing '{selected}'...")
        except Exception as e:
            print(f"Error playing MIDI file: {e}")




def create_gradient(canvas, width, height, color1, color2):
    """Create a gradient background on the given canvas."""
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr:04x}{ng:04x}{nb:04x}'
        canvas.create_line(0, i, width, i, fill=color)

def resize_gradient(event):
    """Resize gradient background dynamically with window size."""
    create_gradient(canvas, event.width, event.height, "#333333", "#1a1a1a")


# Add a stop button to stop the playback
def stop_playback():
    """Stop the MIDI playback."""
    pygame.mixer.music.stop()
    print("Playback stopped.")

# Initialize main window
root = TkinterDnD.Tk() #line 123
root.title("Chord Progression Builder")
root.geometry("900x500")  # Increased window size

# Create canvas for gradient background
canvas = tk.Canvas(root, width=2500, height=800) #Cant adjust canvas size any more???
canvas.pack(fill=tk.BOTH, expand=True)
create_gradient(canvas, 2200, 600, "#333333", "#1a1a1a")

# Bind the resize event to dynamically resize the gradient
canvas.bind("<Configure>", resize_gradient)


# Frame to hold widgets
frame_left = tk.Frame(canvas, bg="#333333")
frame_left.place(relx=0.25, rely=0.5, anchor=tk.CENTER)

frame_right = tk.Frame(canvas, bg="#333333")
frame_right.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

# Key selection dropdown
selected_key = tk.StringVar()
selected_key.set('C major')  # default value
key_menu = tk.OptionMenu(frame_left, selected_key, *KEYS.keys(), command=on_select_key)
key_menu.config(bg="#555555", fg="white", font=("Arial", 12), highlightthickness=0)
key_menu.pack(pady=10)

# Chords listbox
chords_listbox = tk.Listbox(frame_left, height=10, bg="#444444", fg="white", font=("Arial", 12), selectbackground="#555555")
chords_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
chords_listbox.bind("<Double-Button-1>", on_chord_click)

# Progression bar
progression_bar = tk.Listbox(frame_left, height=3, bg="#444444", fg="white", font=("Arial", 12), selectbackground="#555555")
progression_bar.pack(pady=10, fill=tk.X)

# Note interval slider #debug
note_interval_slider = tk.Scale(frame_right, from_=120, to=960, orient=tk.HORIZONTAL, label="Note Interval (ms)",
                                bg="#555555", fg="white", font=("Arial", 12), highlightthickness=0)
note_interval_slider.set(480)  # Default note interval
note_interval_slider.pack(pady=10)

# Clear and Download buttons
button_frame = tk.Frame(frame_left, bg="#333333")
button_frame.pack(pady=10)

clear_button = tk.Button(button_frame, text="Clear Progression", command=on_clear_progression, bg="#555555", fg="white", font=("Arial", 12))
clear_button.grid(row=0, column=0, padx=10)

download_button = tk.Button(button_frame, text="Download MIDI", command=on_download_midi, bg="#555555", fg="white", font=("Arial", 12))
download_button.grid(row=0, column=1, padx=10)

# Progressions listbox on the right side
progression_listbox = tk.Listbox(frame_right, height=10, bg="#444444", fg="white", font=("Arial", 12), selectbackground="#555555")
progression_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
update_progression_list()



volume_label = tk.Label(frame_left, text="Volume:", bg="#333333", fg="white", font=("Arial", 12))
volume_label.pack(pady=(10, 0))

volume_slider = tk.Scale(frame_left, from_=0, to=127, orient=tk.HORIZONTAL, bg="#555555", fg="white", font=("Arial", 12), troughcolor="#444444", highlightthickness=0)

volume_slider.set(64)  # Default volume
volume_slider.pack(pady=5)


# Delete and Play buttons
action_button_frame = tk.Frame(frame_right, bg="#333333")
action_button_frame.pack(pady=10)

delete_button = tk.Button(action_button_frame, text="Delete Progression", command=delete_selected_progression, bg="#555555", fg="white", font=("Arial", 12))
delete_button.grid(row=0, column=0, padx=10)

play_button = tk.Button(action_button_frame, text="Play Progression", command=play_selected_progression, bg="#555555", fg="white", font=("Arial", 12))
play_button.grid(row=0, column=1, padx=10)

# Add Stop button
stop_button = tk.Button(action_button_frame, text="Stop Playback", command=stop_playback, bg="#555555", fg="white", font=("Arial", 12))
stop_button.grid(row=0, column=2, padx=10)


# Bind the drop event for MIDI files
def on_drop(event):
    """Handle dropping MIDI files into the application."""
    files = root.tk.splitlist(event.data)
    for file_path in files:
        if file_path.endswith(".mid"):
            dest_path = os.path.join(PROGRESSIONS_FOLDER, os.path.basename(file_path))
            if not os.path.exists(dest_path):
                os.rename(file_path, dest_path)
                update_progression_list()
                print(f"Imported '{file_path}'.")

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Initialize UI
on_select_key(None)  # Populate chords list
root.mainloop()

