
import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# Tests for extra_time_charge()

def test_within_included_time():
    assert extra_time_charge("haircut", 20, "junior", False) == 0


def test_member_haircut_within_included_time():
    assert extra_time_charge("haircut", 40, "junior", True) == 0


def test_member_colour_extra_time():
    assert extra_time_charge("colour", 80, "junior", True) == 50


def test_non_member_senior_extra_time():
    assert extra_time_charge("haircut", 40, "senior", False) == 180


def test_junior_rate_above_60_extra_minutes():
    assert extra_time_charge("spa", 160, "junior", False) == 1260


def test_senior_rate_above_60_extra_minutes():
    assert extra_time_charge("spa", 160, "senior", False) == 2100


def test_spa_member_does_not_get_extra_included_time():
    assert extra_time_charge("spa", 100, "junior", True) == 100


def test_unknown_service_raises_error():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("massage", 30, "junior", False)


# Tests for can_book()

def test_regular_booking_allowed():
    assert can_book(2, 1, False) is True


def test_walk_in_with_two_people_allowed():
    assert can_book(2, 1, True) is True


def test_walk_in_with_more_than_two_people_rejected():
    assert can_book(3, 1, True) is False


def test_regular_booking_with_more_than_four_people_rejected():
    assert can_book(5, 1, False) is False


def test_regular_booking_with_more_than_two_services_rejected():
    assert can_book(4, 3, False) is False


def test_regular_booking_with_four_people_and_two_services():
    assert can_book(4, 2, False) is True


# Tests for arrival_status()

def test_arrival_open_on_weekday():
    assert arrival_status(5, False, False) == "open"


def test_arrival_late_on_weekday():
    assert arrival_status(0, False, False) == "late"


def test_arrival_closed_on_weekday():
    assert arrival_status(-11, False, False) == "closed"


def test_colour_customer_open_on_weekday():
    assert arrival_status(10, True, False) == "open"


def test_colour_customer_late_on_weekday():
    assert arrival_status(0, True, False) == "late"


def test_weekend_customer_open():
    assert arrival_status(15, False, True) == "open"


def test_weekend_colour_customer_late():
    assert arrival_status(10, True, True) == "late"


def test_weekend_colour_customer_closed():
    assert arrival_status(4, True, True) == "closed"

def test_negative_duration_current_behavior():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -5, "junior", False)