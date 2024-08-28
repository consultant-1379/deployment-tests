##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

# pylint: disable=W1201

"""Common functions"""

import re
import subprocess
import time
from configuration.logging import LOG
import helpers.common.constants as constants


def execute_cli_locally(command, timeout=constants.CLI_EXECUTION_TIMEOUT, log_command=True,
                        log_output=True, return_output_as_string=True):
    """
    Execute CLI locally

    :param command: Command to execute
    :param timeout: Command execution timeout
    :param log_command: If True, log the command to execute
    :param log_output: If True, log command output (stdout)
    :param return_output_as_string: If True, Return output as string, Else, as list.
    :return: stdout if command succeeds, else False
    """
    try:
        if log_command:
            LOG.info("Executing command :\n%s", command)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        retval = proc.wait(timeout)

        if retval == 1 or proc.stderr is not None:
            return handle_command_error_output(proc)

        stdout = None
        if proc.stdout is not None:
            stdout = proc.stdout.readlines()
            if return_output_as_string:
                stdout = convert_list_to_string(stdout).strip()
            if log_output:
                LOG.info("Stdout :\n%s", stdout)
        return stdout

    except (OSError, Exception) as error:
        return handle_common_exception(error, constants.COMMON_EXCEPTION_MESSAGE)


def execute_command_and_wait_for_regex_count_match(
        command, regex_to_match, regex_match_count=constants.REGEX_MATCH_COUNT_DEFAULT,
        timeout=constants.COMMAND_OUTPUT_REGEX_MATCH_TIMEOUT):
    """
    Wait for regex match for given count times in command output

    :param command: Command to execute
    :param regex_to_match: Regex to match in the logs
    :param regex_match_count: Count to match regex in the logs
    :param timeout: Timeout
    :return: True if regex match count found in command output, else False
    """
    try:
        LOG.info("Waiting for regex = [%s] match for %s times in output", regex_to_match,
                 regex_match_count)

        timeout = time.time() + timeout

        regex_obj = re.compile(regex_to_match)
        log_regex_match_count = 0
        stdout = ""
        while log_regex_match_count != regex_match_count:
            stdout = execute_cli_locally(command, log_command=False, log_output=False)
            if stdout is not None:
                regex_match = regex_obj.findall(stdout)
                if regex_match is not None:
                    log_regex_match_count = len(regex_match)

            LOG.info("Regex match count : %d", log_regex_match_count)
            if time.time() > timeout:
                LOG.info("Stdout :\n%s", str(stdout))
                LOG.error("timed out waiting for regex = [%s] to match %s times in output",
                          regex_to_match, regex_match_count)
                return False
            time.sleep(constants.COMMAND_OUTPUT_REGEX_MATCH_SLEEP_TIME)

        LOG.info("Stdout with matched regex count :\n%s", stdout)
        return True

    except (OSError, Exception) as error:
        return handle_common_exception(error, constants.COMMON_EXCEPTION_MESSAGE)


def execute_command_and_match_regex_list(command, regex_list):
    """
    Execute command and match multiple regex in the output

    :param command: Command to execute
    :param regex_list: List of regex to match
    :return: True if regex list matched in command output, else False
    """
    try:
        LOG.info("Regex list to match : %s", str(regex_list))
        stdout = execute_cli_locally(command)

        regex_match = re.findall("|".join(regex_list), stdout)
        if regex_match is None:
            LOG.error("None of the regex matched in the output")
            return False

        LOG.info("Matched regex : %s", str(regex_match))
        regex_match = list(dict.fromkeys(regex_match))
        LOG.info("Matched regex without duplicates : %s", str(regex_match))

        regex_list_count = len(regex_list)
        regex_match_count = len(regex_match)
        LOG.info("Regex list count : %d", regex_list_count)
        LOG.info("Matched regex count : %d", regex_match_count)

        if regex_match_count != regex_list_count:
            return False

        return True

    except (OSError, Exception) as error:
        return handle_common_exception(error, constants.COMMON_EXCEPTION_MESSAGE)


def handle_command_error_output(proc):
    """
    Handle command error output

    :param proc: subprocess instance
    :return: False as error response
    """
    LOG.error("Command execution resulted in error response.")
    if proc.stdout is not None:
        log_command_error_output(proc.stdout.readlines(), "Stdout :")
    if proc.stderr is not None:
        log_command_error_output(proc.stderr.readlines(), "Stderr :")
    return False


def log_command_error_output(lines, error_message=None):
    """
    Log command output error

    :param lines: Command output lines
    :param error_message: (optional) Error message
    """
    log_message = ""
    if error_message is not None:
        log_message = error_message + "\n"
    for line in lines:
        log_message += line.decode(constants.BYTE_TO_STRING_DECODE_TYPE_UTF_8) + "\n"
    LOG.error(log_message)


def handle_common_exception(error, message=None):
    """
    Handle common exception

    :param error: Exception error instance
    :param message: (optional) Error message
    :return: False as error response
    """
    log_message = ""
    if message is not None:
        log_message = message + "\n"
    LOG.error(log_message + str(error))
    return False


def convert_list_to_string(string_list):
    """
    Convert list to string

    :param string_list: List to be converted to string
    :return: converted string
    """
    output_string = ""
    for line in string_list:
        if isinstance(line, bytes):
            line = line.decode(constants.BYTE_TO_STRING_DECODE_TYPE_UTF_8)
        output_string += str(line) + "\n"

    LOG.debug("Output string : %s\n", output_string)
    return output_string
