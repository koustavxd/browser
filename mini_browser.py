#!/usr/bin/env python3
"""
MiniBrowser - A simple educational web browser with Game Library
Built with Python, tkinter, requests, and BeautifulSoup

This project teaches core browser concepts:
- HTTP requests
- HTML parsing
- GUI event handling
- History management
- Basic persistence
- Game library integration
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
from datetime import datetime
import webbrowser


class MiniBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniBrowser - Educational Web Browser")
        self.root.geometry("1000x750")
        self.root.minsize(800, 600)

        # State
        self.history = []          # List of visited URLs (in order)
        self.current_index = -1    # Current position in history
        self.current_url = ""
        self.bookmarks_file = "bookmarks.json"
        self.bookmarks = self.load_bookmarks()
        self.link_map = {}         # For sidebar: listbox index -> full URL
        
        # Game library
        self.games_library = [
            {
                "title": "BrawlGO",
                "description": "Multiplayer fighting game",
                "url": "https://koustavxd.itch.io/brawlgo",
                "icon": "🎮"
            },
            {
                "title": "Example Game",
                "description": "Your other games here",
                "url": "https://itch.io",
                "icon": "🕹️"
            }
        ]

        # Variables for UI binding
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.title_var = tk.StringVar(value="Welcome to MiniBrowser")

        # Build UI
        self.create_menu()
        self.create_toolbar()
        self.create_main_content()
        self.create_status_bar()

        # Start with a demo page
        self.root.after(100, lambda: self.navigate_to("https://example.com", add_to_history=True))

    def create_menu(self):
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Window (not implemented)", state="disabled")
        file_menu.add_separator()
        file_menu.add_command(label="Save Page as Text...", command=self.save_page_text)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Bookmarks menu
        self.bookmarks_menu = tk.Menu(menubar, tearoff=0)
        self.bookmarks_menu.add_command(label="Bookmark Current Page", command=self.add_bookmark)
        self.bookmarks_menu.add_command(label="Manage Bookmarks...", command=self.show_bookmarks_window)
        self.bookmarks_menu.add_separator()
        self.update_bookmarks_menu()  # Add initial bookmarks
        menubar.add_cascade(label="Bookmarks", menu=self.bookmarks_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About MiniBrowser", command=self.show_about)
        help_menu.add_command(label="How it Works (Educational)", command=self.show_educational_info)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def update_bookmarks_menu(self):
        """Refresh the bookmarks submenu with current bookmarks"""
        # Clear existing dynamic items (keep first 3 static)
        self.bookmarks_menu.delete(3, tk.END)
        if not self.bookmarks:
            self.bookmarks_menu.add_command(label="(No bookmarks yet)", state="disabled")
            return

        for url in self.bookmarks[:15]:  # Limit to avoid huge menu
            display = url[:60] + "..." if len(url) > 60 else url
            self.bookmarks_menu.add_command(
                label=display,
                command=lambda u=url: self.navigate_to(u, add_to_history=True)
            )

    def create_toolbar(self):
        toolbar = ttk.Frame(self.root, padding=5)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        # Navigation buttons
        nav_frame = ttk.Frame(toolbar)
        nav_frame.pack(side=tk.LEFT)

        self.back_btn = ttk.Button(nav_frame, text="◀ Back", command=self.go_back, width=10)
        self.back_btn.pack(side=tk.LEFT, padx=2)

        self.forward_btn = ttk.Button(nav_frame, text="Forward ▶", command=self.go_forward, width=10)
        self.forward_btn.pack(side=tk.LEFT, padx=2)

        self.home_btn = ttk.Button(nav_frame, text="🏠 Home", command=self.go_home, width=10)
        self.home_btn.pack(side=tk.LEFT, padx=2)

        self.refresh_btn = ttk.Button(nav_frame, text="⟳ Refresh", command=self.refresh_page, width=10)
        self.refresh_btn.pack(side=tk.LEFT, padx=2)

        # URL bar
        url_frame = ttk.Frame(toolbar)
        url_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        ttk.Label(url_frame, text="URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=60)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.url_entry.bind("<Return>", lambda e: self.on_url_enter())

        self.go_btn = ttk.Button(url_frame, text="Go", command=self.on_url_enter, width=6)
        self.go_btn.pack(side=tk.LEFT, padx=2)

        # Game Library button
        self.game_library_btn = ttk.Button(toolbar, text="🎮 Game Library", command=self.show_game_library)
        self.game_library_btn.pack(side=tk.RIGHT, padx=5)

        # Bookmark button
        self.bookmark_btn = ttk.Button(toolbar, text="★ Bookmark", command=self.add_bookmark)
        self.bookmark_btn.pack(side=tk.RIGHT, padx=5)

        self.update_nav_buttons()

    def create_main_content(self):
        # Main horizontal split: Content (left) + Links sidebar (right)
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # === Left: Page content ===
        content_frame = ttk.LabelFrame(main_paned, text="Page Content", padding=5)
        main_paned.add(content_frame, weight=3)

        # Page title
        title_frame = ttk.Frame(content_frame)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(title_frame, text="Title:", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        ttk.Label(title_frame, textvariable=self.title_var, font=("Helvetica", 11)).pack(side=tk.LEFT, padx=5)

        # Main text display
        self.content_text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#f8f9fa",
            fg="#212529",
            padx=10,
            pady=10
        )
        self.content_text.pack(fill=tk.BOTH, expand=True)
        self.content_text.config(state=tk.DISABLED)  # Read-only

        # === Right: Links sidebar ===
        links_frame = ttk.LabelFrame(main_paned, text="Links on Page (double-click to open)", padding=5)
        main_paned.add(links_frame, weight=1)

        self.links_listbox = tk.Listbox(
            links_frame,
            font=("Consolas", 10),
            bg="#ffffff",
            selectbackground="#0d6efd",
            selectforeground="white",
            activestyle="none"
        )
        self.links_listbox.pack(fill=tk.BOTH, expand=True)
        self.links_listbox.bind("<Double-1>", self.on_link_double_click)

        scrollbar = ttk.Scrollbar(links_frame, orient=tk.VERTICAL, command=self.links_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.links_listbox.config(yscrollcommand=scrollbar.set)

        # Quick tip at bottom of sidebar
        tip = ttk.Label(links_frame, text="Tip: Double-click any link to navigate", font=("Helvetica", 8, "italic"))
        tip.pack(pady=3)

    def create_status_bar(self):
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=5
        )
        self.status_label.pack(fill=tk.X, expand=True)

    # ==================== Game Library ====================

    def show_game_library(self):
        """Display game library in a new window."""
        win = tk.Toplevel(self.root)
        win.title("Game Library")
        win.geometry("600x400")
        win.transient(self.root)

        ttk.Label(win, text="🎮 Your Game Library", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Create scrollable frame for games
        canvas = tk.Canvas(win, bg="#f8f9fa")
        scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add game buttons
        for game in self.games_library:
            game_frame = ttk.LabelFrame(scrollable_frame, text=f"{game['icon']} {game['title']}", padding=10)
            game_frame.pack(fill=tk.X, padx=10, pady=8)

            ttk.Label(game_frame, text=game['description'], font=("Helvetica", 10)).pack(anchor=tk.W)

            button_frame = ttk.Frame(game_frame)
            button_frame.pack(fill=tk.X, pady=(8, 0))

            ttk.Button(
                button_frame,
                text="▶ Play in Browser",
                command=lambda url=game['url']: self.play_game(url, win)
            ).pack(side=tk.LEFT, padx=5)

            ttk.Button(
                button_frame,
                text="🔗 Open External",
                command=lambda url=game['url']: webbrowser.open(url)
            ).pack(side=tk.LEFT, padx=5)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Close button
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def play_game(self, game_url, window):
        """Load game in the browser and close the game library window."""
        window.destroy()
        self.navigate_to(game_url, add_to_history=True)

    # ==================== Core Browser Logic ====================

    def navigate_to(self, url, add_to_history=True):
        """Main navigation method. Handles scheme, history, and display."""
        if not url or not url.strip():
            return

        url = url.strip()

        # Add scheme if missing
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        # Update UI immediately
        self.url_var.set(url)
        self.status_var.set(f"Loading {url}...")
        self.root.update_idletasks()

        try:
            title, text_content, links, final_url = self.fetch_page(url)

            # Update history only for new navigations
            if add_to_history:
                # Truncate forward history if we went back then navigated new
                self.history = self.history[:self.current_index + 1]
                self.history.append(final_url)
                self.current_index = len(self.history) - 1

            self.current_url = final_url
            self.url_var.set(final_url)
            self.title_var.set(title[:80] if title else "Untitled Page")

            # Display content
            self.display_page(title, text_content, links)

            self.status_var.set(f"✓ Loaded: {final_url}  |  {len(links)} links found")

        except Exception as e:
            error_msg = f"Error loading page: {str(e)}"
            self.status_var.set(error_msg)
            self.display_error(error_msg)
            messagebox.showerror("Load Error", error_msg)

        self.update_nav_buttons()

    def fetch_page(self, url):
        """Fetch HTML, parse with BeautifulSoup, return structured data."""
        headers = {
            "User-Agent": "MiniBrowser/1.0 (Educational Python Browser)",
            "Accept": "text/html,application/xhtml+xml"
        }

        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()

        final_url = response.url  # After any redirects

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        # Clean content: remove scripts, styles, etc.
        for tag in soup(["script", "style", "noscript", "meta", "head"]):
            tag.decompose()

        # Get readable text
        text_content = soup.get_text(separator="\n", strip=True)

        # Limit text length for performance/display
        if len(text_content) > 50000:
            text_content = text_content[:50000] + "\n\n[Content truncated for display...]"

        # Extract links
        links = []
        seen_urls = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue

            full_url = urljoin(final_url, href)

            # Only http/https links
            if not full_url.startswith(("http://", "https://")):
                continue

            # Avoid duplicates
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            link_text = a_tag.get_text(strip=True)[:70] or "[No text]"
            links.append((link_text, full_url))

            if len(links) >= 80:  # Limit number of links shown
                break

        return title, text_content, links, final_url

    def display_page(self, title, text_content, links):
        """Update the text widget and links sidebar."""
        # Content area
        self.content_text.config(state=tk.NORMAL)
        self.content_text.delete("1.0", tk.END)

        header = f"{title}\n{'=' * min(len(title), 80)}\n\n"
        self.content_text.insert(tk.END, header)
        self.content_text.insert(tk.END, text_content)
        self.content_text.config(state=tk.DISABLED)

        # Links sidebar
        self.links_listbox.delete(0, tk.END)
        self.link_map.clear()

        for idx, (link_text, full_url) in enumerate(links):
            display = f"{link_text}\n    → {full_url[:65]}"
            self.links_listbox.insert(tk.END, display)
            self.link_map[idx] = full_url

    def display_error(self, error_msg):
        """Show error in content area."""
        self.content_text.config(state=tk.NORMAL)
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert(tk.END, f"⚠️ Error\n{'='*40}\n\n{error_msg}\n\n")
        self.content_text.insert(tk.END, "Try a different URL or check your internet connection.")
        self.content_text.config(state=tk.DISABLED)

        self.links_listbox.delete(0, tk.END)
        self.link_map.clear()

    def on_url_enter(self):
        """Called when user presses Enter or clicks Go."""
        url = self.url_var.get().strip()
        if url:
            self.navigate_to(url, add_to_history=True)

    def on_link_double_click(self, event):
        """Navigate when user double-clicks a link in the sidebar."""
        selection = self.links_listbox.curselection()
        if selection:
            idx = selection[0]
            url = self.link_map.get(idx)
            if url:
                self.navigate_to(url, add_to_history=True)

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            url = self.history[self.current_index]
            self.navigate_to(url, add_to_history=False)

    def go_forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            url = self.history[self.current_index]
            self.navigate_to(url, add_to_history=False)

    def go_home(self):
        """Go to a nice starting page."""
        self.navigate_to("https://en.wikipedia.org/wiki/Main_Page", add_to_history=True)

    def refresh_page(self):
        if self.current_url:
            self.navigate_to(self.current_url, add_to_history=False)

    def update_nav_buttons(self):
        """Enable/disable back/forward buttons based on history position."""
        self.back_btn.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
        self.forward_btn.config(state=tk.NORMAL if self.current_index < len(self.history) - 1 else tk.DISABLED)

    # ==================== Bookmarks ====================

    def load_bookmarks(self):
        if os.path.exists(self.bookmarks_file):
            try:
                with open(self.bookmarks_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # Default bookmarks
        return [
            "https://example.com",
            "https://en.wikipedia.org/wiki/Main_Page",
            "https://news.ycombinator.com",
            "https://github.com"
        ]

    def save_bookmarks(self):
        try:
            with open(self.bookmarks_file, "w", encoding="utf-8") as f:
                json.dump(self.bookmarks, f, indent=2)
        except Exception as e:
            messagebox.showwarning("Save Error", f"Could not save bookmarks: {e}")

    def add_bookmark(self):
        if not self.current_url:
            messagebox.showinfo("Bookmark", "No page loaded to bookmark.")
            return

        if self.current_url in self.bookmarks:
            messagebox.showinfo("Bookmark", "This page is already bookmarked!")
            return

        self.bookmarks.append(self.current_url)
        self.save_bookmarks()
        self.update_bookmarks_menu()
        messagebox.showinfo("Bookmark Added", f"Bookmarked:\n{self.current_url}")

    def show_bookmarks_window(self):
        """Open a window to manage bookmarks."""
        win = tk.Toplevel(self.root)
        win.title("Manage Bookmarks")
        win.geometry("700x450")
        win.transient(self.root)

        ttk.Label(win, text="Your Bookmarks (double-click to open)", font=("Helvetica", 11, "bold")).pack(pady=8)

        listbox = tk.Listbox(win, font=("Consolas", 10), height=15)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for url in self.bookmarks:
            listbox.insert(tk.END, url)

        def load_selected():
            sel = listbox.curselection()
            if sel:
                url = self.bookmarks[sel[0]]
                win.destroy()
                self.navigate_to(url, add_to_history=True)

        def delete_selected():
            sel = listbox.curselection()
            if sel:
                idx = sel[0]
                if messagebox.askyesno("Delete Bookmark", f"Remove this bookmark?\n{self.bookmarks[idx]}"):
                    del self.bookmarks[idx]
                    self.save_bookmarks()
                    self.update_bookmarks_menu()
                    listbox.delete(idx)

        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=8)

        ttk.Button(btn_frame, text="Open Selected", command=load_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=win.destroy).pack(side=tk.LEFT, padx=5)

        listbox.bind("<Double-1>", lambda e: load_selected())

    # ==================== Other ====================

    def save_page_text(self):
        if not self.current_url:
            messagebox.showinfo("Save", "No page loaded.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if filename:
            try:
                content = self.content_text.get("1.0", tk.END)
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"URL: {self.current_url}\n")
                    f.write(f"Saved: {datetime.now()}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(content)
                messagebox.showinfo("Saved", f"Page text saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def show_about(self):
        about_text = """MiniBrowser v2.0

