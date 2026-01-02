#!/usr/bin/env python3
"""
Asciinema Integration Demo

This example demonstrates how to use terminal-state with asciinema
for recording terminal sessions and converting them to GIFs.

Requirements:
- asciinema (for playback)
- agg (for GIF conversion)

These are automatically available in the devenv environment.
"""

from pathlib import Path
import time
from terminal_state import TerminalSession


def demo_basic_recording():
    """Basic recording example - exports to asciinema format."""
    print("=== Basic Asciinema Recording ===\n")

    with TerminalSession.create(width=100, height=30) as session:
        # Execute some commands
        session.send_command("echo 'Welcome to terminal-state!'")
        time.sleep(0.5)

        session.send_command("ls -la")
        time.sleep(1.0)

        session.send_command("echo 'Recording complete!'")
        time.sleep(0.5)

        # Export to asciinema format
        output_path = Path("demo_basic.cast")
        session.recording.to_asciinema(output_path)
        print(f"✓ Recorded to: {output_path}")
        print(f"  Play with: asciinema play {output_path}")
        print(f"  Or use: play-cast {output_path}\n")


def demo_gif_export():
    """Recording with GIF export."""
    print("=== Recording with GIF Export ===\n")

    with TerminalSession.create(width=100, height=30) as session:
        # Create a more visual demo
        session.send_command("echo '╔════════════════════════════════════╗'")
        time.sleep(0.3)
        session.send_command("echo '║  terminal-state GIF Demo          ║'")
        time.sleep(0.3)
        session.send_command("echo '╚════════════════════════════════════╝'")
        time.sleep(0.5)

        session.send_command('for i in {1..5}; do echo "Frame $i"; sleep 0.2; done')
        time.sleep(2.0)

        # Export to both formats
        cast_path = Path("demo_with_gif.cast")
        gif_path = Path("demo_with_gif.gif")

        session.recording.to_asciinema(cast_path)
        session.recording.to_gif(gif_path, fps=10)

        print(f"✓ Recorded to: {cast_path}")
        print(f"✓ GIF created: {gif_path}")
        print(f"  Play with: asciinema play {cast_path}")
        print(f"  Or convert manually: cast-to-gif {cast_path} output.gif\n")


def demo_interactive_session():
    """Recording an interactive session with multiple commands."""
    print("=== Interactive Session Recording ===\n")

    with TerminalSession.create(width=120, height=40) as session:
        # Simulate an interactive workflow
        commands = [
            ("git status", 0.5),
            ("git log --oneline -5", 1.0),
            ("python --version", 0.3),
            ("pip list | head -10", 0.8),
            ("echo 'Session complete!'", 0.5),
        ]

        for cmd, delay in commands:
            session.send_command(cmd)
            time.sleep(delay)

        # Export to asciinema
        output_path = Path("demo_interactive.cast")
        session.recording.to_asciinema(output_path)
        print(f"✓ Interactive session recorded: {output_path}\n")


def demo_with_metadata():
    """Recording with custom metadata."""
    print("=== Recording with Custom Metadata ===\n")

    # Create recording with title and environment info
    config_dict = {
        "width": 100,
        "height": 30,
        "shell": "/bin/bash",
    }

    with TerminalSession.create(**config_dict) as session:
        # Set recording title
        session.recording.title = "terminal-state Demo Recording"
        session.recording.environment = {
            "TERM": "xterm-256color",
            "SHELL": "/bin/bash",
        }

        session.send_command("echo 'Recording with metadata'")
        time.sleep(0.5)

        session.send_command("uname -a")
        time.sleep(0.5)

        # Export
        output_path = Path("demo_metadata.cast")
        session.recording.to_asciinema(output_path)
        print(f"✓ Recorded with metadata: {output_path}\n")


def print_break():
    """Print a visual break in the console."""
    print("\n\n" + "-" * 60 + "\n\n")


def main():
    """Run all demo examples."""
    print("\n" + "=" * 60)
    print("  terminal-state + asciinema Integration Demo")
    print("=" * 60 + "\n")

    # Create output directory for demos
    output_dir = Path("examples/asciinema_demos")
    output_dir.mkdir(exist_ok=True)

    # Change to output directory
    import os

    os.chdir(output_dir)
    print(f"Output directory: {output_dir.absolute()}\n")

    try:
        # Run demos
        demo_basic_recording()
        print_break()

        demo_gif_export()
        print_break()

        demo_interactive_session()
        print_break()

        demo_with_metadata()

        print("=" * 60)
        print("All demos completed successfully!")
        print("\nYou can now:")
        print("  1. Play recordings: asciinema play <file.cast>")
        print("  2. Convert to GIF: agg <file.cast> <output.gif>")
        print("  3. Or use devenv commands: play-cast / cast-to-gif")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"Error running demos: {e}")
        raise


if __name__ == "__main__":
    main()
