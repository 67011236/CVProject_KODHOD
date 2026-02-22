import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

from colorextract import extract_color, apply_color_filter, get_extraction_colors, get_color_filters
from image_configs import get_image_config

FONT       = 'Segoe UI'
BG_DARK    = '#121212'
BG_CARD    = '#1e1e1e'
BG_HEADER  = '#000000'
BG_THUMB   = '#2a2a2a'
ACCENT     = '#4f8ef7'
ACCENT2    = '#2ecc71'
TEXT_PRI   = '#f0f0f0'
TEXT_SEC   = '#888899'
TEXT_HINT  = '#555566'
BTN_BACK   = '#2a2a3a'
BTN_SAVE   = '#2563eb'
BORDER_W   = 2

class ColorExtractionUI:
    def __init__(self):
        
        self.current_image = None
        self.original_image = None
        self.hsv_image = None
        self.result_image = None
        self.image_paths = []
        self.current_image_index = 0
        self.image_buttons = []
        self.thumbnail_refs = []
        
        self.extraction_colors = get_extraction_colors()
        self.color_filters = get_color_filters()
        
        self.setup_main_window()
        self.create_user_interface()
        
    def setup_main_window(self):
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
        bar = tk.Frame(self.main_page_frame, bg=BG_HEADER, height=60)
        bar.pack(fill='x')
        bar.pack_propagate(False)
        tk.Label(bar, text="KODHOD",
                 font=(FONT, 20, 'bold'), bg=BG_HEADER, fg=TEXT_PRI).pack(side=tk.LEFT, padx=24, pady=14)

    
    def create_image_selection_section(self):
        _center_wrap = tk.Frame(self.main_page_frame, bg=BG_DARK)
        _center_wrap.pack(fill='both', expand=True)

        self.image_selection_container = tk.Frame(_center_wrap, bg=BG_DARK)
        self.image_selection_container.place(relx=0.5, rely=0.5, anchor='center')

        self.current_image_indicator = tk.Label(
            self.image_selection_container,
            text="Loading…",
            font=(FONT, 13, 'bold'),
            bg=BG_DARK, fg=TEXT_PRI
        )
        self.current_image_indicator.pack(pady=(0, 6))

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
        
        _c = tk.Frame(self.main_page_frame, bg=BG_DARK)
        self.extract_color_button = tk.Button(_c, command=self.show_extraction_options)
        self.change_color_button  = tk.Button(_c, command=self.show_filter_options)
    def setup_image_buttons(self):
        
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
                canvas = Image.new('RGB', (THUMB_W, THUMB_H), tuple(int(BG_THUMB.lstrip('#')[j*2:j*2+2], 16) for j in range(3)))
                offset = ((THUMB_W - pil_img.width) // 2, (THUMB_H - pil_img.height) // 2)
                canvas.paste(pil_img, offset)
                photo = ImageTk.PhotoImage(canvas)
            except Exception:
                photo = None
            self.thumbnail_refs.append(photo)

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
        
        for i, frame in enumerate(self.image_buttons):
            frame.config(bg=ACCENT if i == self.current_image_index else BG_THUMB)
    
    def update_image_indicator(self):
        
        if self.image_paths:
            self.current_image_indicator.config(text=f"IMAGE {self.current_image_index + 1}")
    
    def on_thumbnail_double_click(self, idx):
        
        if self.current_image_index != idx:
            self.switch_to_image(idx)
        self.show_choice_page(idx)

    def _hide_all_secondary_pages(self):
        
        for frame in (self.extraction_page_frame, self.choice_page_frame):
            for w in frame.winfo_children():
                w.destroy()
            frame.pack_forget()

    def show_choice_page(self, idx):
        
        image_path = self.image_paths[idx]
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        original   = self.original_image.copy()

        self._hide_all_secondary_pages()
        self.main_page_frame.pack_forget()
        self.choice_page_frame.pack(fill='both', expand=True)

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
        _GLOW_PAD     = 10
        IMG_W         = (CARD_W + _GLOW_PAD * 2) * 2 + 16

        tk.Label(center, text=f"IMAGE {idx + 1}",
                 font=(FONT, 13, 'bold'), bg=BG_DARK, fg=TEXT_PRI).pack(pady=(0, 8))
        rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        h2, w2 = rgb.shape[:2]
        sc = min(IMG_W / w2, 320 / h2, 1.0)
        rgb = cv2.resize(rgb, (int(w2 * sc), int(h2 * sc)))
        canvas_img = Image.new('RGB', (IMG_W, int(h2 * sc)),
                               tuple(int(BG_DARK.lstrip('#')[j*2:j*2+2], 16) for j in range(3)))
        canvas_img.paste(Image.fromarray(rgb), ((IMG_W - int(w2*sc))//2, 0))
        photo = ImageTk.PhotoImage(canvas_img)
        prev_lbl = tk.Label(center, image=photo, bg=BG_DARK)
        prev_lbl.image = photo
        prev_lbl.pack(pady=(0, 16))

        cards_row = tk.Frame(center, bg=BG_DARK)
        cards_row.pack()

        def _make_card(parent, icon, title, subtitle, bg_color, border_color, command):
            
            GLOW_LAYERS = 8
            GLOW_PAD    = GLOW_LAYERS + 2
            AW = CARD_W + GLOW_PAD * 2
            AH = CARD_H + GLOW_PAD * 2

            wrapper = tk.Frame(parent, bg=BG_DARK, cursor='hand2')
            wrapper.pack(side=tk.LEFT, padx=16)

            cv = tk.Canvas(wrapper, width=AW, height=AH,
                           bg=BG_DARK, highlightthickness=0, cursor='hand2')
            cv.pack()

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

            card = tk.Frame(cv, bg=bg_color, width=CARD_W, height=CARD_H, cursor='hand2')
            cv.create_window(AW // 2, AH // 2, window=card,
                             width=CARD_W, height=CARD_H)
            card.pack_propagate(False)
            tk.Label(card, text=icon,  font=(FONT, 34), bg=bg_color, fg='white', cursor='hand2').pack(pady=(18, 4))
            tk.Label(card, text=title, font=(FONT, 13, 'bold'), bg=bg_color, fg='white', cursor='hand2').pack()
            tk.Label(card, text=subtitle, font=(FONT, 9), bg=bg_color, fg='white', cursor='hand2',
                     wraplength=CARD_W - 20).pack(pady=(4, 18))

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
        
        image_path = self.image_paths[idx]
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        original   = self.original_image.copy()
        hsv        = self.hsv_image.copy()

        self._hide_all_secondary_pages()
        self.main_page_frame.pack_forget()
        self.extraction_page_frame.pack(fill='both', expand=True)

        _refs = {}; _result = {}
        _fcfg = get_image_config(image_path)

        hdr = tk.Frame(self.extraction_page_frame, bg=BG_HEADER, height=60)
        hdr.pack(fill='x'); hdr.pack_propagate(False)
        tk.Label(hdr, text="Change Mood",
                 font=(FONT, 16, 'bold'), bg=BG_HEADER, fg=TEXT_PRI).place(relx=0.5, rely=0.5, anchor='center')

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
        res_outer.rowconfigure(2, weight=0)
        res_outer.columnconfigure(0, weight=1)
        tk.Label(res_outer, textvariable=res_title_var, font=(FONT, 13, 'bold'),
                 bg='#1e1e1e', fg=TEXT_PRI).grid(row=0, column=0, sticky='w', padx=14, pady=(12, 8))
        res_lbl = tk.Label(res_outer, bg='#1e1e1e', text='Select a filter below',
                           font=(FONT, 10, 'italic'), fg=TEXT_HINT, anchor='center')
        res_lbl.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 12))

        desc_container_f = tk.Frame(res_outer, bg='#1e1e1e', height=160)
        desc_container_f.grid(row=2, column=0, sticky='ew', padx=12, pady=(0, 14))
        desc_container_f.grid_propagate(False)
        desc_container_f.columnconfigure(0, weight=1)
        
        desc_card_f = tk.Frame(desc_container_f, bg='#141414')
        desc_card_f.grid(row=0, column=0, sticky='ew')
        desc_card_f.columnconfigure(0, weight=1)
        tk.Frame(desc_card_f, bg=ACCENT, height=3).grid(row=0, column=0, sticky='ew')
        inner_f = tk.Frame(desc_card_f, bg='#141414')
        inner_f.grid(row=1, column=0, sticky='ew', padx=20, pady=16)
        inner_f.columnconfigure(0, weight=1)
        desc_title_f = tk.Label(inner_f, text='', bg='#141414', fg='white',
                                font=(FONT, 13, 'bold'), anchor='w', justify='left')
        desc_title_f.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        desc_body_f = tk.Label(inner_f, text='', bg='#141414', fg='#e0e0e0',
                               font=(FONT, 11), anchor='w', justify='left', wraplength=400)
        desc_body_f.grid(row=1, column=0, sticky='ew')
        desc_card_f.grid_remove()
        sv = tk.StringVar(value="Select a filter to apply")
        tk.Label(self.extraction_page_frame, textvariable=sv,
                 font=(FONT, 9), bg=BG_DARK, fg=TEXT_HINT).pack(pady=2)

        bar = tk.Frame(self.extraction_page_frame, bg='#000000', height=60)
        bar.pack(fill='x', side=tk.BOTTOM); bar.pack_propagate(False)

        tk.Button(bar, text="↩  Back",
                  font=(FONT, 11), bg=BTN_BACK, fg=TEXT_PRI,
                  relief='flat', cursor='hand2', bd=0,
                  activebackground='#3a3a4a', activeforeground=TEXT_PRI,
                  command=lambda: self.show_choice_page(idx)).pack(side=tk.LEFT, padx=16, pady=12)

        ff = tk.Frame(bar, bg='#000000')
        ff.place(relx=0.5, rely=0.5, anchor='center')
        _allowed_fc = _fcfg.get('filter_colors')
        for fk, fi in self.color_filters.items():
            if _allowed_fc is not None and fk not in _allowed_fc:
                continue
            if _allowed_fc is None and fk == 'blue':
                continue
            tk.Button(ff, text=fi['display_name'],
                      font=(FONT, 11, 'bold'), bg=fi['button_color'], fg='white',
                      width=15, padx=4, pady=6, relief='flat', cursor='hand2', bd=0,
                      activeforeground='white',
                      command=lambda k=fk: _do_filter(k)).pack(side=tk.LEFT, padx=6)

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

        _filter_descs = _fcfg.get('filter_descriptions', {})

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
                entry = _filter_descs.get(fk)
                if entry:
                    title, body = entry
                    desc_title_f.config(text=title)
                    desc_body_f.config(text=body)
                    desc_card_f.grid()
                else:
                    desc_card_f.grid_remove()
            except Exception as e:
                sv.set(f"Error: {e}")

    def show_extraction_page(self, idx):
        
        image_path = self.image_paths[idx]
        image_name = os.path.basename(image_path)
        original   = self.original_image.copy()
        hsv        = self.hsv_image.copy()

        self._hide_all_secondary_pages()
        self.main_page_frame.pack_forget()
        self.extraction_page_frame.pack(fill='both', expand=True)

        _refs   = {}
        _result = {}

        header = tk.Frame(self.extraction_page_frame, bg=BG_HEADER, height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text="Color Extraction",
                 font=(FONT, 16, 'bold'), bg=BG_HEADER, fg=TEXT_PRI).place(relx=0.5, rely=0.5, anchor='center')

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
        res_outer.rowconfigure(2, weight=0)
        res_outer.columnconfigure(0, weight=1)
        tk.Label(res_outer, textvariable=res_title_var, font=(FONT, 13, 'bold'),
                 bg='#1e1e1e', fg=TEXT_PRI).grid(row=0, column=0, sticky='w', padx=14, pady=(12, 8))
        res_lbl = tk.Label(res_outer, bg='#1e1e1e',
                           text="\u2190  Select a color below",
                           font=(FONT, 10, 'italic'), fg=TEXT_HINT, anchor='center')
        res_lbl.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 4))

        desc_container = tk.Frame(res_outer, bg='#1e1e1e', height=160)
        desc_container.grid(row=2, column=0, sticky='ew', padx=12, pady=(0, 14))
        desc_container.grid_propagate(False)
        desc_container.columnconfigure(0, weight=1)
        
        desc_card = tk.Frame(desc_container, bg='#141414')
        desc_card.grid(row=0, column=0, sticky='ew')
        desc_card.columnconfigure(0, weight=1)

        tk.Frame(desc_card, bg=ACCENT, height=3).grid(row=0, column=0, sticky='ew')

        inner_pad = tk.Frame(desc_card, bg='#141414')
        inner_pad.grid(row=1, column=0, sticky='ew', padx=20, pady=16)
        inner_pad.columnconfigure(0, weight=1)

        desc_title_lbl = tk.Label(inner_pad, text='', bg='#141414', fg='white',
                                  font=(FONT, 13, 'bold'), anchor='w', justify='left')
        desc_title_lbl.grid(row=0, column=0, sticky='ew', pady=(0, 10))

        desc_body_lbl = tk.Label(inner_pad, text='', bg='#141414', fg='#e0e0e0',
                                 font=(FONT, 11), anchor='w', justify='left',
                                 wraplength=400)
        desc_body_lbl.grid(row=1, column=0, sticky='ew')

        desc_card.grid_remove()

        status_var = tk.StringVar(value="Image loaded successfully")
        tk.Label(self.extraction_page_frame, textvariable=status_var,
                 font=(FONT, 9), bg=BG_DARK, fg=TEXT_HINT).pack(pady=2)

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
        _ecfg = get_image_config(image_path)
        _allowed_ec = _ecfg.get('extract_colors')
        for ck, ci in self.extraction_colors.items():
            if _allowed_ec is not None and ck not in _allowed_ec:
                continue
            if _allowed_ec is None and ck == 'black':
                continue
            tk.Button(colors_center,
                      text=f"\u25cf {ci['display_name']}",
                      font=(FONT, 11, 'bold'),
                      bg=ci['button_color'], fg='white',
                      width=15, padx=4, pady=6,
                      relief='flat', cursor='hand2', bd=0,
                      activeforeground='white',
                      command=lambda k=ck: _do_extract(k)).pack(side=tk.LEFT, padx=6)

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

        _extract_descs = _ecfg.get('extract_descriptions', {})

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
                entry = _extract_descs.get(color_key)
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
        
        self._hide_all_secondary_pages()
        self.main_page_frame.pack(fill='both', expand=True)

    def previous_image(self):
        
        if len(self.image_paths) > 1:
            previous_index = (self.current_image_index - 1) % len(self.image_paths)
            self.switch_to_image(previous_index)
    
    def next_image(self):
        
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
    
    
    def switch_to_image(self, image_index):
        
        if 0 <= image_index < len(self.image_paths):
            self.current_image_index = image_index
            self.load_current_image()
            
            self.update_image_indicator()
            
            self.update_image_buttons()
            
            self.hide_filter_options()
    
    def show_extraction_options(self):
        
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        self.hide_filter_options()
        
        self.extraction_controls_container.pack(pady=20)
    
    def hide_extraction_options(self):
        
        self.extraction_controls_container.pack_forget()
        self.results_display_container.pack_forget()
    
    def show_filter_options(self):
        
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        self.hide_extraction_options()
        
        self.filter_controls_container.pack(pady=20)
    
    def hide_filter_options(self):
        
        self.filter_controls_container.pack_forget()
        self.results_display_container.pack_forget()
    
    def cv2_to_tk_image(self, cv2_image, max_width=400, max_height=300):
        
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        
        height, width = rgb_image.shape[:2]
        if width > max_width or height > max_height:
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            rgb_image = cv2.resize(rgb_image, (new_width, new_height))
        
        pil_image = Image.fromarray(rgb_image)
        return ImageTk.PhotoImage(pil_image)
    
    def display_results(self, operation_name, is_filter=False):
        
        self.results_display_container.pack_forget()
        self.results_display_container = tk.Frame(self.main_page_frame, bg='#f0f0f0')
        self.results_display_container.pack(pady=20, fill='both', expand=True)
        
        operation_type = "Filter" if is_filter else "Extraction"
        current_image_name = os.path.splitext(os.path.basename(self.image_paths[self.current_image_index]))[0]
        results_title = tk.Label(self.results_display_container, 
                                text=f"✨ {operation_name} {operation_type} Results\nImage {self.current_image_index + 1} of {len(self.image_paths)}: {current_image_name}", 
                                font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        results_title.pack(pady=10)
        
        images_container = tk.Frame(self.results_display_container, bg='#f0f0f0')
        images_container.pack()
        
        original_frame = tk.Frame(images_container, bg='white', relief='solid', bd=2)
        original_frame.pack(side=tk.LEFT, padx=20)
        
        original_label = tk.Label(original_frame, text="Original Image", 
                                 font=('Arial', 12, 'bold'), bg='white', fg='#333')
        original_label.pack(pady=5)
        
        original_tk_image = self.cv2_to_tk_image(self.original_image)
        original_image_label = tk.Label(original_frame, image=original_tk_image, bg='white')
        original_image_label.image = original_tk_image
        original_image_label.pack(padx=10, pady=10)
        
        result_frame = tk.Frame(images_container, bg='white', relief='solid', bd=2)
        result_frame.pack(side=tk.LEFT, padx=20)
        
        operation_type = "Filter Applied" if is_filter else "Extracted"
        result_label = tk.Label(result_frame, text=f"{operation_name} {operation_type}", 
                               font=('Arial', 12, 'bold'), bg='white', fg='#333')
        result_label.pack(pady=5)
        
        result_tk_image = self.cv2_to_tk_image(self.result_image)
        result_image_label = tk.Label(result_frame, image=result_tk_image, bg='white')
        result_image_label.image = result_tk_image
        result_image_label.pack(padx=10, pady=10)
        
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
        
        if filter_key not in self.color_filters:
            messagebox.showerror("Error", "Invalid filter selection!")
            return False
        
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return False
        
        filter_info = self.color_filters[filter_key]
        self.show_progress(f"Applying {filter_info['display_name']}...")
        
        try:
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
    
    
    def update_status(self, message, success=True):
        
        color = '#4CAF50' if success else '#f44336'
        self.status_label.config(text=message, fg=color)
    
    def save_result(self):
        
        if self.result_image is not None:
            try:
                current_image_path = self.image_paths[self.current_image_index]
                original_name = os.path.splitext(os.path.basename(current_image_path))[0]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{original_name}_processed_{timestamp}.jpg"
                
                filepath = os.path.join(os.path.dirname(current_image_path), filename)
                cv2.imwrite(filepath, self.result_image)
                
                messagebox.showinfo("Success", f"Image saved as:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
        else:
            messagebox.showwarning("Warning", "No result image to save!")
    
    def show_progress(self, message="Processing..."):
        
        self.status_label.config(text=message, fg='#FF9800')
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10)
        self.root.update()
    
    def hide_progress(self):
        
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
    
    def load_current_image(self):
        
        if self.current_image_index < len(self.image_paths):
            return self.load_image(self.image_paths[self.current_image_index])
        return False
    
    
    def load_image(self, image_path):
        
        try:
            self.original_image = cv2.imread(image_path)
            if self.original_image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
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
        
        if color_key not in self.extraction_colors:
            messagebox.showerror("Error", "Invalid color selection!")
            return False
        
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return False
        
        color_info = self.extraction_colors[color_key]
        self.show_progress(f"Extracting {color_info['display_name']} color...")
        
        try:
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
        
        self.hide_extraction_options()
        self.hide_filter_options()
    
    
    def run(self, image_paths):
        
        try:
            self.image_paths = image_paths
            
            self.setup_image_buttons()
            
            if self.load_current_image():
                self.update_image_buttons()
                
                self.root.update_idletasks()
                width = self.root.winfo_width()
                height = self.root.winfo_height()
                x = (self.root.winfo_screenwidth() // 2) - (width // 2)
                y = (self.root.winfo_screenheight() // 2) - (height // 2)
                self.root.geometry(f'{width}x{height}+{x}+{y}')
                
                self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Application error:\n{str(e)}")
