<p align="center">
  <a href="https://datapane.com">
    <img src="https://datapane.com/static/datapane-logo-dark.png" width="250px" alt="Datapane" />
  </a>
</p>

# Deploying Datapane on-premise

Deploying Datapane on-premise ensures that all access to internal data is managed within your own cloud environment. You also have the flexibility to control how Datapane is setup within your infrastructure and integrate Datapane more closely with the other platforms you use.

We also provide a fully-managed hosted version of Datapane - this is always up-to-date and managed by the Datapane team. Furthermore we offer _Datapane Enterprise_, where our team will work with yourself to customise, install, and manage Datapane on your own infrastructure. For information on either option, see our [pricing page](https://datapane.com/pricing/).

## Select a Datapane version number
We recommend you set your Datapane deployment to a specific version of Datapane (that is, a specific semver version number in the format `X.Y.Z`, instead of a tag name). This will help prevent unexpected behavior in your Datapane instances. When you are ready to upgrade Datapane, you can bump the version number to the specific new version you want.

To help you select a version, see our [changelog](https://docs.datapane.com/resources/changelog). If you're not sure which version to install, the latest stable release can be found in the pip badge shown below.

<a href="https://pypi.org/project/datapane/">
    <img src="https://img.shields.io/pypi/v/datapane?color=blue" alt="Latest release" />
</a>


# dp-setup

`dp-setup.py` is a simple Python 3 script to help manage setup your Datapane Server on-premise installation.

It currently supports docker-compose deployments and has 3 main commands,
- `check` - check all required dependencies
- `configure` - generate a docker-compose.yaml file and datapane.env configuration to run
  - this command can be run headlessly
  - this command is optional, you can copy the docker files from `./docker/` and edit them yourselves manually
- `upgrade` - update the Datapane Server installation

To use, follow the deployment instructions below.


# Deployments

Get set up in 15 minutes by deploying Datapane on a single machine. 


## Docker compose

1. Obtain access to a Linux-based machine capable of running datapane
   1. This can be a cloud VM, a bare-metal VM, your local Linux installation, or even an instance of Docker Desktop for Windows / Mac
1. Install Docker and Docker Compose
1. Run the command `git clone https://github.com/datapane/datapane-onpremise.git`.
1. Run the command `cd datapane-onpremise` to enter the cloned repository's directory.
1. Run `dp-setup.py check` to check the installation is valid and all dependencies exist.
1. Run `dp-setup.py configure` and choose the `Dev` option to launch the setup wizard that will generate your `docker.env` file.
   - To manually configure, simply copy `datapane.env` and a `docker-compose.yaml` file from the `/docker` dir and edit as needed.
<!--1. In your `datapane.env` add the following:
    ```
    # License key granted to you by Datapane
    LICENSE_KEY=YOUR_LICENSE_KEY 
    ```
-->
1. (Optional) Edit the `datapane.env` as needed - see the [environment variables](#environemnt_variables) for more information.
1. (Optional) Edit the `docker-compose.yaml` file to set the version of Datapane you want to install. To do this, replace `X.Y.Z` in `FROM datapane/dp-server:X.Y.Z` with your desired version. See [Select a Datapane version number](#select-a-datapane-version-number) to help you choose a version.
1. Run `docker-compose run server ./reset.sh`. This will populate the datapane server with the initial users and settings - you can run this whenever you want reset your instance.
1. Run `docker-compose up -d` to start the Datapane server.
1. Run `docker-compose ps` to make sure all the containers are up and running.
1. Login to your instance using the credentials in [next steps](#next-steps)

## Cloud deployments

### Deploying on AWS

Datapane can be run on AWS (or other cloud platforms) using their existing primitives. Unlike running the standalone `docker-compose` option above, this approach uses your cloud's storage and database backends, which is strongly recommended for any production deployments.

#### S3

S3 is used to store all your report assets, e.g. plots, tables, etc.

1. Create an private S3 bucket, e.g. `datapane-assets`
1. In the S3 console, select the bucket and click **Permissions**. Scroll down the CORS section and set the CORS configuration on the bucket the following,
```json
[
    {
        "MaxAgeSeconds": 3600,
        "AllowedHeaders": [],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```
1. Make a note of the bucket settings, including region, as you will need them editing your `datapane.env` file as mentioned futher on. 

#### RDS (Postgres)
If you do not have an existing Postgres database, setup a standard Postgres database using RDS. Make sure your RDS instance is accessible from your EC2 server instance. This may take a few minutes to boot, so continue with the rest of the steps while you wait.

#### EC2
Spin up a new EC2 instance. If using AWS, use the following steps:
1. Click **Launch Instance** from the EC2 dashboard.
1. Click **Select** and select a Linux instance, such as Amazon Linux 2 or Ubuntu `16.04` or higher.
1. Select an instance type of at least `t3.medium` and click **Next**.
1. Ensure you select a VPC that will include the database you will want to connect to and click **Next: Add Storage**.
1. Increase the storage size to `60` GB or higher and click **Next: Add Tags**. 
1. Optionally add some Tags (e.g. `app = datapane`) and click **Next: Configure Security Group**.
1. Set the network security groups for ports `22` and `8090`, with sources set to `0.0.0.0/0` and `::/0`, and click **Review and Launch**. By default on a vanilla EC2, Datapane will run on port `8090`. If you are running Datapane behind a load balancer, also open the required ports you will be usined. 
1. On the **Review Instance Launch** screen, click **Launch** to start your instance. Optionally download your keypair for connecting to your instance.

#### Datapane Server Setup
1. SSH into your EC2 instance, or connect to it through the AWS UI.
2. If `git` is not included in your distribution, install it using your package manager.
1. Run the command `git clone https://github.com/datapane/datapane-onpremise.git`.
1. Run the command `cd datapane-onpremise` to enter the cloned repository's directory.
1. If they are not installed, install both Docker and Docker Compose. Ensure the Docker daemon is running. If you are not running as root, ensure that [your user has the correct permissions](https://stackoverflow.com/questions/47854463/docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socke).
1. `python3 dp-setup.py check` to check the installation is valid. 
1. Run `python3 dp-setup.py configure` to launch the setup wizard and and select the production option. This will generate your `datapane.env` file, which contains your environment.
<!--1. In your `docker.env` (this file is only created after running `dp-setup.py setup`) add the following:
    ```
    # License key granted to you by Datapane
    LICENSE_KEY=YOUR_LICENSE_KEY 
    ```
-->
1. Edit your `datapane.env ` file to add the following information:
  - Your database credentials
  - S3 bucket name, region, and access keys
  - The full external URL your server will be accessed on, including the protocol and port. 
  - [Optional] You can optionally change the redis location to use a third-party cache, although we do not recommend this for most installs
  - SMTP credentials if you want email support (see below)
  - see the [environment variables](#environemnt_variables) for more information
1. [Optional] Edit the `docker-compose.yml` to set the version of Datapane you want to install. To do this, replace `X.Y.Z` in `FROM datapane/dp-server:X.Y.Z` with your desired version. See [Select a Datapane version number](#select-a-datapane-version-number) to help you choose a version.
1. Run `docker-compose run server ./reset.sh` to reset your Datapane instance and create the initial database and users.
1. Run `sudo docker-compose up -d` to start the Datapane server.
1. Run `sudo docker-compose ps` to make sure all the containers are up and running.
1. Navigate to your server's IP address in a web browser. Datapane should now be running on port `8090`.
1. Login to your instance using the credentials in [next steps](#next-steps)

#### Email
You will need an email server bin order to invite external users and receive notifcations - you can use AWS SES for this. Simply edit `datapane.env` and set the `EMAIL_URL` setting to your SMTP connection string. You can also edit `SERVER_EMAIL` to modify the adddress that emails are sent from.

#### Load Balancer (Optional)
It it recommended that you run your cloud instance behind a load balancer such as ELB, which can provide SSL termination. If you use a load balancer, make sure to update the `DOMAIN` setting in your `datapane.env` file to point to your new external URL (including the port and protocol - e.g. `https://your-datapane-server.your-company.com:8000`)


### Deploying on Heroku

🚧 **Coming Soon**

### Running Datapane using Aptible

🚧 **Coming Soon**

### Deploying to Render

🚧 **Coming Soon**

## Managed deployments

🚧 **Coming Soon**

<!--
Deploy Datapane on a managed service. We're working on providing some starter template files for Cloudformation setups (ECS + Fargate), Kubernetes, and Helm.

Additionally, we hope to be available in the AWS, Azure, and GCS marketplaces shortly.-->

## Additional features

**For details on additional features like SAML SSO, custom certs, and more, visit our [deployment docs](https://docs.datapane.com/deployment).**

## Environment Variables

You can set environment variables in the `datapane.env` to enable custom functionality like storage backends, customizing logging, email, and more.

| Name             | Default                        | Description                                                                                  | 
| -----------------|--------------------------------|----------------------------------------------------------------------------------------------| 
| `DATABASE_URL`   | `postgres://postgres:postgres@db:5432/datapane` | Database connection string for a postgres database, using psql format       | 
| `REDIS_HOST`   | `redis` | Redis connection string, set if using an external redis caching layer | 
| `AWS_ACCESS_KEY_ID`   | - | AWS credentials | 
| `AWS_SECRET_ACCESS_KEY`   | - | AWS credentials | 
| `AWS_STORAGE_BUCKET_NAME`   | - |  Name of the bucket on AWS | 
| `AWS_S3_REGION_NAME`   | `us-east-1` |  Set to your S3 region | 
| `AWS_S3_ENDPOINT_URL`   | - |  Set if using a thrid-party S3 API | 
| `EMAIL_URL` | `submission://user:pass@smtp.example.com` | SMTP connection string |
| `SERVER_EMAIL` | `datapane@datapane.com` | Email address to send notifications from |
| `DOMAIN` | - | Set to the full (external) domain where Datapane Server will be accessed |
| `DP_TENANT_NAME` | `datapane` | The name of your instance |
| `LOG_LEVEL` | `INFO` | Set to `DEBUG`, `INFO`, or `WARNING` to set the logging level |


# Next Steps

Once you have Datapane Server installed and running, you'll want to get invite users, setup groups, and more - please see the [getting started docs](https://docs.datapane.com/datapane-teams)

By default there are 2 users created, 
- `admin` (password `admin-stackhut`) - this is the instance superuser with full permissions.
- `datapane` (password `datapane-stackhut`) - a demo user which is used to create all the examples and demos. This user has no permissions and can safely be deleted if needed.

The `admin` user also has permissions to access the management panel, available at `/dp-admin/` - however be aware when working with the management panel.

We recommend changing the admin password immediately once logged-in from the settings page, and inviting and using extra users rather than using the admin user for day-to-day usage.




## Health check endpoint 

<!-- TODO: Add other watchman endpoint -->

Datapane also has a health check endpoint that you can set up to monitor liveliness of Datapane. You can configure your probe to make a `GET` request to `/site/watchman/`.

<!--## Troubleshooting

- 
-->
## Updating Datapane

The latest Datapane releases can be pulled from Docker Hub. When you run an on-premise instance of Datapane, you’ll need to pull an updated image in order to get new features and fixes. 

<!--See more information on our different versions and recommended update strategies in [our documentation](https://docs.datapane.com/deployment).
-->

### Updating Docker Compose deployments
Update the version number in your `docker-compose.yml`.
```
FROM datapane/dp-server:X.Y.Z
```
Then run the included update command `dp-setup.py update` from this directory.

<!--### Kubernetes deployments
To update Datapane on Kubernetes, you can use the following command, replacing `X.Y.Z` with the version number or named tag that you’d like to update to.

```
kubectl set image deploy/api api=datapane/dp-server:X.Y.Z
```
-->

## Releases

Release notes can be found at https://docs.datapane.com/resources/changelog.

## Docker cheatsheet

Below is a cheatsheet for useful Docker commands. Note that you may need to prefix them with `sudo`. 

| Command                     | Description                                                                                                                   | 
| ----------------------------|-------------------------------------------------------------------------------------------------------------------------------| 
| `docker-compose up -d`      | Builds, (re)creates, starts, and attaches to containers for a service. `-d`allows containers to run in background (detached). | 
| `docker-compose down`       | Stops and remove containers and networks                                                                                      |
| `docker-compose stop`       | Stops containers, but does not remove them and their networks                                                                 |
| `docker ps -a`              | Display all Docker containers                                                                                                 |
| `docker-compose ps -a`      | Display all containers related to images declared in the `docker-compose` file.                                               |
| `docker logs -f <container_name>` | Stream container logs to stdout                                                                                         |
| `docker exec -it <container_name> psql -U <postgres_user> -W <postgres_password> <postgres_db>` | Runs `psql` inside a container                            |
| `docker kill $(docker ps -q)` | Kills all running containers                                                                                                |
| `docker rm $(docker ps -a -q)` | Removes all containers and networks                                                                                        |
| `docker rmi -f $(docker images -q)`| Removes (and un-tags) all images from the host                                                                         |
| `docker volume rm $(docker volume ls -q)` | Removes all volumes and completely wipes any persisted data                                                     |


## Attribution

These install docs are based on the template provided by our friends at [Retool](https://github.com/tryretool/retool-onpremise)
