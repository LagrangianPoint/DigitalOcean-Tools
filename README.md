# DigitalOcean Tools
Tools for setting up and configuring your new DigitalOcean VPS
The goal of this project is for helping you get your clean server up and running, with the least amount of effort. 

*Notice* This only works on Debian for now. Redhat support will be added only if requested.

## Install Instructions: 
- Run the following script:
```
wget https://raw.githubusercontent.com/LagrangianPoint/DigitalOcean-Tools/master/setup.sh 
```
- Give the previous script execution permissions with:
```
chmod +x setup.sh 
```
- Execute the file to install the minimal amount of packages needed to get this working
```
./setup.sh 
```


## Ideas:
- Create code for finding all wordpress installations in a given path, and finding out the wordpress version for each directory
- Create code for finding out what the latest Wordpress version is
- Create code that tells you which Wordpress installation needs upgrade 
- Create code for automatically upgrading wordpress
- BAN IPs automatically via IP tables.

