import pytest
from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_calculate_multiply_correctly(self):
        assert self.calc.multiply(self, 2, 2) == 4

    def test_calculation_multiply_failed(self):
        assert self.calc.multiply(self, 2, 2) == 5