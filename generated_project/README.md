# SimpleCalc

## Project Title
**SimpleCalc** – A lightweight, web‑based calculator built with plain HTML, CSS, and JavaScript.

## Brief Description
SimpleCalc provides a clean, responsive interface for performing basic arithmetic operations. It works entirely in the browser—no server, no build steps—making it perfect for learning, quick calculations, or embedding in other web pages.

---

## Tech Stack
- **HTML5** – Structure and layout of the calculator UI.
- **CSS3** – Styling, responsive design, and visual feedback for button presses.
- **JavaScript (ES6+)** – Core logic handling button clicks, keyboard shortcuts, calculations, and error handling.

---

## Features
- **Basic arithmetic** – Addition, subtraction, multiplication, and division.
- **Keyboard support** – Use the keyboard for rapid entry:
  - Numbers `0‑9`
  - Decimal point `.`
  - Operators `+`, `-`, `*`, `/`
  - `Enter` → `=` (calculate)
  - `Backspace` → `⌫` (delete last entry)
  - `Esc` → `C` (clear all)
- **Error handling** – Division by zero displays a clear error message.
- **Responsive design** – Optimized for both desktop and mobile browsers.
- **No dependencies** – Pure client‑side code, no frameworks or build tools required.

---

## Screenshot
> *(Replace the placeholder below with an actual screenshot of the calculator UI)*

```
[Insert screenshot here]
```

---

## Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/simplecalc.git
   cd simplecalc
   ```
2. **Open the application**
   - No build step is needed. Simply open `index.html` in any modern web browser.
   ```bash
   open index.html   # macOS
   # or double‑click the file in Explorer/Finder
   ```

---

## Usage
- **Button clicks** – Click any on‑screen button to input numbers, operators, or commands.
- **Keyboard shortcuts**
  - `0‑9` – Enter digits.
  - `.` – Insert a decimal point.
  - `+`, `-`, `*`, `/` – Choose an operator.
  - `Enter` – Perform the calculation (`=`).
  - `Backspace` – Delete the last character (`⌫`).
  - `Esc` – Clear the entire expression (`C`).
- **Result display** – The current expression and the computed result appear in the display area.
- **Error handling** – Attempting to divide by zero shows the message `Error: Division by zero` and clears the expression.

---

## Responsive Design
SimpleCalc automatically adapts to the screen size:
- **Desktop** – Buttons are arranged in a classic calculator grid.
- **Mobile** – Buttons scale and re‑flow for comfortable tapping on smaller screens.
The layout is achieved using CSS Flexbox/Grid and media queries, ensuring usability across devices.

---

## Contributing
Contributions are welcome! Follow these steps to get involved:
1. **Fork the repository**.
2. **Create a new branch** for your feature or bug‑fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and ensure the calculator still works locally.
4. **Commit with clear messages** and push to your fork.
5. **Open a Pull Request** against the `main` branch, describing the changes and why they are needed.

Please adhere to the existing code style (indentation, naming conventions) and include any relevant tests or documentation updates.

---

## License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

*Happy calculating!*