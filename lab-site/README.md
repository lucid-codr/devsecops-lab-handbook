# DevSecOps lab handbook

Open dist/index.html directly in a browser. The offline handbook ZIP is in dist/downloads. Extract the entire archive before opening index.html; the relative paths are needed for styles, other pages, and downloads.

To preview using HTTP, run this from the lab-site directory, then open http://127.0.0.1:8765/:

    python -m http.server 8765 --bind 127.0.0.1 --directory dist

To refresh the generated pages and downloads after editing, run:

    python build.py

Use Python 3.9 or newer. Guide content lives in guides/, starter files in starters/, and browser assets in web/. Guides use a small Markdown subset: a title, a prerequisite line prefixed with >, section headings, paragraphs, links, unordered lists, fenced code using tildes, and @file directives for starter files. Starter file content shown on pages comes from the same source as the downloads.

The build only assembles the handbook. Participants run each practical manually using the shell and tools listed on the guide.

## Deploy to Coolify

Push the `lab-site` source to a Git branch that Coolify can read. If you use the existing lab repository, stage only `lab-site` and check the staged files before committing. Coolify rebuilds the HTML and ZIPs from source, so the deployment can omit the generated `dist/` directory.

In your Coolify project, add an application from that Git repository and select the branch you pushed. Use these settings:

| Coolify field | Value |
| --- | --- |
| Build Pack | Dockerfile |
| Base Directory | `/lab-site` |
| Dockerfile Location | `/Dockerfile` |
| Ports Exposes | `80` |
| Domain | Your HTTPS hostname, for example `https://labs.example.com` |

Use `/` as the base directory if you put the contents of `lab-site` at the root of a dedicated repository. Point the hostname at your Coolify server and let Coolify handle HTTPS. The image serves the generated files with Nginx on port 80. The app needs no environment variables, host port mapping, or volumes. The image checks `/index.html` for health. If you configure the check in Coolify, use HTTP, port `80`, path `/index.html`, and expected status `200`. [Coolify Dockerfile deployments](https://coolify.io/docs/applications/builds/dockerfile) · [Coolify health checks](https://coolify.io/docs/applications/configuration/health-checks)

Select **Deploy**, then open the domain and test a guide and the offline handbook download. For the one-day window, use **Stop** on the application when the window ends and check that the homepage and `/downloads/devsecops-lab-handbook.zip` are both unavailable.

### Preview the container locally

Run these commands from `lab-site` with Docker running:

```sh
docker build -t devsecops-handbook .
docker run --rm -p 127.0.0.1:8765:80 devsecops-handbook
```

Open `http://127.0.0.1:8765/`. Press Ctrl+C in the Docker terminal to stop the preview.
