# Drawn

**Drawn** is a lightweight CLI tool for **diagrams-as-code** – helping architects and engineers design, version, and share system diagrams using simple text syntax.

## Philosophy

- **Simple over complex** - Minimal syntax that anyone can learn
- **Fast feedback** - From idea to diagram in 30 seconds
- **Git-friendly** - Text-based diagrams that version well
- **Local-first** - No internet required, no complex setup

## Quick Start

### Installation
```bash
# Clone the repo
git clone git@github.com:parthivrmenon/drawn.git
cd drawn

# Install dependencies
pip install graphviz

# Create your first diagram
echo "API --> Server --> DB" > flow.drawn
python main.py flow.drawn
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run tests with verbose output
python -m pytest tests/ -v

# Test the parser
python -c "from drawn.parser import parse; print(parse(['A --> B --> C']))"

# Test rendering
echo "API --> Server --> DB" > test.drawn
python main.py test.drawn
# Check that drawn_flow.svg was created
```

## Project Structure

```
drawn/
├── drawn/
│   ├── parser.py     # Parse .drawn syntax
│   └── render.py     # Generate diagrams with Graphviz
├── tests/
│   └── test_all.py   # Test coverage
├── main.py           # CLI entry point
└── README.md
```

## Features

- **Simple arrow syntax** - `A --> B --> C`
- **Multi-line support** - Handle complex flows
- **Branching flows** - One node to multiple destinations  
- **Professional output** - High-quality SVG/PNG via Graphviz
- **Fast rendering** - Instant feedback
- **Test coverage** - Reliable and maintainable

## Why Drawn?

**vs Mermaid:**
- Simpler syntax (no `graph TD` boilerplate)
- Local CLI tool (no browser required)
- Faster iteration cycle
- Better error messages

**vs Complex tools:**
- No learning curve
- No subscription fees
- Works offline
- Git-friendly text format

## Roadmap

- [ ] Live preview (`drawn watch`)
- [ ] More diagram types (sequence, architecture)
- [ ] Custom styling options
- [ ] Package distribution (pip install)

---

*Built with Python and Graphviz for maximum simplicity and quality.*