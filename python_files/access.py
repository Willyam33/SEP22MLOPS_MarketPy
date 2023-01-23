import database_functions
import log

ERROR = -1
DENIED = 0
GRANTED = 1

USER_EXISTS = True
USER_DOESNT_EXIST = False

USER_IS_ADMIN = True
NOT_ADMIN = False

def verify_password(username,password):
    """ Vérify User Password """
    return_from_get_password=database_functions.get_password(username)
    if return_from_get_password==ERROR:
        return { 'status': ERROR, 'error_code': log.error_messages['DATABASE_ERROR'] }
    else:
        if return_from_get_password!=password:
            return { 'status': DENIED, 'error_code': log.error_messages['BAD_PASSWORD'] }
        else:
            return { 'status': GRANTED, 'error_code': '' }

def verify_user_login(username,password):
    """ Vérify User exists """
    return_from_get_users_username=database_functions.get_users_username()
    if return_from_get_users_username==ERROR:
        return ERROR
    else:
        if username in return_from_get_users_username:    
            return USER_EXISTS
        else:
            return USER_DOESNT_EXIST

def verify_admin_login(username,password):
    """ Vérify User is an admin """
    if username == "admin":
        return USER_IS_ADMIN
    else:
        return NOT_ADMIN

def verify_user_access(username,password):
    return_from_verify_user_login=verify_user_login(username,password)
    if return_from_verify_user_login==ERROR:
        return { 'status': ERROR, 'error_code': log.error_messages['DATABASE_ERROR'] }    
    elif return_from_verify_user_login==USER_DOESNT_EXIST:
        return { 'status': DENIED, 'error_code': log.error_messages['USER_UNKNOWN'] }    
    else:
        return verify_password(username,password)
        
def verify_admin_access(username,password):
    if verify_admin_login(username,password)==NOT_ADMIN:
        return { 'status': DENIED, 'error_code': log.error_messages['NOT_ADMIN'] }    
    else:
        return verify_password(username,password)

