import os
import django
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import unittest
from location.utils.utils import CheckRequestLocation, create_responce
from location.serializers import LocationRequestSerializer

# Կարգավորում ենք Django միջավայրը
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaedo.settings")  # Փոխարինեք "vaedo" ձեր նախագծի անունով
django.setup()



class TestCheckLocationRequestSerializer(unittest.TestCase):
    def setUp(self):
        self.valid_latitude = 43.8
        self.valid_longitude = 40.75
        self.invalid_latitude = "100.0"  # Out of range
        self.invalid_longitude = "200.0"  # Out of range
        self.invalid_type_latitude = '10dgsh0.0'  # Out of range
        self.invalid_type_longitude = '20trhrh0.0'  # Out of range
        self.invalid_latitude_ = "43.76001"  # Out of range
        self.invalid_longitude_ = "40.706001"  # Out of range
    def test_missing_coordinates(self):
        serializer = LocationRequestSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, AssertionError)
    
    def test_invalid_thpe_coordinates(self):
        """Test with missing latitude and longitude"""
        serializer = LocationRequestSerializer(data={"latitude":self.invalid_type_latitude, "longitude":self.invalid_type_longitude})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, _("Invalid request"))
        
    def test_out_of_range_coordinates(self):
        """Test with out-of-range latitude and longitude"""
        serializer = LocationRequestSerializer(data={"latitude":self.invalid_latitude, "longitude":self.invalid_longitude})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {"detail":_("Sorry, the service is not available at the specified location.")})

    def test_out_of_range_avelable_space(self):
        """Test with out-of-range latitude and longitude"""
        serializer = LocationRequestSerializer(data={"latitude":self.invalid_latitude_, "longitude":self.invalid_longitude_})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {"detail":_("Sorry, the service is not available at the specified location.")})



# class Testcreate_responce(unittest.TestCase):
#     def setUp(self):
#         pass

class TestCheckRequestLocation(unittest.TestCase):
    def setUp(self):

        self.valid_latitude = 43.8
        self.valid_longitude = 40.75
        self.invalid_latitude = "100.0"  # Out of range
        self.invalid_longitude = "200.0"  # Out of range
        self.invalid_type_latitude = '10dgsh0.0'  # Out of range
        self.invalid_type_longitude = '20trhrh0.0'  # Out of range
        self.invalid_latitude_ = "43.76001"  # Out of range
        self.invalid_longitude_ = "40.706001"  # Out of range

    def test_missing_coordinates(self):
        """Test with missing latitude and longitude"""
        checker = CheckRequestLocation(lang='en')
        self.assertFalse(checker.is_valid)
        self.assertEqual(checker.reason_validation, _("Invalid request"))


    def test_invalid_thpe_coordinates(self):
        """Test with missing latitude and longitude"""
        checker = CheckRequestLocation(lang='en',latitude= self.invalid_type_latitude, longitude=self.invalid_type_longitude)
        is_valid = checker.is_valid
        self.assertFalse(checker.is_valid)
        self.assertEqual(checker.reason_validation, _("Invalid request"))

    def test_out_of_range_coordinates(self):
        """Test with out-of-range latitude and longitude"""
        checker = CheckRequestLocation(lang='en', latitude=self.invalid_latitude, longitude=self.invalid_longitude)
        self.assertFalse(checker.is_valid)
        self.assertEqual(checker.reason_validation, {"detail":_("Sorry, the service is not available at the specified location.")})

    def test_out_of_range_avelable_space(self):
        """Test with out-of-range latitude and longitude"""
        checker = CheckRequestLocation(lang='en',latitude=self.invalid_latitude_, longitude=self.invalid_longitude_)
        self.assertFalse(checker.is_valid)
        self.assertEqual(checker.reason_validation, {"detail":_("Sorry, the service is not available at the specified location.")})



# python -m unittest location.tests.test_utils

if __name__ == "__main__":
    unittest.main()