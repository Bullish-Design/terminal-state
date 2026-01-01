# terminal-state

A high-level, Pydantic-based Python library for terminal automation focused on state capture and export.

## Features

- 🎯 **Type-safe** - Full Pydantic models for validation and type safety
- 🖥️ **Terminal automation** - Control terminals with tmux backend
- 📸 **State capture** - Record terminal output as structured data
- 🎬 **Multiple export formats** - Screenshots (PNG), GIF animations, and asciinema recordings
- 🔄 **Simple API** - Clean, intuitive interface for common tasks

## Installation

```bash
pip install terminal-state
```

### Requirements

- Python >= 3.11
- tmux (for terminal session management)
- System fonts (for GIF/PNG export)

### Optional Dependencies

```bash
# Install with all optional features
pip install terminal-state[all]

# Install with pyte for advanced text extraction
pip install terminal-state[pyte]

# Install development dependencies
pip install terminal-state[dev]
```

### NixOS / devenv Setup

For NixOS users, this project includes a complete development environment configuration:

```bash
# Install devenv (one-time setup)
nix profile install --accept-flake-config github:cachix/devenv/latest

# Enter the development environment
devenv shell

# Or use direnv for automatic activation
direnv allow
```

The devenv environment includes:
- Python 3.11 with all dependencies
- asciinema for terminal recording
- agg for fast GIF conversion
- Development tools (pytest, black, ruff, mypy)
- Pre-commit hooks

See [DEVENV_SETUP.md](DEVENV_SETUP.md) for detailed setup instructions.

## Quick Start

### Basic Recording

```python
from terminal_state import TerminalSession

# Create a terminal session
with TerminalSession.create(width=120, height=40) as session:
    # Execute commands
    session.send_command("echo 'Hello World'")
    session.send_command("ls -la")

    # Export to different formats
    session.recording.to_asciinema("demo.cast")
    session.recording.to_gif("demo.gif", fps=10)
```

### Testing Workflow

```python
from terminal_state import TerminalSession, Keys

session = TerminalSession.create()

# Test nvim workflow
session.send_command("nvim test.py")
session.send_keys("i")  # Insert mode
session.send_keys("print('hello')")
session.send_keys(Keys.ESCAPE)
session.send_keys(":wq")
session.send_keys(Keys.ENTER)

# Verify expected output
if not session.expect_text("written", timeout=2):
    session.recording.to_gif("nvim-failure.gif")
    raise AssertionError("Failed to save file")

session.destroy()
```

### Screenshot Generation

```python
from terminal_state import TerminalSession
import time

session = TerminalSession.create()
session.send_command("htop")
time.sleep(2)

# Capture screenshot of current state
frame = session.capture()
session.recording.to_screenshot("htop-screenshot.png", frame_index=0)

session.destroy()
```

## API Reference

### TerminalSession

High-level interface for terminal automation.

```python
from terminal_state import TerminalSession

# Create with custom configuration
session = TerminalSession.create(
    width=120,
    height=40,
    shell="/bin/bash"
)

# Send commands
session.send_command("echo 'hello'")

# Send key sequences
session.send_keys("some text")
session.send_keys(Keys.ESCAPE)

# Capture current state
frame = session.capture()

# Wait for text to appear
if session.expect_text("pattern", timeout=5.0):
    print("Found!")

# Context manager support
with TerminalSession.create() as session:
    session.send_command("ls")
```

### Frame

Immutable snapshot of terminal state.

```python
from terminal_state import Frame

frame = session.capture()
print(frame.content)      # Raw terminal output
print(frame.width)        # Terminal width
print(frame.height)       # Terminal height
print(frame.timestamp)    # Unix timestamp
```

### Recording

Collection of frames with timing information.

```python
from terminal_state import Recording

recording = session.recording

# Add frames manually
recording.add_frame(session.capture())

# Export to different formats
recording.to_asciinema("output.cast")
recording.to_gif("output.gif", fps=10)
recording.to_screenshot("screenshot.png", frame_index=-1)

# Access properties
print(recording.duration)  # Total duration in seconds
print(len(recording.frames))  # Number of frames
```

### KeySequence

Type-safe key input with tmux notation.

