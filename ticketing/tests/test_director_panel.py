from django.test import TestCase

from django.urls import reverse

from http import HTTPStatus

from ticketing.tests.utility.seeding import SeededTestCase


def make_director_command_query(user_role):
    return {'commands_account_role': user_role}


def make_director_filter_query(id, first_name, last_name, email, user_role):
    return {
        'id': id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'account_role': user_role,
    }


def make_add_user_form_query(
    email, first_name, last_name, password, user_role
):
    return {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': password,
        'add_user_account_role': user_role,
    }


class TestDirectorPanel(SeededTestCase):
    pass


#     def setUp(self):

#         super().setUp()

#         self.valid_filters = []

#         for i in range(len(self.user_list)):
#             self.valid_filters.append(make_director_filter_query(
#                                                                 i + 1, # + 1 as IDs start at 1 and i starts at 0
#                                                                 self.user_list[i].first_name,
#                                                                 self.user_list[i].last_name,
#                                                                 self.user_list[i].email,
#                                                                 self.user_list[i].account_role))

#         self.valid_filters.append(make_director_filter_query("", "", "", "", ""))


#         # self.valid_filters.append(make_director_filter_data(
#         #                         "1", "Luke", "Test", "luke@7ic.net", User.Role.STUDENT))


# class TestDirectorPanelView(TestDirectorPanel):
#     def setUp(self):
#         super().setUp()


#     def test_POST_and_GET(self):
#         #
#         # If post_type == None, then GET request will be tested, and query will be used as the GET query
#         #
#         def run(post_type, post_value, valid, query, selected = None):


#             if query == None:
#                 query = {}

#             if selected == None:
#                 selected = []


#             if post_type == None:
#                 # GET request

#                 # Test filters


#                 response = self.client.get(reverse("director_panel"), data = query)

#                 return


#         run(None, None, True, None)

#         for i in range(len(self.valid_filters)):
#             run(None, None, True, self.valid_filters[i])
