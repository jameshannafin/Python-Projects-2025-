import tkinter as tk
from tkinterdnd2 import TkinterDnD
from mido import Message, MidiFile, MidiTrack

# Define chord mappings and their MIDI notes
KEYS = {
    'C major': {
        'C': [60, 64, 67], 'Dm': [62, 65, 69], 'Em': [64, 67, 71], 
        'F': [65, 69, 72], 'G': [67, 71, 74], 'Am': [69, 72, 76], 'Bdim': [71, 74, 77]
    },
    'G major': {
        'G': [67, 71, 74], 'Am': [69, 72, 76], 'Bm': [71, 74, 78], 
        'C': [60, 64, 67], 'D': [62, 66, 69], 'Em': [64, 67, 71], 'F#dim': [66, 69, 73]
    },
    'A minor': {
        'Am': [69, 72, 76], 'Bdim': [71, 74, 77], 'C': [60, 64, 67], 
        'Dm': [62, 65, 69], 'Em': [64, 67, 71], 'F': [65, 69, 72], 'G': [67, 71, 74]
    },
    'E minor': {
        'Em': [64, 67, 71], 'F#dim': [66, 69, 73], 'G': [67, 71, 74], 
        'Am': [69, 72, 76], 'Bm': [71, 74, 78], 'C': [60, 64, 67], 'D': [62, 66, 69]
    }
}

def generate_midi_file(progression):
    """Generate a MIDI file for the given chord progression and save it."""
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    for chord in progression:
        notes = KEYS[selected_key.get()][chord]
        for note in notes:
            track.append(Message('note_on', note=note, velocity=64, time=0))
        for note in notes:
            track.append(Message('note_off', note=note, velocity=64, time=480))
    
    filename = "chord_progression.mid"
    midi.save(filename)

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
        print("MIDI file 'chord_progression.mid' downloaded successfully!")

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

# Initialize main window
root = TkinterDnD.Tk()
root.title("Chord Progression Builder")
root.geometry("600x500")  # Increased window size

# Create canvas for gradient background
canvas = tk.Canvas(root, width=600, height=500)
canvas.pack(fill=tk.BOTH, expand=True)
create_gradient(canvas, 600, 500, "#333333", "#1a1a1a")

# Frame to hold widgets
frame = tk.Frame(canvas, bg="#333333")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Key selection dropdown
selected_key = tk.StringVar()
selected_key.set('C major')  # default value
key_menu = tk.OptionMenu(frame, selected_key, *KEYS.keys(), command=on_select_key)
key_menu.config(bg="#555555", fg="white", font=("Arial", 12), highlightthickness=0)
key_menu.pack(pady=10)

# Chords listbox
chords_listbox = tk.Listbox(frame, height=10, bg="#444444", fg="white", font=("Arial", 12), selectbackground="#555555")
chords_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
chords_listbox.bind("<Double-Button-1>", on_chord_click)

# Progression bar
progression_bar = tk.Listbox(frame, height=3, bg="#444444", fg="white", font=("Arial", 12), selectbackground="#555555")
progression_bar.pack(pady=10, fill=tk.X)

# Clear and Download buttons
button_frame = tk.Frame(frame, bg="#333333")
button_frame.pack(pady=10)

clear_button = tk.Button(button_frame, text="Clear Progression", command=on_clear_progression, bg="#555555", fg="white", font=("Arial", 12))
clear_button.grid(row=0, column=0, padx=10)

download_button = tk.Button(button_frame, text="Download MIDI", command=on_download_midi, bg="#555555", fg="white", font=("Arial", 12))
download_button.grid(row=0, column=1, padx=10)

# Populate the initial chord list
on_select_key(None)

# Run the application
root.mainloop()
