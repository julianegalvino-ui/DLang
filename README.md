# DoLang - Alpha

# 📖 Dolang - Complete Language Reference

## What is DoLang?

**DoLang** is an interpreted programming language designed for rapid development of desktop applications and automation tools. Built on top of Python, it offers a clean, intuitive syntax that eliminates the boilerplate of traditional languages while providing native GUI support, smart string interpolation, and explicit memory management.

DoLang was created with a simple philosophy: **"Don't write code for the computer. Write code for yourself."** It's the perfect tool for developers, students, and hobbyists who want to build functional desktop applications in minutes, not hours.

---

##  Core Philosophy

DoLang follows three main principles:

1. **Simplicity First**: Every command is short, memorable, and does exactly what it says. No complex imports, no verbose syntax.
2. **Visual by Default**: GUI development is built into the language. Create windows, buttons, and labels without external libraries.
3. **Explicit Control**: You have full control over memory and types with commands like `demolish`, `collapse`, and type transformers.

---

##  Type System

DoLang has a dynamic type system with four core types:

- **`nde`** (Integer): Whole numbers like `42`, `-7`, `0`
- **`dec`** (Decimal): Floating-point numbers like `3.14`, `-0.5`
- **`chr`** (Character/String): Text values like `"Hello"`, `'World'`
- **`vaco`** (Empty): Represents an empty/null value
- **`hollow`**: Represents a declared variable without a value

Types can be explicitly declared or inferred automatically:

```text
pin nde.age = 25          # Explicit integer
pin dec.pi = 3.14         # Explicit decimal
pin chr.name = "Douglas"  # Explicit string
pin x = 10                # Type inferred as nde
pin y = "text"            # Type inferred as chr
```

---

##  Core Commands

### Variable Declaration (`pin`)
The `pin` command declares and initializes variables. It's the foundation of DoLang's memory system.

```text
pin nde.counter = 0
pin chr.message = tck("Enter your name: ")
pin dec.result = 10.5 * 2
```

### Output (`show`)
The `show()` command prints values to the terminal or GUI console.

```text
show("Hello, World!")
show(42)
show("The result is: " + result)
```

### Input (`tck`)
The `tck()` command (short for "take") prompts the user for input and returns the value.

```text
pin chr.name = tck("What is your name? ")
pin nde.age = tck("How old are you? ")
```

---

##  Control Flow

### Conditional Statements (`if`, `ifat`, `else`)

