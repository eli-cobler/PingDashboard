import sqlalchemy as sa
from ping_dashboard.data.modelbase import SqlAlchemyBase

class Location(SqlAlchemyBase):
    __tablename__ = 'locations'

    id = sa.Column(sa.String, primary_key=True, index=True)
    anonymized_name = sa.Column(sa.String, index=True)
    response_time = sa.Column(sa.String, index=True)
    ping = sa.Column(sa.Integer, index=True)
    status = sa.Column(sa.String, index=True)
    url = sa.Column(sa.String, index=True)
    status_color = sa.Column(sa.String, index=True)
    type = sa.Column(sa.String, index=True)

    def __repr__(self):
        return f'<Server {self.id}>'