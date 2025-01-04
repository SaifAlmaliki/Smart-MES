"""initila migration

Revision ID: 08e15ed6c6b8
Revises: 
Create Date: 2025-01-03 13:20:03.411498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08e15ed6c6b8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('count_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_path', sa.String(length=255), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tag_path')
    )
    op.create_index(op.f('ix_count_tag_id'), 'count_tag', ['id'], unique=False)
    op.create_table('count_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('count_type', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('count_type')
    )
    op.create_index(op.f('ix_count_type_id'), 'count_type', ['id'], unique=False)
    op.create_table('enterprise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_enterprise_id'), 'enterprise', ['id'], unique=False)
    op.create_table('product_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_code', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_code')
    )
    op.create_index(op.f('ix_product_code_id'), 'product_code', ['id'], unique=False)
    op.create_table('state_reason',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reason_name', sa.String(length=255), nullable=False),
    sa.Column('reason_code', sa.String(length=50), nullable=False),
    sa.Column('record_downtime', sa.Boolean(), nullable=True),
    sa.Column('planned_downtime', sa.Boolean(), nullable=True),
    sa.Column('operator_selectable', sa.Boolean(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['state_reason.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('reason_code')
    )
    op.create_index(op.f('ix_state_reason_id'), 'state_reason', ['id'], unique=False)
    op.create_table('site',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('enterprise_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['enterprise_id'], ['enterprise.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_site_id'), 'site', ['id'], unique=False)
    op.create_table('work_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('work_order_number', sa.String(length=50), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('closed', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('product_code_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_code_id'], ['product_code.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('work_order_number')
    )
    op.create_index(op.f('ix_work_order_id'), 'work_order', ['id'], unique=False)
    op.create_table('area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['site_id'], ['site.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_area_id'), 'area', ['id'], unique=False)
    op.create_table('line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('area_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['area.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_line_id'), 'line', ['id'], unique=False)
    op.create_table('cell',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('line_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['line_id'], ['line.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cell_id'), 'cell', ['id'], unique=False)
    op.create_table('product_code_line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_code_id', sa.Integer(), nullable=False),
    sa.Column('line_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['line_id'], ['line.id'], ),
    sa.ForeignKeyConstraint(['product_code_id'], ['product_code.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_code_line_id'), 'product_code_line', ['id'], unique=False)
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('schedule_type', sa.String(length=50), nullable=True),
    sa.Column('note', sa.String(length=255), nullable=True),
    sa.Column('schedule_start_datetime', sa.DateTime(), nullable=True),
    sa.Column('schedule_finish_datetime', sa.DateTime(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('line_id', sa.Integer(), nullable=False),
    sa.Column('work_order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['line_id'], ['line.id'], ),
    sa.ForeignKeyConstraint(['work_order_id'], ['work_order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedule_id'), 'schedule', ['id'], unique=False)
    op.create_table('run',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.Column('run_start_datetime', sa.DateTime(), nullable=True),
    sa.Column('run_stop_datetime', sa.DateTime(), nullable=True),
    sa.Column('closed', sa.Boolean(), nullable=True),
    sa.Column('estimated_finish_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_run_id'), 'run', ['id'], unique=False)
    op.create_table('count_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('count_type_id', sa.Integer(), nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['count_type_id'], ['count_type.id'], ),
    sa.ForeignKeyConstraint(['run_id'], ['run.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['count_tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_count_history_id'), 'count_history', ['id'], unique=False)
    op.create_table('run_metrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=False),
    sa.Column('good_count', sa.Integer(), nullable=True),
    sa.Column('waste_count', sa.Integer(), nullable=True),
    sa.Column('total_count', sa.Integer(), nullable=True),
    sa.Column('availability', sa.Float(), nullable=True),
    sa.Column('performance', sa.Float(), nullable=True),
    sa.Column('quality', sa.Float(), nullable=True),
    sa.Column('oee', sa.Float(), nullable=True),
    sa.Column('unplanned_downtime', sa.Float(), nullable=True),
    sa.Column('planned_downtime', sa.Float(), nullable=True),
    sa.Column('total_time', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['run_id'], ['run.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('run_id')
    )
    op.create_index(op.f('ix_run_metrics_id'), 'run_metrics', ['id'], unique=False)
    op.create_table('state_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=True),
    sa.Column('state_reason_id', sa.Integer(), nullable=False),
    sa.Column('reason_name', sa.String(length=255), nullable=False),
    sa.Column('reason_code', sa.String(length=50), nullable=False),
    sa.Column('line_id', sa.Integer(), nullable=True),
    sa.Column('run_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['line_id'], ['line.id'], ),
    sa.ForeignKeyConstraint(['run_id'], ['run.id'], ),
    sa.ForeignKeyConstraint(['state_reason_id'], ['state_reason.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_state_history_id'), 'state_history', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_state_history_id'), table_name='state_history')
    op.drop_table('state_history')
    op.drop_index(op.f('ix_run_metrics_id'), table_name='run_metrics')
    op.drop_table('run_metrics')
    op.drop_index(op.f('ix_count_history_id'), table_name='count_history')
    op.drop_table('count_history')
    op.drop_index(op.f('ix_run_id'), table_name='run')
    op.drop_table('run')
    op.drop_index(op.f('ix_schedule_id'), table_name='schedule')
    op.drop_table('schedule')
    op.drop_index(op.f('ix_product_code_line_id'), table_name='product_code_line')
    op.drop_table('product_code_line')
    op.drop_index(op.f('ix_cell_id'), table_name='cell')
    op.drop_table('cell')
    op.drop_index(op.f('ix_line_id'), table_name='line')
    op.drop_table('line')
    op.drop_index(op.f('ix_area_id'), table_name='area')
    op.drop_table('area')
    op.drop_index(op.f('ix_work_order_id'), table_name='work_order')
    op.drop_table('work_order')
    op.drop_index(op.f('ix_site_id'), table_name='site')
    op.drop_table('site')
    op.drop_index(op.f('ix_state_reason_id'), table_name='state_reason')
    op.drop_table('state_reason')
    op.drop_index(op.f('ix_product_code_id'), table_name='product_code')
    op.drop_table('product_code')
    op.drop_index(op.f('ix_enterprise_id'), table_name='enterprise')
    op.drop_table('enterprise')
    op.drop_index(op.f('ix_count_type_id'), table_name='count_type')
    op.drop_table('count_type')
    op.drop_index(op.f('ix_count_tag_id'), table_name='count_tag')
    op.drop_table('count_tag')
    # ### end Alembic commands ###
