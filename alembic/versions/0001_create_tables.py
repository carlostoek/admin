from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('telegram_id', sa.Integer, unique=True, nullable=False),
        sa.Column('is_vip', sa.Boolean, default=False),
        sa.Column('vip_expiry', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_table(
        'tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('token', sa.String, unique=True, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
        sa.Column('is_used', sa.Boolean, default=False),
        sa.Column('expires_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('tokens')
    op.drop_table('users')