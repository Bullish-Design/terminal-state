# terminal-state Examples

This directory contains example scripts demonstrating various features of terminal-state.

## Available Examples

### asciinema_demo.py

Demonstrates integration with asciinema for terminal recording and GIF creation.

**Features:**
- Basic asciinema recording
- GIF export from recordings
- Interactive session recording
- Custom metadata in recordings

**Usage:**

```bash
# Make sure you're in the devenv environment
cd examples
python asciinema_demo.py
```

The script will create an `asciinema_demos/` directory with various `.cast` and `.gif` files.

## Using with devenv

If you're using the NixOS devenv setup:

```bash
# Enter the development environment
devenv shell

# Run the demo
python examples/asciinema_demo.py

# Use the built-in scripts
cd examples/asciinema_demos
play-cast demo_basic.cast
cast-to-gif demo_basic.cast demo_basic_converted.gif
```

## Creating Your Own Recordings

### Basic Recording

```python
from terminal_state import TerminalSession
from pathlib import Path

with TerminalSession.create() as session:
    session.send_command("echo 'Hello World'")
    session.recording.to_asciinema(Path("output.cast"))
```

### Recording to GIF

```python
from terminal_state import TerminalSession
from pathlib import Path

with TerminalSession.create(width=100, height=30) as session:
    session.send_command("htop")
    session.recording.to_gif(Path("htop.gif"), fps=10)
```

### Using External Tools

You can also record with asciinema directly and play back:

```bash
# Record manually
asciinema rec my_session.cast

# Play it back
asciinema play my_session.cast

# Convert to GIF
agg my_session.cast my_session.gif
```

## Tips

1. **FPS Settings**: Lower FPS (5-10) creates smaller GIFs
2. **Terminal Size**: Smaller terminals (80x24) are better for documentation
3. **Timing**: Add `time.sleep()` between commands for better pacing
4. **Colors**: Use ANSI colors for visual appeal in recordings

## Resources

- [asciinema Documentation](https://asciinema.org/docs)
- [agg - asciinema to GIF](https://github.com/asciinema/agg)
- [terminal-state README](../README.md)