DLang uses `--` for indentation (one level per `--`). The `ifat` keyword (IF it's not that, it will be thAT) provides a cleaner alternative to `else if`.

```text
pin nde.score = 85

if score >= 90:
--show("Excellent!")
ifat score >= 70:
--show("Good job!")
ifat score >= 50:
--show("You passed.")
else:
--show("Try again.")
```

**Comparison Operators:**
- `==` (Equal)
- `=/` (Not equal)
- `>` (Greater than)
- `<` (Less than)
- `>=` (Greater or equal)
- `<=` (Less or equal)

### Loops (`repeat`, `repeat while`)

The `repeat` command executes a block multiple times or infinitely. The `repeat while` command loops while a condition is true.

```text
# Repeat a command 5 times
repeat: counter(5)

# Infinite loop (Ctrl+C to stop)
repeat: counter

# Loop while condition is true
pin nde.i = 0
repeat while i < 10:
--<pybt>show("Count: {i}")
--pin nde.i = i + 1
```

---

##  Functions

Functions in DLang are defined with `fn` and return values with `ret`.

```text
fn multiply(a, b):
--ret a * b

fn greet(name):
--ret "Hello, " + name + "!"

pin nde.result = multiply(4, 5)
pin chr.message = greet("Douglas")
show(result)      # Outputs: 20
show(message)     # Outputs: Hello, Douglas!
```

Functions can contain complex logic, conditionals, and loops:

```text
fn factorial(n):
--if n <= 1:
----ret 1
--else:
----ret n * factorial(n - 1)

pin nde.result = factorial(5)
show(result)  # Outputs: 120
```

---

##  Type Transformer (`>>`)

The `>>` operator transforms variable types or assigns new values while respecting the declared type.

```text
pin nde.x = 10

# Convert to decimal
x >> dec
show(x)  # Outputs: 10.0

# Convert to string
x >> chr
show(x)  # Outputs: "10"

# Assign new value (must be compatible with type)
x >> 42
show(x)  # Outputs: 42

# This will fail (string can't be nde)
x >> "hello"  # Error!
```

---

##  Memory Management

DoLang provides explicit memory control with two unique commands:

### `demolish` - Clear Value
Sets a variable's value to `vaco` (empty) but keeps the variable in memory.

```text
pin nde.x = 10
demolish: x
show(x)  # Outputs: vaco
```

### `collapse` - Delete Variable
Completely removes a variable from memory. Trying to use it afterward will cause an error.

```text
pin nde.y = 20
collapse: y
show(y)  # Error: The variable "y" does not exist.
```

---

##  GUI Development

DoLang's standout feature is its native GUI support. Create desktop applications without external libraries!

### Creating Windows

```text
window MyApp:
--title = "My First App"
--size = 400, 300
```

### Adding Widgets

**Labels** (Text display):
```text
label Welcome:
--text = "Hello, DLang!"
--position = 50, 50
--color = blue
```

**Buttons** (Interactive elements):
```text
button ClickMe:
--text = "Click Here"
--position = 50, 100
--command:
----show("Button clicked!")
----pin nde.x = 42
----<pybt>show("Value: {x}")
```

### Complete GUI Example

```text
window Calculator:
--title = "Simple Calculator"
--size = 350, 250

label Title:
--text = "Enter two numbers:"
--position = 50, 30
--color = blue

button Add:
--text = "Add"
--position = 50, 80
--command:
----pin nde.a = tck("First number: ")
----pin nde.b = tck("Second number: ")
----<pybt>show("Result: {a + b}")

button Multiply:
--text = "Multiply"
--position = 150, 80
--command:
----pin nde.a = tck("First number: ")
----pin nde.b = tck("Second number: ")
----<pybt>show("Result: {a * b}")
```

---

##  Smart Interpolation (`<pybt>`)

The `<pybt>` tag (Put You Back Together) enables f-string-like interpolation, allowing you to embed variables and expressions directly in strings.

```text
pin nde.x = 10
pin nde.y = 20
pin chr.name = "Douglas"

# Without <pybt> - prints literally
show("Sum: {x + y}")  # Outputs: Sum: {x + y}

# With <pybt> - evaluates expressions
<pybt>show("Sum: {x + y}")  # Outputs: Sum: 30
<pybt>show("Hello, {name}!")  # Outputs: Hello, Douglas!
<pybt>show("Double of {x} is {x * 2}")  # Outputs: Double of 10 is 20
```

---

##  Comments

Use `#` for comments. Comments require blank lines before and after them for clarity.

```text
pin nde.x = 10

# This is a comment explaining the next line

pin nde.y = 20

# Another comment
show(x + y)
```

---

##  Command Reference Table

| Command | Description | Example |
|---------|-------------|---------|
| `pin` | Declare variable | `pin nde.x = 10` |
| `show()` | Print to terminal | `show("Hello")` |
| `tck()` | Get user input | `tck("Name: ")` |
| `if` | Conditional | `if x > 5:` |
| `ifat` | Else-if alternative | `ifat x < 10:` |
| `else` | Default case | `else:` |
| `repeat` | Loop N times | `repeat: x(5)` |
| `repeat while` | Conditional loop | `repeat while x < 10:` |
| `fn` | Define function | `fn sum(a, b):` |
| `ret` | Return value | `ret a + b` |
| `>>` | Type transformer | `x >> dec` |
| `demolish` | Clear variable value | `demolish: x` |
| `collapse` | Delete variable | `collapse: x` |
| `window` | Create GUI window | `window MyApp:` |
| `label` | GUI text element | `label Title:` |
| `button` | GUI button | `button Click:` |
| `<pybt>` | String interpolation | `<pybt>show("{x}")` |
| `#` | Comment | `# This is a comment` |

---

##  Getting Started

### Installation
1. Install Python 3.8 or higher
2. Clone the repository: `git clone https://github.com/YOUR_USERNAME/DLang.git`
3. Run the GUI: `python GUI.py`

### Your First Program
```text
pin chr.name = tck("What is your name? ")
<pybt>show("Hello, {name}! Welcome to DLang!")
```

### Your First GUI App
```text
window HelloApp:
--title = "Hello DLang"
--size = 300, 200

label Greeting:
--text = "Welcome!"
--position = 50, 50
--color = blue

button ClickMe:
--text = "Click Here"
--position = 50, 100
--command:
----show("Button clicked!")
```

---

##  Roadmap

### ✅ Completed Features
- Core interpreter and type system
- Control flow (if, ifat, else, loops)
- Functions and return values
- GUI system (windows, labels, buttons)
- String interpolation (`<pybt>`)
- Memory management (`demolish`, `collapse`)
- Visual IDE with integrated terminal

###  Planned Features
- File I/O (read/write files)
- More widgets (Entry, Checkbox, Dropdown, Listbox)
- Error handling (try/catch)
- Standard library (math, dates, file operations)
- Module system (imports)
- Package manager
- Compilation to executable (.exe)
- Documentation website

---

##  Contributing

DoLang is in active development and contributions are welcome! Whether you want to add new features, fix bugs, improve documentation, or create examples, your help is appreciated.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

##  License

This project is open source and available under the MIT License. See the [LICENSE](LICENSE) file for details.

---

##  Acknowledgments

- Built with Python and Tkinter
- Inspired by the simplicity of scripting languages like Lua and Python
- Created as a learning project about interpreters, parsers, and language design
- Special thanks to the open-source community for inspiration and support

---

**Made with ❤️ by [Douglas]**

*If you enjoy DoLang, please give it a ⭐️ on GitHub and share it with others!*

