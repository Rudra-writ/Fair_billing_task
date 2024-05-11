import re

class Helper:
    def __init__(self, file_path):
        self.file_path = file_path

    
    #Method to validate each line read from file to ensure they follow the "HH:MM:SS user_name Start/End" pattern. 
    #Returns False if patterns don't match.
    def line_validation(self, line):
        pattern = r"^(2[0-3]|[01]\d):([0-5]?\d):([0-5]?\d) [A-Za-z0-9@]+ (Start|End)$" #picked from chatgpt
        return bool(re.match(pattern, line))



    #Method to get total seconds from hour,minute and second in each line
    def get_session_info(self, line):
        try:
            time, user, session_type = line.split()
            hh, mm, ss = map(int, time.split(':'))
            seconds = hh * 3600 + mm * 60 + ss
            return seconds, user, session_type
        except ValueError:
            raise ValueError(f"Expected 3 elements in line but got {len(line.split())}")
        except Exception as e:
            print(str(e))



    #Method to print the results in required format
    @staticmethod
    def display_session_info(user_session, highest_second):
        results = []
        for user, sessions in user_session.items():
            duration = 0
            total_sessions = len(sessions)
            for session_info in sessions.values():
                if session_info["session_end"] != 0:
                    duration += session_info["session_end"] - session_info["session_start"]
                else:
                    duration += highest_second - session_info["session_start"]
            print(f"{user} {total_sessions} {duration}")
            results.append(f"{user} {total_sessions} {duration}")
        return results



    #Method to get the start time (in seconds). If first line is in invalid format then it is fetched from subsequent lines, as soon valid line is found.
    def get_start_time(self):
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    got_line = line.strip()
                    if self.line_validation(got_line):
                        seconds, _ , _ = self.get_session_info(got_line)
                        return seconds
                raise Exception("Start time could not be computed")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found at path: {self.file_path}")
        except ValueError as e:
            raise ValueError(f"Error processing line: {e}")
        except Exception as e:
            print(str(e))


    #Method to get the end time (in seconds). If last line is in invalid format then it is fetched from previous lines.
    def get_end_time(self):
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                for line in reversed(lines): #Start reading last line in reverse order
                    got_line = line.strip()
                    if self.line_validation(got_line):
                        seconds, _ , _ = self.get_session_info(got_line)
                        return seconds
                raise Exception("End time could not be computed")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found at path: {self.file_path}")
        except ValueError as e:
            raise ValueError(f"Error processing line: {e}")
        except Exception as e:
            print(str(e))