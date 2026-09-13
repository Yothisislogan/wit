"""Shared selection rules for the existing course and state-law content."""

from sqlalchemy import and_, or_

from .models import Module, User


def module_scope(user: User, course: str | None = None):
    """Include the selected track's general content and selected state only.

    State seed scripts use state-law-{state}-{course} slugs. Keep this rule in
    one place until content has explicit jurisdiction metadata.
    """
    selected_course = course or user.course or "pc"
    jurisdiction = ~Module.slug.like("state-law-%")
    if user.state:
        jurisdiction = or_(
            jurisdiction,
            Module.slug == f"state-law-{user.state.lower()}-{selected_course}",
        )
    return and_(
        Module.is_active.is_(True),
        Module.course == selected_course,
        jurisdiction,
    )
