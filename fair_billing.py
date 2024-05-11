'''
Assumptions:

1. The usernames can contain alphanumeric characters and only "@" as special symbol

2. The sessions types "Start/End" in the log file adhere exactly to the spelling mentioned.

3. The "HH:MM:SS" is a string in the log file

4. If an END session type is encountered after 2 Start session types, then it is paired with the latest Start,    rather than the previous Start. 

        for example:

        "14:02:58 ALICE99 Start",
        "14:03:33 ALICE99 Start",
        "14:03:35 ALICE99 End",
        "14:04:05 ALICE99 End",

        In such a case, the first Start is paired with last End and second Start is paired with second last End.

5. If an end session is encountered for an user after all their session has already been paired, then the End session is assumed to be coming from a session that has not started in the current file and hence the first time in the current file is considered as it's session Start time. For example:

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

        In this case, the last session for ALICE99 is an END session with no previous unpaired Start session. Hence, it will be paired with the start time in the file.

'''



from helper import Helper
import sys

#Function to compute user session for each user from log file and store in 'user_session' dict.
def process_log_file(file_path, helper_functions):
    user_session = {} #Dict to store user sessions
    session_tracker = {} #Dict that keeps track of how many sessions have started for a particular user. (To be used in 'end' block to pair user sessions)
    lowest_second = helper_functions.get_start_time()
    highest_second = helper_functions.get_end_time()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not helper_functions.line_validation(line): #check if line is valid
                    continue

                current_second, user, session_type = helper_functions.get_session_info(line)

                if session_type == 'Start': 

                    if  user not in user_session: 
                        #if the user is encountered for the first time create a nested dict of form: {user1 : { 1: { "session_start": current_second, "session_end": 0}}}
                        user_session[user] = {}
                        session_tracker[user] = [] 
                        session_number = 1
                        user_session[user][session_number]= {"session_start": current_second, "session_end": 0 }
                        session_tracker[user] = [session_number]
                    else:
                        #if user already exists then create a new entry for the user at an updated session number
                        new_session_number = max(list(user_session[user].keys())) + 1
                        user_session[user][new_session_number]= {"session_start": current_second, "session_end": 0 }
                        session_tracker[user].append(new_session_number)

                elif session_type == 'End':

                    if user not in user_session: 
                        #if user is not already present (case when there is no start tag for a user), create an entry with 'session_start' to be the lowest time in file.
                        user_session[user] = {}
                        session_tracker[user] = []
                        session_number = 1
                        user_session[user][session_number]= {"session_start": lowest_second, "session_end": current_second }
                    else:
                        latest_session_number = list(user_session[user].keys())[-1]
                        if user_session[user][latest_session_number]["session_start"] == lowest_second:
                            #Handling the situation if user is already present but their 'session_start' is equal to lowest time it means that this entry has been created either by user with no start session or by this block itself or by the a 'start' session for the user in the very first line.
                            user_session[user][session_number]["session_end"]= current_second
                        else:
                            #If none of the above conditions meet, it means user has a start session other than in the first line of file. 
                            latest_started_session = session_tracker[user].pop()
                            if user_session[user][latest_started_session]["session_end"] == 0:
                                #If the "session_end" of the last value in the session tracker is still zero, it means a session has started but not ended. It can be paired with the current time of encountered end tag.
                                user_session[user][latest_started_session]["session_end"] = current_second
                            else:
                                #In other case it means all the started sessions have been paired. The end tag encountered is considered to be coming from an earlier session that is not in the current file. 
                                user_session[user][latest_session_number + 1] = {"session_start": lowest_second, "session_end": current_second }
        
        results = helper_functions.display_session_info(user_session, highest_second)
        return results

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'samplelog.txt'  #googled
    helper_functions = Helper(file_path)
    process_log_file(file_path, helper_functions)

                        
                

                        
                        


