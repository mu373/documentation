# documentation

Available at https://minamiueda.com/docs/. This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Usage

### Installation

```
$ yarn
```

### Converting notebooks
```sh
# Install requirements
pip install -r requirements.txt

# Convert notebooks to markdown
# Use following command if the specific Python interpreter (for example from conda) you want to use is not detected
# python3 python scripts/convert_all_notebooks.py .
yarn nb-convert

# Copy extracted images from notebook to static directory.
yarn run nb-copy-image

# Or run following. This runs nb-convert and nb-copy-image at once.
yarn run nb-build
```


### Local Development
```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build/docs` directory and can be served using any static contents hosting service. You can change the target directory in `package.json` by changing the build command `"docusaurus build --out-dir build/docs`.

## Writing documents

### Frontmatter
```yaml
---
title: Lorem Ipsum
hide_title: false # Optional: You can hide the title (h1).
slug: lorem-ipsum # Custom URL
tags:
  - notes
sidebar_position: 1
custom_edit_url: "" # Optional: Use this field to customize "edit" or "view source" link. Set empty value to hide.
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
