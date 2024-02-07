project_dir := .
notebooks_dir := notebooks
scripts_dir := scripts

# Convert Jupyter notebooks to Python scripts
.PHONY: notebooks_to_py
notebooks_to_py:
	@jupyter nbconvert --to script $(notebooks_dir)/*.ipynb --output-dir=$(scripts_dir)

# Lint code and converted notebooks
.PHONY: lint
lint: notebooks_to_py
	@black --check --diff $(project_dir) $(scripts_dir)
	@ruff $(project_dir) $(scripts_dir)
	@mypy $(project_dir) --strict

# Reformat code and converted notebooks
.PHONY: reformat
reformat: notebooks_to_py
	@black $(project_dir) $(scripts_dir)
	@ruff $(project_dir) --fix
