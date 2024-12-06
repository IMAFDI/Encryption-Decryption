import tkinter as tk
from tkinter import filedialog, messagebox
from encryption import encrypt_file as encrypt_file_function
from encryption import decrypt_file
from s3_handler import upload_to_s3
import os
import webbrowser
import logging

def start_app():
    # Initialize the main window
    root = tk.Tk()
    root.title("File Encryption & Decryption")
    root.geometry("800x800")  # Set the window size
    root.configure(bg="#2d2f34")  # Set background color

    # Add window icon
    root.iconbitmap("assets/encryption.ico")

    # Set the taskbar icon
    # ico_path = "assets/encryption.ico"  

    # try:
    #     if os.path.exists(ico_path):  
    #         root.iconbitmap(ico_path)
    #     else:
    #         print("No valid icon file found. Default icon will be used.")
    # except Exception as e:
    #     print(f"Error setting icon: {e}")

    title_font = ("Times", 20, "bold")
    text_font = ("Helvetica", 12)
    button_bg = "#4CAF50"
    button_fg = "white"
    frame_bg = "#3e4149"
    label_color = "#ffffff"

    # Create status bar at the bottom
    global status_label
    status_label = tk.Label(root, text="Status: Ready", bg="#333", fg="white", anchor="w", padx=10)
    status_label.pack(fill="x", side="bottom", pady=5)

    # Add a title label
    title_label = tk.Label(root, text="File Encryption & Decryption\n By ABADULLAH FARIDI", font=title_font ,fg=label_color, bg="#2d2f34")
    title_label.pack(pady=20)

    # Create Frames for sections
    encrypt_frame = tk.LabelFrame(root, text="Encrypt a File", font=text_font, fg=label_color, padx=30, pady=30, bg=frame_bg)
    decrypt_frame = tk.LabelFrame(root, text="Decrypt a File", font=text_font, fg=label_color, padx=30, pady=30, bg=frame_bg)
    logs_frame = tk.LabelFrame(root, text="Logs",font=text_font, fg=label_color, padx=20, pady=20, bg=frame_bg)

    encrypt_frame.place(relx=0.5, rely=0.3, anchor='center')
    decrypt_frame.place(relx=0.5, rely=0.6, anchor='center')
    logs_frame.place(relx=0.5, rely=0.8, anchor='center')

    # Encrypt Section
    tk.Label(encrypt_frame, text="Select File to Encrypt:", bg=frame_bg, fg=label_color).grid(row=0, column=0, pady=5, sticky="e")
    encrypt_file_path = tk.StringVar()

    tk.Entry(encrypt_frame, textvariable=encrypt_file_path, width=40).grid(row=0, column=1, padx=5)
    tk.Button(encrypt_frame, text="Browse", command=lambda: browse_file(encrypt_file_path), bg=button_bg, fg=button_fg).grid(row=0, column=2)
    tk.Button(encrypt_frame, text="Encrypt", command=lambda: handle_encryption(root, encrypt_file_path.get()), bg=button_bg, fg=button_fg).grid(row=1, column=1, pady=10)

    # Logs Section
    tk.Label(logs_frame, text=" ", bg=frame_bg, fg=label_color).grid(row=0, column=0, pady=5, sticky="e")
    tk.Button(logs_frame, text="View Logs", command=lambda: show_logs(root), bg=button_bg, fg=button_fg).grid(row=0, column=0, pady=10)

    # Decrypt Section
    tk.Label(decrypt_frame, text="Select File to Decrypt:", bg=frame_bg, fg=label_color).grid(row=0, column=0, pady=10, sticky="e")
    decrypt_file_path = tk.StringVar()

    tk.Entry(decrypt_frame, textvariable=decrypt_file_path, width=40).grid(row=0, column=1, padx=5)
    tk.Button(decrypt_frame, text="Browse", command=lambda: browse_file(decrypt_file_path), bg=button_bg, fg=button_fg).grid(row=0, column=2)
    tk.Button(decrypt_frame, text="Decrypt", command=lambda: handle_decryption(decrypt_file_path.get()), bg=button_bg, fg=button_fg).grid(row=1, column=1, pady=10)

    # Status Bar
    #status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor='w', bg="#f0f0f0")
    #status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()

def browse_file(file_path_var):
    # update the file path variable
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_var.set(file_path)

def update_status(message):
    status_label.config(text=f"Status: {message}")

