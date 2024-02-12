import pytest
from incollege import InCollegeApp

@pytest.fixture
def app():
    return InCollegeApp()

def test_successful_account_creation(app):
    result = app.create_account("user1", "ValidPass123!")
    assert result == "Account created successfully", "Account should be created successfully with valid credentials"

def test_account_creation_with_invalid_password(app):
    result = app.create_account("user2", "pass")
    assert "Password must" in result, "Account should not be created with an invalid password"

def test_account_creation_with_invalid_password_CAPITAL(app):
    result = app.create_account("user2", "pass1234!")
    assert "Password must" in result, "Account should not be created with an invalid password"

def test_account_creation_with_invalid_password_digit(app):
    result = app.create_account("user2", "passWord!")
    assert "Password must" in result, "Account should not be created with an invalid password"

def test_account_creation_with_invalid_password_special(app):
    result = app.create_account("user2", "passW0rds")
    assert "Password must" in result, "Account should not be created with an invalid password"

def test_account_creation_limit(app):
    for i in range(1, 6):
        app.create_account(f"user{i}", "ValidPass123!")

    result = app.create_account("user6", "ValidPass123!")
    assert result == "Maximum number of student accounts created.", "Should not allow creating more than 5 accounts"

def test_successful_login(app):
    app.create_account("user1", "ValidPass123!")
    result = app.login("user1", "ValidPass123!")
    assert result == "You have successfully logged in", "Login should be successful with correct credentials"

def test_failed_login(app):
    result = app.login("nonexistent_user", "wrongpassword")
    assert result == "Incorrect username / password, please try again.", "Login should fail with incorrect credentials"

def test_post_login_options(app):
    result = app.get_post_login_options()
    assert result == "1. Job search/Internship\n2. Find someone you know\n3. Learn a new skill", "Post-login options should be correctly listed"

@pytest.mark.parametrize("option_number, expected_result", [
    ("1", "Under construction."),
    ("2", "Under construction."),
    ("3", "1. Programming\n2. Data Analysis\n3. Graphic Design\n4. Digital Marketing\n5. Project Management\n6. return to previous level\nSelect a skill to learn."),
    ("4", "Invalid Option"),
    ("5", "Invalid Option")  # Test an invalid option
])

def test_select_option(app, option_number, expected_result):
    result = app.select_option(option_number)
    assert result == expected_result, f"Response for option number '{option_number}' should be correct"

def test_select_skill(app):
    result = app.select_skill("1")
    assert result == "Under construction.", "Selecting a skill should be under construction"

    result = app.select_skill("6")
    assert result == "1. Job search/Internship\n2. Find someone you know\n3. Learn a new skill", "Selecting the last skill should return to previous level"

    result = app.select_skill("7")
    assert result == "Invalid Option", "Selecting an invalid skill should return an invalid option message"