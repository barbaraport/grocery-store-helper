.PHONY: uv-setup uv-uninstall uv-init-project run test deps

uv-init-project:
	@uv python install 3.12
	@uv init . --name $(name) --python 3.12
	@uv sync

uv-setup:
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv self update

uv-uninstall:
	@uv cache clean
	@rm -rf "$(uv python dir)"
	@rm -rf "$(uv tool dir)"
	@rm -f ~/.local/bin/uv ~/.local/bin/uvx

deps:
	@uv sync

run:
	@uv run main.py