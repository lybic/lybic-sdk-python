#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Test that callId fields generate unique IDs for each instance."""

from lybic.dto import (
    MouseClickAction,
    KeyboardTypeAction,
    KeyboardHotkeyAction,
    ScreenshotAction,
    WaitAction,
    TouchTapAction,
    AndroidBackAction,
    AndroidHomeAction,
    ComputerUseActionDto,
    ExecuteSandboxActionDto,
    PixelLength,
)


def test_mouse_actions_unique_callids():
    """Test that mouse actions generate unique callIds."""
    action1 = MouseClickAction(
        type='mouse:click',
        x=PixelLength(type='px', value=100),
        y=PixelLength(type='px', value=200),
        button=1
    )

    action2 = MouseClickAction(
        type='mouse:click',
        x=PixelLength(type='px', value=300),
        y=PixelLength(type='px', value=400),
        button=1
    )

    assert action1.callId != action2.callId, "MouseClickAction instances should have unique callIds"
    print("✓ MouseClickAction: unique callIds")


def test_keyboard_actions_unique_callids():
    """Test that keyboard actions generate unique callIds."""
    action1 = KeyboardTypeAction(type='keyboard:type', content='Hello')
    action2 = KeyboardTypeAction(type='keyboard:type', content='World')

    assert action1.callId != action2.callId, "KeyboardTypeAction instances should have unique callIds"
    print("✓ KeyboardTypeAction: unique callIds")

    action3 = KeyboardHotkeyAction(type='keyboard:hotkey', keys='ctrl+c')
    action4 = KeyboardHotkeyAction(type='keyboard:hotkey', keys='ctrl+v')

    assert action3.callId != action4.callId, "KeyboardHotkeyAction instances should have unique callIds"
    print("✓ KeyboardHotkeyAction: unique callIds")


def test_common_actions_unique_callids():
    """Test that common actions generate unique callIds."""
    action1 = ScreenshotAction(type='screenshot')
    action2 = ScreenshotAction(type='screenshot')

    assert action1.callId != action2.callId, "ScreenshotAction instances should have unique callIds"
    print("✓ ScreenshotAction: unique callIds")

    action3 = WaitAction(type='wait', duration=1000)
    action4 = WaitAction(type='wait', duration=2000)

    assert action3.callId != action4.callId, "WaitAction instances should have unique callIds"
    print("✓ WaitAction: unique callIds")


def test_touch_actions_unique_callids():
    """Test that touch actions generate unique callIds."""
    action1 = TouchTapAction(
        type='touch:tap',
        x=PixelLength(type='px', value=100),
        y=PixelLength(type='px', value=200)
    )

    action2 = TouchTapAction(
        type='touch:tap',
        x=PixelLength(type='px', value=300),
        y=PixelLength(type='px', value=400)
    )

    assert action1.callId != action2.callId, "TouchTapAction instances should have unique callIds"
    print("✓ TouchTapAction: unique callIds")


def test_android_actions_unique_callids():
    """Test that Android actions generate unique callIds."""
    action1 = AndroidBackAction(type='android:back')
    action2 = AndroidBackAction(type='android:back')

    assert action1.callId != action2.callId, "AndroidBackAction instances should have unique callIds"
    print("✓ AndroidBackAction: unique callIds")

    action3 = AndroidHomeAction(type='android:home')
    action4 = AndroidHomeAction(type='android:home')

    assert action3.callId != action4.callId, "AndroidHomeAction instances should have unique callIds"
    print("✓ AndroidHomeAction: unique callIds")

def test_dto_wrappers_unique_callids():
    """Test that DTO wrappers generate unique callIds."""
    dto1 = ComputerUseActionDto(
        action=ScreenshotAction(type='screenshot')
    )

    dto2 = ComputerUseActionDto(
        action=ScreenshotAction(type='screenshot')
    )

    assert dto1.callId != dto2.callId, "ComputerUseActionDto instances should have unique callIds"
    print("✓ ComputerUseActionDto: unique callIds")

    dto3 = ExecuteSandboxActionDto(
        action=ScreenshotAction(type='screenshot')
    )

    dto4 = ExecuteSandboxActionDto(
        action=ScreenshotAction(type='screenshot')
    )

    assert dto3.callId != dto4.callId, "ExecuteSandboxActionDto instances should have unique callIds"
    print("✓ ExecuteSandboxActionDto: unique callIds")


def test_all_action_types():
    """Run all tests."""
    print("\nTesting unique callId generation across all action types...")
    test_mouse_actions_unique_callids()
    test_keyboard_actions_unique_callids()
    test_common_actions_unique_callids()
    test_touch_actions_unique_callids()
    test_android_actions_unique_callids()
    test_dto_wrappers_unique_callids()
    print("\n✓ All tests passed! Each action instance generates a unique callId.\n")


if __name__ == "__main__":
    test_all_action_types()
