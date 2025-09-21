# documentation

Available at https://minamiueda.com/docs/. This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Usage

### Installation

This project uses [`bun`](https://bun.sh/docs/installation) as the runtime.

```sh
# Install bun first: https://bun.sh/docs/installation
$ bun install
```

### Converting notebooks

For converting Jupyter notebooks into Markdown, we use Python from [`uv`](https://docs.astral.sh/uv/).

```sh
# Install uv first: https://docs.astral.sh/uv/getting-started/installation/

# Install dependencies
$ uv sync
```

```sh
# Convert notebooks to markdown

# For single notebook
bun run nb-convert-single docs/stats/computational-statistics/rejection-sampling.ipynb

# For all notebooks
bun run nb-convert

# Copy extracted images from notebook to static directory.
bun run nb-copy-image

# Or run following. This runs nb-convert and nb-copy-image at once.
bun run nb-build
```


### Local Development
```sh
$ bun run start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```sh
$ bun run build
```

This command generates static content into the `build/docs` directory and can be served using any static contents hosting service. You can change the target directory in `package.json` by changing the build command `"docusaurus build --out-dir build/docs`.

## Writing documents

### Frontmatter
```yaml
---
title: 'Lorem Ipsum | Chapter 1' # Used in doc pages header and <title> tags
custom_title: Lorem Ipsum # Optional: Overrides `title` if set in doc pages
sidebar_label: Lorem # Optional: Label shown in sidebar and breadcrumbs
hide_title: false # Optional: You can hide the title (h1).
slug: lorem-ipsum # Custom URL
tags:
  - notes
sidebar_position: 1
custom_edit_url: "" # Optional: Use this field to customize "edit" or "view source" link. Set empty value to hide.
header: # Optional: Additional informations shown in the doc header. Accepts any key-value pair.
  - Class: Introduction to Computer Science
  - Year: 2025
---
```

### Jupyter Notebooks

At the beginning of the notebook, include raw cell with:
```yaml
# !chapter
---
chapter-title: My chapter title
---
```

Optional: If you want to split a single notebook in to multiple pages in the documentation website, include the raw cell in the following format at the beginning of each sections. `# !pagebreak` is required to split pages.
```yaml
# !pagebreak
---
title: Introduction
slug: intro
---
```

To hide cells, add add `hide` or `hide_input` field in the JSON metadata.
```json
  {
   "cell_type": "markdown",
   "metadata": {
    "hide_input": true
   },
   "source": [
    "My markdown text"
   ]
  },
```
```json
  {
   "cell_type": "code",
   "metadata": {
    "hide_input": true
   },
   "outputs": [],
   "source": [
    "1 + 1"
   ]
  },
```


## Testing

Run tests on notebook conversion. This test is automated on [GitHub Actions](https://github.com/mu373/documentation/actions/workflows/test-notebook-convert.yml).
```sh
pytest tests/test-notebook-convert.py -v
```

## License
This project uses multiple licenses (MIT and CC-BY) depending on the part of the repository. See [LICENSE.md](https://github.com/mu373/documentation/blob/main/LICENSE.md) for details.

## References
- [Docs only mode](https://docusaurus.io/docs/docs-introduction#docs-only-mode)
- [Using /docs directory for baseUrl](https://github.com/facebook/docusaurus/issues/6294)