# Configure logging
logging.basicConfig(
    filename=os.path.join("logs", "activity_logs.txt"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def handle_encryption(root, file_path):
    if not file_path:
        update_status("Please select a file to encrypt!")
        messagebox.showerror("Error", "Please select a file to encrypt!")
        return

    update_status("Encrypting file...")
    encrypted_file, key_file = encrypt_file_function(file_path)

    if encrypted_file:
        logging.info(f"File encrypted: {encrypted_file}")
        # Upload the key file to S3
        key_name_in_s3 = os.path.basename(key_file)
        success, message, download_link = upload_to_s3(key_file, key_name_in_s3)

        if success:
            update_status("Encryption successful!")
            # Create a new window for showing success message and copy link & download link 
            def copy_to_clipboard():
                if download_link:
                    root.clipboard_clear()
                    root.clipboard_append(download_link)
                    root.update()  # Keep the clipboard updated
                    messagebox.showinfo("Copied", "Download link copied to clipboard!")
                else:
                    messagebox.showerror("Error", "No download link available!")

            def open_in_browser():
                if download_link:
                    webbrowser.open(download_link)
                else:
                    messagebox.showerror("Error", "Download link is unavailable!")

            top = tk.Toplevel(root)
            top.title("Encryption Successful")
            top.geometry("500x300")
            top.configure(bg="#3e4149")

            tk.Label(top, text="File encrypted and key uploaded!", font=("Arial", 14, "bold"), fg="white", bg="#3e4149").pack(pady=10)
            tk.Label(top, text=f"Encrypted File: {encrypted_file}", fg="white", bg="#3e4149").pack(pady=5)
            tk.Label(top, text="Key Download Link:", fg="white", bg="#3e4149").pack(pady=5)

            # Display the link in an entry widget
            link_label = tk.Entry(top, width=50, font=("Arial", 10))
            link_label.insert(0, download_link)
            link_label.config(state="readonly")  # Make it non-editable
            link_label.pack(pady=5)

            # Buttons for copying the link and opening in browser
            tk.Button(top, text="Copy Link", command=copy_to_clipboard, bg="#4CAF50", fg="white").pack(pady=10)
            tk.Button(top, text="Download Key", command=open_in_browser, bg="#4CAF50", fg="white").pack(pady=10)

        else:
            update_status(f"File encrypted but key upload failed: {message}")
            messagebox.showwarning(
                "Warning",
                f"File encrypted but key upload failed: {message}"
            )
    else:
        update_status(f"Encryption failed! {key_file}")
        messagebox.showerror("Error", f"Encryption failed! {key_file}")

def handle_decryption(file_path):
    if not file_path:
        update_status("Please select a file to decrypt!")
        messagebox.showerror("Error", "Please select a file to decrypt!")
        return

    update_status("Decrypting file...")
    key_file = filedialog.askopenfilename(title="Select Key File", filetypes=(("Key Files", "*.key"), ("All Files", "*.*")))
    if not key_file:
        update_status("Key file is required to decrypt!")
        messagebox.showerror("Error", "Key file is required to decrypt!")
        return

    decrypted_file, error = decrypt_file(file_path, key_file)

    if decrypted_file:
        update_status(f"Decryption successful! Decrypted File: {decrypted_file}")
        messagebox.showinfo("Success", f"File decrypted successfully!\nDecrypted File: {decrypted_file}")
    else:
        update_status(f"Decryption failed: {error}")
        messagebox.showerror("Error", f"Decryption failed! {error}")

    if decrypted_file:
        logging.info(f"File decrypted: {file_path} -> {decrypted_file}")
    else:
        logging.error(f"Decryption failed for file: {file_path}")

def show_logs(root):
    try:
        log_file_path = os.path.join("logs", "activity_logs.txt")
        with open(log_file_path, "r") as log_file:
            logs = log_file.read()

        # Create a new window to display logs
        top = tk.Toplevel(root)
        top.title("Logs")
        top.geometry("600x500")
        top.configure(bg="#2d2f34")

        # Text widget for logs
        text_widget = tk.Text(top, wrap="word", bg="#1c1e22", fg="white", font=("Helvetica", 12))
        text_widget.insert("1.0", logs)
        text_widget.configure(state="disabled")
        text_widget.pack(fill="both", expand=True)

        # Clear logs in both UI and log file
        def clear_logs():
            # Clear the text widget
            text_widget.configure(state="normal")  # Enable editing
            text_widget.delete("1.0", tk.END)      # Clear all content
            text_widget.configure(state="disabled")  # Disable editing again

            # Clear the log file
            with open(log_file_path, "w") as log_file:
                log_file.write("")  # Overwrite the log file with an empty string

        refresh_button = tk.Button(
            top,
            text="Clear Logs",
            command=clear_logs,
            bg="#4CAF50",
            fg="white"
        )
        refresh_button.pack(pady=10)

    except FileNotFoundError:
        messagebox.showerror("Error", "Log file not found!")

# Start the application
#start_app()
