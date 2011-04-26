"""
pgxn.client -- package exceptions

These exceptions can be used to signal expected problems and to exit in a
controlled way from the program.

"""

# Copyright (C) 2011 Daniele Varrazzo

# This file is part of the PGXN client

class PgxnException(Exception):
    """Base class for the exceptions known in the pgxn package."""

class PgxnClientException(PgxnException):
    """Base class for the exceptions raised by the pgxn.client package."""

class BadSpecError(PgxnClientException):
    """A bad package specification."""

class NetworkError(PgxnClientException):
    """An error from the other side of the wire."""

class ResourceNotFound(NetworkError):
    """Resource not found on the server."""

class BadRequestError(Exception):
    """Bad request from our side.

    This exception is a basic one because it should be rased upon an error
    on our side.
    """