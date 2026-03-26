# Urbano Documentation

Urbano Component Documentation source repository.

| Environment  | URL                        | Status |
|--------------|----------------------------|--------|
| Development  | https://dev.docs.urbano.io | [![Netlify Status](https://api.netlify.com/api/v1/badges/bcd58e56-769e-498b-a69b-d1928d214479/deploy-status)](https://app.netlify.com/projects/dev-docs-urbano/deploys) |
| Production   | https://docs.urbano.io     | [![ci](https://github.com/Urbano-io/Urbano-Documentation/actions/workflows/deploy.yml/badge.svg)](https://github.com/Urbano-io/Urbano-Documentation/actions/workflows/deploy.yml) |

## Local Development

You can run the documentation site locally using Docker:

```bash
./serve-docker.sh
```
Or directly:
```bash
docker run --rm -it -p 8080:8000 -v $(pwd):/docs custom-mkdocs-material
```

## Versioning

Urbano 2 documentation uses `mike` for versioning. The version selector dropdown **will not appear** during a standard local `mkdocs serve` or when running the Docker container locally using the default command. It is only injected when the site is deployed.

To deploy a new version to the `gh-pages` branch (which automatically builds the version dropdown), use the `mike` CLI. 

For example, to deploy version `2.1.0` and tag it as `latest`:
```bash
mike deploy 2.1.0 latest --update-aliases
```

To preview the versioned site locally (including the dropdown):
```bash
mike serve
```
*(Note: `mike` commands need to be run inside an environment where the mkdocs dependencies are installed.)*
