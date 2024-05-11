'''
Assumptions:

The helper methods used in various test cases uses the "samplelog.txt" file. Hence the results for all the test cases should be considered in accordance with the start time and end time of the "samplelog.txt" file. For example:

"14:02:05 CHARLIE End" This line 


'''













import pytest
from fair_billing import process_log_file, Helper


@pytest.fixture
def helper():
    return Helper('samplelog.txt')


#Tests for the helper function
def test_line_validation(helper):
    assert helper.line_validation('14:02:03 ALICE99 Start') == True
    assert helper.line_validation('Invalid line') == False

def test_get_session_info(helper):
    current_second, user, session_type = helper.get_session_info('14:02:03 ALICE99 Start')
    assert current_second == 50523
    assert user == 'ALICE99'
    assert session_type == 'Start'

def test_get_start_time(helper):
    assert helper.get_start_time() == 50523

def test_get_end_time(helper):
    assert helper.get_end_time() == 50682




#Tests for the process_log_file function

@pytest.fixture
def test_log_contents():
    return [
        "14:02:03 ALICE99 Start",
        "14:02:05 CHARLIE End",
        "14:02:34 ALICE99 End",
        "14:02:58 ALICE99 Start",
        "14:03:02 CHARLIE Start",
        "14:03:33 ALICE99 Start",
        "14:03:35 ALICE99 End",
        "14:03:37 CHARLIE End",
        "14:04:05 ALICE99 End",
        "14:04:23 ALICE99 End",
        "14:04:41 CHARLIE Start",
        "14:04:42 JJJJJJJ End",
        "14:04:42 Start",
        "14:04:42 sss4544 Start",
        "14:04:42 CHARLIE wrew",
        "99:04:42 CHARLIE Start",
        "14:04:42 CH@RLI3 Start",
        "14:04:42 ******* Start"
    ]

def test_valid_start_and_end_sessions(test_log_contents, helper):

    with open('test_log.txt', 'w') as file:
        for line in test_log_contents:
            file.write(line + '\n')

    expected_output = ['ALICE99 4 240', 'CHARLIE 3 38', 'JJJJJJJ 1 159', 'sss4544 1 0', 'CH@RLI3 1 0']
    assert process_log_file('test_log.txt', helper) == expected_output

def test_invalid_time_format(helper):

    invalid_time_format_log = ["99:04:42 CHARLIE Start"]

    with open('test_log.txt', 'w') as file:
        for line in invalid_time_format_log:
            file.write(line + '\n')

    expected_output = []
    assert process_log_file('test_log.txt', helper) == expected_output

def test_start_without_end_session(helper):

    start_without_end_log = ["14:04:42 CH@RLI3 Start"]

    with open('test_log.txt', 'w') as file:
        for line in start_without_end_log:
            file.write(line + '\n')

    expected_output = ['CH@RLI3 1 0']
    assert process_log_file('test_log.txt', helper) == expected_output

def test_end_without_start_session(helper):

    end_without_start_log = [
        "14:02:05 CHARLIE End",
        
        ]

    with open('test_log.txt', 'w') as file:
        for line in end_without_start_log:
            file.write(line + '\n')

    expected_output = ["CHARLIE 1 2"]
    assert process_log_file('test_log.txt', helper) == expected_output


def test_invalid_username(helper):

    invalid_username_log = ["14:04:42 ******* Start"]

    with open('test_log.txt', 'w') as file:
        for line in invalid_username_log:
            file.write(line + '\n')

    expected_output = []
    assert process_log_file('test_log.txt', helper) == expected_output


def test_invalid_session_type(helper):

    invalid_session_type_log = ["14:04:42 CHARLIE wrew"]

    with open('test_log.txt', 'w') as file:
        for line in invalid_session_type_log:
            file.write(line + '\n')

    expected_output = []
    assert process_log_file('test_log.txt', helper) == expected_output

def test_overlapping_session(helper):

    overlapping_session_log = [
        "14:02:58 ALICE99 Start",
        "14:03:02 CHARLIE Start",
        "14:03:33 ALICE99 Start",
        "14:03:35 ALICE99 End",
        "14:03:37 CHARLIE End",
        "14:04:05 ALICE99 End",
    ]
    with open('test_log.txt', 'w') as file:
        for line in overlapping_session_log:
            file.write(line + '\n')

    expected_output = ['ALICE99 2 69', 'CHARLIE 1 35']
    assert process_log_file('test_log.txt', helper) == expected_output

if __name__ == "__main__":
    pytest.main()
    



