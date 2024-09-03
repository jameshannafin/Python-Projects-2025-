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

# Function to play the generated sound using pyaudio
def play_wave(wave, sample_rate=44100):
    try:
        print("Playing sound...")
        audio = (wave * 32767).astype(np.int16).tobytes()
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)
        stream.write(audio)
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Sound playback finished.")
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function to save sound to a .wav file
def save_wave(wave, filename, sample_rate=44100):
    try:
        audio = (wave * 32767).astype(np.int16)
        audio_segment = AudioSegment(audio.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
        audio_segment.export(filename, format='wav')
        print(f"Sound saved as '{filename}'")
    except Exception as e:
        print(f"Error saving sound: {e}")

# Function to handle the sound generation when the button is clicked
def generate_sound():
    try:
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave_type = wave_var.get()

        if wave_type == "Sine":
            wave = generate_sine_wave(frequency, duration)
        elif wave_type == "Square":
            wave = generate_square_wave(frequency, duration)
        elif wave_type == "Noise":
            wave = generate_noise(duration)

        print("Generating sound...")
        threading.Thread(target=play_wave, args=(wave,)).start()
        print("Sound generation complete.")
    except Exception as e:
        print(f"Error generating sound: {e}")

# Function to handle exporting the sound to a .wav file
def export_sound():
    try:
        frequency = float(frequency_entry.get())
        duration = float(duration_entry.get())
        wave_type = wave_var.get()

        if wave_type == "Sine":
            wave = generate_sine_wave(frequency, duration)
        elif wave_type == "Square":
            wave = generate_square_wave(frequency, duration)
        elif wave_type == "Noise":
            wave = generate_noise(duration)

        # Create the directory if it doesn't exist
        directory = "created_sounds"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Determine the file name
        base_filename = os.path.join(directory, "generated_sound")
        extension = ".wav"
        filename = base_filename + extension
        counter = 1

        # Check if the file exists and increment the counter if it does
        while os.path.exists(filename):
            filename = f"{base_filename}_{counter}{extension}"
            counter += 1

        save_wave(wave, filename)
        print(f"Sound saved as '{filename}'")
        update_file_list()
    except Exception as e:
        print(f"Error exporting sound: {e}")

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
        new_name = (rename_entry.get())+".wav"
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

# Function to generate a square wave
def generate_square_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    return wave

# Function to generate white noise
def generate_noise(duration, sample_rate=44100, amplitude=0.5):
    wave = amplitude * np.random.uniform(-1, 1, int(sample_rate * duration))
    return wave

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

# Dropdown menu for selecting waveform type
ttk.Label(root, text="Waveform Type:").pack(pady=5)
wave_var = tk.StringVar(value="Sine")
waveform_menu = ttk.OptionMenu(root, wave_var, "Sine", "Sine", "Square", "Noise")
waveform_menu.pack(pady=5)

# Button to generate and play the sound
generate_button = ttk.Button(root, text="Generate Sound", command=generate_sound)
generate_button.pack(pady=20)

# Button to export the generated sound to a .wav file
export_button = ttk.Button(root, text="Export Sound", command=export_sound)
export_button.pack(pady=20)

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
