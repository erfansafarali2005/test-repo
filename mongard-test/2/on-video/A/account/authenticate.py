from django.contrib.auth.models import User

class EmailBackend: # first it tries to load the user form the default authentication system but it it rturns None it comes to this class and tries to authenticate it
    def authenticate(self , request , username=None , password=None): #the authencticate function that we use it in views.py
        #                                 ^-> username = cd['form_login_username'] -> this username is the name of the username collumn of the model
        try: #try if the user was ok
            user = User.objects.get(email=username) #checks the user by its email with the comming username from views.py
            #                         ^-> fitst authenticate check : email = email , so it dosn't work so it comes to check username as email
            if user.check_password(password):#if user password  which is comming from cleandata was correct
                return user # this user returns back to the user variable in view where we authenticate with cleaned_data | : user = authenticate(...)
            else:
                return None
        except User.DoesNotExist: # if check by email was wrong :
            return None
    def get_user(self , user_id): #after authenticate this fuction will be execuded to return the user to the views.py
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None

    # add the class to the settings.py