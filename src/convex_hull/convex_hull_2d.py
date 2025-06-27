# src/convex_hull/convex_hull_2d.py
"""
2D Convex Hull implementation using Graham Scan algorithm.

Ο αλγόριθμος Graham Scan βρίσκει το convex hull ενός συνόλου σημείων
σε O(n log n) χρόνο.
"""

from typing import List, Optional
import sys
import os

# Προσθήκη του src directory στο path για imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.geometry import Point2D, ccw, polar_angle
from src.utils.performance import measure_time


class ConvexHull2D:
    """Κλάση για υπολογισμό 2D Convex Hull"""
    
    def __init__(self, points: List[Point2D]):
        """
        Initialize με λίστα από 2D σημεία.
        
        Args:
            points: Λίστα από Point2D objects
        """
        if len(points) < 3:
            raise ValueError("Χρειάζονται τουλάχιστον 3 σημεία για convex hull")
        
        self.points = points
        self.hull = []
    
    def graham_scan(self) -> List[Point2D]:
        """
        Υλοποίηση του Graham Scan algorithm.
        
        Returns:
            Λίστα με τα σημεία του convex hull σε counter-clockwise σειρά
        """
        # Βήμα 1: Βρες το κατώτατο σημείο (με το μικρότερο y, και σε περίπτωση ισοπαλίας το μικρότερο x)
        start = min(self.points, key=lambda p: (p.y, p.x))
        
        # Βήμα 2: Ταξινόμησε τα υπόλοιπα σημεία κατά πολική γωνία ως προς το start
        other_points = [p for p in self.points if p != start]
        
        # Ταξινόμηση κατά πολική γωνία, και κατά απόσταση σε περίπτωση ίδιας γωνίας
        sorted_points = sorted(other_points, 
                             key=lambda p: (polar_angle(start, p), 
                                          start.distance_to(p)))
        
        # Βήμα 3: Αφαίρεσε σημεία με την ίδια γωνία (κράτα μόνο το πιο μακρινό)
        filtered_points = self._remove_same_angle_points(start, sorted_points)
        
        # Αν έχουμε λιγότερα από 2 σημεία μετά το filtering, επέστρεψε απλό hull
        if len(filtered_points) < 2:
            return [start] + filtered_points
        
        # Βήμα 4: Graham scan
        hull = [start, filtered_points[0], filtered_points[1]]
        
        for i in range(2, len(filtered_points)):
            # Αφαίρεσε σημεία που δημιουργούν δεξιά στροφή
            while len(hull) > 1 and not ccw(hull[-2], hull[-1], filtered_points[i]):
                hull.pop()
            hull.append(filtered_points[i])
        
        self.hull = hull
        return hull
    
    def _remove_same_angle_points(self, origin: Point2D, points: List[Point2D]) -> List[Point2D]:
        """
        Αφαιρεί σημεία με την ίδια πολική γωνία, κρατώντας μόνο το πιο μακρινό.
        """
        if not points:
            return []
        
        filtered = [points[0]]
        
        for i in range(1, len(points)):
            angle_prev = polar_angle(origin, filtered[-1])
            angle_curr = polar_angle(origin, points[i])
            
            if abs(angle_prev - angle_curr) < 1e-9:  # Ίδια γωνία
                # Κράτα το πιο μακρινό
                if origin.distance_to(points[i]) > origin.distance_to(filtered[-1]):
                    filtered[-1] = points[i]
            else:
                filtered.append(points[i])
        
        return filtered
    
    @measure_time
    def compute_hull(self) -> List[Point2D]:
        """Wrapper method με time measurement"""
        return self.graham_scan()
    
    def get_hull_vertices(self) -> List[Point2D]:
        """Επιστρέφει τα vertices του hull"""
        return self.hull
    
    def get_hull_area(self) -> float:
        """
        Υπολογίζει το εμβαδόν του convex hull χρησιμοποιώντας τον τύπο Shoelace.
        """
        if len(self.hull) < 3:
            return 0.0
        
        area = 0.0
        n = len(self.hull)
        
        for i in range(n):
            j = (i + 1) % n
            area += self.hull[i].x * self.hull[j].y
            area -= self.hull[j].x * self.hull[i].y
        
        return abs(area) / 2.0
    
    def get_hull_perimeter(self) -> float:
        """Υπολογίζει την περίμετρο του convex hull"""
        if len(self.hull) < 2:
            return 0.0
        
        perimeter = 0.0
        n = len(self.hull)
        
        for i in range(n):
            j = (i + 1) % n
            perimeter += self.hull[i].distance_to(self.hull[j])
        
        return perimeter


def quick_hull(points: List[Point2D]) -> List[Point2D]:
    """
    Alternative: QuickHull algorithm implementation.
    Θα το υλοποιήσουμε αργότερα για σύγκριση performance.
    """
    # TODO: Implement QuickHull
    pass


# Utility function για εύκολη χρήση
def compute_convex_hull(points: List[Point2D], algorithm: str = "graham") -> List[Point2D]:
    """
    Υπολογίζει το convex hull με τον επιλεγμένο αλγόριθμο.
    
    Args:
        points: Λίστα από Point2D
        algorithm: "graham" ή "quick" (μόνο graham υλοποιημένο προς το παρόν)
    
    Returns:
        Λίστα με τα σημεία του convex hull
    """
    if algorithm == "graham":
        ch = ConvexHull2D(points)
        return ch.compute_hull()
    elif algorithm == "quick":
        return quick_hull(points)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")