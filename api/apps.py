from django.apps import AppConfig



class ApiConfig(AppConfig):
    name = 'api'
    names = set()

    def ready(self):

        print("-------------------------RAN READY FUNCTION----------------------------")

        global names
        file = open('validation_data/names.txt')
        for f in file:
            l = list(f.split("\n"))
            names.add(l[0])
