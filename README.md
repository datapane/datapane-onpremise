<p align="center">
  <a href="https://datapane.com">
    <img src="https://datapane.com/static/datapane-logo-dark.png" width="250px" alt="Datapane" />
  </a>
</p>

# Deploying Datapane on-premise

Deploying Datapane on-premise ensures that all access to internal data is managed within your own cloud environment. You also have the flexibility to control how Datapane is setup within your infrastructure, configure logging, and enable custom features such as SAML SSO (under development).

We also provide a fully-managed hosted version of Datapane - this is always up-to-date and managed by the Datapane Team - see our [pricing page](https://datapane.com/pricing/).
Furthermore we offer _Datapane Enterprise_, where our skilled devops team will work with yourself to customise and install Datapane on your own infrastructure, again, please see our [pricing page](https://datapane.com/pricing/) 

# Table of contents
- [Select a Datapane version number](#select-a-datapane-version-number)
- [Simple deployments](#simple-deployments)
    - [EC2 and Docker](#deploying-on-ec2)
    - [Heroku](#deploying-on-heroku)
    - [Aptible](#running-datapane-using-aptible)
    - [Render](#deploying-to-render)
- [Managed deployments](#managed-deployments)
- [Additional features](#additional-features)
    - [Health check endpoint](#health-check-endpoint)
    - [Environment variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Updating Datapane](#updating-datapane)
- [Releases](#releases)
- [Docker cheatsheet](#docker-cheatsheet)

## Select a Datapane version number
We recommend you set your Datapane deployment to a specific version of Datapane (that is, a specific semver version number in the format `X.Y.Z`, instead of a tag name). This will help prevent unexpected behavior in your Datapane instances. When you are ready to upgrade Datapane, you can bump the version number to the specific new version you want.

To help you select a version, see our [changelog](https://docs.datapane.com/resources/changelog). If you're not sure which version to install, the latest stable release can be found in the pip badge shown below.

<a href="https://pypi.org/project/datapane/">
    <img src="https://img.shields.io/pypi/v/datapane?color=blue" alt="Latest release" />
</a>


## Simple Deployments

Get set up in 15 minutes by deploying Datapane on a single machine. 

### Docker compose

1. Obtain access to a Linux-based machine capable of running datapane
   1. This can be a cloud VM, a bare-metal VM, your local Linux installation, or even an instance of Docker Desktop for Windows / Mac
1. Install Docker and Docker Compose
1. Run the command `git clone https://github.com/datapane/datapane-onpremise.git`.
1. Run the command `cd datapane-onpremise` to enter the cloned repository's directory.
1. Edit the `Dockerfile` to set the version of Datapane you want to install. To do this, replace `X.Y.Z` in `FROM datapane/dp-server:X.Y.Z` with your desired version. See [Select a Datapane version number](#select-a-datapane-version-number) to help you choose a version.
1. Run `dp-setup.py check` to check the installation is valid and all dependencies exist
1. Run `dp-setup.py setup` to launch the setup wizard that will generate your `docker.env` file
1. In your `docker.env` (this file is only created after running `dp-setup.py setup`) add the following:
    ```
    # License key granted to you by Datapane
    LICENSE_KEY=YOUR_LICENSE_KEY 
    ```
1. Run `docker-compose up -d` to start the Datapane server.
1. Run `docker-compose ps` to make sure all the containers are up and running.



### Deploying on EC2
Spin up a new EC2 instance. If using AWS, use the following steps:
1. Click **Launch Instance** from the EC2 dashboard.
1. Click **Select** for an instance of Ubuntu `16.04` or higher.
1. Select an instance type of at least `t3.medium` and click **Next**.
1. Ensure you select the VPC that also includes the databases / API’s you will want to connect to and click **Next**.
1. Increase the storage size to `60` GB or higher and click **Next**. 
1. Optionally add some Tags (e.g. `app = datapane`) and click **Next**. This makes it easier to find if you have a lot of instances.
1. Set the network security groups for ports `80`, `443`, `22` and `8090`, with sources set to `0.0.0.0/0` and `::/0`, and click **Review and Launch**. We need to open ports `80` (http) and `443` (https) so you can connect to the server from a browser, as well as port `22` (ssh) so that you can ssh into the instance to configure it and run Datapane. By default on a vanilla EC2, Datapane will run on port `8090`.
1. On the **Review Instance Launch** screen, click **Launch** to start your instance.
1. If you're connecting to internal databases, whitelist the VPS's IP address in your database.
1. From your command line tool, SSH into your EC2 instance.
1. Run the command `git clone https://github.com/datapane/datapane-onpremise.git`.
1. Run the command `cd datapane-onpremise` to enter the cloned repository's directory.
1. Edit the `Dockerfile` to set the version of Datapane you want to install. To do this, replace `X.Y.Z` in `FROM datapane/dp-server:X.Y.Z` with your desired version. See [Select a Datapane version number](#select-a-datapane-version-number) to help you choose a version.
1. Install Docker and Docker Compose and run `dp-setup.py check` to check the installation is valid.
1. Run `dp-setup.py setup` to launch the setup wizard that will generate your `docker.env` file
1. In your `docker.env` (this file is only created after running `dp-setup.py setup`) add the following:
    ```
    # License key granted to you by Datapane
    LICENSE_KEY=YOUR_LICENSE_KEY 
    ```
1. Run `sudo docker-compose up -d` to start the Datapane server.
1. Run `sudo docker-compose ps` to make sure all the containers are up and running.
1. Navigate to your server's IP address in a web browser. Datapane should now be running on port `3000`.
1. Click Sign Up, since we're starting from a clean slate. The first user to into an instance becomes the administrator. 

### Deploying on Heroku

🚧 **Coming Soon**

### Running Datapane using Aptible

🚧 **Coming Soon**

### Deploying to Render

🚧 **Coming Soon**

## Managed deployments

🚧 **Coming Soon**

Deploy Datapane on a managed service. We're working on providing some starter template files for Cloudformation setups (ECS + Fargate), Kubernetes, and Helm.

Additionally, we hope to be available in the AWS, Azure, and GCS marketplaces shortly.

## Additional features

**For details on additional features like SAML SSO, custom certs, and more, visit our [deployment docs](https://docs.datapane.com/deployment).**

### Environment Variables

You can set environment variables to enable custom functionality like storage backends, customizing logs, and much more. For a list of all environment variables visit our [docs](https://docs.datapane.com/deployment/environment-variables).

### Health check endpoint 

<!-- TODO: Add other watchman endpoint -->

Datapane also has a health check endpoint that you can set up to monitor liveliness of Datapane. You can configure your probe to make a `GET` request to `/site/watchman/ping/`.

## Troubleshooting

- ...

## Updating Datapane

The latest Datapane releases can be pulled from Docker Hub. When you run an on-premise instance of Datapane, you’ll need to pull an updated image in order to get new features and fixes. 

See more information on our different versions and recommended update strategies in [our documentation](https://docs.datapane.com/deployment).

### Docker Compose deployments
Update the version number in the first line of your `Dockerfile`.

```
FROM datapane/dp-server:X.Y.Z
```
Then run the included update command `dp-setup.py update` from this directory.

### Kubernetes deployments
To update Datapane on Kubernetes, you can use the following command, replacing `X.Y.Z` with the version number or named tag that you’d like to update to.

```
kubectl set image deploy/api api=datapane/dp-server:X.Y.Z
```

## Releases

Release notes can be found at https://docs.datapane.com/resources/changelog.

## Docker cheatsheet

Below is a cheatsheet for useful Docker commands. Note that you may need to prefix them with `sudo`. 

| Command                     | Description                                                                                                                     | 
| ----------------------------|-------------------------------------------------------------------------------------------------------------------------------| 
| `docker-compose up -d`      | Builds, (re)creates, starts, and attaches to containers for a service. `-d`allows containers to run in background (detached). | 
| `docker-compose down`       | Stops and remove containers and networks                                                                                      |
| `docker-compose stop`       | Stops containers, but does not remove them and their networks                                                                 |
| `docker ps -a`              | Display all Docker containers                                                                                                 |
| `docker-compose ps -a`      | Display all containers related to images declared in the `docker-compose` file. 
| `docker logs -f <container_name>` | Stream container logs to stdout                                                                                     |
| `docker exec -it <container_name> psql -U <postgres_user> -W <postgres_password> <postgres_db>` | Runs `psql` inside a container                            |
| `docker kill $(docker ps -q)` | Kills all running containers                                                                                                |
| `docker rm $(docker ps -a -q)` | Removes all containers and networks                                                                                        |
| `docker rmi -f $(docker images -q)`| Removes (and un-tags) all images from the host                                                                         |
| `docker volume rm $(docker volume ls -q)` | Removes all volumes and completely wipes any persisted data                                                     |


## Attribution

These install docs are based on the template provided by our friends at [Retool](https://github.com/tryretool/retool-onpremise)