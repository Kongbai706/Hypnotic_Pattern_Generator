"""Smoke test for hypnotic_patterns
- Imports SymmetryEngine
- Tests rotational, reflection, and spiral transformations
- Verifies basic geometry operations
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

import pygame
import numpy as np
from main import SymmetryEngine, CENTER


def test_symmetry_engine():
    engine = SymmetryEngine(900, 900, symmetry_order=6)
    
    # Test rotational symmetry
    points_rot = engine.transform_rotational(450, 350, 6)
    assert len(points_rot) > 0, "Rotational symmetry produced no points"
    assert all(isinstance(p, tuple) and len(p) == 2 for p in points_rot), "Invalid point format"
    
    # Test reflection symmetry
    points_ref = engine.transform_reflection(450, 350, 4)
    assert len(points_ref) > 0, "Reflection symmetry produced no points"
    
    # Test spiral transformation
    points_spiral = engine.transform_spiral(450, 350, 0.05)
    assert len(points_spiral) > 0, "Spiral symmetry produced no points"
    
    # Test symmetry points getter
    pts = engine.get_symmetry_points(450, 350, 'rotational', 6)
    assert len(pts) == 6, f"Expected 6 rotational points, got {len(pts)}"
    
    # Test canvas
    assert isinstance(engine.canvas, pygame.Surface), "Canvas is not a Pygame Surface"
    assert engine.canvas.get_size() == (900, 900), "Canvas size incorrect"
    
    # Test gesture history
    engine.add_gesture_point(450, 350, 5.0)
    assert len(engine.gesture_history) == 1, "Gesture history not updated"
    
    # Test clear
    engine.clear()
    assert len(engine.gesture_history) == 0, "Clear did not reset gesture history"
    
    print("SMOKE TEST PASSED")


if __name__ == '__main__':
    test_symmetry_engine()
