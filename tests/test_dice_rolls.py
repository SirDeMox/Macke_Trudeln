import pytest
from dice_rolls import DiceRolls

def test_init_parsing():
    rolls = DiceRolls(5)
    assert sum(list(rolls.roll_results.values()))==0
    assert rolls.toak is None
    assert rolls.macke is None
    assert rolls.count_rolled_dice == 5
    assert rolls.dice_remaining is None
    assert rolls.score is None
    assert rolls.previous_score is None

def test_n_dice_are_rolled():
    rolls = DiceRolls(5)
    rolls.roll_dice()
    assert sum(rolls.roll_results.values()) == 5

def test_set_fixed_rolls_insertion():
    _fixed_rolls = [1, 0, 0, 3, 1, 0]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.set_fixed_rolls()
    assert list(frolls.roll_results.values()) == _fixed_rolls

def test_evaluate_macke_on_macke():
    _macke_rolls = [0, 2, 1, 1, 0, 1]
    mrolls = DiceRolls(fixed_rolls=_macke_rolls)
    mrolls.set_fixed_rolls()
    mrolls.evaluate_macke()
    assert mrolls.macke is True

def test_evaluate_macke_on_non_macke():
    _non_macke_rolls = [0, 2, 1, 0, 1, 1]
    nmrolls = DiceRolls(fixed_rolls=_non_macke_rolls)
    nmrolls.set_fixed_rolls()
    nmrolls.evaluate_macke()
    assert nmrolls.macke is False

def test_roll_results_toak_cleanup():
    _fixed_rolls = [1, 0, 0, 3, 1, 0]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.set_fixed_rolls()
    frolls.roll_results_toak_cleanup()
    assert sum(frolls.roll_results.values())==2

def test_count_dice_remaining_0():
    _fixed_rolls = [1, 0, 0, 3, 1, 0]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.set_fixed_rolls()
    frolls.roll_results_toak_cleanup()
    frolls.count_dice_remaining()
    assert frolls.dice_remaining == 0

def test_count_dice_remaining_for_bigger_0():
    _fixed_rolls = [1, 0, 1, 2, 1, 0]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.set_fixed_rolls()
    frolls.roll_results_toak_cleanup()
    frolls.count_dice_remaining()
    assert frolls.dice_remaining == 3

def test_evaluate_points_toak():
    _fixed_rolls = [1, 0, 0, 3, 1, 0]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.set_fixed_rolls()
    frolls.roll_results_toak_cleanup()
    frolls.count_dice_remaining()
    frolls.evaluate_points()
    assert frolls.toak == 4
    assert frolls.score == 550


def test_evaluate_points_1toak():
    _fixed_rolls = [4, 0, 0, 0, 1, 0]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.set_fixed_rolls()
    frolls.roll_results_toak_cleanup()
    frolls.count_dice_remaining()
    frolls.evaluate_points()
    assert frolls.toak == 1
    assert frolls.score == 1150

def test_evaluate_points_no_toak():
    _fixed_rolls = [1, 1, 1, 1, 1, 0]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.set_fixed_rolls()
    frolls.roll_results_toak_cleanup()
    frolls.count_dice_remaining()
    frolls.evaluate_points()
    assert frolls.score == 150

def test_evaluate_points_macke():
    _fixed_rolls = [0, 2, 1, 1, 0, 1]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.set_fixed_rolls()
    frolls.evaluate_macke()
    frolls.roll_results_toak_cleanup()
    frolls.count_dice_remaining()
    frolls.evaluate_points()

    assert frolls.macke is True
    assert frolls.score == 0

def test_run_on_toak_1_remaining():
    _fixed_rolls = [1, 0, 0, 3, 0, 1]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.run()
    assert frolls.count_rolled_dice == 5
    assert frolls.score == 500
    assert frolls.dice_remaining == 1
    assert frolls.macke is False

def test_run_on_4_dice_2_remaining():
    _fixed_rolls = [1, 0, 0, 1, 1, 1]
    frolls = DiceRolls(fixed_rolls=_fixed_rolls)
    frolls.run()
    assert frolls.count_rolled_dice == 4
    assert frolls.score == 150
    assert frolls.dice_remaining == 2
    assert frolls.macke is False
