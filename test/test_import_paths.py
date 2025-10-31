#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Test that both import paths work: lybic.dto.xxxx and lybic.action.xxxx"""

# Test importing from lybic.dto (backward compatibility)
from lybic.dto import (
    MouseClickAction as MouseClickActionFromDto,
    PixelLength as PixelLengthFromDto,
)

# Test importing from lybic.action (new path)
from lybic.action import (
    MouseClickAction as MouseClickActionFromAction,
    PixelLength as PixelLengthFromAction,
)


def test_both_import_paths():
    """Test that both import paths provide the same classes."""
    # Verify that both imports point to the same class
    assert MouseClickActionFromDto is MouseClickActionFromAction, \
        "MouseClickAction should be the same class from both imports"
    assert PixelLengthFromDto is PixelLengthFromAction, \
        "PixelLength should be the same class from both imports"

    print("✓ Both import paths (lybic.dto and lybic.action) provide the same classes")


def test_create_action_from_dto_import():
    """Test creating an action using the dto import path."""
    action = MouseClickActionFromDto(
        type='mouse:click',
        x=PixelLengthFromDto(type='px', value=100),
        y=PixelLengthFromDto(type='px', value=200),
        button=1
    )
    assert action.type == 'mouse:click'
    assert action.x.value == 100
    print("✓ Can create actions using lybic.dto import path")


def test_create_action_from_action_import():
    """Test creating an action using the new action import path."""
    action = MouseClickActionFromAction(
        type='mouse:click',
        x=PixelLengthFromAction(type='px', value=100),
        y=PixelLengthFromAction(type='px', value=200),
        button=1
    )
    assert action.type == 'mouse:click'
    assert action.x.value == 100
    print("✓ Can create actions using lybic.action import path")


def test_all_import_paths():
    """Run all import path tests."""
    print("\nTesting both import paths (lybic.dto and lybic.action)...")
    test_both_import_paths()
    test_create_action_from_dto_import()
    test_create_action_from_action_import()
    print("\n✓ All import path tests passed!\n")


if __name__ == "__main__":
    test_all_import_paths()
