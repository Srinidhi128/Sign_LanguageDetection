import tkinter as tk
from tkinter import ttk, scrolledtext
from googletrans import Translator
import customtkinter as ctk
from PIL import Image, ImageTk

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Dictionary mapping language codes to full language names
LANGUAGES = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'ko': 'Korean',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'mk': 'Macedonian',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'no': 'Norwegian',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sr': 'Serbian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'yi': 'Yiddish'
}

def translate():
    """Translate text from input to selected language"""
    # Get the selected language code from the language name
    selected_language_name = language_var.get()
    lang_code = [code for code, name in LANGUAGES.items() if name == selected_language_name][0]
    
    # Get input text
    text = input_text.get("1.0", "end-1c")
    if not text.strip():
        output_text.delete("1.0", "end")
        output_text.insert("1.0", "Please enter some text to translate")
        return
    
    try:
        # Create translator and translate
        translator = Translator()
        translation = translator.translate(text, dest=lang_code)
        
        # Display translation
        output_text.delete("1.0", "end")
        output_text.insert("1.0", translation.text)
        
        # Show success message
        status_label.configure(text=f"Successfully translated to {selected_language_name}", 
                               text_color="green")
    except Exception as e:
        status_label.configure(text=f"Translation error: {str(e)}", 
                               text_color="red")

def swap_languages():
    """Swap input and output text"""
    input_content = input_text.get("1.0", "end-1c")
    output_content = output_text.get("1.0", "end-1c")
    
    input_text.delete("1.0", "end")
    input_text.insert("1.0", output_content)
    
    output_text.delete("1.0", "end")
    output_text.insert("1.0", input_content)

def clear_text():
    """Clear both input and output text fields"""
    input_text.delete("1.0", "end")
    output_text.delete("1.0", "end")
    status_label.configure(text="Ready to translate", text_color="white")

# Create the main application window
app = ctk.CTk()
app.title("Advanced Language Translator")
app.geometry("900x600")
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)

# Create header frame
header_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))

title_label = ctk.CTkLabel(header_frame, text="Language Translator", 
                          font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(pady=10)

# Create control frame
control_frame = ctk.CTkFrame(app, corner_radius=10)
control_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
control_frame.grid_columnconfigure((0, 1, 2), weight=1)

# Language selection
language_var = ctk.StringVar(value="Spanish")  # Default language
language_names = sorted(list(LANGUAGES.values()))
language_label = ctk.CTkLabel(control_frame, text="Translate to:", 
                             font=ctk.CTkFont(size=14))
language_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

language_dropdown = ctk.CTkOptionMenu(control_frame, values=language_names, 
                                     variable=language_var, 
                                     width=200,
                                     font=ctk.CTkFont(size=14))
language_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Buttons frame
buttons_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
buttons_frame.grid(row=0, column=2, padx=10, pady=10)

translate_button = ctk.CTkButton(buttons_frame, text="Translate", 
                                command=translate, 
                                font=ctk.CTkFont(size=14, weight="bold"),
                                width=120, height=40)
translate_button.pack(side="left", padx=5)

swap_button = ctk.CTkButton(buttons_frame, text="Swap", 
                           command=swap_languages,
                           font=ctk.CTkFont(size=14),
                           width=80, height=40)
swap_button.pack(side="left", padx=5)

clear_button = ctk.CTkButton(buttons_frame, text="Clear", 
                            command=clear_text,
                            font=ctk.CTkFont(size=14),
                            width=80, height=40,
                            fg_color="#D35B58", hover_color="#C77C78")
clear_button.pack(side="left", padx=5)

# Input and output frames
input_frame = ctk.CTkFrame(app, corner_radius=10)
input_frame.grid(row=2, column=0, padx=(20, 10), pady=(10, 20), sticky="nsew")

output_frame = ctk.CTkFrame(app, corner_radius=10)
output_frame.grid(row=2, column=1, padx=(10, 20), pady=(10, 20), sticky="nsew")

# Configure frames to expand
input_frame.grid_rowconfigure(1, weight=1)
input_frame.grid_columnconfigure(0, weight=1)
output_frame.grid_rowconfigure(1, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

# Input area
input_label = ctk.CTkLabel(input_frame, text="Enter Text:", 
                          font=ctk.CTkFont(size=16, weight="bold"))
input_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

input_text = ctk.CTkTextbox(input_frame, font=ctk.CTkFont(size=14), wrap="word", height=400)
input_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

# Output area
output_label = ctk.CTkLabel(output_frame, text="Translation:", 
                           font=ctk.CTkFont(size=16, weight="bold"))
output_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

output_text = ctk.CTkTextbox(output_frame, font=ctk.CTkFont(size=14), wrap="word", height=400)
output_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

# Status label
status_frame = ctk.CTkFrame(app, fg_color="transparent")
status_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))

status_label = ctk.CTkLabel(status_frame, text="Ready to translate", 
                           font=ctk.CTkFont(size=14))
status_label.pack(pady=5)

# Start the application
app.mainloop()
