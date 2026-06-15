# MiniBrowser 🕸️

A simple **educational web browser** project built with Python. Perfect for learning how web browsers work under the hood!

## What is this?

MiniBrowser is a lightweight, **text-only** web browser with a graphical interface. It fetches real web pages, extracts readable content and links, and lets you navigate — all while staying simple enough to understand every line of code.

It's designed as a **learning project** to teach:
- HTTP requests and web fetching
- HTML parsing
- GUI programming with event-driven design
- History management (back/forward stack)
- Basic state persistence (bookmarks)

**Note**: This is *not* a replacement for Chrome/Firefox. It has no JavaScript, no CSS styling, no images, and no video. It's intentionally basic (like a modern Lynx with a GUI) so you can focus on core browser concepts.

## Features

- ✅ URL bar + Go button
- ✅ Back / Forward / Home / Refresh buttons
- ✅ Page title + clean text content display
- ✅ Sidebar with clickable links from the current page
- ✅ Browsing history (back/forward stack)
- ✅ Bookmark pages (saved to `bookmarks.json`)
- ✅ Bookmarks menu to quickly load saved pages
- ✅ Status bar showing load status and link count
- ✅ Error handling and user-friendly messages
- ✅ Keyboard support (Enter to load URL)

## Requirements

- Python 3.8 or newer
- `requests` library
- `beautifulsoup4` library

**tkinter** comes built-in with Python on most systems (including Windows, macOS, Linux).

## Quick Start

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

## Common Issues & Fixes

- **"tkinter not found"** on Linux: `sudo apt install python3-tk`
- **SSL errors**: Update certifi or use `verify=False` (not recommended for production)
- **Slow pages**: Add a loading spinner or thread the fetch (advanced: use `threading`)
- **Unicode issues**: Already handled by requests/BeautifulSoup

## Why Build This?

Understanding browsers at this level helps you become a better web developer, debugger, or even security researcher. Many concepts (URLs, HTTP, DOM parsing) transfer directly to building web scrapers, APIs, or your own tools.

## License

This project is released under the **MIT License**. Feel free to use it for learning, teaching, portfolios, or hacking on it further!

---

**Happy browsing and coding!** 🚀

If you extend it or have questions, feel free to share your improvements. 

Built as an educational example by Grok.
