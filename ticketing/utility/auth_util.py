from ticketing.const import *

def landing_redirect_by_role(role):
    return redirect("login")
    # match role:
    #     case ROLE_STUDENT:
    #         return redirect("login")

    #     case ROLE_SPECIALIST:
    #         return redirect("login")

    #     case ROLE_DIRECTOR:
    #         return redirect("login")