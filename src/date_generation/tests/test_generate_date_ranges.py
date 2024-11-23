import unittest
from datetime import date

from src.common.conventions import GeneralConventions
from src.date_generation.generate_date_ranges import generate_date_ranges


class TestGenerateDateRanges(unittest.TestCase):
    def test_generate_date_ranges_monthly_full_year(self):
        """Test monthly frequency for a single year with all months."""
        years = [2024]
        months = None
        frequency = GeneralConventions.frequency_monthly
        result = generate_date_ranges(years, months, frequency)
        print(result)
        expected = [(date(2024, 1, 1), date(2024, 1, 31)),
                    (date(2024, 2, 1), date(2024, 2, 29)),
                    (date(2024, 3, 1), date(2024, 3, 31)),
                    (date(2024, 4, 1), date(2024, 4, 30)),
                    (date(2024, 5, 1), date(2024, 5, 31)),
                    (date(2024, 6, 1), date(2024, 6, 30)),
                    (date(2024, 7, 1), date(2024, 7, 31)),
                    (date(2024, 8, 1), date(2024, 8, 31)),
                    (date(2024, 9, 1), date(2024, 9, 30)),
                    (date(2024, 10, 1), date(2024, 10, 31)),
                    (date(2024, 11, 1), date(2024, 11, 30)),
                    (date(2024, 12, 1), date(2024, 12, 31))]

        self.assertEqual(result, expected)

    def test_generate_date_ranges_yearly(self):
        """Test yearly frequency for multiple years."""
        years = [2023, 2024]
        frequency = GeneralConventions.frequency_yearly
        result = generate_date_ranges(years, frequency=frequency)

        expected = [
            (date(2023, 1, 1), date(2023, 12, 31)),
            (date(2024, 1, 1), date(2024, 12, 31))
        ]
        self.assertEqual(result, expected)

    def test_generate_date_ranges_monthly_specific_months(self):
        """Test monthly frequency for specific months in a single year."""
        years = [2024]
        months = [1, 12]  # January and December
        frequency = GeneralConventions.frequency_monthly
        result = generate_date_ranges(years, months, frequency)

        expected = [
            (date(2024, 1, 1), date(2024, 1, 31)),
            (date(2024, 12, 1), date(2024, 12, 31))
        ]
        self.assertEqual(result, expected)

    def test_multi_year(self):
        years = [2022, 2023]
        months = None
        frequency = GeneralConventions.frequency_multiyear
        expected = [(date(2022, 1, 1)), date(2024, 12, 31)]
        result = generate_date_ranges(years, months, frequency)
        self.assertEqual(result, expected)

    def test_generate_date_ranges_invalid_frequency(self):
        """Test invalid frequency."""
        years = [2024]
        months = None
        frequency = 'invalid_frequency'
        with self.assertRaises(ValueError):
            generate_date_ranges(years, months, frequency)
