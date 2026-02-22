# ============================================================================
#                           COLOR EXTRACTION GUI APPLICATION
# ============================================================================
# This application provides a GUI for:
# 1. Extracting specific colors (Green, Purple, Blue) from images
# 2. Applying color filters (Red, Yellow, Grayscale) to images  
# 3. Working with multiple images and switching between them
# ============================================================================

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

# Import our color processing module
from colorextract import extract_color, apply_color_filter, get_extraction_colors, get_color_filters

# ============================================================================
#                        DESIGN TOKENS  (single source of truth)
# ============================================================================
FONT       = 'Segoe UI'          # primary font; fallback: Arial
BG_DARK    = '#121212'           # deep charcoal – main background
BG_CARD    = '#1e1e1e'           # card / panel surface
BG_HEADER  = '#000000'           # top-bar / header surface
BG_THUMB   = '#2a2a2a'           # thumbnail inner bg
ACCENT     = '#4f8ef7'           # blue accent (active selection)
ACCENT2    = '#2ecc71'           # green accent
TEXT_PRI   = '#f0f0f0'           # primary text
TEXT_SEC   = '#888899'           # secondary / muted text
TEXT_HINT  = '#555566'           # placeholder / hint text
BTN_BACK   = '#2a2a3a'           # back button bg
BTN_SAVE   = '#2563eb'           # save button bg
BORDER_W   = 2                   # active thumbnail border width

