import customtkinter
from tkinter import filedialog
from tkinter import IntVar
from pytube import YouTube
import os
import youtube_dl

def is_youtube_music_link(url):
    return "music.youtube.com" in url

def download_video(url, output_dir, file_format):
    yt = YouTube(url)
    if file_format.get() == 1:  # MP4 format
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video.download(output_dir)
    elif file_format.get() == 2:  # MP3 format
        if is_youtube_music_link(url):
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        else:
            audio = yt.streams.filter(only_audio=True).first()
            audio_file = audio.download(output_dir)
            mp4_path = os.path.join(output_dir, audio.default_filename)
            mp3_path = os.path.splitext(mp4_path)[0] + '.mp3'
            os.rename(mp4_path, mp3_path)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        download_folder.delete(0, "end")  # Clear any existing text
        download_folder.insert(0, folder_path)  # Insert selected folder path into the entry widget

def start_download():
    url = link.get()
    output_dir = download_folder.get()
    try:
        download_video(url, output_dir, file_format)
        print("Download completed successfully!")
    except Exception as e:
        print("An error occurred:", e)

#UI
#Main Frame
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x360")

frame = customtkinter.CTkFrame(master=root)
frame.pack(padx="20", pady="20", fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Youtube Download", corner_radius=100, fg_color="#f53e31", font=("impact", 26))
label.pack(padx=10, pady=20, anchor="center")

file_format = IntVar()
file_format.set(1)

#Radio Buttons
radio_frame = customtkinter.CTkFrame(master=frame)
radio_frame.pack(padx=10, pady=10)

mp4_radio = customtkinter.CTkRadioButton(master=radio_frame, text="MP4", variable=file_format, value=1, font=("arial", 16))
mp4_radio.pack(side="left", padx=(20,0), pady=10, anchor="center")

mp3_radio = customtkinter.CTkRadioButton(master=radio_frame, text="MP3", variable=file_format, value=2, font=("arial", 16))
mp3_radio.pack(side="left", pady=10, anchor="center")

#Floder Section
folder_frame = customtkinter.CTkFrame(master=frame)
folder_frame.pack(padx=10, pady=10)

download_folder = customtkinter.CTkEntry(master=folder_frame, placeholder_text="Folder", font=("arial", 18), width=300)
download_folder.pack(side="left", padx=10, pady=10)

select_button = customtkinter.CTkButton(master=folder_frame, text="Select", command=select_folder, fg_color="#f53e31", font=("arial", 16), width=50)
select_button.pack(side="left", padx=10, pady=10)

#Link Section
link_frame = customtkinter.CTkFrame(master=frame)
link_frame.pack(padx=10, pady=10)

link = customtkinter.CTkEntry(master=link_frame, placeholder_text="Youtube Link", font=("arial", 18), width=380)
link.pack(padx=10, pady=10)

#Start Button
start_button = customtkinter.CTkButton(master=frame, text="Start", command=start_download, fg_color="#f53e31", font=("arial", 16), width=50)
start_button.pack(padx=10, pady=10)

root.mainloop()