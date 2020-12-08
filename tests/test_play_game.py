import pytest

from dice_rolls import DiceRolls
from play_game import PlayGame

def test_game_init_parsing():
    pg = PlayGame(method="earlystop", threshold=300)
    assert pg.method == "earlystop"
    assert pg.threshold == 300

def test_check_for_macke_on_no_macke():

    pg = PlayGame()
    _fixed_rolls = [1, 0, 0, 3, 1, 0]
    pg.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()
    pg.check_for_macke()
    assert pg.current_roll.macke is False
    assert pg.continued is True
    assert pg.total_score >= 0

def test_check_for_macke_on_no_macke():
    pg = PlayGame()
    _fixed_rolls = [0, 1, 2, 2, 0, 0]
    pg.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()
    pg.check_for_macke()
    assert pg.current_roll.macke is True
    assert pg.continued is False
    assert pg.total_score == 0

pg = PlayGame()

def test_account_for_new_score_on_no_macke():
    _fixed_rolls = [0, 1, 0, 3, 0, 1]
    pg.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()
    pg.account_for_new_score()

    assert pg.rolls == 1
    assert pg.total_score == 400
    assert pg.dice_remaining == 2

def test_new_score_addition_no_macke():
    _fixed_rolls = [1, 0, 0, 0, 1, 0]
    pg.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()
    pg.account_for_new_score()

    assert pg.rolls == 2
    assert pg.total_score == 550
    assert pg.dice_remaining == 5
    assert pg.resets == 1

def test_new_score_addition_with_macke():
    _fixed_rolls = [0, 1, 1, 1, 0, 2]
    pg.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()
    pg.check_for_macke()
    pg.account_for_new_score()

    assert pg.score_before_end == 550
    assert pg.rolls == 3
    assert pg.total_score == 0
    assert pg.dice_remaining == 5
    assert pg.resets == 1
    assert pg.continued is False



def test_earlystop_with_enough_points():
    early_stop_pg = PlayGame(method="earlystop", threshold=300)
    _fixed_rolls = [0, 1, 1, 3, 0, 0]
    early_stop_pg.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()
    early_stop_pg.check_for_macke()
    early_stop_pg.account_for_new_score()
    early_stop_pg.method_interpreter()

    assert early_stop_pg.total_score >= early_stop_pg.threshold
    assert early_stop_pg.continued is False


def test_earlystop_with_enough_points_but_forced_continue():
    early_stop_pg = PlayGame(method="earlystop", threshold=300)
    _fixed_rolls = [0, 0, 0, 3, 2, 0]
    early_stop_pg.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()
    early_stop_pg.check_for_macke()
    early_stop_pg.account_for_new_score()
    early_stop_pg.method_interpreter()

    assert early_stop_pg.total_score >= early_stop_pg.threshold
    assert early_stop_pg.continued is True

def test_nrolls_with_enough_rolls():
    nrolls_pg = PlayGame(method="nrolls", threshold=2)
    _fixed_rolls = [1, 2, 2, 1, 0, 0]
    nrolls_pg.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()
    nrolls_pg.check_for_macke()
    nrolls_pg.account_for_new_score()
    nrolls_pg.method_interpreter()
    _fixed_rolls = [1, 2, 2, 0, 0, 0]
    nrolls_pg.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()
    nrolls_pg.check_for_macke()
    nrolls_pg.account_for_new_score()
    nrolls_pg.method_interpreter()

    assert nrolls_pg.rolls == nrolls_pg.threshold
    assert nrolls_pg.continued is False

def test_run4s_on_4_remaining_dice():
    run4s_game = PlayGame(method="earlystop", threshold=300, special=["run4s"])
    _fixed_rolls = [1, 2, 2, 0, 0, 0] # 4 remaining dice
    run4s_game.total_score = 500 # score set to 500
    run4s_game.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()

    run4s_game.check_for_macke()
    run4s_game.account_for_new_score()
    run4s_game.method_interpreter()

    assert run4s_game.dice_remaining == 4
    assert run4s_game.total_score >= run4s_game.threshold
    assert run4s_game.continued == True


def test_not_run4s_on_4_remaining_dice():
    run4s_game = PlayGame(method="earlystop", threshold=300, special=[])
    _fixed_rolls = [1, 2, 2, 0, 0, 0]  # 4 remaining dice
    run4s_game.total_score = 500  # score set to 500
    run4s_game.current_roll = DiceRolls(fixed_rolls=_fixed_rolls).run()

    run4s_game.check_for_macke()
    run4s_game.account_for_new_score()
    run4s_game.method_interpreter()

    assert run4s_game.dice_remaining == 4
    assert run4s_game.total_score >= run4s_game.threshold
    assert run4s_game.continued == False

#todo test stopping reason