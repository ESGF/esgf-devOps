# esgf-devOps
The ESGF DevOps scripts provides convenient interfaces for ESGF release and resource management.

## Installation

### Prerequisites

#### Package Uploader
1. [Conda](https://conda.io/en/latest/)
2. [Anaconda CLI](https://docs.anaconda.com/anaconda-repository/user-guide/tasks/install-client-cli/)
3. Python 3.x
4. An account and write access to a channel of anaconda.org

#### ESGF Build
1. Path to directory with ESGF repositories
2. Dependencies installed:
    * Python 2.7
    * Apache Ant
3. A .netrc file with a GitHub access token entry.  ESGF-Build uses the githubrelease python module under the hood and it uses token-based authentication.  See [Configuring githubrelease](https://github.com/j0057/github-release#configuring)

### Installing:
1. Clone the esgf-devOps repo ```git clone https://github.com/ESGF/esgf-devOps.git ```

2. Create the `dev_ops` virtual environment by running `conda env create -f dev_ops_env.yml`

## Push Packages to a Conda Channel

### Usage
The `push_env_packages.py` script can parse an exported Conda environment file and upload the packages to a Conda channel.  The script will copy the packages listed in the environment file from the Conda-Forge channel to a channel specified by the user.

1. Login to the Anaconda CLI
2. Invoke the script using the available command line options.  Example: `python push_env_packages.py --env cog_env.yml --origin conda-forge --destination esgf`

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


## ESGF Build

The ESGF Build script provides a convenient interface for building binary assets from multiple ESGF projects.  The script
has a command line interface for providing arguments as well as interactive prompts as a fallback.

The build process typically works as follows: checkout a branch/tag from GitHub -> pull the latest changes -> build the project -> (optionally) update the tag for the project -> (optionally) push the built assets to GitHub

### Building With Script:
1. Run *esgf_build.py* by typing:
    ``` shell
    python esgf_build.py [repo_1 repos_2 ...repo_n]
    ```
  The esgf_build has command line arguments that can be passed to the script.
  ```shell
  --directory /path/to/repos
    Enter the path to the directory containing repositories on the system.
  --branch branch_name
    Choose which branch/tag you will be building from. Valid options are any branch name for a repo or 'latest'. 'latest' builds from the most recent tag.
  --bump version_component
    Bump the version number according to the Semantic Versioning specification. Valid options are 'major', 'minor', or 'patch'. Leaves version unchanged if option is omitted.
  --name release_name
    Enter a name for the release.  The release will default to tag number as the name if this option is omitted.
  --prerelease
    Boolean flag for tagging the release a nonproduction. Defaults to False if omitted
  --dryrun
    Boolean flag for performing a dry run of the release. Defaults to False if omitted
  --synctag
    Boolean flag for performing deleting local tags that are not in sync with the remote repo. Defaults to False if omitted
  --upload/--no-upload
    Boolean flag to choose whether to upload built assets to GitHub.
```
 If any of the command line options are not passed to the script invocation, then the script will prompt for the user input.

2. Enter a title for the release when prompted.  
3. Enter 'yes' or 'no' when prompted to bump the version number.  You will be able to bump the version number according to the [Semantic Versioning](https://semver.org/) guidelines.

The script will then upload the binaries to the respective GitHub repositories.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/ESGF/esgf-build/tags).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
