
from tkinter import filedialog
from tkinter import IntVar
import requests
from PIL import Image, ImageDraw
from io import BytesIO
import os

import customtkinter
from pytube import YouTube
from moviepy.editor import VideoFileClip


def download_video(url, output_dir, file_format):
    yt = YouTube(url)
    write_to_file(url, output_dir, file_format)
    if int(file_format) == 1:  # MP4 format
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video.download(output_dir)
    elif int(file_format) == 2:  # MP3 format
        audio = yt.streams.filter(progressive=True, file_extension='mp4').first()
        audio_file = audio.download(output_dir)
        mp4_path = os.path.join(output_dir, audio.default_filename)
        mp3_path = os.path.splitext(mp4_path)[0] + '.mp3'

        video_clip = VideoFileClip(mp4_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(mp3_path)

        audio_clip.close()
        video_clip.close()

        os.remove(mp4_path)

def write_to_file(yt_url, output_dir, file_format):
    yt_video = YouTube(yt_url)
    filename = "history.txt"
    try: # We use strip because it can cause whitespaces
        with open(filename, 'a') as file:
            title = yt_video.title.strip()
            author = yt_video.author.strip()
            length = str(yt_video.length).strip()
            publish_date = str(yt_video.publish_date).strip()
            thumbnail_url = yt_video.thumbnail_url.strip()
            video_id = yt_video.video_id.strip()
            url = yt_url.strip()
            format = str(file_format).strip()
            output = output_dir.strip()
            
            file.write(f"{title}  {author}  {length}  {publish_date}  {thumbnail_url}  {video_id}  {url}  {format}  {output}\n")
        print(f"Successfully wrote to {filename}")
    except IOError as e:
        print(f"An I/O error occurred: {e.strerror}")


video_list = []
def read_from_file():
    video_list.clear()
    unique_entries = set()
    filename = "history.txt"
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                elements = line.strip().split("  ")
                if len(elements) >= 9:
                    data = {
                        "title": elements[0],
                        "artist": elements[1],
                        "length": elements[2],
                        "date": elements[3],
                        "image_url": elements[4],
                        "url": elements[6],
                        "format": elements[7],
                        "output": elements[8]
                    }
                    unique_key = (data["url"])
                    if unique_key not in unique_entries:
                        unique_entries.add(unique_key)
                        video_list.append(data)
    except IOError as e:
        print(f"An I/O error occurred: {e.strerror}")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        download_folder.delete(0, "end") 
        download_folder.insert(0, folder_path)

def start_download():
    url = link.get()
    output_dir = download_folder.get()
    format = file_format.get()
    try:
        download_video(url, output_dir, format)
        print("Download completed successfully!")
    except Exception as e:
        print("An error occurred:", e)

def on_button_click(button_name):
    print(f"Button {button_name} clicked!")

def toggle_sidebar():
    if sidebar_frame.winfo_ismapped():
        sidebar_frame.pack_forget()
    else:
        sidebar_frame.pack(side="left", fill="y")

#UI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("700x360")

#SideBar
def sidebar_control(toggle_name):
    if toggle_name == "download":
        history_frame.pack_forget()
        frame.pack(padx=20, pady=20, fill="both", expand=True, side="left")
        root.geometry("700x360")
        print("Download")
    elif toggle_name == "history":
        frame.pack_forget()
        for widget in history_frame.winfo_children():
            widget.destroy()
        history_frame.pack(padx=20, pady=20, fill="both", expand=True, side="left")
        read_from_file()
        for item_data in video_list:
            history_frame_function(item_data)
        root.geometry("1000x360")
        print("History")

sidebar_frame = customtkinter.CTkFrame(root, width=100, corner_radius=0)
sidebar_frame.pack(side="left", fill="y")

logo_label = customtkinter.CTkLabel(sidebar_frame, text="Youtube Download", font=customtkinter.CTkFont(size=18, weight="bold"))
logo_label.pack(padx=20, pady=(20, 10))

sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, text="Download", command=lambda: sidebar_control("download"), fg_color="#f53e31",
                                           font=customtkinter.CTkFont(size=15), width=100)
