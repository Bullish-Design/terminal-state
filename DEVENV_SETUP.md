# NixOS Development Environment Setup

This project uses [devenv](https://devenv.sh/) for a reproducible NixOS development environment.

## Prerequisites

1. **Nix Package Manager** (with flakes enabled)
   ```bash
   # Install Nix (if not already installed)
   curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
   ```

2. **devenv**
   ```bash
   # Install devenv
   nix profile install --accept-flake-config github:cachix/devenv/latest
   ```

3. **direnv** (optional, but recommended)
   ```bash
   # Install direnv
   nix profile install nixpkgs#direnv

   # Add to your shell (bash)
   echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

   # Or for zsh
   echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
   ```

## Quick Start

### Option 1: Using direnv (Recommended)

```bash
# Navigate to the project directory
cd terminal-state

# Allow direnv to load the environment
direnv allow

# The environment will automatically activate!
```

### Option 2: Manual Activation

```bash
# Navigate to the project directory
cd terminal-state

# Enter the development shell
devenv shell
```

## What's Included

The devenv environment provides:

### Core Tools
- **Python 3.11** with uv package manager
- **tmux** - Terminal multiplexer (required by libtmux)
- **asciinema** - Terminal session recorder
- **agg** - Fast asciinema to GIF converter

### Development Tools
- **pytest** - Testing framework
- **black** - Code formatter
- **ruff** - Fast Python linter
- **mypy** - Static type checker
- **pre-commit hooks** - Automatic code quality checks

### Utilities
- **git** - Version control
- **imagemagick** - Image processing
- **System fonts** - DejaVu, Liberation, Source Code Pro

## Available Commands

Once in the devenv environment, you have access to these custom commands:

| Command | Description |
|---------|-------------|
| `record-terminal` | Record terminal session with asciinema |
| `cast-to-gif <in.cast> <out.gif>` | Convert asciinema to GIF |
| `play-cast <file.cast>` | Play asciinema recording |
| `test` | Run pytest tests |
| `format` | Format code with black |
| `lint` | Lint with ruff and mypy |
| `build-package` | Build the Python package |

## Getting Started

1. **Enter the environment:**
   ```bash
   devenv shell
   # or just `cd terminal-state` if using direnv
   ```

2. **Install Python dependencies:**
   ```bash
   uv sync --all-extras
   ```

3. **Run tests:**
   ```bash
   test
   ```

4. **Try the asciinema demo:**
   ```bash
   python examples/asciinema_demo.py
   ```

## Usage Examples

### Recording Terminal Sessions

```bash
# Start recording
record-terminal my-session.cast

# ... do your terminal work ...

# Stop recording (Ctrl+D or type 'exit')

# Play it back
play-cast my-session.cast

# Convert to GIF
cast-to-gif my-session.cast my-session.gif
```

### Using with Python

```python
from terminal_state import TerminalSession
from pathlib import Path

# Create a terminal session
with TerminalSession.create(width=100, height=30) as session:
    session.send_command("echo 'Hello from terminal-state!'")

    # Export to asciinema format
    session.recording.to_asciinema(Path("demo.cast"))

    # Or export directly to GIF
    session.recording.to_gif(Path("demo.gif"), fps=10)
```

### Development Workflow

```bash
# 1. Make your changes
vim src/terminal_state/...

# 2. Format code
format

# 3. Lint code
lint

# 4. Run tests
test

# 5. Commit (pre-commit hooks will run automatically)
git commit -m "Add new feature"
```

## Pre-commit Hooks

The environment includes automatic pre-commit hooks that run on every commit:

- **black** - Formats Python code
- **ruff** - Lints Python code
- **mypy** - Type checks Python code
- **nixpkgs-fmt** - Formats Nix files

These hooks are automatically installed when you enter the devenv shell.

## Customization

### Local Configuration

Create a `devenv.local.nix` file for local overrides (automatically gitignored):

```nix
{ pkgs, ... }:

{
  # Add your local customizations here
  packages = [ pkgs.neovim ];

  env.MY_LOCAL_VAR = "value";
}
```

### Python Package Management

The environment uses **uv** for fast Python package management:

```bash
# Install dependencies
uv sync

# Install with all extras
uv sync --all-extras

# Install dev dependencies
uv sync --extra dev

# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name
```

## Troubleshooting

### Environment Not Activating

```bash
# Make sure direnv is allowed
direnv allow

# Or manually enter the shell
devenv shell
```

### Python Packages Not Found

```bash
# Sync Python dependencies
uv sync --all-extras
```

### tmux Socket Errors

The environment creates a `.tmux/` directory for sockets. If you encounter issues:

```bash
# Clean tmux sockets
rm -rf .tmux/
mkdir -p .tmux/
```

### Cache Issues

```bash
# Clean devenv cache
rm -rf .devenv/

# Re-enter the environment
devenv shell
```

## CI/CD Integration

You can use the devenv environment in CI/CD:

```yaml
# Example GitHub Actions
- uses: cachix/install-nix-action@v24
  with:
    extra_nix_config: |
      accept-flake-config = true

- uses: cachix/cachix-action@v12
  with:
    name: devenv

- name: Install devenv.sh
  run: nix profile install --accept-flake-config github:cachix/devenv/latest

- name: Run tests
  run: |
    devenv shell test
```

## Additional Resources

- [devenv Documentation](https://devenv.sh/)
- [Nix Package Search](https://search.nixos.org/packages)
- [direnv Documentation](https://direnv.net/)
- [asciinema Documentation](https://asciinema.org/docs)
- [agg - asciinema GIF generator](https://github.com/asciinema/agg)

## Getting Help

If you encounter issues:

1. Check the [devenv troubleshooting guide](https://devenv.sh/guides/troubleshooting/)
2. Review the project's [GitHub Issues](https://github.com/Bullish-Design/terminal-state/issues)
3. Consult the [NixOS Discourse](https://discourse.nixos.org/)
