from ticketing.models import User

# Emails
valid_emails = ["luke@test.net", "peter@hotmail.net", "person@later.com", "water@postbox.info",
                 "test@example.com", "a@a.c", "t@t.h", "LUKE@JJJK.NEt", "jssdfjsoiojIOJOJ@GFSIOJIOJ.COM"]

invalid_emails = ["jfkdjs", "JIJFIO", "kfjskl.co.uk", "@.com", "@", "a", "someone@com"]

# Names
valid_first_names = ["Luke", "Hello", "Later", "Furthermore", "House", "Trello", 
                        "jhhiuHUIGHDFUIHUISFGIOUHOUI", "jfsiojhijkPjfSj", "John"]
invalid_first_names = ["a" * 60, "b" * 60, "", "jiffsfsfbJIOJ" * 20, ("lk" * 10) + "fjiok" * 10]

print("VALID FIRST IS: ", list(reversed(valid_first_names)))
valid_last_names = list(reversed(valid_first_names))
invalid_last_names = list(reversed(invalid_first_names))

# Passwords
valid_passwords = ["Hello123%", "Hello12345567%", "jifjio&jj8ifgjK", "SuperPassword987%", "NoWayToGuess87", 
                    "Trello87^^", "iojjhioughuirehuHjfgjfgji0nfkljdngknkjg", "asbfHu7y", "&*(&*^^*&^&*(&6jH8"]

invalid_passwords = ["a" * 7, "jsfjsojoisfghuishgiusah", "IUHGDIUDHIFGHFDIUGHUIDFHGI", "589794754937589347589",
                        "fjsdkfsjkf7", "JIJFSOIJ8", "djfiosjfiojJIOJOIJIO", "yes", "further", "jj8Hk"]

# Roles
valid_roles = [User.Role.STUDENT, User.Role.SPECIALIST, User.Role.DIRECTOR]
invalid_roles = ["GJK", "", "AB", "99", "S", "D", "897", "jfjdij", "l"],
