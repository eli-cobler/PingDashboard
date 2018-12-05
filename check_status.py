from ping import verbose_ping

def ping_server(ipAddress):                                                             # simple function to ping server in locations
    return verbose_ping(ipAddress, count = 1)                                           # returns the results from those pings in ms or None if timeout

def check_ms(locationKey, response_in_milliseconds):                                    # gets us our status code for front end
    status = ""                                                                         # sets status to empty string
    if response_in_milliseconds == None :                                               
        status = "Timeout Error"                                                        # sets status to Timeout Error
    elif response_in_milliseconds >= 1 and response_in_milliseconds <= 100:
        status = "green"                                                                # sets status to Green 
    elif response_in_milliseconds >= 101 and response_in_milliseconds <= 150:
        status = "yellow"                                                               # sets status to Yellow
    elif response_in_milliseconds >= 151 and response_in_milliseconds <= 250:
        status = "orange"                                                               # sets status to Orange
    elif response_in_milliseconds >= 251 and response_in_milliseconds <= 400:
        status = "red"                                                                  # sets status to Red
    elif response_in_milliseconds > 400:
        status = "purple"                                                               # sets status to Purple
    else:
        status = "Your shit ain't working"                                              # else case for anything unexpected

    return status                                                                       # returns out status code