"""Common constants shared by all modules."""

APPNAME = "mwiki"


## Http Method GET 
M_GET = "GET" 
# Http Method Post
M_POST = "POST"
# Http Delete Method
M_DELETE = "DELETE"

STATUS_CODE_400_BAD_REQUEST        = 400
STATUS_CODE_405_METHOD_NOT_ALLOWED = 405
STATUS_CODE_403_FORBIDDEN          = 403
STATUS_CODE_401_UNAUTHORIZED       = 401
STATUS_CODE_404_NOT_FOUND          = 404

## User types constants
USER_MASTER_ADMIN = 100 
USER_ADMIN = 50 
USER_EDITOR = 20
USER_GUEST = 10  
USER_ANONYMOUS = 0 