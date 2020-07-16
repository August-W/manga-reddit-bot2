import pytest
from unittest.mock import MagicMock
from app import config_service, data_access_service, data_transform_util
import importlib
import os
from praw import Reddit


def test_fetch_new_subscriber_messages():
    