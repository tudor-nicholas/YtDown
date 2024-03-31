import customtkinter
from tkinter import filedialog
from pytube import YouTube

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def download_video(url, output_dir):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    video.download(output_dir)

root = customtkinter.CTk()
root.geometry("500x320")

frame = customtkinter.CTkFrame(master=root)
frame.pack(padx="20", pady="20", fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Youtube Download", corner_radius=100, fg_color="#f53e31", font=("impact", 26))
label.pack(padx=10, pady=20, anchor="center")

folder_frame = customtkinter.CTkFrame(master=frame)
folder_frame.pack(padx=10, pady=10)

download_folder = customtkinter.CTkEntry(master=folder_frame, placeholder_text="Folder", font=("arial", 18), width=300)
download_folder.pack(side="left", padx=10, pady=10)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        download_folder.delete(0, "end")  # Clear any existing text
        download_folder.insert(0, folder_path)  # Insert selected folder path into the entry widget

select_button = customtkinter.CTkButton(master=folder_frame, text="Select", command=select_folder, fg_color="#f53e31", font=("arial", 16), width=50)
select_button.pack(side="left", padx=10, pady=10)

link_frame = customtkinter.CTkFrame(master=frame)
link_frame.pack(padx=10, pady=10)

link = customtkinter.CTkEntry(master=link_frame, placeholder_text="Youtube Link", font=("arial", 18), width=380)
link.pack(padx=10, pady=10)

def start_download():
    url = link.get()
    output_dir = download_folder.get()
    try:
        download_video(url, output_dir)
        print("Download completed successfully!")
    except Exception as e:
        print("An error occurred:", e)

start_button = customtkinter.CTkButton(master=frame, text="Start", command=start_download, fg_color="#f53e31", font=("arial", 16), width=50)
start_button.pack(padx=10, pady=10)

root.mainloop()