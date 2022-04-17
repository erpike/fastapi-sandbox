from fastapi import Path, Query

notations = {
    'note_id': Path(
        default=None,
        description="`id` parameter for targeting note.",
        gt=0,
    ),
    'limit': Query(
        None,
        description="SQL query `limit` param.",
        gt=0,
    ),
    'offset': Query(
        None,
        description="SQL query `offset` param.",
        gt=0,
    ),
    'username': Path(
        default=None,
        description="Unique `username` parameter for new user.",
        max_length=255,
    ),
    'user_id': Query(
        None,
        description="Select all notes by selected `user_id` (optional) param.",
        gt=0,
    ),
}
