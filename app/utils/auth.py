from fastapi import HTTPException, status

def is_admin_or_manager(user):
    """
    Checks if the user has a role of 'admin' or 'manager'.
    Raises an HTTPException if the user does not have the required role.

    :param user: An instance of User with a 'role' attribute.
    :raises HTTPException: If the user is neither an admin nor a manager.
    """
    if user.role not in ['admin', 'manager']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have the required permissions."
        )
    return True