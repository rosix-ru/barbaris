# -*- coding: utf-8 -*-
from django.db import connection, transaction
import os

def upload_to(cls, filename):
    """ Function for the reference to a method 
        of a yet not definition class
    """
    return cls.upload_to(filename)

def osdelete(filename):
    if os.path.exists(filename):
        os.remove(filename)
        return True
    else:
        return False
