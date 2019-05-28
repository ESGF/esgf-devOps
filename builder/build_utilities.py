"""Utility functions for esgf_build.py."""
import os
import hashlib
import errno
import logging
from contextlib import contextmanager
from plumbum import local
from plumbum import TEE
from plumbum import BG
from plumbum.commands import ProcessExecutionError

logger = logging.getLogger(__name__)


def call_binary(binary_name, arguments=None, silent=False, conda_env=None, stderr_output=None):
    """Use plumbum to make a call to a CLI binary.  The arguments should be passed as a list of strings."""
    RETURN_CODE = 0
    STDOUT = 1
    STDERR = 2
    logger.debug("binary_name: %s", binary_name)
    logger.debug("arguments: %s", arguments)
    if conda_env is not None:
        if arguments is not None:
            arguments = [conda_env, binary_name] + arguments
        else:
            arguments = [conda_env, binary_name]
        binary_name = os.path.join(os.path.dirname(__file__), "run_in_env.sh")
    try:
        command = local[binary_name]
    except ProcessExecutionError:
        logger.error("Could not find %s executable", binary_name)
        raise

    for var in os.environ:
        local.env[var] = os.environ[var]

    if silent:
        if arguments is not None:
            cmd_future = command.__getitem__(arguments) & BG
        else:
            cmd_future = command.run_bg()
        cmd_future.wait()
        output = [cmd_future.returncode, cmd_future.stdout, cmd_future.stderr]
    else:
        if arguments is not None:
            output = command.__getitem__(arguments) & TEE
        else:
            output = command.run_tee()

    # special case where checking java version is displayed via stderr
    if command.__str__() == '/usr/local/java/bin/java' and output[RETURN_CODE] == 0 or stderr_output:
        return output[STDERR]

    # Check for non-zero return code
    if output[RETURN_CODE] != 0:
        logger.error("Error occurred when executing %s %s", binary_name, " ".join(arguments))
        logger.error("STDERR: %s", output[STDERR])
        raise ProcessExecutionError
    else:
        return output[STDOUT]


def get_md5sum(file_name):
    """Wrap md5sum so it may be used on either mac or linux machines."""
    hasher = hashlib.md5()
    with open(file_name, 'rb') as file_handle:
        buf = file_handle.read()
        hasher.update(buf)
        file_name_md5 = hasher.hexdigest()
    return file_name_md5


def mkdir_p(path, mode=0777):
    """Make directory, passes if directory already exists."""
    try:
        os.makedirs(path, mode)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            print "{path} already exists".format(path=path)
        else:
            raise


@contextmanager
def pushd(new_dir):
    """Mimic Bash's pushd functionality.

    Usage:
    with pushd(some_dir):
        print os.getcwd() # "some_dir"
        some_actions
    print os.getcwd() # "starting_directory"
    """
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    yield
    os.chdir(previous_dir)
