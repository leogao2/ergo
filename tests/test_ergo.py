import ergo
import pytest  # type: ignore
import requests

test_uname = "oughttest"
test_pwd = "6vCo39Mz^rrb"
test_user_id = 112420

mock_sample = [1, 2, 3]


def test_version():
    assert ergo.__version__ == '0.3.0'


class TestMetaculus:
    metaculus = ergo.Metaculus(test_uname, test_pwd)
    euro_question = metaculus.get_question(3706)
    uk_question = metaculus.get_question(3761)
    trump_question = metaculus.get_question(1100)

    def test_login(self):
        assert self.metaculus.user_id == test_user_id

    def test_get_question(self):
        # make sure we're getting the user-specific data
        assert "my_predictions" in self.euro_question.data

    def test_submission(self):
        euro_response = self.euro_question.submit(
            0.534894790856232, 0.02)
        assert euro_response.status_code == 202

    def test_submission_for_closed_question_fails(self):
        with pytest.raises(requests.exceptions.HTTPError):
            uk_response = self.uk_question.submit(
                0.534894790856232, 0.02)

    def test_show_submission(self):
        self.euro_question.show_submission(mock_sample)

    def test_score_binary(self):
        # smoke test
        self.trump_question.get_scored_predictions()

    def test_score_continuous(self):
        # smoke test
        self.euro_question.get_scored_predictions()

    def test_show_prediction_results(self):
        # smoke test
        self.metaculus.get_prediction_results()


class TestData:
    def test_confirmed_infections(self):
        confirmed = ergo.data.covid19.ConfirmedInfections()
        assert confirmed.get("Iran", "3/25/20") == 27017