```python
from terminal_state import KeySequence, Keys

# Literal text
seq = KeySequence(keys="Hello World", literal=True)

# Special keys (tmux notation)
seq = KeySequence(keys="Escape")
seq = KeySequence(keys="Enter")

# Control sequences
seq = KeySequence(keys="C-c")  # Ctrl+C

# Predefined keys
Keys.ESCAPE
Keys.ENTER
Keys.TAB
Keys.CTRL_C
Keys.CTRL_D
Keys.UP
Keys.DOWN
Keys.LEFT
Keys.RIGHT
```

### SessionConfig

Configuration for terminal sessions.

```python
from terminal_state import SessionConfig
from pathlib import Path

config = SessionConfig(
    width=120,
    height=40,
    shell="/bin/bash",
    environment={"TERM": "xterm-256color"},
    socket_dir=Path("/tmp/terminal-state")
)

session = TerminalSession(config)
```

### Export Formats

#### Asciinema

```python
from terminal_state.export import AsciinemaExporter

exporter = AsciinemaExporter()
exporter.export(recording, Path("output.cast"))
```

#### GIF

```python
from terminal_state.export import GifExporter, GifConfig

config = GifConfig(
    fps=10,
    font_size=14,
    bg_color=(0, 0, 0),
    fg_color=(200, 200, 200)
)

exporter = GifExporter(config)
exporter.export(recording, Path("output.gif"))
```

#### Screenshot

```python
from terminal_state.export import ScreenshotExporter

exporter = ScreenshotExporter()
exporter.export_frame(frame, Path("screenshot.png"))
```

## Architecture

```
terminal-state/
├── src/terminal_state/
│   ├── session/           # Session management
│   │   ├── terminal.py    # TerminalSession
│   │   └── backend.py     # TmuxBackend
│   ├── capture/           # Frame capture
│   │   ├── frame.py       # Frame model
│   │   └── recorder.py    # Recording
│   ├── input/             # Input handling
│   │   └── keys.py        # KeySequence
│   ├── export/            # Output formats
│   │   ├── asciinema.py   # Asciinema export
│   │   ├── gif.py         # GIF generation
│   │   └── screenshot.py  # PNG screenshots
│   └── models/            # Shared models
│       └── config.py      # Configuration
```

## Design Principles

1. **Pydantic-First** - All data structures use Pydantic for validation and type safety
2. **Layered Architecture** - Clear separation between high-level API and backend implementations
3. **Multiple Export Targets** - Support for asciinema, GIF, PNG, and JSON formats
4. **Optional Advanced Features** - Core functionality is simple, advanced features are optional

## Use Cases

### Automated Testing

```python
with TerminalSession.create() as session:
    session.send_command("pytest tests/")

    if not session.expect_text("passed", timeout=30):
        session.recording.to_gif("test-failure.gif")
        raise AssertionError("Tests failed")
```

### Documentation Generation

```python
recording = Recording()
session = TerminalSession.create()

session.send_command("git status")
recording.add_frame(session.capture())

session.send_command("git commit -m 'update'")
recording.add_frame(session.capture())

recording.to_gif("git-workflow.gif")
```

### CI/CD Integration

```python
import os
from terminal_state import TerminalSession

# Run in CI environment
if os.getenv("CI"):
    session = TerminalSession.create()
    session.send_command("npm test")
    session.send_command("npm run build")

    # Save artifacts
    session.recording.to_asciinema("ci-run.cast")
    session.recording.to_gif("ci-run.gif")
    session.destroy()
```

## Comparison to Alternatives

| Feature | terminal-state | asciinema | expect | pyte |
|---------|---------------|-----------|--------|------|
| Type safety | ✓ Pydantic | ✗ | ✗ | ✗ |
| Recording | ✓ Built-in | ✓ Native | ✗ | ✗ |
| Screenshots | ✓ | ✗ | ✗ | ✗ |
| GIF export | ✓ | Via agg | ✗ | ✗ |
| Session mgmt | ✓ tmux | ✗ | ✗ | ✗ |
| Input injection | ✓ Type-safe | ✗ | ✓ Basic | ✗ |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Parallel session support
- [ ] Full VT100 parsing with pyte integration
- [ ] True-color support in exports
- [ ] Web player integration
- [ ] Visual regression testing
- [ ] Alternative PTY backend
- [ ] Recording compression
- [ ] Real-time streaming export

## Credits

Built with:
- [Pydantic](https://pydantic.dev/) - Data validation
- [libtmux](https://libtmux.git-pull.com/) - Tmux session management
- [Pillow](https://python-pillow.org/) - Image processing
- [asciinema](https://asciinema.org/) - Recording format
