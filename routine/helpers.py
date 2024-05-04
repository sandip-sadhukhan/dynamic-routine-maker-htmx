import random
import string

from django.utils.text import slugify

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_slug_for_routine(routine_name, Routine):
    slug = slugify(routine_name)
    final_slug = slug

    # Check if the slug is already in use
    while True:
        if not Routine.objects.filter(slug=final_slug).exists():
            break
        
        final_slug = slug + "-" + generate_random_string()

    return final_slug