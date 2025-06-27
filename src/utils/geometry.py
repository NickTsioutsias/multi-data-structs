# src/utils/geometry.py
"""Βασικές γεωμετρικές κλάσεις για το project"""

import math
from typing import List, Tuple, Optional


class Point2D:
    """Σημείο στο 2D επίπεδο"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return False
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        """Για sorting: πρώτα κατά x, μετά κατά y"""
        if self.x != other.x:
            return self.x < other.x
        return self.y < other.y
    
    def distance_to(self, other: 'Point2D') -> float:
        """Ευκλείδεια απόσταση από άλλο σημείο"""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def to_tuple(self) -> Tuple[float, float]:
        """Μετατροπή σε tuple για plotting"""
        return (self.x, self.y)


class Point3D:
    """Σημείο στο 3D χώρο (για R-trees αργότερα)"""
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"Point3D({self.x}, {self.y}, {self.z})"
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)


class Line:
    """Ευθεία γραμμή που ορίζεται από δύο σημεία"""
    
    def __init__(self, p1: Point2D, p2: Point2D):
        self.p1 = p1
        self.p2 = p2
    
    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"


class Segment:
    """Ευθύγραμμο τμήμα με αρχή και τέλος"""
    
    def __init__(self, start: Point2D, end: Point2D):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"Segment({self.start}, {self.end})"
    
    def length(self) -> float:
        """Μήκος του segment"""
        return self.start.distance_to(self.end)


def orientation(p: Point2D, q: Point2D, r: Point2D) -> int:
    """
    Βρίσκει τον προσανατολισμό του ordered triplet (p, q, r).
    
    Returns:
        0: Collinear (συνευθειακά)
        1: Clockwise (δεξιόστροφα)
        2: Counterclockwise (αριστερόστροφα)
    """
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise ή Counterclockwise


def ccw(p1: Point2D, p2: Point2D, p3: Point2D) -> bool:
    """
    Ελέγχει αν τα τρία σημεία είναι σε counter-clockwise σειρά.
    Χρήσιμο για convex hull.
    """
    return orientation(p1, p2, p3) == 2


def polar_angle(origin: Point2D, point: Point2D) -> float:
    """
    Υπολογίζει την πολική γωνία του point σε σχέση με το origin.
    Χρήσιμο για το Graham Scan.
    """
    dx = point.x - origin.x
    dy = point.y - origin.y
    return math.atan2(dy, dx)