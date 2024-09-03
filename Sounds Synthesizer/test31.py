import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pyaudio
import threading
from pydub import AudioSegment
import os

# Function to generate a sine wave
def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

# Function to generate a square wave
def generate_square_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    return wave

# Function to generate white noise
def generate_noise(duration, sample_rate=44100, amplitude=0.5):
    wave = amplitude * np.random.uniform(-1, 1, int(sample_rate * duration))
    return wave

# Function to play the generated sound using pyaudio
def play_wave(wave, sample_rate=44100):
    try:
        audio = (wave * 32767).astype(np.int16).tobytes()
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)
        stream.write(audio)
        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function to save sound to a .wav file
def save_wave(wave, filename, sample_rate=44100):
    try:
        audio = (wave * 32767).astype(np.int16)
        audio_segment = AudioSegment(audio.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
        audio_segment.export(filename, format='wav')
    except Exception as e:
        print(f"Error saving sound: {e}")

# Function to handle the sound generation when the button is clicked
def generate_sound(wave_type, frequency, duration):
    if wave_type == "Sine":
        return generate_sine_wave(frequency, duration)
    elif wave_type == "Square":
        return generate_square_wave(frequency, duration)
    elif wave_type == "Noise":
        return generate_noise(duration)

# Function to handle exporting the sound to a .wav file
def export_sound(waves, filename):
    combined = sum(waves)
    save_wave(combined, filename)

# Function to update the file list in the GUI
def update_file_list():
    file_listbox.delete(0, tk.END)
    directory = "created_sounds"
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_listbox.insert(tk.END, filename)

# Function to rename the selected file
def rename_file():
    try:
        selected_file = file_listbox.get(tk.ACTIVE)
        new_name = rename_entry.get()
        if selected_file and new_name:
            old_path = os.path.join("created_sounds", selected_file)
            new_path = os.path.join("created_sounds", new_name)
            os.rename(old_path, new_path)
            update_file_list()
            rename_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Renamed '{selected_file}' to '{new_name}'")
    except Exception as e:
        messagebox.showerror("Error", f"Error renaming file: {e}")

# Function to delete the selected file
def delete_file():
    try:
        selected_file = file_listbox.get(tk.ACTIVE)
        if selected_file:
            file_path = os.path.join("created_sounds", selected_file)
            os.remove(file_path)
            update_file_list()
            messagebox.showinfo("Success", f"Deleted '{selected_file}'")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting file: {e}")

# Function to play all sounds
def play_all_sounds():
    for wave_type in ["Sine", "Square", "Noise"]:
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave = generate_sound(wave_type, frequency, duration)
        threading.Thread(target=play_wave, args=(wave,)).start()

# Function to generate and export all sounds
def generate_and_export_all_sounds():
    waves = []
    for wave_type in ["Sine", "Square", "Noise"]:
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave = generate_sound(wave_type, frequency, duration)
        waves.append(wave)

    # Create the directory if it doesn't exist
    directory = "created_sounds"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Determine the file name
    base_filename = os.path.join(directory, "combined_sound")
    extension = ".wav"
    filename = base_filename + extension
    counter = 1

    # Check if the file exists and increment the counter if it does
    while os.path.exists(filename):
        filename = f"{base_filename}_{counter}{extension}"
        counter += 1

    export_sound(waves, filename)
    update_file_list()

# Function to play checked sounds
def play_checked_sounds():
    if sine_var.get():
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave = generate_sound("Sine", frequency, duration)
        threading.Thread(target=play_wave, args=(wave,)).start()
    if square_var.get():
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave = generate_sound("Square", frequency, duration)
        threading.Thread(target=play_wave, args=(wave,)).start()
    if noise_var.get():
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave = generate_sound("Noise", frequency, duration)
        threading.Thread(target=play_wave, args=(wave,)).start()

# Function to generate and export checked sounds
def generate_and_export_checked_sounds():
    waves = []
    if sine_var.get():
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave = generate_sound("Sine", frequency, duration)
        waves.append(wave)
    if square_var.get():
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave = generate_sound("Square", frequency, duration)
        waves.append(wave)
    if noise_var.get():
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave = generate_sound("Noise", frequency, duration)
        waves.append(wave)

    # Create the directory if it doesn't exist
    directory = "created_sounds"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Determine the file name
    base_filename = os.path.join(directory, "combined_sound")
    extension = ".wav"
    filename = base_filename + extension
    counter = 1

    # Check if the file exists and increment the counter if it does
    while os.path.exists(filename):
        filename = f"{base_filename}_{counter}{extension}"
        counter += 1

    export_sound(waves, filename)
    update_file_list()

# Create the main application window using Tkinter
root = tk.Tk()
root.title("Game SFX Synthesizer")
root.geometry("600x600")

# Set up GUI controls for frequency input
ttk.Label(root, text="Frequency (Hz):").pack(pady=5)
frequency_entry = ttk.Entry(root)
frequency_entry.insert(0, "440")
frequency_entry.pack(pady=5)

# Set up GUI controls for duration input
ttk.Label(root, text="Duration (s):").pack(pady=5)
duration_entry = ttk.Entry(root)
duration_entry.insert(0, "1")
duration_entry.pack(pady=5)

# Checkbuttons for selecting sounds to play or generate
sine_var = tk.BooleanVar()
square_var = tk.BooleanVar()
noise_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Sine", variable=sine_var).pack(pady=5)
ttk.Checkbutton(root, text="Square", variable=square_var).pack(pady=5)
ttk.Checkbutton(root, text="Noise", variable=noise_var).pack(pady=5)

# Button to play all sounds
play_all_button = ttk.Button(root, text="Play All Sounds", command=play_all_sounds)
play_all_button.pack(pady=5)

# Button to play checked sounds
play_checked_button = ttk.Button(root, text="Play Checked Sounds", command=play_checked_sounds)
play_checked_button.pack(pady=5)

# Button to generate and export all sounds
generate_export_all_button = ttk.Button(root, text="Generate and Export All Sounds", command=generate_and_export_all_sounds)
generate_export_all_button.pack(pady=5)

# Button to generate and export checked sounds
generate_export_checked_button = ttk.Button(root, text="Generate and Export Checked Sounds", command=generate_and_export_checked_sounds)
generate_export_checked_button.pack(pady=5)

# Listbox to display files in the created_sounds folder
ttk.Label(root, text="Files in 'created_sounds' folder:").pack(pady=5)
file_listbox = tk.Listbox(root)
file_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

# Entry and button to rename the selected file
ttk.Label(root, text="Rename selected file to:").pack(pady=5)
rename_entry = ttk.Entry(root)
rename_entry.pack(pady=5)
rename_button = ttk.Button(root, text="Rename File", command=rename_file)
rename_button.pack(pady=5)

# Button to delete the selected file
delete_button = ttk.Button(root, text="Delete File", command=delete_file)
delete_button.pack(pady=5)

# Update the file list when the application starts
update_file_list()

# Start the main event loop
root.mainloop()
