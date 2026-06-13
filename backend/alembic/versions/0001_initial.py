"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-13
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(255), nullable=False), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("full_name", sa.String(120), nullable=False), sa.Column("role", sa.String(40), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("candidates", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(180)), sa.Column("email", sa.String(255)), sa.Column("phone", sa.String(50)), sa.Column("linkedin_url", sa.String(500)), sa.Column("github_url", sa.String(500)), sa.Column("skills", sa.JSON(), nullable=False), sa.Column("education", sa.JSON(), nullable=False), sa.Column("certifications", sa.JSON(), nullable=False), sa.Column("experience", sa.JSON(), nullable=False), sa.Column("projects", sa.JSON(), nullable=False), sa.Column("internships", sa.JSON(), nullable=False), sa.Column("experience_years", sa.Float(), nullable=False), sa.Column("status", sa.String(40), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_candidates_name", "candidates", ["name"])
    op.create_index("ix_candidates_email", "candidates", ["email"])
    op.create_table("skills", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False), sa.Column("category", sa.String(80)))
    op.create_index("ix_skills_name", "skills", ["name"], unique=True)
    op.create_table("job_descriptions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(180), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("required_skills", sa.JSON(), nullable=False), sa.Column("preferred_skills", sa.JSON(), nullable=False), sa.Column("experience_requirements", sa.JSON(), nullable=False), sa.Column("created_by_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("resumes", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False), sa.Column("file_name", sa.String(255), nullable=False), sa.Column("file_path", sa.String(1000), nullable=False), sa.Column("content_type", sa.String(120), nullable=False), sa.Column("raw_text", sa.Text(), nullable=False), sa.Column("parsed_json", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("rankings", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False), sa.Column("job_description_id", sa.Integer(), sa.ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False), sa.Column("match_score", sa.Float(), nullable=False), sa.Column("weighted_score", sa.Float(), nullable=False), sa.Column("suspicion_score", sa.Integer(), nullable=False), sa.Column("hiring_recommendation", sa.String(80), nullable=False), sa.Column("confidence_score", sa.Integer(), nullable=False), sa.Column("details", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("interview_questions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False), sa.Column("job_description_id", sa.Integer(), sa.ForeignKey("job_descriptions.id")), sa.Column("questions", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("reports", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(180), nullable=False), sa.Column("report_type", sa.String(60), nullable=False), sa.Column("payload", sa.JSON(), nullable=False), sa.Column("created_by_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("created_at", sa.DateTime(), nullable=False))


def downgrade() -> None:
    op.drop_table("reports")
    op.drop_table("interview_questions")
    op.drop_table("rankings")
    op.drop_table("resumes")
    op.drop_table("job_descriptions")
    op.drop_index("ix_skills_name", table_name="skills")
    op.drop_table("skills")
    op.drop_index("ix_candidates_email", table_name="candidates")
    op.drop_index("ix_candidates_name", table_name="candidates")
    op.drop_table("candidates")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
