# Windows setup
> Start with the tools listed on your lab page. You can do each practical independently.

## Choose a workspace
Extract the main download and open index.html in your browser for offline instructions. Extract a lab's starter ZIP into its own directory, then open the shell named in the guide and change into the extracted lab folder before running the commands. Keep files for Linux tools under your WSL home directory. Labs 3 and 4 use explicit Windows paths so the Jenkins service can find the files.

## Set up Ubuntu on WSL2
Open PowerShell as Administrator if you need to install WSL. Restart if prompted and complete the Ubuntu username and password setup on first launch.
~~~PowerShell
wsl --install -d Ubuntu
~~~
From a normal PowerShell window, check that Ubuntu shows version 2.
~~~PowerShell
wsl --list --verbose
~~~
For the Ansible lab, use a dedicated Ubuntu WSL distro with systemd running. Check from Ubuntu with the command below. If PID 1 is neither systemd nor a systemd executable path, follow Microsoft's systemd setup link.
~~~WSL Bash
ps -p 1 -o comm=
~~~
- [Microsoft WSL setup](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)
- [Enable systemd in WSL](https://learn.microsoft.com/en-us/windows/wsl/systemd)

## Set up Docker Desktop
Install and start Docker Desktop with Linux containers and the WSL2 engine. Enable Ubuntu integration in Settings → Resources → WSL Integration for Lab 8. Run these checks from the shell you will use for the lab and look for a server version as well as a client version.
~~~PowerShell or WSL Bash
docker version
docker compose version
~~~
- [Docker Desktop with WSL2](https://docs.docker.com/desktop/features/wsl/)

## Prepare for a live demo
- Check account access, package downloads, and lab tools before the demonstration. Packages, image pulls, and hosted services may still need internet access when reading the instructions offline.
- Close services you used for earlier labs or check for port conflicts. The guides use Jenkins 8080, Docker demos 8081 and 8082, SonarQube 9000, and monitoring 9090, 9093, and 9100.
- Replace values marked YOUR_ or REPLACE_ before running a command. Keep tokens, login screens, private keys, and cloud account details out of the demo.
- Open the lab's Show the professor section for the result to reproduce live. Use the cleanup section when the demo is over.
