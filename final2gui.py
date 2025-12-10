import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
import threading
import subprocess
import os
import sys
import platform

SCRIPT_NAME = os.path.join(os.path.dirname(__file__), "final2cli.py")

VOICE_OPTIONS = {
    "Hindi (hi-IN-SwaraNeural)": "hi-IN-SwaraNeural",
    "Telugu (te-IN-ShrutiNeural)": "te-IN-ShrutiNeural",
    "Kannada (kn-IN-SapnaNeural)": "kn-IN-SapnaNeural",
    "Tamil (ta-IN-PallaviNeural)": "ta-IN-PallaviNeural",
    "Malayalam (ml-IN-SobhanaNeural)": "ml-IN-SobhanaNeural",
    "Gujarati (gu-IN-DhwaniNeural)": "gu-IN-DhwaniNeural",
    "English India (en-IN-NeerjaNeural)": "en-IN-NeerjaNeural",
    "English US (en-US-AriaNeural)": "en-US-AriaNeural",
    "English UK (en-GB-LibbyNeural)": "en-GB-LibbyNeural",
    "Hindi (hi-IN-MadhurNeural)": "hi-IN-MadhurNeural",
    "Telugu (te-IN-MohanNeural)": "te-IN-MohanNeural",
    "Kannada (kn-IN-GaganNeural)": "kn-IN-GaganNeural",
    "Tamil (ta-IN-ValluvarNeural)": "ta-IN-ValluvarNeural",
    "Malayalam (ml-IN-MidhunNeural)": "ml-IN-MidhunNeural",
    "English US (en-US-GuyNeural)": "en-US-GuyNeural",
    "English Neutral (en-AU-NatashaNeural)": "en-AU-NatashaNeural",
    "Hindi (hi-IN-KalpanaNeural)": "hi-IN-KalpanaNeural",
    "English (en-IE-EmilyNeural)": "en-IE-EmilyNeural",
    "English (en-KE-AsiliaNeural)": "en-KE-AsiliaNeural",
    "English (en-NZ-MitchellNeural)": "en-NZ-MitchellNeural",
    "English (en-ZA-LeahNeural)": "en-ZA-LeahNeural",
    "Arabic (ar-AE-FatimaNeural)": "ar-AE-FatimaNeural",
    "Spanish (es-ES-ElviraNeural)": "es-ES-ElviraNeural",
    "French (fr-FR-DeniseNeural)": "fr-FR-DeniseNeural",
    "German (de-DE-KatjaNeural)": "de-DE-KatjaNeural",
    "Japanese (ja-JP-NanamiNeural)": "ja-JP-NanamiNeural",
    "Chinese (zh-CN-XiaoxiaoNeural)": "zh-CN-XiaoxiaoNeural",
}

VIDEO_PRESETS = {
    "Instagram Reel (720x1280)": (720, 1280),
    "YouTube Shorts (1080x1920)": (1080, 1920),
    "Square (1080x1080)": (1080, 1080),
}

BG_COLOR = "#f5f7fa"
INPUT_BG = "#ffffff"
ACCENT_COLOR = "#ff6f91"
ACCENT_HOVER = "#ff4b6e"
TEXT_COLOR = "#444444"
LOG_BG = "#e1e8f0"
LOG_TEXT_COLOR = "#2c3e50"
BTN_TEXT_COLOR = "white"

FONT_DEFAULT = ("Segoe UI", 11)
FONT_HEADER = ("Segoe UI", 20, "bold")
FONT_LOG = ("Consolas", 10)


class CoolieReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎥 Coolie Review Video Generator")
        self.root.geometry("1150x800")
        self.root.minsize(950, 700)
        self.root.configure(bg=BG_COLOR)

        self.font_color = "#000000"
        self.box_color = "#ffffff"
        self.shadow_color = "#000000"
        self.progress_color = "#ffffff"

        self.process = None
        self.process_thread = None

        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_DEFAULT)
        style.configure("Header.TLabel", font=FONT_HEADER, background=BG_COLOR, foreground="#222222")
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TButton", background=ACCENT_COLOR, foreground=BTN_TEXT_COLOR, font=FONT_DEFAULT, padding=8)
        style.map("TButton", background=[("active", ACCENT_HOVER), ("pressed", ACCENT_HOVER)])

        style.configure("TEntry", padding=6, relief="flat", font=FONT_DEFAULT, foreground=TEXT_COLOR)
        style.configure("TCombobox", padding=6, relief="flat", font=FONT_DEFAULT, foreground=TEXT_COLOR)

        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=BG_COLOR,
            bordercolor=BG_COLOR,
            background=ACCENT_COLOR,
            thickness=18,
        )

    def create_widgets(self):
        header = ttk.Label(self.root, text="Coolie Review Generator", style="Header.TLabel")
        header.pack(pady=(20, 15))

        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=25, pady=(0, 10))

        left_frame = tk.Frame(main_frame, bg=BG_COLOR)
        right_frame = tk.Frame(main_frame, bg=BG_COLOR)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right_frame.pack(side="left", fill="both", expand=True)

        # ---------- LEFT: files + a few basic globals ----------
        row = 0
        self.review_path = self.create_file_picker(left_frame, "Review Text File (.txt)", row)
        row += 1
        self.bg_image = self.create_file_picker(left_frame, "Background Image / Folder (optional)", row)
        row += 1
        self.logo_image = self.create_file_picker(left_frame, "Logo Image (optional)", row)
        row += 1
        self.bg_music = self.create_file_picker(left_frame, "Background Music (optional)", row)
        row += 1
        self.font_file = self.create_file_picker(left_frame, "Font File (.ttf)", row)
        row += 1
        self.output_file = self.create_save_picker(left_frame, "Output Video File (.mp4)", row)
        row += 1

        ttk.Separator(left_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=(5, 10)
        )
        row += 1

        ttk.Label(left_frame, text="Video Size Preset").grid(row=row, column=0, sticky="w", pady=(0, 6))
        self.video_preset_var = tk.StringVar(value="Instagram Reel (720x1280)")
        preset_names = list(VIDEO_PRESETS.keys())
        self.video_preset_dropdown = ttk.Combobox(
            left_frame,
            values=preset_names,
            state="readonly",
            textvariable=self.video_preset_var,
            width=25,
        )
        self.video_preset_dropdown.grid(row=row, column=1, sticky="ew", pady=(0, 6))
        row += 1

        ttk.Label(left_frame, text="Min Slide Duration (sec, 0 = auto)").grid(
            row=row, column=0, sticky="w", pady=(0, 6)
        )
        self.min_duration_entry = ttk.Entry(left_frame, width=20)
        self.min_duration_entry.insert(0, "0")
        self.min_duration_entry.grid(row=row, column=1, sticky="ew", pady=(0, 6))
        row += 1

        self.progress_enable_var = tk.BooleanVar(value=False)
        self.progress_check = tk.Checkbutton(
            left_frame,
            text="Enable Progress Bar",
            variable=self.progress_enable_var,
            bg=BG_COLOR,
            anchor="w",
        )
        self.progress_check.grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 6))
        row += 1

        for i in range(3):
            left_frame.columnconfigure(i, weight=1)

        # ---------- RIGHT: Notebook with styling + advanced ----------
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        notebook = ttk.Notebook(right_frame)
        notebook.grid(row=0, column=0, sticky="nsew")

        basic_frame = tk.Frame(notebook, bg=BG_COLOR)
        advanced_frame = tk.Frame(notebook, bg=BG_COLOR)
        notebook.add(basic_frame, text="Basic")
        notebook.add(advanced_frame, text="Advanced")

        # BASIC TAB
        row = 0
        ttk.Label(basic_frame, text="Voice / Language").grid(row=row, column=0, sticky="w", pady=(8, 4))
        self.voice_var = tk.StringVar(value="Hindi (hi-IN-SwaraNeural)")
        voice_names = list(VOICE_OPTIONS.keys())
        self.voice_dropdown = ttk.Combobox(
            basic_frame, values=voice_names, state="readonly", textvariable=self.voice_var, width=32
        )
        self.voice_dropdown.grid(row=row, column=1, sticky="ew", pady=(8, 4))
        row += 1

        ttk.Label(basic_frame, text="TTS Speaking Rate (e.g. +10%, -5%)").grid(
            row=row, column=0, sticky="w", pady=(4, 4)
        )
        self.rate_entry = ttk.Entry(basic_frame, width=34)
        self.rate_entry.insert(0, "+10%")
        self.rate_entry.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        ttk.Label(basic_frame, text="Font Size").grid(row=row, column=0, sticky="w", pady=(4, 4))
        self.font_size_var = tk.IntVar(value=60)
        self.font_size_dropdown = ttk.Combobox(
            basic_frame,
            values=[20, 30, 40, 50, 60, 70, 80, 90, 100],
            textvariable=self.font_size_var,
            state="readonly",
            width=10,
        )
        self.font_size_dropdown.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        ttk.Label(basic_frame, text="Font Color").grid(row=row, column=0, sticky="w", pady=(4, 4))
        self.font_color_btn = tk.Button(
            basic_frame,
            text="Choose Font Color",
            command=self.choose_font_color,
            bg=self.font_color,
            fg="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            activebackground=ACCENT_HOVER,
            cursor="hand2",
            bd=0,
            padx=8,
            pady=4,
        )
        self.font_color_btn.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        ttk.Label(basic_frame, text="Text Box Background Color").grid(row=row, column=0, sticky="w", pady=(4, 4))
        self.box_color_btn = tk.Button(
            basic_frame,
            text="Choose Box Color",
            command=self.choose_box_color,
            bg=self.box_color,
            fg="#333",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            activebackground=ACCENT_HOVER,
            cursor="hand2",
            bd=0,
            padx=8,
            pady=4,
        )
        self.box_color_btn.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        ttk.Label(basic_frame, text="Text Box Transparency (0-255)").grid(
            row=row, column=0, sticky="w", pady=(4, 4)
        )
        self.alpha_entry = ttk.Entry(basic_frame, width=34)
        self.alpha_entry.insert(0, "160")
        self.alpha_entry.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        ttk.Label(basic_frame, text="Style Preset").grid(row=row, column=0, sticky="w", pady=(4, 4))
        self.style_var = tk.StringVar(value="default")
        self.style_dropdown = ttk.Combobox(
            basic_frame,
            values=["default", "caption", "subtitle"],
            state="readonly",
            textvariable=self.style_var,
            width=32,
        )
        self.style_dropdown.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        ttk.Label(basic_frame, text="Text Position").grid(row=row, column=0, sticky="w", pady=(4, 4))
        self.text_position_var = tk.StringVar(value="center")
        self.text_position_dropdown = ttk.Combobox(
            basic_frame,
            values=["center", "top", "bottom"],
            state="readonly",
            textvariable=self.text_position_var,
            width=32,
        )
        self.text_position_dropdown.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        self.shadow_enable_var = tk.BooleanVar(value=False)
        self.shadow_check = tk.Checkbutton(
            basic_frame,
            text="Enable Text Shadow",
            variable=self.shadow_enable_var,
            bg=BG_COLOR,
            anchor="w",
        )
        self.shadow_check.grid(row=row, column=0, columnspan=2, sticky="w", pady=(4, 4))
        row += 1

        ttk.Label(basic_frame, text="Logo Position").grid(row=row, column=0, sticky="w", pady=(4, 4))
        self.logo_position_var = tk.StringVar(value="top-center")
        self.logo_position_dropdown = ttk.Combobox(
            basic_frame,
            values=["top-center", "top-left", "top-right", "bottom-center", "bottom-left", "bottom-right"],
            state="readonly",
            textvariable=self.logo_position_var,
            width=32,
        )
        self.logo_position_dropdown.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        ttk.Label(basic_frame, text="Logo Opacity (0.1–1.0)").grid(row=row, column=0, sticky="w", pady=(4, 4))
        self.logo_opacity_var = tk.DoubleVar(value=1.0)
        self.logo_opacity_scale = tk.Scale(
            basic_frame,
            from_=0.1,
            to=1.0,
            resolution=0.05,
            orient="horizontal",
            variable=self.logo_opacity_var,
            bg=BG_COLOR,
            highlightthickness=0,
        )
        self.logo_opacity_scale.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        basic_frame.columnconfigure(1, weight=1)

        # ADVANCED TAB
        row = 0
        ttk.Label(advanced_frame, text="Shadow Color").grid(row=row, column=0, sticky="w", pady=(8, 4))
        self.shadow_color_btn = tk.Button(
            advanced_frame,
            text="Choose Shadow Color",
            command=self.choose_shadow_color,
            bg=self.shadow_color,
            fg="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            activebackground=ACCENT_HOVER,
            cursor="hand2",
            bd=0,
            padx=8,
            pady=4,
        )
        self.shadow_color_btn.grid(row=row, column=1, sticky="ew", pady=(8, 4))
        row += 1

        ttk.Label(advanced_frame, text="Shadow Offset X / Y").grid(row=row, column=0, sticky="w", pady=(4, 4))
        offset_frame = tk.Frame(advanced_frame, bg=BG_COLOR)
        offset_frame.grid(row=row, column=1, sticky="w", pady=(4, 4))
        self.shadow_offset_x_entry = ttk.Entry(offset_frame, width=6)
        self.shadow_offset_x_entry.insert(0, "2")
        self.shadow_offset_x_entry.pack(side="left", padx=(0, 5))
        self.shadow_offset_y_entry = ttk.Entry(offset_frame, width=6)
        self.shadow_offset_y_entry.insert(0, "2")
        self.shadow_offset_y_entry.pack(side="left")
        row += 1

        ttk.Label(advanced_frame, text="Progress Bar Color").grid(row=row, column=0, sticky="w", pady=(8, 4))
        self.progress_color_btn = tk.Button(
            advanced_frame,
            text="Choose Progress Color",
            command=self.choose_progress_color,
            bg=self.progress_color,
            fg="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            activebackground=ACCENT_HOVER,
            cursor="hand2",
            bd=0,
            padx=8,
            pady=4,
        )
        self.progress_color_btn.grid(row=row, column=1, sticky="ew", pady=(8, 4))
        row += 1

        ttk.Label(advanced_frame, text="Progress Bar Height (px)").grid(row=row, column=0, sticky="w", pady=(4, 4))
        self.progress_height_entry = ttk.Entry(advanced_frame, width=34)
        self.progress_height_entry.insert(0, "6")
        self.progress_height_entry.grid(row=row, column=1, sticky="ew", pady=(4, 4))
        row += 1

        advanced_frame.columnconfigure(1, weight=1)

        # Buttons + progress bar
        btn_frame = tk.Frame(right_frame, bg=BG_COLOR)
        btn_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        self.start_button = tk.Button(
            btn_frame,
            text="Generate Video",
            command=self.start_process,
            bg=ACCENT_COLOR,
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            activebackground=ACCENT_HOVER,
            cursor="hand2",
            bd=0,
            padx=10,
            pady=8,
        )
        self.start_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.cancel_button = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.cancel_process,
            bg="#bbbbbb",
            fg="#333333",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            activebackground="#aaaaaa",
            cursor="hand2",
            bd=0,
            padx=10,
            pady=8,
        )
        self.cancel_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        self.cancel_button.config(state="disabled")

        self.progress = ttk.Progressbar(
            right_frame,
            mode="indeterminate",
            style="Horizontal.TProgressbar",
        )
        self.progress.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        # Log output
        log_frame = tk.Frame(self.root, bg=BG_COLOR)
        log_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))
        ttk.Label(log_frame, text="Log Output").pack(anchor="w")

        self.log_text = tk.Text(
            log_frame,
            height=12,  # increased
            bg=LOG_BG,
            fg=LOG_TEXT_COLOR,
            font=FONT_LOG,
            relief="flat",
            wrap="word",
        )
        self.log_text.pack(fill="both", expand=True, pady=(5, 0))

    # Utility widgets
    def create_file_picker(self, parent, label_text, row):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=(10, 6))
        var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=1, sticky="ew", pady=(10, 6))
        btn = ttk.Button(parent, text="Browse", command=lambda: self.browse_file(var))
        btn.grid(row=row, column=2, sticky="ew", padx=(5, 0), pady=(10, 6))
        return var

    def create_save_picker(self, parent, label_text, row):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=(10, 6))
        var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=1, sticky="ew", pady=(10, 6))
        btn = ttk.Button(parent, text="Save As", command=lambda: self.save_file(var))
        btn.grid(row=row, column=2, sticky="ew", padx=(5, 0), pady=(10, 6))
        return var

    def browse_file(self, var):
        filename = filedialog.askopenfilename()
        if filename:
            var.set(filename)

    def save_file(self, var):
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")],
        )
        if filename:
            var.set(filename)

    def choose_font_color(self):
        color_code = colorchooser.askcolor(title="Choose font color", initialcolor=self.font_color)
        if color_code[1]:
            self.font_color = color_code[1]
            self.font_color_btn.configure(bg=self.font_color)

    def choose_box_color(self):
        color_code = colorchooser.askcolor(title="Choose box background color", initialcolor=self.box_color)
        if color_code[1]:
            self.box_color = color_code[1]
            self.box_color_btn.configure(bg=self.box_color)

    def choose_shadow_color(self):
        color_code = colorchooser.askcolor(title="Choose shadow color", initialcolor=self.shadow_color)
        if color_code[1]:
            self.shadow_color = color_code[1]
            self.shadow_color_btn.configure(bg=self.shadow_color)

    def choose_progress_color(self):
        color_code = colorchooser.askcolor(title="Choose progress bar color", initialcolor=self.progress_color)
        if color_code[1]:
            self.progress_color = color_code[1]
            self.progress_color_btn.configure(bg=self.progress_color)

    # Process control
    def start_process(self):
        if self.process and self.process.poll() is None:
            messagebox.showinfo("Info", "A process is already running.")
            return

        try:
            box_alpha_255 = int(self.alpha_entry.get())
            if box_alpha_255 < 0 or box_alpha_255 > 255:
                raise ValueError
            box_alpha = box_alpha_255 / 255.0
        except ValueError:
            messagebox.showerror("Error", "Box transparency must be an integer between 0 and 255.")
            return

        try:
            min_duration = float(self.min_duration_entry.get().strip() or "0")
            if min_duration < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Min slide duration must be a number (0 or above).")
            return

        try:
            shadow_offset_x = int(self.shadow_offset_x_entry.get().strip() or "2")
            shadow_offset_y = int(self.shadow_offset_y_entry.get().strip() or "2")
        except ValueError:
            messagebox.showerror("Error", "Shadow offsets must be integers.")
            return

        try:
            progress_height = int(self.progress_height_entry.get().strip() or "6")
            if progress_height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Progress bar height must be a positive integer.")
            return

        preset_name = self.video_preset_var.get()
        width, height = VIDEO_PRESETS.get(preset_name, (720, 1280))

        args = {
            "--input": self.review_path.get(),
            "--background": self.bg_image.get(),
            "--logo": self.logo_image.get(),
            "--music": self.bg_music.get(),
            "--font": self.font_file.get(),
            "--output": self.output_file.get(),
            "--voice": VOICE_OPTIONS.get(self.voice_var.get(), "hi-IN-SwaraNeural"),
            "--rate": self.rate_entry.get(),
            "--font-size": self.font_size_var.get(),
            "--font-color": self.font_color,
            "--box-color": self.box_color,
            "--box-alpha": str(box_alpha),
            "--width": str(width),
            "--height": str(height),
            "--style": self.style_var.get(),
            "--text-position": self.text_position_var.get(),
            "--shadow-color": self.shadow_color,
            "--shadow-offset-x": str(shadow_offset_x),
            "--shadow-offset-y": str(shadow_offset_y),
            "--logo-position": self.logo_position_var.get(),
            "--logo-opacity": str(self.logo_opacity_var.get()),
            "--min-duration": str(min_duration),
            "--progress-color": self.progress_color,
            "--progress-height": str(progress_height),
        }

        flags = []
        if self.shadow_enable_var.get():
            flags.append("--enable-shadow")
        if self.progress_enable_var.get():
            flags.append("--enable-progress-bar")

        if not os.path.isfile(args["--input"]):
            messagebox.showerror("Error", "Review text file is required and must exist.")
            return
        if not os.path.isfile(args["--font"]):
            messagebox.showerror("Error", "Font file is required and must exist.")
            return
        if not args["--output"]:
            messagebox.showerror("Error", "Output file name is required.")
            return

        cmd = [sys.executable, SCRIPT_NAME]
        for k, v in args.items():
            if v not in [None, ""]:
                cmd.append(k)
                cmd.append(str(v))
        for flag in flags:
            cmd.append(flag)

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "🚀 Starting video generation...\n")

        self.start_button.config(state="disabled", text="Generating...")
        self.cancel_button.config(state="normal")
        self.progress.start(10)

        self.process_thread = threading.Thread(target=self.run_subprocess, args=(cmd,), daemon=True)
        self.process_thread.start()

    def run_subprocess(self, cmd):
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            for line in self.process.stdout:
                self.log_text.insert(tk.END, line)
                self.log_text.see(tk.END)
            self.process.wait()
            exit_code = self.process.returncode
            if exit_code == 0:
                self.log_text.insert(tk.END, "\n✅ Video generation completed successfully.\n")
                output_path = self.output_file.get()
                if os.path.isfile(output_path):
                    try:
                        if platform.system() == "Windows":
                            os.startfile(output_path)
                        elif platform.system() == "Darwin":
                            subprocess.Popen(["open", output_path])
                        else:
                            subprocess.Popen(["xdg-open", output_path])
                    except Exception as e:
                        self.log_text.insert(tk.END, f"\n⚠️ Could not open video automatically: {e}\n")
            else:
                self.log_text.insert(tk.END, f"\n❌ Video generation failed with exit code {exit_code}\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"\n❌ Error: {e}\n")
        finally:
            self.start_button.config(state="normal", text="Generate Video")
            self.cancel_button.config(state="disabled")
            self.progress.stop()
            self.process = None

    def cancel_process(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.log_text.insert(tk.END, "\n❌ Process cancelled by user.\n")
            self.start_button.config(state="normal", text="Generate Video")
            self.cancel_button.config(state="disabled")
            self.progress.stop()
            self.process = None


if __name__ == "__main__":
    root = tk.Tk()
    app = CoolieReviewApp(root)
    root.mainloop()
