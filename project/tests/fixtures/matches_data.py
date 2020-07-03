import pytest

from project import db
from project.models.match import MatchModel


@pytest.fixture
def matches_data():
    """Sample matches data."""
    db.session.add_all([MatchModel(squad_id=1,match_date='2019-08-10', round_name='Week 1',
    first_squad_name='Liverpool', first_squad_score=0,
    first_squad_points=0,second_squad_name='Manchester City',second_squad_score=5,
    second_squad_points=3),
    MatchModel(squad_id=2,match_date='2019-08-10', round_name='Week 2',
    first_squad_name='Manchester City', first_squad_score=0,
    first_squad_points=0,second_squad_name='Liverpool',second_squad_score=5,
    second_squad_points=2),
    MatchModel(squad_id=3,match_date='2019-08-10', round_name='Week 2',
    first_squad_name='Manchester City', first_squad_score=0,
    first_squad_points=0,second_squad_name='Burnley',second_squad_score=5,
    second_squad_points=2)])
    db.session.commit()