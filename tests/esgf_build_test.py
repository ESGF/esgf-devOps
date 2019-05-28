from builder import esgf_build
from builder import build_utilities
from builder import purge_and_clone_fresh_repos
from builder import repo_info
import os
import shutil
import pytest
from git import Repo


def finalizer_function():
    print "Deleting temp repos"
    shutil.rmtree("/tmp/esgf_repos")


@pytest.fixture(scope="session", autouse=True)
def setup_test_env(request):
    # prepare something ahead of all tests
    build_utilities.mkdir_p("/tmp/esgf_repos")
    with build_utilities.pushd("/tmp/esgf_repos/"):
        for repo in repo_info.ALL_REPO_URLS.values():
            build_utilities.call_binary("git", ["clone", repo])
    request.addfinalizer(finalizer_function)


def test_choose_directory():
    build_utilities.mkdir_p("/tmp/esgf_repos")
    assert esgf_build.choose_directory("/tmp/esgf_repos") == "/tmp/esgf_repos"


def test_get_latest_tag():
    for repo in repo_info.ALL_REPO_URLS:
        with build_utilities.pushd(os.path.join("/tmp", "esgf_repos", repo)):
            print "========================================"
            print "Testing get_latest_tag for {}".format(repo)
            print "========================================"
            repo = Repo(os.getcwd())
            latest_commit = build_utilities.call_binary("git", ["rev-list", "--tags", "--max-count=1"]).strip()
            git_describe_output = build_utilities.call_binary("git", ["describe", "--tags", latest_commit])
            print 'git_describe_output for annotated tag for {}: {}'.format(repo, git_describe_output)
            latest_tag = esgf_build.get_latest_tag(repo)
            print "latest_tag for {}: {}".format(repo, latest_tag)
            assert latest_tag.strip() == git_describe_output.strip().split("-", 1)[0]


def test_list_remote_tags():
    for repo in repo_info.ALL_REPO_URLS:
        with build_utilities.pushd(os.path.join("/tmp", "esgf_repos", repo)):
            assert esgf_build.list_remote_tags() is not []


def test_list_local_tags():
    with build_utilities.pushd("/tmp/esgf_repos/esg-orp"):
        repo = Repo(os.getcwd())
        assert esgf_build.list_local_tags(repo) is not []


def test_update_tags():
    with build_utilities.pushd("/tmp/esgf_repos/esg-orp"):
        repo = Repo(os.getcwd())
        latest_commit = build_utilities.call_binary("git", ["rev-list", "--tags", "--max-count=1"]).strip()
        git_describe_output = build_utilities.call_binary("git", ["describe", "--tags", latest_commit])
        remote_tags = esgf_build.list_remote_tags()
        print "remote_tags:", remote_tags
        print "git_describe_output:", git_describe_output
        assert esgf_build.update_tags(repo) is True
        assert remote_tags[0].strip() == git_describe_output.strip().split("-", 1)[0]


def test_get_published_releases():
    repo = 'esg-orp'
    releases = esgf_build.get_published_releases("ESGF/{}".format(repo))
    assert releases is not []
