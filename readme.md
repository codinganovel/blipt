# blipt
**blipt** is a fast, disposable scratchpad for your terminal. It's a tool designed to let you quickly jot down, copy, and clear lists of ideas, todos, or notes — without the need for saving files manually. Every session lives in memory, and a markdown-based history is saved automatically in your current folder.
> No clutter. No pressure. Just type and toss.
---
## ✨ Features
- In-memory scratchpad that resets on exit  
- Numbered bullet list interface  
- Markdown-based history file saved as `Scratchmd.md`  
- Copy individual items or the full list to your clipboard  
- Clean TUI-style redraw after every command  
---
## 📦 Installation

[get yanked](https://github.com/codinganovel/yanked)

---
### Available Commands
| Command         | Description                          |
|----------------|--------------------------------------|
| `add <text>`    | Adds a new line to the scratchpad     |
| `copy <n>`      | Copies item `n` to the clipboard       |
| `copy all`      | Copies all items to the clipboard      |
| `delete <n>`    | Deletes item `n` from the list         |
| `delete all`    | Clears the entire scratchpad           |
| `exit`          | Exits the app                         |
A file named `Scratchmd.md` is created in the working directory and logs each `add` entry with a timestamp.
---
## 📋 Clipboard Support & Dependencies
`blipt` uses [pyperclip](https://pypi.org/project/pyperclip/) to interact with the system clipboard.
### macOS  
✅ Works out of the box using built-in `pbcopy`
### Windows  
✅ Works out of the box using Windows clipboard API
### Linux  
⚠️ You need to install a clipboard utility:
```bash
sudo apt install xclip   # or
sudo apt install xsel
```
---
## 📄 License

under ☕️, check out [the-coffee-license](https://github.com/codinganovel/The-Coffee-License)

I've included both licenses with the repo, do what you know is right. The licensing works by assuming you're operating under good faith.
---
## ✍️ Created by Sam  
Because some thoughts don’t deserve to be remembered forever.
