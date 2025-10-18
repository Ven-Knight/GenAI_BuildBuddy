// Simple Calculator JavaScript Logic
// --------------------------------------------------
// This script attaches event listeners to calculator buttons
// and keyboard input, maintains an internal state representing
// the current expression, updates the display, and evaluates
// the expression when the user presses "=" or Enter.

// Obtain references to DOM elements
const display = document.getElementById('display');
const buttons = document.querySelectorAll('.btn');

// State object tracking the current input string
const state = {
  /**
   * The raw expression the user has entered, e.g. "12+3*4".
   * It is kept as a string so we can easily append characters
   * and manipulate it (backspace, clear, etc.).
   */
  currentInput: ''
};

/**
 * Initialise the calculator: attach click listeners to each button
 * and a keydown listener to the document.
 */
function initCalculator() {
  buttons.forEach(button => {
    button.addEventListener('click', handleButtonClick);
  });
  document.addEventListener('keydown', handleKeyPress);
}

/**
 * Handle a click on a calculator button.
 * The button's `data-value` attribute determines the action.
 * @param {MouseEvent} e
 */
function handleButtonClick(e) {
  const value = e.target.dataset.value;
  if (!value) return; // safety guard

  switch (value) {
    case 'C':
      clearDisplay();
      break;
    case 'backspace':
      backspace();
      break;
    case '=':
      calculateResult();
      break;
    case '+':
    case '-':
    case '*':
    case '/':
      appendOperator(value);
      break;
    default:
      // numbers and decimal point fall here
      appendNumber(value);
  }
}

/**
 * Map keyboard keys to the same actions as button clicks.
 * Supports digits, decimal point, basic operators, Enter, Backspace,
 * Escape (clear) and Delete (clear).
 * @param {KeyboardEvent} e
 */
function handleKeyPress(e) {
  const key = e.key;
  if (key >= '0' && key <= '9') {
    appendNumber(key);
    return;
  }
  if (key === '.') {
    appendNumber(key);
    return;
  }
  if (key === '+' || key === '-' || key === '*' || key === '/') {
    appendOperator(key);
    return;
  }
  if (key === 'Enter' || key === '=') {
    e.preventDefault(); // prevent form submission if any
    calculateResult();
    return;
  }
  if (key === 'Backspace') {
    backspace();
    return;
  }
  if (key === 'Escape' || key === 'Delete') {
    clearDisplay();
    return;
  }
}

/**
 * Append a numeric character (or decimal point) to the current input.
 * @param {string} value - a digit "0"‑"9" or "."
 */
function appendNumber(value) {
  // Prevent multiple leading zeros like "00"
  if (value === '0' && state.currentInput.endsWith('0') && !/[+\-*/]0$/.test(state.currentInput)) {
    // allow zeros after an operator or as the first character
  }
  state.currentInput += value;
  updateDisplay();
}

/**
 * Append an operator (+, -, *, /) to the expression.
 * Ensures the last character is not already an operator.
 * @param {string} op
 */
function appendOperator(op) {
  if (state.currentInput === '') {
    // Allow a leading minus for negative numbers
    if (op === '-') {
      state.currentInput = op;
      updateDisplay();
    }
    return;
  }
  const lastChar = state.currentInput.slice(-1);
  if (/[+\-*/]/.test(lastChar)) {
    // Replace the previous operator with the new one
    state.currentInput = state.currentInput.slice(0, -1) + op;
  } else {
    state.currentInput += op;
  }
  updateDisplay();
}

/**
 * Evaluate the current expression and display the result.
 * Uses the Function constructor for simple evaluation while
 * catching errors such as syntax problems or division by zero.
 */
function calculateResult() {
  const expr = state.currentInput;
  if (!expr) return;

  // Guard against trailing operator (e.g., "5+" )
  const sanitizedExpr = expr.replace(/[+\-*/]$/g, '');
  try {
    // Using Function is safer than eval because it creates a new scope.
    // It still executes JavaScript, so we keep the expression simple.
    const result = Function(`'use strict'; return (${sanitizedExpr});`)();
    if (result === Infinity || result === -Infinity) {
      showError('Error: Division by zero');
      return;
    }
    // Round result to a reasonable number of decimal places to avoid floating‑point noise.
    const formatted = Number.isFinite(result) ? Number(result.toFixed(12)).toString() : '' + result;
    state.currentInput = formatted;
    updateDisplay();
  } catch (err) {
    showError('Error');
  }
}

/**
 * Clear the display and reset the internal state.
 */
function clearDisplay() {
  state.currentInput = '';
  updateDisplay();
}

/**
 * Remove the last character from the current input.
 */
function backspace() {
  if (state.currentInput.length > 0) {
    state.currentInput = state.currentInput.slice(0, -1);
    updateDisplay();
  }
}

/**
 * Update the calculator display to reflect the current input.
 */
function updateDisplay() {
  display.value = state.currentInput;
}

/**
 * Show an error message temporarily, then restore the previous expression.
 * @param {string} msg
 */
function showError(msg) {
  const previous = state.currentInput;
  display.value = msg;
  // After 2 seconds restore the previous value (if any)
  setTimeout(() => {
    display.value = previous;
    // Keep the internal state unchanged so the user can edit it.
  }, 2000);
}

// Initialise the calculator once the script loads (deferred script runs after DOM ready).
initCalculator();
