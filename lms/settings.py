app_name = "lms"
host_dir = "lms"
rel_login_url = "login"
def on_authenticate(model):
    return True
def on_get_language_resource_item(language,appname,view,key,value):
    return value