An educational web browser built to demonstrate
how browsers fetch, parse, and display web content.
Now with Game Library integration!

Created as a learning project using:
• Python + tkinter (GUI)
• requests (HTTP client)
• BeautifulSoup (HTML parser)

This browser is intentionally simple (text-only)
to help you understand core concepts clearly.

Features:
✓ URL Navigation & History
✓ Bookmarks Management
✓ Game Library Browser
✓ Link Discovery

Enjoy exploring!"""

        messagebox.showinfo("About MiniBrowser", about_text)

    def show_educational_info(self):
        info = """How MiniBrowser Works (Educational Overview)

1. FETCHING
   - When you enter a URL, we use the 'requests' library
     to send an HTTP GET request to the server.
   - We include a User-Agent header so servers treat us nicely.
   - We follow redirects automatically.

2. PARSING
   - BeautifulSoup turns raw HTML into a structured tree.
   - We remove <script>, <style>, etc. for clean text.
   - We extract the <title> and all <a href="..."> links.
   - Relative URLs are converted to absolute using urljoin().

3. DISPLAY
   - The main area shows readable text content.
   - The sidebar lists clickable links found on the page.
   - Double-clicking a link calls navigate_to() again.

4. HISTORY
   - We keep a simple Python list of URLs + an index.
   - Back/Forward just move the index and re-fetch.
   - New navigation truncates any 'forward' pages.

5. BOOKMARKS
   - Stored in a plain JSON file for easy editing.
   - Menu and dedicated window for management.

6. GAME LIBRARY
   - Browse and play games directly in the browser.
   - Each game can be launched in-browser or externally.

This is similar to how real browsers work, but without
a rendering engine (Blink/WebKit), JavaScript, or CSS.

Want to extend it? Add tabs, caching, or a search feature!"""

        messagebox.showinfo("How MiniBrowser Works", info)


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniBrowser(root)
    root.mainloop()
