# documentation

Available at https://minamiueda.com/docs/. This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Usage

### Installation

```
$ yarn
```

### Converting notebooks
```sh
conda activate nbdoc
python3 scripts/notebook_split_convert.py docs/network-science/notebook.ipynb .
```
This command converts Jupyter notebook into mdx files. It would be splitted into multiple files.

At the beginning of the chapter, include raw cell with:
```txt
# !chapter
---
chapter-title: SIR model with PGF
---
```

At the beginning of sections, include raw cell with:
```txt
# !pagebreak
---
title: Introduction
slug: intro
---
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

### Deployment

Using SSH:

```
$ USE_SSH=true yarn deploy
```

Not using SSH:

```
$ GIT_USER=<Your GitHub username> yarn deploy
```

Using Vercel:

Connect the GitHub repository to Vercel. Once build succeeds, the website will be available at `https://your-vercel-project-name.vercel/docs/`.


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

### References
- [Docs only mode](https://docusaurus.io/docs/docs-introduction#docs-only-mode)
- [Using /docs directory for baseUrl](https://github.com/facebook/docusaurus/issues/6294)
