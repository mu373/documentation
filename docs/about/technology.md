---
sidebar_position: 2
title: Technology
slug: technology
---

## Overview
The website is developed using [Docusaurus](https://docusaurus.io/), an open-source static-site generator developed by [Meta](https://opensource.fb.com/projects/docusaurus/).

- Static-site generator: [Docusaurus](https://docusaurus.io/)
- Repository: [GitHub](https://github.com/mu373/documentation/)
- CI: [GitHub Actions](https://github.com/mu373/documentation/actions/workflows/deploy.yml)
    - Runs the Jupyter notebook conversion and builds the entire website
    - Automatically deploys to Vercel
- Hosting: [Vercel](https://vercel.com/)
    - Deploys to subdomain (e.g., `https://mysubdomain.minamiueda.com/docs/`)
- Reverse Proxy: [Cloudflare Workers](https://developers.cloudflare.com/workers/)
    - To serve the contents under the subdirectory of the domain root (at `https://minamiueda.com/docs/`), Cloudflare Workers is used to rewrite the request to the actual origin hosted at the subdomain.
    - It's just a matter of preference, but I wanted have them under subdirectory, not at subdomain, while maintaining other things managed as separate projects served from different servers.

All of the codes and documentation conents are published on [GitHub](https://github.com/mu373/documentation/).

## Jupyter notebook

### Build system
The customized build system **supports Jupyter notebook as an input** for documentation, in addition to the usual Markdown files. This allows the mixed usage of `ipynb` and `mdx` as the source of documentation.

Jupyter notebooks (`.ipynb`) are converted into Markdown files (`.mdx`) using a [custom script](https://github.com/mu373/documentation/blob/main/scripts/notebook_convert.py) in Python, which was originally forked from [LangChain documentation repository](https://github.com/langchain-ai/langchain/blob/master/docs/scripts/notebook_convert.py). We use [nbconvert](https://github.com/jupyter/nbconvert) to process the notebooks.

The [conversion script](https://github.com/mu373/documentation/blob/main/scripts/notebook_convert.py) `notebook_convert.py` supports:
- Splitting a Jupyter notebook into multiple Markdown files (which are then built as pages)
- Extracting embedded output images from the notebook
- Excluding cells with `{'hide': true}` from output

See [README.md](https://github.com/mu373/documentation/blob/main/README.md#converting-notebooks) for details on the notebook conversion.

### Example
Here are the example of the pages that were converted from a notebook.
- Source (notebook): [sir.ipynb](https://github.com/mu373/documentation/blob/dev/docs/epi/infectious-disease/sir.ipynb)
- Output
    - https://minamiueda.com/docs/epi/infectious-disease/sir/model
    - https://minamiueda.com/docs/epi/infectious-disease/sir/implementations