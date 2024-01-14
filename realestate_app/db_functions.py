from django.db.models import Func


class Unaccent(Func):
    function = "UNACCENT"
