from ticketing.utility.user import get_user

from types import SimpleNamespace

def get_user_from_id_param(end):
    def decorator(function):

        INVALID_ID_MSG = "The given ID is invalid"
        UNASSIGNED_ID_MSG = "There is no user with the given ID"

        def inner(ptr, request):
            error_str = ""

            if not request.GET.get("id"):
                error_str = INVALID_ID_MSG

                return end(ptr, request)

            try:
                id = int(request.GET.get("id"))

            except ValueError:
                error_str = INVALID_ID_MSG

                return end(ptr, request)

            if id < 0:
                error_str = INVALID_ID_MSG

                return end(ptr, request)

            user = get_user(id)
            if not user:
                error_str = UNASSIGNED_ID_MSG

                return end(ptr, request)
        

            return function(ptr, request, user)
            
        return inner
    return decorator