sidebar_button_1.pack(padx=10, pady=10)

sidebar_button_2 = customtkinter.CTkButton(sidebar_frame, text="History", command=lambda: sidebar_control("history"), fg_color="#f53e31",
                                           font=customtkinter.CTkFont(size=15), width=100)
sidebar_button_2.pack(padx=10, pady=10)

sidebar_button_3 = customtkinter.CTkButton(sidebar_frame, text="Button 3", command=lambda: sidebar_control("b3"), fg_color="#f53e31",
                                           font=customtkinter.CTkFont(size=15), width=100)
sidebar_button_3.pack(padx=10, pady=10)

# Main frame
frame = customtkinter.CTkFrame(master=root)
frame.pack(padx=20, pady=20, fill="both", expand=True, side="left")

label = customtkinter.CTkLabel(master=frame, text="Download Section", corner_radius=100, fg_color="#f53e31", font=customtkinter.CTkFont(size=22, weight="bold"))
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

link = customtkinter.CTkEntry(master=link_frame, placeholder_text="Youtube Link", font=("arial", 18), width=330)
link.pack(side="left", padx=10, pady=10)

toggle_button = customtkinter.CTkButton(master= link_frame, text="=", command=toggle_sidebar, fg_color="#f53e31", font=("arial", 16), width=30)
toggle_button.pack(side="left", padx=10, pady=10)

#Start Button
start_button = customtkinter.CTkButton(master=frame, text="Start", command=start_download, fg_color="#f53e31", font=("arial", 16), width=50)
start_button.pack(padx=10, pady=10)

#History

history_frame = customtkinter.CTkFrame(root)
history_frame.pack(padx=20, pady=20, fill="both", expand=True, side="left")

def history_frame_function(item_data):
    list_frame = customtkinter.CTkFrame(history_frame)
    list_frame.pack(fill="x", padx=10, pady=5)

    try:
        # Get Image
        response = requests.get(item_data["image_url"])
        response.raise_for_status()

        # Convert Image
        image = Image.open(BytesIO(response.content))
        image = image.resize((30, 30), Image.BICUBIC)

        # Round Image
        mask_size = (image.width * 6, image.height * 6)
        mask = Image.new("L", mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask_size[0], mask_size[1]), fill=255)
        mask = mask.resize(image.size, Image.BICUBIC)
        result = Image.new("RGBA", image.size, 0)
        result.paste(image, mask=mask)

        # Apply Image
        ctk_image = customtkinter.CTkImage(result, size=(30, 30))
        ctk_image_label = customtkinter.CTkButton(list_frame, image=ctk_image, fg_color="transparent", corner_radius=100, text="", height=10, width=10, hover_color="#f53e31",
                                        command=lambda: download_video(item_data["url"], item_data["output"], item_data["format"]))
        ctk_image_label.pack(padx=10, pady=10)
        ctk_image_label.pack(side="left")
    except Exception as e:
        print(f"An error occurred while loading image: {e}")

    text_label = customtkinter.CTkLabel(list_frame, text=item_data["title"], font=customtkinter.CTkFont(size=18, weight="bold"))
    text_label.pack(side="left", padx=(0, 5))

    text_label = customtkinter.CTkLabel(list_frame, text=f"from artist {item_data['artist']}", font=customtkinter.CTkFont(size=18))
    text_label.pack(side="left", padx=(0, 10))

    year = item_data["date"]
    text_label = customtkinter.CTkLabel(list_frame, text=f"{year[:4]}", font=customtkinter.CTkFont(size=18, weight="bold"))
    text_label.pack(side="right", padx=(0, 10))

    minutes = int(item_data["length"]) // 60
    seconds = int(item_data["length"]) % 60
    if seconds < 10:
        text_label = customtkinter.CTkLabel(list_frame, text=f"{minutes}:0{seconds}", font=customtkinter.CTkFont(size=18))
    else:
        text_label = customtkinter.CTkLabel(list_frame, text=f"{minutes}:{seconds}", font=customtkinter.CTkFont(size=18))
    text_label.pack(side="right", padx=(0, 20))

root.mainloop()
