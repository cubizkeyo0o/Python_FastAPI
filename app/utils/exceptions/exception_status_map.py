from app.utils.exceptions.common_exceptions import *

exception_status_map = {
    # Authentication

    # Not found
    EntityNotFoundException: 404,

    # Not match
    NotMatchException: 400,

    # Conflict
    ConflictException: 409,

    # Bad request
    BusinessRuleViolationException: 400,

    # Other
}