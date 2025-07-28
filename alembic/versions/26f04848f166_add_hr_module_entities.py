"""Add HR module entities

Revision ID: 26f04848f166
Revises: 3b35e08c8668
Create Date: 2025-07-28 18:25:34.171389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26f04848f166'
down_revision: Union[str, None] = '3b35e08c8668'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS hr")
    
    op.create_table('employees',
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('position', sa.String(length=100), nullable=False),
        sa.Column('hire_date', sa.Date(), nullable=False),
        sa.Column('termination_date', sa.Date(), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
        schema='hr'
    )
    op.create_index(op.f('ix_hr_employees_email'), 'employees', ['email'], unique=True, schema='hr')

    op.create_table('attendances',
        sa.Column('employee_id', sa.UUID(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['hr.employees.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='hr'
    )
    op.create_index(op.f('ix_hr_attendances_employee_id'), 'attendances', ['employee_id'], unique=False, schema='hr')

    op.create_table('payrolls',
        sa.Column('employee_id', sa.UUID(), nullable=False),
        sa.Column('pay_period_start', sa.Date(), nullable=False),
        sa.Column('pay_period_end', sa.Date(), nullable=False),
        sa.Column('payment_date', sa.Date(), nullable=True),
        sa.Column('total_hours', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('gross_pay', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('deductions', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('net_pay', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['hr.employees.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='hr'
    )
    op.create_index(op.f('ix_hr_payrolls_employee_id'), 'payrolls', ['employee_id'], unique=False, schema='hr')

    op.create_table('salary_rates',
        sa.Column('employee_id', sa.UUID(), nullable=False),
        sa.Column('hourly_rate', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('effective_date', sa.Date(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['hr.employees.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='hr'
    )
    op.create_index(op.f('ix_hr_salary_rates_employee_id'), 'salary_rates', ['employee_id'], unique=False, schema='hr')

    op.create_table('time_logs',
        sa.Column('employee_id', sa.UUID(), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['hr.employees.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='hr'
    )
    op.create_index(op.f('ix_hr_time_logs_employee_id'), 'time_logs', ['employee_id'], unique=False, schema='hr')



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_hr_time_logs_employee_id'), table_name='time_logs', schema='hr')
    op.drop_table('time_logs', schema='hr')

    op.drop_index(op.f('ix_hr_salary_rates_employee_id'), table_name='salary_rates', schema='hr')
    op.drop_table('salary_rates', schema='hr')

    op.drop_index(op.f('ix_hr_payrolls_employee_id'), table_name='payrolls', schema='hr')
    op.drop_table('payrolls', schema='hr')

    op.drop_index(op.f('ix_hr_attendances_employee_id'), table_name='attendances', schema='hr')
    op.drop_table('attendances', schema='hr')

    op.drop_index(op.f('ix_hr_employees_email'), table_name='employees', schema='hr')
    op.drop_table('employees', schema='hr')
