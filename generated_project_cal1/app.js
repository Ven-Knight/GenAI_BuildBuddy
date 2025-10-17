// SimpleCalc core logic
// This script assumes the following HTML structure:
// - An input (or textarea) with id="display" to show the current expression/result.
// - Buttons with class "btn" and a data-value attribute indicating their function/value.
//   Typical values: digits "0"‑"9", decimal ".", operators "+", "-", "*", "/",
//   "C" (clear entry), "AC" (all clear), "←" (backspace), "=" (evaluate).

// ------------------------------------------------------------
// 1. DOM references and helper to update the display
const displayEl = document.getElementById('display');
const buttons = document.querySelectorAll('.btn');

function updateDisplay(value) {
  // Ensure the display always shows a string (e.g., "0" when empty)
  displayEl.value = value;
}

// ------------------------------------------------------------
// 2. Calculator class definition
class Calculator {
  constructor() {
    this.expression = '';
    this.lastResult = null; // Holds the numeric result of the last evaluation
  }

  // Helper: determine if a character is an operator
  static isOperator(ch) {
    return /[+\-*/]/.test(ch);
  }

  // Helper: get the last character of the current expression
  _lastChar() {
    return this.expression.slice(-1);
  }

  // Helper: get the current number segment (since the last operator)
  _currentNumber() {
    const parts = this.expression.split(/(?=[+\-*/])/); // split before each operator
    return parts.length ? parts[parts.length - 1] : '';
  }

  // Reset expression after a result when the user starts a new number
  resetAfterResult() {
    if (this.lastResult !== null && this.expression === '') {
      // Starting a new expression; clear stored result
      this.lastResult = null;
    }
  }

  // Append a character (digit, decimal point, or operator) with validation
  append(char) {
    // If we just displayed a result and the user types a digit or '.' start fresh
    if (this.lastResult !== null && (/[0-9.]/.test(char))) {
      this.expression = '';
      this.lastResult = null;
    }

    if (/[0-9]/.test(char)) {
      // Simple digit – always allowed
      this.expression += char;
    } else if (char === '.') {
      // Allow a single decimal point per number segment
      const currentNum = this._currentNumber();
      if (!currentNum.includes('.')) {
        // If the current segment is empty (e.g., expression ends with an operator), prepend a leading zero
        if (currentNum === '') {
          this.expression += '0';
        }
        this.expression += '.';
      }
    } else if (Calculator.isOperator(char)) {
      // Prevent consecutive operators (except allowing '-' as a unary minus at start)
      const last = this._lastChar();
      if (this.expression === '' && char === '-') {
        // Allow leading negative sign
        this.expression += char;
      } else if (last && Calculator.isOperator(last)) {
        // Replace the previous operator with the new one (more user‑friendly)
        this.expression = this.expression.slice(0, -1) + char;
      } else if (last) {
        this.expression += char;
      }
    }
    // Any other characters are ignored silently
  }

  // Clear the current entry (C)
  clearEntry() {
    this.expression = '';
  }

  // All clear (AC) – reset everything
  allClear() {
    this.expression = '';
    this.lastResult = null;
  }

  // Remove the last character (Backspace)
  backspace() {
    if (this.expression.length > 0) {
      this.expression = this.expression.slice(0, -1);
    }
  }

  // Evaluate the current arithmetic expression safely
  evaluate() {
    if (!this.expression) {
      throw 'Empty expression';
    }
    // Disallow trailing operator (e.g., "5+"), which would cause a syntax error
    const trimmedExpr = this.expression.replace(/[+\-*/]$/g, '');
    try {
      // Using Function constructor for evaluation – sandboxed enough for basic arithmetic
      const result = Function('"use strict"; return (' + trimmedExpr + ')')();
      // Detect division by zero or other infinite results
      if (!isFinite(result)) {
        throw 'Math error';
      }
      // Store result and clear expression for next input
      this.lastResult = result;
      this.expression = '';
      return result;
    } catch (e) {
      // Rethrow a generic error string for UI handling
      throw typeof e === 'string' ? e : 'Error';
    }
  }
}

// ------------------------------------------------------------
// 3. Instantiate a single calculator
const calculator = new Calculator();

// ------------------------------------------------------------
// 4. Button click handling
buttons.forEach(btn => {
  btn.addEventListener('click', () => {
    const value = btn.getAttribute('data-value');
    try {
      switch (value) {
        case 'C':
          calculator.clearEntry();
          break;
        case 'AC':
          calculator.allClear();
          break;
        case '←': // backspace symbol – adjust if your HTML uses a different label
        case '←': // duplicate for safety
          calculator.backspace();
          break;
        case '=':
          calculator.evaluate();
          break;
        default:
          // Assume any other value is a character to append (digit, '.', operator)
          calculator.append(value);
      }
    } catch (err) {
      // Show error temporarily
      const previous = calculator.expression || calculator.lastResult || '0';
      updateDisplay('Error');
      setTimeout(() => updateDisplay(previous), 1500);
      return; // Skip the normal display update below
    }
    // Update display after successful action
    const displayValue = calculator.expression || (calculator.lastResult !== null ? calculator.lastResult : '0');
    updateDisplay(displayValue);
  });
});

// ------------------------------------------------------------
// 5. Keyboard input handling
document.addEventListener('keydown', (e) => {
  const key = e.key;
  // Allow only relevant keys – ignore modifiers like Shift (except for '*')
  const allowedDigits = /[0-9]/;
  const allowedOps = /[+\-*/]/;
  let handled = false;

  if (allowedDigits.test(key) || key === '.') {
    calculator.append(key);
    handled = true;
  } else if (allowedOps.test(key)) {
    // For '*' key on the main keyboard it's fine; for 'x' we could map, but not required
    calculator.append(key);
    handled = true;
  } else if (key === 'Enter' || key === '=') {
    try {
      calculator.evaluate();
    } catch (err) {
      const previous = calculator.expression || calculator.lastResult || '0';
      updateDisplay('Error');
      setTimeout(() => updateDisplay(previous), 1500);
    }
    handled = true;
  } else if (key === 'Backspace') {
    calculator.backspace();
    handled = true;
  } else if (key === 'Escape') {
    calculator.allClear();
    handled = true;
  }

  if (handled) {
    e.preventDefault();
    const displayValue = calculator.expression || (calculator.lastResult !== null ? calculator.lastResult : '0');
    updateDisplay(displayValue);
  }
});

// ------------------------------------------------------------
// 6. Export for testing (Node environment)
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
  module.exports = { Calculator, calculator };
}