class ColorExtractionUI:
    """
    Main GUI class for Color Extraction Program
    
    Features:
    - Multi-image support (switch between 2 images)
    - Color extraction (isolate specific colors, make rest gray)
    - Color filtering (apply color tints and effects)
    - Save processed results
    """
    def __init__(self):
        """Initialize the Color Extraction GUI application"""
        
        # ==================== IMAGE DATA VARIABLES ====================
        self.current_image = None           # Currently displayed image (BGR format)
        self.original_image = None          # Original loaded image (BGR format)  
        self.hsv_image = None              # HSV version for color extraction
        self.result_image = None           # Processed result image
        self.image_paths = []              # List of available image paths
        self.current_image_index = 0       # Index of currently active image
        self.image_buttons = []            # List of image selection buttons (border frames)
        self.thumbnail_refs = []           # Keep PhotoImage refs alive (prevent GC)
        
        # ==================== COLOR PROCESSING CONFIGURATION ====================
        # Get color configurations from the colorextract module
        self.extraction_colors = get_extraction_colors()
        self.color_filters = get_color_filters()
        
        # ==================== GUI SETUP ====================
        self.setup_main_window()
        self.create_user_interface()
        
    # ============================================================================
    #                           GUI SETUP AND INITIALIZATION
    # ============================================================================
    
    def setup_main_window(self):
        """Configure the main application window"""
        self.root = tk.Tk()
        self.root.title("KODHOD")
        self.root.geometry("1200x800")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.Horizontal.TProgressbar',
                        background=ACCENT, troughcolor=BG_CARD)
    
    def create_user_interface(self):
        """Three pages inside self.root; only one visible at a time."""
        self.main_page_frame = tk.Frame(self.root, bg=BG_DARK)
        self.main_page_frame.pack(fill='both', expand=True)

        self.create_title_section()
        self.create_image_selection_section()
        self.create_main_action_buttons()
        self.create_extraction_controls()
        self.create_filter_controls()
        self.create_results_display_area()
        self.create_status_and_progress_indicators()

        self.extraction_page_frame = tk.Frame(self.root, bg=BG_DARK)
        self.choice_page_frame     = tk.Frame(self.root, bg=BG_DARK)
    
    def create_title_section(self):
        """App title bar at top of main page."""
        bar = tk.Frame(self.main_page_frame, bg=BG_HEADER, height=60)
        bar.pack(fill='x')
        bar.pack_propagate(False)
        tk.Label(bar, text="KODHOD",
                 font=(FONT, 20, 'bold'), bg=BG_HEADER, fg=TEXT_PRI).pack(side=tk.LEFT, padx=24, pady=14)

    
    def create_image_selection_section(self):
        """Thumbnail strip + prev/next navigation."""
        # Centering wrapper — fills remaining space and centers content
        _center_wrap = tk.Frame(self.main_page_frame, bg=BG_DARK)
        _center_wrap.pack(fill='both', expand=True)

        self.image_selection_container = tk.Frame(_center_wrap, bg=BG_DARK)
        self.image_selection_container.place(relx=0.5, rely=0.5, anchor='center')

        # Current image name label
        self.current_image_indicator = tk.Label(
            self.image_selection_container,
            text="Loading…",
            font=(FONT, 13, 'bold'),
            bg=BG_DARK, fg=TEXT_PRI
        )
        self.current_image_indicator.pack(pady=(0, 6))

        # Prev / Next
        nav = tk.Frame(self.image_selection_container, bg=BG_DARK)
        nav.pack(pady=(0, 6))
        for txt, cmd in (("\u2190  Prev", self.previous_image), ("Next  \u2192", self.next_image)):
            tk.Button(nav, text=txt,
                      font=(FONT, 10, 'bold'),
                      bg=BTN_BACK, fg=TEXT_PRI,
                      width=10, height=1,
                      relief='flat', cursor='hand2',
                      activebackground='#3a3a4a', activeforeground=TEXT_PRI,
                      command=cmd).pack(side=tk.LEFT, padx=4)

        self.image_buttons_container = tk.Frame(self.image_selection_container, bg=BG_DARK)
        self.image_buttons_container.pack(pady=6)
    
    def create_main_action_buttons(self):
        """No visible buttons on main page – double-click thumbnail is the entry point.
        Widgets kept for legacy method compatibility only."""
        _c = tk.Frame(self.main_page_frame, bg=BG_DARK)  # hidden container
        self.extract_color_button = tk.Button(_c, command=self.show_extraction_options)
        self.change_color_button  = tk.Button(_c, command=self.show_filter_options)
    def setup_image_buttons(self):
        """Render thumbnail grid — 5 per row."""
        for w in self.image_buttons_container.winfo_children():
            w.destroy()
        self.image_buttons.clear()
        self.thumbnail_refs = []
        if not self.image_paths:
            return

        THUMB_W, THUMB_H = 210, 148
        COLS = 5

        current_row = None
        for i, image_path in enumerate(self.image_paths):
            if i % COLS == 0:
                current_row = tk.Frame(self.image_buttons_container, bg=BG_DARK)
                current_row.pack(anchor='center', pady=6)

            try:
                pil_img = Image.open(image_path)
                pil_img.thumbnail((THUMB_W, THUMB_H), Image.LANCZOS)
                # Pad to exact size so all cards are identical
                canvas = Image.new('RGB', (THUMB_W, THUMB_H), tuple(int(BG_THUMB.lstrip('#')[j*2:j*2+2], 16) for j in range(3)))
                offset = ((THUMB_W - pil_img.width) // 2, (THUMB_H - pil_img.height) // 2)
                canvas.paste(pil_img, offset)
                photo = ImageTk.PhotoImage(canvas)
            except Exception:
                photo = None
            self.thumbnail_refs.append(photo)

            # Border frame (coloured highlight) → inner thumb
            border = tk.Frame(current_row, bg=BG_THUMB, cursor='hand2')
            border.pack(side=tk.LEFT, padx=6, pady=2)
            inner = tk.Frame(border, bg=BG_THUMB)
            inner.pack(padx=2, pady=2)

            if photo:
                img_lbl = tk.Label(inner, image=photo, bg=BG_THUMB, cursor='hand2')
            else:
                img_lbl = tk.Label(inner, text=os.path.splitext(os.path.basename(image_path))[0][:10],
                                   width=18, height=6, bg=BG_THUMB, fg=TEXT_SEC,
                                   font=(FONT, 9), cursor='hand2')
            img_lbl.pack()

            for w in (border, inner, img_lbl):
                w.bind("<Button-1>",        lambda e, idx=i: self.switch_to_image(idx))
                w.bind("<Double-Button-1>", lambda e, idx=i: self.on_thumbnail_double_click(idx))

            self.image_buttons.append(border)

        hint = tk.Label(self.image_buttons_container,
                        text="Single-click to select  ·  Double-click to process",
                        font=(FONT, 9), bg=BG_DARK, fg=TEXT_HINT)
        hint.pack(pady=(8, 0))
        self.update_image_indicator()
    
    def update_image_buttons(self):
        """Highlight the active thumbnail with accent border."""
        for i, frame in enumerate(self.image_buttons):
            frame.config(bg=ACCENT if i == self.current_image_index else BG_THUMB)
    
    def update_image_indicator(self):
        """Show IMAGE N indicator."""
        if self.image_paths:
            self.current_image_indicator.config(text=f"IMAGE {self.current_image_index + 1}")
    
    def on_thumbnail_double_click(self, idx):
        """Double-click: show function-choice page for the selected image."""
        if self.current_image_index != idx:
            self.switch_to_image(idx)
        self.show_choice_page(idx)

    def _hide_all_secondary_pages(self):
        """Hide both secondary page frames cleanly."""
        for frame in (self.extraction_page_frame, self.choice_page_frame):
            for w in frame.winfo_children():
                w.destroy()
            frame.pack_forget()

    def show_choice_page(self, idx):
        """Full-window page: choose Extract Color or Change Color."""
        image_path = self.image_paths[idx]
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        original   = self.original_image.copy()

        self._hide_all_secondary_pages()
        self.main_page_frame.pack_forget()
        self.choice_page_frame.pack(fill='both', expand=True)

        # ── Header bar ───────────────────────────────────────────────────────
        hdr = tk.Frame(self.choice_page_frame, bg=BG_HEADER, height=52)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Button(hdr, text="\u2190  Back",
                  font=(FONT, 11), bg=BTN_BACK, fg=TEXT_PRI,
                  relief='flat', cursor='hand2', bd=0,
                  activebackground='#3a3a4a', activeforeground=TEXT_PRI,
                  command=self.show_main_page).pack(side=tk.LEFT, padx=18, pady=12)
        tk.Label(hdr, text="Select Function",
                 font=(FONT, 15, 'bold'), bg=BG_HEADER, fg=TEXT_PRI).pack(side=tk.LEFT, padx=6)

        # ── Body: preview + two centered cards ────────────────────────────────
        body = tk.Frame(self.choice_page_frame, bg=BG_DARK)
        body.pack(fill='both', expand=True)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)

        center = tk.Frame(body, bg=BG_DARK)
        center.place(relx=0.5, rely=0.5, anchor='center')

        CARD_W        = 200
        CARD_H        = 180
        BORDER_GREEN  = '#2ecc71'
        BORDER_ORANGE = '#e07020'
        _GLOW_PAD     = 10                 # must match GLOW_LAYERS+2 inside _make_card
        IMG_W         = (CARD_W + _GLOW_PAD * 2) * 2 + 64   # spans both glow canvases + padx

        # Preview thumbnail — sized to span both cards
        tk.Label(center, text=f"IMAGE {idx + 1}",
                 font=(FONT, 13, 'bold'), bg=BG_DARK, fg=TEXT_PRI).pack(pady=(0, 8))
        rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        h2, w2 = rgb.shape[:2]
        sc = min(IMG_W / w2, 240 / h2, 1.0)
        rgb = cv2.resize(rgb, (int(w2 * sc), int(h2 * sc)))
        # Pad to exact IMG_W so image always fills the full width
        canvas_img = Image.new('RGB', (IMG_W, int(h2 * sc)),
                               tuple(int(BG_DARK.lstrip('#')[j*2:j*2+2], 16) for j in range(3)))
        canvas_img.paste(Image.fromarray(rgb), ((IMG_W - int(w2*sc))//2, 0))
        photo = ImageTk.PhotoImage(canvas_img)
        prev_lbl = tk.Label(center, image=photo, bg=BG_DARK)
        prev_lbl.image = photo
        prev_lbl.pack(pady=(0, 16))

        # Cards row
        cards_row = tk.Frame(center, bg=BG_DARK)
        cards_row.pack()

        def _make_card(parent, icon, title, subtitle, bg_color, border_color, command):
            """Card with glow border on hover."""
            GLOW_LAYERS = 8          # number of glow rings
            GLOW_PAD    = GLOW_LAYERS + 2
            AW = CARD_W + GLOW_PAD * 2
            AH = CARD_H + GLOW_PAD * 2

            wrapper = tk.Frame(parent, bg=BG_DARK, cursor='hand2')
            wrapper.pack(side=tk.LEFT, padx=16)

            cv = tk.Canvas(wrapper, width=AW, height=AH,
                           bg=BG_DARK, highlightthickness=0, cursor='hand2')
            cv.pack()

            # Parse border color into RGB
            r = int(border_color[1:3], 16)
            g = int(border_color[3:5], 16)
            b = int(border_color[5:7], 16)
            bg_r = int(BG_DARK[1:3], 16)
            bg_g = int(BG_DARK[3:5], 16)
            bg_b = int(BG_DARK[5:7], 16)

            def _blend(t):
                cr = int(bg_r + (r - bg_r) * t)
                cg = int(bg_g + (g - bg_g) * t)
                cb = int(bg_b + (b - bg_b) * t)
                return f'#{cr:02x}{cg:02x}{cb:02x}'

            # Card content placed on canvas
            card = tk.Frame(cv, bg=bg_color, width=CARD_W, height=CARD_H, cursor='hand2')
            cv.create_window(AW // 2, AH // 2, window=card,
                             width=CARD_W, height=CARD_H)
            card.pack_propagate(False)
            tk.Label(card, text=icon,  font=(FONT, 34), bg=bg_color, fg='white', cursor='hand2').pack(pady=(18, 4))
            tk.Label(card, text=title, font=(FONT, 13, 'bold'), bg=bg_color, fg='white', cursor='hand2').pack()
            tk.Label(card, text=subtitle, font=(FONT, 9), bg=bg_color, fg='white', cursor='hand2',
                     wraplength=CARD_W - 20).pack(pady=(4, 18))

            # Always-visible thin border
            cv.create_rectangle(GLOW_PAD, GLOW_PAD, AW - GLOW_PAD, AH - GLOW_PAD,
                                 outline=border_color, width=1, tags='static')

            glow_step  = [0]
            direction  = [1]
            after_id   = [None]
            MAX_STEP   = 10

            def _draw_glow(step):
                cv.delete('glow')
                intensity = step / MAX_STEP
                for i in range(GLOW_LAYERS, 0, -1):
                    t = intensity * (i / GLOW_LAYERS) ** 0.5
                    color = _blend(t)
                    pad = GLOW_PAD - i
                    cv.create_rectangle(pad, pad, AW - pad, AH - pad,
                                        outline=color, width=1, tags='glow')
                # Bright inner border
                cv.create_rectangle(GLOW_PAD, GLOW_PAD, AW - GLOW_PAD, AH - GLOW_PAD,
                                    outline=border_color,
                                    width=max(1, int(intensity * 3)),
                                    tags='glow')

            def _animate():
                glow_step[0] += direction[0]
                if glow_step[0] >= MAX_STEP:
                    glow_step[0] = MAX_STEP
                    direction[0] = -1
                elif glow_step[0] <= 0:
                    glow_step[0] = 0
                    direction[0] = 1
                _draw_glow(glow_step[0])
                after_id[0] = cv.after(30, _animate)

            def _on_enter(e):
                direction[0] = 1
                if after_id[0] is None:
                    _animate()

            def _on_leave(e):
                if after_id[0]:
                    cv.after_cancel(after_id[0])
                    after_id[0] = None
                cv.delete('glow')
                glow_step[0] = 0

            for w in card.winfo_children() + [card, cv, wrapper]:
                w.bind('<Button-1>', lambda e: command())
                w.bind('<Enter>', _on_enter)
                w.bind('<Leave>', _on_leave)
            return wrapper

        _make_card(cards_row, icon='\U0001f3af', title='Extract Color',
                   subtitle='Isolate a specific color, grey out the rest',
                   bg_color='#1a4731', border_color=BORDER_GREEN,
                   command=lambda: self.show_extraction_page(idx))

        _make_card(cards_row, icon='\U0001f3a8', title='Change Mood',
                   subtitle='Apply a color filter to the whole image',
                   bg_color='#4a2000', border_color=BORDER_ORANGE,
                   command=lambda: self.show_filter_page(idx))

        self.choice_page_frame.update_idletasks()

    def show_filter_page(self, idx):
        """Full-window Change Color page."""
        image_path = self.image_paths[idx]
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        original   = self.original_image.copy()
        hsv        = self.hsv_image.copy()

        self._hide_all_secondary_pages()
        self.main_page_frame.pack_forget()
        self.extraction_page_frame.pack(fill='both', expand=True)

        _refs = {}; _result = {}

        # ── Header ────────────────────────────────────────────────────────
        hdr = tk.Frame(self.extraction_page_frame, bg=BG_HEADER, height=60)
        hdr.pack(fill='x'); hdr.pack_propagate(False)
        tk.Label(hdr, text="Change Mood",
                 font=(FONT, 16, 'bold'), bg=BG_HEADER, fg=TEXT_PRI).place(relx=0.5, rely=0.5, anchor='center')

        # ── Symmetric panels ──────────────────────────────────────────────
        panels = tk.Frame(self.extraction_page_frame, bg=BG_DARK)
        panels.pack(fill='both', expand=True, padx=20, pady=(14, 4))
        panels.columnconfigure(0, weight=1, uniform='half')
        panels.columnconfigure(1, weight=1, uniform='half')
        panels.rowconfigure(0, weight=1)

        def _make_panel(parent, col, title):
            f = tk.Frame(parent, bg='#1e1e1e')
            f.grid(row=0, column=col, sticky='nsew', padx=8)
            f.rowconfigure(1, weight=1)
            tk.Label(f, text=title, font=(FONT, 13, 'bold'),
                     bg='#1e1e1e', fg=TEXT_PRI).grid(row=0, column=0, sticky='w', padx=14, pady=(12, 8))
            lbl = tk.Label(f, bg='#1e1e1e', text='', fg=TEXT_HINT,
                           font=(FONT, 10, 'italic'), anchor='center')
            lbl.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 12))
            f.columnconfigure(0, weight=1)
            return lbl

        orig_lbl = _make_panel(panels, 0, "Original Image")
        res_title_var = tk.StringVar(value="Filtered Result")
        res_outer = tk.Frame(panels, bg='#1e1e1e')
        res_outer.grid(row=0, column=1, sticky='nsew', padx=8)
        res_outer.rowconfigure(1, weight=1)
        res_outer.columnconfigure(0, weight=1)
        tk.Label(res_outer, textvariable=res_title_var, font=(FONT, 13, 'bold'),
                 bg='#1e1e1e', fg=TEXT_PRI).grid(row=0, column=0, sticky='w', padx=14, pady=(12, 8))
        res_lbl = tk.Label(res_outer, bg='#1e1e1e', text='Select a filter below',
                           font=(FONT, 10, 'italic'), fg=TEXT_HINT, anchor='center')
        res_lbl.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 12))

        # ── Status ─────────────────────────────────────────────────────────
        sv = tk.StringVar(value="Select a filter to apply")
        tk.Label(self.extraction_page_frame, textvariable=sv,
                 font=(FONT, 9), bg=BG_DARK, fg=TEXT_HINT).pack(pady=2)

        # ── Bottom bar ──────────────────────────────────────────────────
        bar = tk.Frame(self.extraction_page_frame, bg='#000000', height=60)
        bar.pack(fill='x', side=tk.BOTTOM); bar.pack_propagate(False)

        tk.Button(bar, text="↩  Back",
                  font=(FONT, 11), bg=BTN_BACK, fg=TEXT_PRI,
                  relief='flat', cursor='hand2', bd=0,
                  activebackground='#3a3a4a', activeforeground=TEXT_PRI,
                  command=lambda: self.show_choice_page(idx)).pack(side=tk.LEFT, padx=16, pady=12)

        ff = tk.Frame(bar, bg='#000000')
        ff.place(relx=0.5, rely=0.5, anchor='center')
        for fk, fi in self.color_filters.items():
            tk.Button(ff, text=fi['display_name'],
                      font=(FONT, 11, 'bold'), bg=fi['button_color'], fg='white',
                      width=15, padx=4, pady=6, relief='flat', cursor='hand2', bd=0,
                      activeforeground='white',
                      command=lambda k=fk: _do_filter(k)).pack(side=tk.LEFT, padx=6)

        # ── Helpers ────────────────────────────────────────────────────
        def _render(img, lbl, mw=None, mh=None):
            self.extraction_page_frame.update_idletasks()
            if mw is None: mw = max(lbl.winfo_width() - 20, 400)
            if mh is None: mh = max(lbl.winfo_height() - 20, 350)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h2, w2 = rgb.shape[:2]
            sc = min(mw/w2, mh/h2, 1.0)
            if sc < 1: rgb = cv2.resize(rgb, (int(w2*sc), int(h2*sc)))
            p = ImageTk.PhotoImage(Image.fromarray(rgb))
            lbl.config(image=p, text='')
            lbl.image = p
            return p

        _refs['orig'] = _render(original, orig_lbl)

        def _do_filter(fk):
            fi = self.color_filters[fk]
            sv.set(f"Applying {fi['display_name']}\u2026")
            self.extraction_page_frame.update()
            try:
                result, name = apply_color_filter(original, fk)
                _result.update({'image': result, 'name': name, 'path': image_path})
                _refs['res'] = _render(result, res_lbl)
                res_title_var.set(name)
                sv.set(f"{name} applied")
            except Exception as e:
                sv.set(f"Error: {e}")

    def show_extraction_page(self, idx):
        """Full-window Extract Color page."""
        image_path = self.image_paths[idx]
        image_name = os.path.basename(image_path)
        original   = self.original_image.copy()
        hsv        = self.hsv_image.copy()

        # Clear old content, swap pages
        self._hide_all_secondary_pages()
        self.main_page_frame.pack_forget()
        self.extraction_page_frame.pack(fill='both', expand=True)

        _refs   = {}   # PhotoImage refs
        _result = {}   # processed result

        # ── Header ──────────────────────────────────────────────────────────
        header = tk.Frame(self.extraction_page_frame, bg=BG_HEADER, height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text="Color Extraction",
                 font=(FONT, 16, 'bold'), bg=BG_HEADER, fg=TEXT_PRI).place(relx=0.5, rely=0.5, anchor='center')

        # ── Side-by-side image panels ────────────────────────────────────────
        panels = tk.Frame(self.extraction_page_frame, bg=BG_DARK)
        panels.pack(fill='both', expand=True, padx=20, pady=(14, 4))
        panels.columnconfigure(0, weight=1, uniform='half')
        panels.columnconfigure(1, weight=1, uniform='half')
        panels.rowconfigure(0, weight=1)

        def _make_panel(parent, col, title):
            f = tk.Frame(parent, bg='#1e1e1e')
            f.grid(row=0, column=col, sticky='nsew', padx=8)
            f.rowconfigure(1, weight=1)
            f.columnconfigure(0, weight=1)
            tk.Label(f, text=title, font=(FONT, 13, 'bold'),
                     bg='#1e1e1e', fg=TEXT_PRI).grid(row=0, column=0, sticky='w', padx=14, pady=(12, 8))
            lbl = tk.Label(f, bg='#1e1e1e', text='', fg=TEXT_HINT,
                           font=(FONT, 10, 'italic'), anchor='center')
            lbl.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 12))
            return lbl

        orig_lbl = _make_panel(panels, 0, "Original Image")
        res_title_var = tk.StringVar(value="Extracted Result")
        res_outer = tk.Frame(panels, bg='#1e1e1e')
        res_outer.grid(row=0, column=1, sticky='nsew', padx=8)
        res_outer.rowconfigure(1, weight=1)
        res_outer.columnconfigure(0, weight=1)
        tk.Label(res_outer, textvariable=res_title_var, font=(FONT, 13, 'bold'),
                 bg='#1e1e1e', fg=TEXT_PRI).grid(row=0, column=0, sticky='w', padx=14, pady=(12, 8))
        res_lbl = tk.Label(res_outer, bg='#1e1e1e',
                           text="\u2190  Select a color below",
                           font=(FONT, 10, 'italic'), fg=TEXT_HINT, anchor='center')
        res_lbl.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 4))

        # ── Cinematic description card ────────────────────────────────────────
        desc_card = tk.Frame(res_outer, bg='#141414')
        desc_card.grid(row=2, column=0, sticky='ew', padx=12, pady=(0, 14))
        desc_card.columnconfigure(0, weight=1)

        # Top accent bar
        tk.Frame(desc_card, bg=ACCENT, height=3).grid(row=0, column=0, sticky='ew')

        inner_pad = tk.Frame(desc_card, bg='#141414')
        inner_pad.grid(row=1, column=0, sticky='ew', padx=20, pady=16)
        inner_pad.columnconfigure(0, weight=1)

        desc_title_lbl = tk.Label(inner_pad, text='', bg='#141414', fg='white',
                                  font=(FONT, 13, 'bold'), anchor='w', justify='left')
        desc_title_lbl.grid(row=0, column=0, sticky='ew', pady=(0, 10))

        desc_body_lbl = tk.Label(inner_pad, text='', bg='#141414', fg='#e0e0e0',
                                 font=(FONT, 11), anchor='w', justify='left',
                                 wraplength=520)
        desc_body_lbl.grid(row=1, column=0, sticky='ew')

        desc_card.grid_remove()  # hidden until a color is chosen

        # ── Status ───────────────────────────────────────────────────────────
        status_var = tk.StringVar(value="Image loaded successfully")
        tk.Label(self.extraction_page_frame, textvariable=status_var,
                 font=(FONT, 9), bg=BG_DARK, fg=TEXT_HINT).pack(pady=2)

        # ── Bottom action bar ────────────────────────────────────────────────
        bottom = tk.Frame(self.extraction_page_frame, bg='#000000', height=60)
        bottom.pack(fill='x', side=tk.BOTTOM)
        bottom.pack_propagate(False)

        tk.Button(bottom, text="\u21a9  Back",
                  font=(FONT, 11), bg=BTN_BACK, fg=TEXT_PRI,
                  relief='flat', cursor='hand2', bd=0,
                  activebackground='#3a3a4a', activeforeground=TEXT_PRI,
                  command=lambda: self.show_choice_page(idx)).pack(side=tk.LEFT, padx=16, pady=12)

        colors_center = tk.Frame(bottom, bg='#000000')
        colors_center.place(relx=0.5, rely=0.5, anchor='center')
        for ck, ci in self.extraction_colors.items():
            if idx == 0 and ck == 'blue':
                continue
            tk.Button(colors_center,
                      text=f"\u25cf {ci['display_name']}",
                      font=(FONT, 11, 'bold'),
                      bg=ci['button_color'], fg='white',
                      width=15, padx=4, pady=6,
                      relief='flat', cursor='hand2', bd=0,
                      activeforeground='white',
                      command=lambda k=ck: _do_extract(k)).pack(side=tk.LEFT, padx=6)

        # ── Helpers ──────────────────────────────────────────────────────────
        def _render(cv2_img, label, max_w=None, max_h=None):
            self.extraction_page_frame.update_idletasks()
            if max_w is None: max_w = max(label.winfo_width() - 20, 400)
            if max_h is None: max_h = max(label.winfo_height() - 20, 350)
            rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            h2, w2 = rgb.shape[:2]
            sc = min(max_w / w2, max_h / h2, 1.0)
            if sc < 1.0:
                rgb = cv2.resize(rgb, (int(w2 * sc), int(h2 * sc)))
            photo = ImageTk.PhotoImage(Image.fromarray(rgb))
            label.config(image=photo, text='')
            label.image = photo
            return photo

        _refs['orig'] = _render(original, orig_lbl)

        # Cinematic descriptions per image index and color
        # Format: (title, body)
        DESCRIPTIONS = {
            0: {
                'green':  ("Cinematic Emotion",
                           "This unnatural green shade represents the character's detachment from society. "
                           "It creates a sense of unease and isolation, highlighting a world where the individual "
                           "feels like an outsider in their own environment."),
                'purple': ("Cinematic Emotion",
                           "A somber, low-luminance tone that evokes a feeling of nostalgia and loneliness. "
                           "When paired with green, it creates visual tension that reflects the quiet sadness "
                           "and solitude of life in a vast, empty city."),
            },
        }

        def _do_extract(color_key):
            ci = self.extraction_colors[color_key]
            status_var.set(f"Extracting {ci['display_name']}\u2026")
            self.extraction_page_frame.update()
            try:
                result, name = extract_color(original, hsv, color_key)
                _result.update({'image': result, 'name': name, 'path': image_path})
                _refs['result'] = _render(result, res_lbl)
                res_title_var.set(f"{name} \u2014 Extracted")
                status_var.set(f"{name} extracted successfully")
                # Show cinematic description card if available
                entry = DESCRIPTIONS.get(idx, {}).get(color_key)
                if entry:
                    title, body = entry
                    desc_title_lbl.config(text=title)
                    desc_body_lbl.config(text=body)
                    desc_card.grid()
                else:
                    desc_card.grid_remove()
            except Exception as e:
                status_var.set(f"Extraction failed: {e}")

    def show_main_page(self):
        """Switch back to the main thumbnail grid."""
        self._hide_all_secondary_pages()
        self.main_page_frame.pack(fill='both', expand=True)

    def previous_image(self):
        """Switch to the previous image"""
        if len(self.image_paths) > 1:
            previous_index = (self.current_image_index - 1) % len(self.image_paths)
            self.switch_to_image(previous_index)
    
    def next_image(self):
        """Switch to the next image"""
        if len(self.image_paths) > 1:
            next_index = (self.current_image_index + 1) % len(self.image_paths)
            self.switch_to_image(next_index)
        
    def create_extraction_controls(self):
        self.extraction_controls_container = tk.Frame(self.main_page_frame, bg=BG_DARK)
    
    def create_filter_controls(self):
        self.filter_controls_container = tk.Frame(self.main_page_frame, bg=BG_DARK)
    
    def create_results_display_area(self):
        self.results_display_container = tk.Frame(self.main_page_frame, bg=BG_DARK)

    def create_status_and_progress_indicators(self):
        self.status_label = tk.Label(
            self.main_page_frame,
            text="",
            font=(FONT, 10),
            bg=BG_DARK, fg=TEXT_SEC
        )
        self.status_label.pack(side=tk.BOTTOM, pady=2)
        self.progress_bar = ttk.Progressbar(
            self.main_page_frame,
            style='Dark.Horizontal.TProgressbar',
            mode='indeterminate', length=300
        )
    
    
    # ============================================================================
    #                           USER INTERFACE INTERACTIONS
    # ============================================================================
    
    def switch_to_image(self, image_index):
        """
        Switch between available images
        
        Args:
            image_index (int): Index of image to switch to
        """
        if 0 <= image_index < len(self.image_paths):
            self.current_image_index = image_index
            self.load_current_image()
            
            # Update the current image indicator text
            self.update_image_indicator()
            
            # Update button appearances
            self.update_image_buttons()
            
            # Hide any open option panels and previous results
            self.hide_filter_options()
    
    def show_extraction_options(self):
        """Display the color extraction option buttons"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        # Hide filter options if currently shown
        self.hide_filter_options()
        
        # Show extraction options
        self.extraction_controls_container.pack(pady=20)
    
    def hide_extraction_options(self):
        """Hide the color extraction option buttons"""
        self.extraction_controls_container.pack_forget()
        self.results_display_container.pack_forget()
    
    def show_filter_options(self):
        """Display the color filter option buttons"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        # Hide extraction options if currently shown
        self.hide_extraction_options()
        
        # Show filter options
        self.filter_controls_container.pack(pady=20)
    
    def hide_filter_options(self):
        """Hide the color filter option buttons"""
        self.filter_controls_container.pack_forget()
        self.results_display_container.pack_forget()
    
    def cv2_to_tk_image(self, cv2_image, max_width=400, max_height=300):
        """Convert OpenCV image to Tkinter PhotoImage for display in GUI"""
        # Convert BGR (OpenCV) to RGB (Tkinter/PIL)
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        
        # Resize if image is too large for GUI display
        height, width = rgb_image.shape[:2]
        if width > max_width or height > max_height:
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            rgb_image = cv2.resize(rgb_image, (new_width, new_height))
        
        # Convert to PIL Image then to Tkinter PhotoImage
        pil_image = Image.fromarray(rgb_image)
        return ImageTk.PhotoImage(pil_image)
    
    def display_results(self, operation_name, is_filter=False):
        """Display the original and processed images in GUI"""
        self.results_display_container.pack_forget()  # Remove previous results
        self.results_display_container = tk.Frame(self.main_page_frame, bg='#f0f0f0')
        self.results_display_container.pack(pady=20, fill='both', expand=True)
        
        # Results title
        operation_type = "Filter" if is_filter else "Extraction"
        current_image_name = os.path.splitext(os.path.basename(self.image_paths[self.current_image_index]))[0]
        results_title = tk.Label(self.results_display_container, 
                                text=f"✨ {operation_name} {operation_type} Results\nImage {self.current_image_index + 1} of {len(self.image_paths)}: {current_image_name}", 
                                font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        results_title.pack(pady=10)
        
        # Images container
        images_container = tk.Frame(self.results_display_container, bg='#f0f0f0')
        images_container.pack()
        
        # Original image
        original_frame = tk.Frame(images_container, bg='white', relief='solid', bd=2)
        original_frame.pack(side=tk.LEFT, padx=20)
        
        original_label = tk.Label(original_frame, text="Original Image", 
                                 font=('Arial', 12, 'bold'), bg='white', fg='#333')
        original_label.pack(pady=5)
        
        original_tk_image = self.cv2_to_tk_image(self.original_image)
        original_image_label = tk.Label(original_frame, image=original_tk_image, bg='white')
        original_image_label.image = original_tk_image  # Keep reference
        original_image_label.pack(padx=10, pady=10)
        
        # Result image
        result_frame = tk.Frame(images_container, bg='white', relief='solid', bd=2)
        result_frame.pack(side=tk.LEFT, padx=20)
        
        operation_type = "Filter Applied" if is_filter else "Extracted"
        result_label = tk.Label(result_frame, text=f"{operation_name} {operation_type}", 
                               font=('Arial', 12, 'bold'), bg='white', fg='#333')
        result_label.pack(pady=5)
        
        result_tk_image = self.cv2_to_tk_image(self.result_image)
        result_image_label = tk.Label(result_frame, image=result_tk_image, bg='white')
        result_image_label.image = result_tk_image  # Keep reference
        result_image_label.pack(padx=10, pady=10)
        
        # Action buttons
        action_frame = tk.Frame(self.results_display_container, bg='#f0f0f0')
        action_frame.pack(pady=20)
        
        save_btn = tk.Button(action_frame, text="💾 Save Result", 
                            font=('Arial', 12, 'bold'), bg='#2196F3', fg='white',
                            relief='flat', cursor='hand2', command=self.save_result)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        new_operation_btn = tk.Button(action_frame, text="🔄 New Operation", 
                                      font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',
                                      relief='flat', cursor='hand2', 
                                      command=self.reset_for_new_operation)
        new_operation_btn.pack(side=tk.LEFT, padx=10)
        
        # Add navigation buttons in results for easy image switching
        if len(self.image_paths) > 1:
            nav_frame = tk.Frame(action_frame, bg='#f0f0f0')
            nav_frame.pack(side=tk.LEFT, padx=20)
            
            if self.current_image_index > 0:
                prev_btn = tk.Button(nav_frame, text="← Previous Image", 
                                    font=('Arial', 10, 'bold'), bg='#9C27B0', fg='white',
                                    relief='flat', cursor='hand2', 
                                    command=self.previous_image)
                prev_btn.pack(side=tk.TOP, pady=2)
            
            if self.current_image_index < len(self.image_paths) - 1:
                next_btn = tk.Button(nav_frame, text="Next Image →", 
                                    font=('Arial', 10, 'bold'), bg='#9C27B0', fg='white',
                                    relief='flat', cursor='hand2', 
                                    command=self.next_image)
                next_btn.pack(side=tk.TOP, pady=2)
        
        operation_type = "filter" if is_filter else "extraction"
        self.status_label.config(text=f"✅ {operation_name} {operation_type} completed successfully!", fg='#4CAF50')
    
    def apply_color_filter(self, filter_key):
        """Apply color filter using colorextract module"""
        if filter_key not in self.color_filters:
            messagebox.showerror("Error", "Invalid filter selection!")
            return False
        
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return False
        
        filter_info = self.color_filters[filter_key]
        self.show_progress(f"Applying {filter_info['display_name']}...")
        
        try:
            # Use the colorextract module function
            self.result_image, filter_display_name = apply_color_filter(
                self.current_image, 
                filter_key
            )
            
            self.hide_progress()
            self.display_results(filter_display_name, is_filter=True)
            return True
            
        except Exception as e:
            self.hide_progress()
            self.status_label.config(text=f"❌ Filter failed: {str(e)}", fg='#f44336')
            messagebox.showerror("Error", f"Color filter failed:\n{str(e)}")
            return False
    
    # ============================================================================
    #                           UTILITY AND HELPER METHODS
    # ============================================================================
    
    def update_status(self, message, success=True):
        """
        Update the status label with a message
        
        Args:
            message (str): Status message to display
            success (bool): True for success (green), False for error (red)
        """
        color = '#4CAF50' if success else '#f44336'
        self.status_label.config(text=message, fg=color)
    
    def save_result(self):
        """
        Save the processed result image to the same folder as the original
        
        The saved file will have a descriptive name with timestamp to avoid overwrites.
        """
        if self.result_image is not None:
            try:
                # Generate descriptive filename with timestamp
                current_image_path = self.image_paths[self.current_image_index]
                original_name = os.path.splitext(os.path.basename(current_image_path))[0]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{original_name}_processed_{timestamp}.jpg"
                
                # Save to same directory as original image
                filepath = os.path.join(os.path.dirname(current_image_path), filename)
                cv2.imwrite(filepath, self.result_image)
                
                messagebox.showinfo("Success", f"Image saved as:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
        else:
            messagebox.showwarning("Warning", "No result image to save!")
    
    def show_progress(self, message="Processing..."):
        """Show progress indicator with custom message"""
        self.status_label.config(text=message, fg='#FF9800')
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10)
        self.root.update()
    
    def hide_progress(self):
        """Hide progress indicator"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
    
    def load_current_image(self):
        """
        Load and preprocess the currently selected image
        
        Returns:
            bool: True if image loaded successfully, False otherwise
        """
        if self.current_image_index < len(self.image_paths):
            return self.load_image(self.image_paths[self.current_image_index])
        return False
    
    # ============================================================================
    #                           COLOR PROCESSING OPERATIONS
    # ============================================================================
    
    def load_image(self, image_path):
        """
        Load and preprocess an image from file path
        
        This method loads an image, resizes it if needed for performance,
        and creates the different versions needed for processing.
        
        Args:
            image_path (str): Full path to the image file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.original_image = cv2.imread(image_path)
            if self.original_image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Resize image if too large for processing
            height, width = self.original_image.shape[:2]
            if width > 1200 or height > 900:
                scale = min(1200/width, 900/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                self.original_image = cv2.resize(self.original_image, (new_width, new_height))
            
            self.current_image = self.original_image.copy()
            self.hsv_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2HSV)
            image_name = os.path.basename(image_path)
            self.status_label.config(text="", fg=ACCENT2)
            return True
        except Exception as e:
            self.status_label.config(text=f"❌ Failed to load image: {str(e)}", fg='#f44336')
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
            return False
    
    def perform_color_extraction(self, color_key):
        """
        Extract specified color from image using colorextract module
        
        Args:
            color_key (str): Key identifying which color to extract ('green', 'purple', 'blue')
            
        Returns:
            bool: True if successful, False otherwise
        """
        if color_key not in self.extraction_colors:
            messagebox.showerror("Error", "Invalid color selection!")
            return False
        
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return False
        
        color_info = self.extraction_colors[color_key]
        self.show_progress(f"Extracting {color_info['display_name']} color...")
        
        try:
            # Use the colorextract module function
            self.result_image, color_display_name = extract_color(
                self.current_image, 
                self.hsv_image, 
                color_key
            )
            
            self.hide_progress()
            self.display_results(color_display_name)
            return True
            
        except Exception as e:
            self.hide_progress()
            self.status_label.config(text=f"❌ Extraction failed: {str(e)}", fg='#f44336')
            messagebox.showerror("Error", f"Color extraction failed:\n{str(e)}")
            return False
    
    def reset_for_new_operation(self):
        """Reset UI state for starting a new operation"""
        self.hide_extraction_options()
        self.hide_filter_options()
    
    # ============================================================================
    #                           MAIN APPLICATION ENTRY POINT
    # ============================================================================
    
    def run(self, image_paths):
        """Start the GUI application with the provided images"""
        try:
            self.image_paths = image_paths
            
            # Set up image selection buttons now that we have the paths
            self.setup_image_buttons()
            
            if self.load_current_image():
                # Update image buttons to show current selection
                self.update_image_buttons()
                
                # Center the window
                self.root.update_idletasks()
                width = self.root.winfo_width()
                height = self.root.winfo_height()
                x = (self.root.winfo_screenwidth() // 2) - (width // 2)
                y = (self.root.winfo_screenheight() // 2) - (height // 2)
                self.root.geometry(f'{width}x{height}+{x}+{y}')
                
                # Start the GUI
                self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Application error:\n{str(e)}")
