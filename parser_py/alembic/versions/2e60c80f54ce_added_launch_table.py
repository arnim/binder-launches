"""Added launch table

Revision ID: 2e60c80f54ce
Revises:
Create Date: 2021-03-12 19:30:41.277172

"""
import sqlalchemy as sa
from alembic import op

from parser_py import chunk_time_interval
from parser_py import data_retention_interval


# revision identifiers, used by Alembic.
revision = "2e60c80f54ce"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "launches",
        # sa.Column('id', sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("spec", sa.String(), nullable=False),
        sa.Column("repo", sa.String(), nullable=False),
        sa.Column("ref", sa.String(), nullable=False),
        sa.Column("resolved_ref", sa.String(), nullable=False),
        sa.Column("origin", sa.String(), nullable=False),
        sa.Column("schema", sa.String(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        # sa.PrimaryKeyConstraint('id')
    )

    ###### TimeScale DB
    # https://docs.timescale.com/latest/getting-started/creating-hypertables
    # https://docs.timescale.com/latest/api#create_hypertable
    op.execute(
        f"SELECT create_hypertable('launches', 'timestamp', chunk_time_interval => INTERVAL '{chunk_time_interval}', create_default_indexes=>FALSE);"
    )
    # https://docs.timescale.com/latest/using-timescaledb/data-retention#retention-policy
    op.execute(
        f"SELECT add_retention_policy('launches', INTERVAL '{data_retention_interval}');"
    )
    ###### TimeScale DB

    op.create_index("launches_repo_idx", "launches", ["repo"], unique=False)
    op.create_index("launches_origin_idx", "launches", ["origin"], unique=False)
    op.create_index("launches_provider_idx", "launches", ["provider"], unique=False)
    op.create_index(
        "launches_provider_repo_idx", "launches", ["provider", "repo"], unique=False
    )
    op.create_index(
        "launches_timestamp_idx", "launches", [sa.text("timestamp DESC")], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("launches_timestamp_idx", table_name="launches")
    op.drop_index("launches_provider_repo_idx", table_name="launches")
    op.drop_index("launches_provider_idx", table_name="launches")
    op.drop_index("launches_origin_idx", table_name="launches")
    op.drop_index("launches_repo_idx", table_name="launches")
    op.drop_table("launches")
    # ### end Alembic commands ###