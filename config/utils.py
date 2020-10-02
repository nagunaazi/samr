from logs.models import UserLogs


def create_log(request_details):
    #print(request_details)
    user_logs = UserLogs(username=request_details['username'], log_action=request_details['log_action']
                         , log_host=request_details['log_host']
                         , log_ip=request_details['log-ip'], browser_type=request_details['browser_type'],
                         platform=request_details['browser_type'])
    user_logs.save()
