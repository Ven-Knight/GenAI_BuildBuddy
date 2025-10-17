# SimpleCalc

**SimpleCalc** is a lightweight, web‑based calculator built with plain **HTML**, **CSS**, and **JavaScript**. It runs entirely in the browser – no build tools, servers, or dependencies are required.

---

## Tech Stack
- **HTML5** – structure and accessibility markup
- **CSS3** – responsive layout and visual styling
- **JavaScript (ES6+)** – core calculator logic, DOM interaction, and keyboard support

---

## Features
- Basic arithmetic: addition, subtraction, multiplication, division
- Decimal numbers and unary minus support
- Clear entry (**C**) and all‑clear (**AC**) functions
- Backspace (⌫) to delete the last character
- Mouse interaction via on‑screen buttons
- Full keyboard shortcuts:
  - Digits `0‑9` and `.` for decimal point
  - `+`, `-`, `*`, `/` for operators
  - `Enter` or `=` to evaluate
  - `Backspace` to delete
  - `Escape` to all‑clear
- Graceful error handling (e.g., division by zero, malformed expressions)
- Responsive design that works on desktop and mobile browsers

---

## Setup & Usage
1. **Clone the repository** (or download the ZIP):
   ```bash
   git clone https://github.com/your‑username/simplecalc.git
   cd simplecalc
   ```
2. **Open the calculator** – no build step is required. Simply open `index.html` in any modern browser:
   - Double‑click `index.html`
   - or run `open index.html` (macOS) / `start index.html` (Windows) from the command line.

### Using the Calculator
- **Mouse**: Click the on‑screen buttons to build an expression. Press `=` (or the **equals** button) to evaluate.
- **Keyboard**:
  - Type digits and `.` directly.
  - Use `+`, `-`, `*`, `/` for operators.
  - Press **Enter** or `=` to compute.
  - **Backspace** removes the last character.
  - **Escape** clears everything (AC).
- **Error Cases**:
  - Attempting to evaluate an empty expression or a malformed one shows `Error` briefly, then restores the previous value.
  - Division by zero or any non‑finite result also triggers an error message.

---

## Project Structure
```
├─ index.html      # Main UI markup
├─ styles.css      # Visual styling and layout
├─ app.js          # Calculator core logic & event handling
└─ README.md       # Documentation (this file)
```

---

## Contributing
Contributions are welcome! Feel free to fork the repository, make improvements (e.g., adding scientific functions, theme support, etc.), and submit a pull request.

When submitting code, please:
- Keep the same coding style (ES6 classes, descriptive variable names).
- Update the `README.md` if you add new features.
- Ensure the application still works by opening `index.html` in a browser.

---

## License
[Insert License Here] – This project is provided as‑is for educational purposes.

---

## Screenshot
![Calculator Screenshot](screenshot.png)
