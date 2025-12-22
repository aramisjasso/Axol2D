# Axol2D Compiler 🎮

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Compilers](https://img.shields.io/badge/CS-Compiler%20Design-orange)
![Assembly](https://img.shields.io/badge/Target-MASM%20Assembly-red)
![License](https://img.shields.io/badge/License-MIT-green)

**Axol2D** is a custom Domain-Specific Language (DSL) and compiler designed to simplify the creation of 2D platformer games. It abstracts complex game loop logic and rendering primitives into a high-level, C-like syntax, which is then compiled down to native machine code via MASM (Microsoft Macro Assembler).

## 🚀 Key Features

- **Custom Syntax:** A strictly typed language designed specifically for game logic (Integers, Booleans, Strings, and Game Objects).
- **Game Primitives:** Native data types for `Player`, `Background`, `Platform`, and `Obstacles`.
- **Full Compilation Pipeline:**
    1. **Lexical Analysis:** Tokenization using Regex (via PLY).
    2. **Syntactic Analysis:** LALR(1) parsing to build the derivation tree.
    3. **Semantic Analysis:** Type checking, scope validation, and memory offset calculation.
    4. **Code Generation:** Translates high-level code into low-level **Assembly (x86)**.
    5. **Linking:** Uses `GoLink` to generate the final standalone `.exe`.

## 🛠️ Tech Stack

- **Language Host:** Python 3.
- **Parsing Tools:** [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/).
- **Target Language:** Assembly x86 (MASM).
- **Linker:** GoLink.

## 📝 Syntax Example

Axol2D uses a clean syntax to define levels and game behavior. Here is a snippet of how a level is defined:

```java
import Background;
import Players;

level MyFirstLevel {
    // Variable Declaration
    int score = 0;
    boolean isActive = true;

    // Game Assets Definition
    // [width, height, x, y, r, g, b]
    platform floor = [100, 10, 50, 0, 255, 255, 255];

    // Player Setup
    // [x, y, lives, type]
    player p1 = [0, 0, 3, Players.Mario];

    // Custom Logic Methods
    method int calculateBonus(int coins) {
        if (coins > 50) {
            return coins * 2;
        }
        return coins;
    }

    // Main Game Entry Point
    axol2D play() {
        // Init level with assets
        MyFirstLevel.start(p1, floor, score);
    }
}
```

## ⚙️ Architecture

The compiler follows a standard multi-pass architecture:

1. **Lexer (`lexico.py`):** Scans the source code and converts characters into a stream of tokens (KEYWORDS, ID, NUMBERS, OPERATORS).
2. **Parser (`sintactico.py`):** strict grammar rules defined to validate the structure (e.g., `program -> imports level`). It handles operator precedence and structural errors.
3. **Semantic & Intermediate Code:** Validates that operations are type-safe (e.g., you can't multiply a `Player` by a `String`) and prepares memory allocation.
4. **ASM Generation:** The final pass writes the `.asm` file referencing kernel32 libraries for window creation and rendering.

## 💿 Installation & Usage

### Prerequisites

- Python 3.x
- PIP (`pip install ply`)

### Running the Compiler

To compile a `.axol` file:

Bash

`python main.py`

*(Ensure your `.axol` source file path is configured in the main script)*

The output will be an executable file generated in the `bin/` directory.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

*Developed by [Aramis Jasso](https://github.com/aramisjasso) & [Miguel Lopez](https://github.com/miguellopezramirez) as a final project for Compiler Design.*
