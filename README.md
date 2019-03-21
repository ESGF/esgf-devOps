# esgf-devOps
The ESGF DevOps scripts provides convenient interfaces for ESGF release and resource management.

## Push Packages to a Conda Channel


### Prerequisites
1. [Conda](https://conda.io/en/latest/)
2. [Anaconda CLI](https://docs.anaconda.com/anaconda-repository/user-guide/tasks/install-client-cli/)
3. Python 3.x
4. An account and write access to a channel of anaconda.org


### Usage
The `push_env_packages.py` script can parse an exported Conda environment file and upload the packages to a Conda channel.  The script will copy the packages listed in the environment file from the Conda-Forge channel to a channel specified by the user.

1. Login to the Anaconda CLI
2. Create the `dev_ops` virtual environment by running `conda env create -f dev_ops_env.yml`
3. Invoke the script using the available command line options.  Example: `python push_env_packages.py --env cog_env.yml --origin conda-forge --destination esgf`

### CLI Options
A CLI is available for providing options to the script.  The available CLI options are as follows:

```shell
  --origin origin_channel [Defaults to conda-forge]
    Name of the conda channel to copy packages from
  --destination destination_channel [Defaults to esgf]
    Name of the conda channel to copy packages to
  --env file_name
    Name of the conda environment file for which to upload the packages it contains
```
