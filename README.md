# MiniBrowser 🕸️

A simple **educational web browser** project built with Python. Perfect for learning how web browsers work under the hood!

## ⚡ Quick Start - Open Browser Now!

**[🚀 Click here to launch MiniBrowser](minibrowser://launch)** — This will open the browser application and let you browse the web!

---

## What is this?

MiniBrowser is a lightweight, **text-only** web browser with a graphical interface. It fetches real web pages, extracts readable content and links, and lets you navigate — all while staying simple and educational.

It's designed as a **learning project** to teach:
- HTTP requests and web fetching
- HTML parsing
- GUI programming with event-driven design
- History management (back/forward stack)
- Basic state persistence (bookmarks)
- Game library integration

**Note**: This is *not* a replacement for Chrome/Firefox. It has no JavaScript, no CSS styling, no images, and no video. It's intentionally basic (like a modern Lynx with a GUI) so you can focus on core concepts.

## Features

- ✅ URL bar + Go button
- ✅ Back / Forward / Home / Refresh buttons
- ✅ Page title + clean text content display
- ✅ Sidebar with clickable links from the current page
- ✅ Browsing history (back/forward stack)
- ✅ Bookmark pages (saved to `bookmarks.json`)
- ✅ Bookmarks menu to quickly load saved pages
- ✅ **🎮 Game Library** - Browse and play games directly in the browser
- ✅ Status bar showing load status and link count
- ✅ Error handling and user-friendly messages
- ✅ Keyboard support (Enter to load URL)

## Requirements

- Python 3.8 or newer
- `requests` library
- `beautifulsoup4` library

**tkinter** comes built-in with Python on most systems (including Windows, macOS, Linux).

## Installation & Setup

1. Clone or download this folder.

2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```

3. Run the browser:
   ```bash
   python mini_browser.py
   ```

4. Try typing a URL like:
   - `https://example.com`
   - `https://en.wikipedia.org/wiki/Python_(programming_language)`
   - `https://news.ycombinator.com`

Click links in the sidebar to explore!

## 🎮 Game Library Feature

MiniBrowser now includes a built-in **Game Library** feature:

- Click the **🎮 Game Library** button in the toolbar
- Browse all available games
- Launch games directly in the browser with **"▶ Play in Browser"** button
- Open games externally with **"🔗 Open External"** button
- Currently includes **BrawlGO** - your multiplayer fighting game!

**To add more games**, edit the `games_library` list in `mini_browser.py`:

```python
self.games_library = [
    {
        "title": "Your Game Name",
        "description": "Game description",
        "url": "https://your-game-url.com",
        "icon": "🎮"  # Use any emoji!
    }
]
```

## Project Structure

```
mini_browser_project/
├── mini_browser.py      # Main application (all the magic)
├── README.md            # This file
├── requirements.txt     # Dependencies
└── bookmarks.json       # Auto-created when you bookmark pages
```

## How It Works (Deep Dive for Learners)

### 1. Fetching Content (`fetch_page`)
- Uses `requests.get()` with a custom User-Agent.
- Handles redirects and timeouts.
- Returns the final URL, page title, cleaned text, and list of links.

### 2. HTML Parsing with BeautifulSoup
- Removes `<script>` and `<style>` tags.
- Extracts readable text with `get_text(separator='\n')`.
- Finds all `<a href="...">` tags and converts relative URLs to absolute using `urljoin()`.

### 3. GUI with tkinter
- `ttk` widgets for modern look (buttons, entry, progress).
- `ScrolledText` for the main content area.
- `Listbox` for clickable links.
- Event bindings (`<Return>`, `<Double-1>`).
- `StringVar` and `update_idletasks()` for responsive UI.

### 4. Navigation & History
- History is a simple Python list + current index (classic back/forward pattern).
- New pages truncate any "forward" history.
- Special method to load from history without duplicating entries.

### 5. Persistence
- Bookmarks saved/loaded as JSON for simplicity.

### 6. Game Library Integration
- Games stored in a list with metadata (title, description, URL, icon).
- Dedicated window shows all games with dual-launch options.
- Play games in-browser or externally based on user preference.

## Extending MiniBrowser (Fun Project Ideas)

Here are great ways to level up your project:

| Idea | Difficulty | What to Learn |
|------|------------|---------------|
| Add **tabs** using `ttk.Notebook` | Medium | Managing multiple browser instances |
| **Search bar** that queries DuckDuckGo or Wikipedia | Easy | API usage or form simulation |
| **Download manager** for links ending in .pdf/.zip | Medium | File handling + threading |
| **Dark mode** toggle | Easy | Custom ttk themes |
| **Page source viewer** (View > Source) | Easy | Another text window |
| **Basic cache** (don't re-download same page) | Medium | Dictionaries + timestamps |
| **Keyboard shortcuts** (Ctrl+L for URL bar, etc.) | Easy | bind() with modifiers |
| **Export to Markdown/PDF** | Medium | ReportLab or markdown libs |
| Replace text view with **HTML rendering** (advanced) | Hard | Use `tkhtml` or switch to PyQtWebEngine |
| Add **ad-blocking** (simple domain filter) | Medium | Pre-process HTML before parsing |
| **Multiplayer game integration** | Medium | WebSocket client support |

## Common Issues & Fixes

- **"tkinter not found"** on Linux: `sudo apt install python3-tk`
- **SSL errors**: Update certifi or use `verify=False` (not recommended for production)
- **Slow pages**: Add a loading spinner or thread the fetch (advanced: use `threading`)
- **Unicode issues**: Already handled by requests/BeautifulSoup
- **Games not loading**: Check your internet connection and that the game URL is accessible

## Usage Tips

### Browsing
1. Type a URL in the address bar (with or without `https://`)
2. Press **Enter** or click **Go**
3. Click any link in the sidebar to navigate
4. Use **Back/Forward** buttons to traverse history

### Bookmarks
1. Load any page
2. Click **★ Bookmark** or use **Bookmarks** menu
3. Access saved pages from the **Bookmarks** menu

### Games
1. Click **🎮 Game Library** button
2. Select a game from the list
3. Click **▶ Play in Browser** to play here
4. Use browser controls to navigate within the game

## Why Build This?

Understanding browsers at this level helps you become a better web developer, debugger, or even security researcher. Many concepts (URLs, HTTP, DOM parsing) transfer directly to building web scrapers, automation tools, and modern web apps.

## License

This project is released under the **MIT License**. Feel free to use it for learning, teaching, portfolios, or hacking on it further!

---

**Happy browsing and coding!** 🚀

If you extend it or have questions, feel free to share your improvements.

Built as an educational example by Koustavxd.
