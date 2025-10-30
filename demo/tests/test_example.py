"""Test package example."""

import pytest
            
from demo.core.example import Example


def test_example(capsys):
    """Test that calling Example.example() prints 'Hello World'."""

    ex = Example()
    ex.example()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World"

