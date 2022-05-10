from django.test import TestCase

from .service import calculate_cross_section

# Create your tests here.


result = calculate_cross_section(1000, 30, 45, 1.25, 160, 1)

print(result)
