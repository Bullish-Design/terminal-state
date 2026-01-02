{
  description = "Terminal session recording and management library";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python312;
        in
        {
          default = python.pkgs.buildPythonPackage {
            pname = "terminal-state";
            version = "0.1.0";

            pyproject = true;
            src = ./.;

            # Build system
            build-system = with python.pkgs; [
              setuptools
              wheel
            ];

            # Runtime dependencies
            dependencies = with python.pkgs; [
              libtmux
              pydantic
              pillow  # Include export extras by default
            ];

            # System dependencies (for runtime)
            propagatedBuildInputs = [ pkgs.tmux ];

            # Optional: Include pyte for terminal emulation
            passthru.optional-dependencies = {
              pyte = [ python.pkgs.pyte ];
            };

            # Skip tests during build (they can be run separately)
            doCheck = false;

            meta = with pkgs.lib; {
              description = "Terminal session recording and state management";
              homepage = "https://github.com/Bullish-Design/terminal-state";
              license = licenses.mit;
              maintainers = [ ];
              platforms = platforms.unix;
            };
          };
        });

      # Development shell (keeps existing devenv.nix workflow)
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python312;
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              python
              tmux
              asciinema
              agg
              imagemagick
              ghostscript
            ] ++ (with python.pkgs; [
              # Python development tools
              pip
              setuptools
              wheel
              # Testing and linting
              pytest
              pytest-cov
              black
              mypy
              ruff
              # Runtime dependencies
              libtmux
              pydantic
              pillow
              pyte
            ]);

            shellHook = ''
              echo ""
              echo "╔════════════════════════════════════════════════════════════╗"
              echo "║         terminal-state Development Environment            ║"
              echo "╚════════════════════════════════════════════════════════════╝"
              echo ""
              echo "📦 Project: terminal-state"
              echo "🐍 Python: $(python --version)"
              echo "🖥️  tmux: $(tmux -V)"
              echo ""
              echo "Available commands:"
              echo "  pytest              - Run tests"
              echo "  black               - Format code"
              echo "  ruff                - Lint code"
              echo "  mypy                - Type check"
              echo ""
              echo "Note: Use 'devenv shell' for full devenv experience"
              echo ""
            '';
          };
        });

      # Expose formatter for nix fmt
      formatter = forAllSystems (system:
        nixpkgs.legacyPackages.${system}.nixpkgs-fmt
      );
    };
}
