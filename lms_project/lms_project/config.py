"""
Environment Utility Module

This module provides helper functions to load and retrieve environment variables.

Functions:
- get_env: Fetch an environment variable with optional default value and type casting.

Usage:
    load_dotenv() should be called to load variables from a .env file.
    Use get_env(key, default, cast) to safely retrieve and cast environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_env(key, default=None, cast=str):
    """
    Retrieve an environment variable and optionally cast it to a specific type.

    **Args:**
        - key (str): The name of the environment variable to fetch.
        - default (Any, optional): The default value to return if the variable is not found. Defaults to None.
        - cast (Callable, optional): A function to cast the value to a desired type. Defaults to str.

    **Returns:**
        - Any: The environment variable value cast to the specified type, or the default value if not found or casting fails.

    **Example:**
        - DEBUG = get_env("DEBUG", default=False, cast=bool)
    """
    value = os.getenv(key, default)

    if value is None:
        return value

    try:
        return cast(value)
    except Exception:
        return default
