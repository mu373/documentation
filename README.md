# documentation

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

### Installation

```
$ yarn
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

### References
- [Docs only mode](https://docusaurus.io/docs/docs-introduction#docs-only-mode)
- [Using /docs directory for baseUrl](https://github.com/facebook/docusaurus/issues/6294)
