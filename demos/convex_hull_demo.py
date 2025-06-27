# demos/convex_hull_demo.py
"""
Demo script για Convex Hull algorithms.

Δείχνει πώς να χρησιμοποιήσετε τον Graham Scan και να visualize τα αποτελέσματα.
"""

import sys
import os
import random
import numpy as np
from typing import List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils.geometry import Point2D
from src.convex_hull.convex_hull_2d import ConvexHull2D, compute_convex_hull
from src.convex_hull.visualization import plot_convex_hull
from src.utils.performance import Timer


def generate_random_points(n: int, 
                         x_range: tuple = (0, 100), 
                         y_range: tuple = (0, 100),
                         seed: int = None) -> List[Point2D]:
    """Δημιουργεί n τυχαία σημεία"""
    if seed:
        random.seed(seed)
        np.random.seed(seed)
    
    points = []
    for _ in range(n):
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        points.append(Point2D(x, y))
    
    return points


def generate_circle_points(n: int, 
                         center: tuple = (50, 50), 
                         radius: float = 40,
                         noise: float = 0) -> List[Point2D]:
    """Δημιουργεί σημεία σε κύκλο (με προαιρετικό θόρυβο)"""
    points = []
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    
    for angle in angles:
        r = radius + random.uniform(-noise, noise)
        x = center[0] + r * np.cos(angle)
        y = center[1] + r * np.sin(angle)
        points.append(Point2D(x, y))
    
    return points


def generate_clusters(n_clusters: int = 3, 
                     points_per_cluster: int = 20,
                     cluster_std: float = 5) -> List[Point2D]:
    """Δημιουργεί σημεία σε clusters"""
    points = []
    
    for _ in range(n_clusters):
        # Random cluster center
        cx = random.uniform(20, 80)
        cy = random.uniform(20, 80)
        
        # Generate points around center
        for _ in range(points_per_cluster):
            x = np.random.normal(cx, cluster_std)
            y = np.random.normal(cy, cluster_std)
            points.append(Point2D(x, y))
    
    return points


def demo_basic():
    """Βασικό demo με λίγα σημεία"""
    print("=== Basic Convex Hull Demo ===\n")
    
    # Δημιουργία απλού dataset
    points = [
        Point2D(30, 30), Point2D(50, 60), Point2D(10, 40),
        Point2D(70, 30), Point2D(50, 20), Point2D(20, 50),
        Point2D(60, 40), Point2D(40, 70), Point2D(30, 10)
    ]
    
    # Υπολογισμός convex hull
    ch = ConvexHull2D(points)
    with Timer("Graham Scan"):
        hull = ch.graham_scan()
    
    print(f"\nNumber of input points: {len(points)}")
    print(f"Number of hull vertices: {len(hull)}")
    print(f"Hull area: {ch.get_hull_area():.2f}")
    print(f"Hull perimeter: {ch.get_hull_perimeter():.2f}")
    
    # Εκτύπωση hull vertices
    print("\nHull vertices (in order):")
    for i, p in enumerate(hull):
        print(f"  {i+1}: ({p.x:.2f}, {p.y:.2f})")
    
    # Visualization
    plot_convex_hull(points, hull, title="Basic Convex Hull Example")


def demo_random_points():
    """Demo με τυχαία σημεία"""
    print("\n=== Random Points Demo ===\n")
    
    n_points = 100
    points = generate_random_points(n_points, seed=42)
    
    # Υπολογισμός hull
    hull = compute_convex_hull(points)
    
    print(f"Number of input points: {n_points}")
    print(f"Number of hull vertices: {len(hull)}")
    print(f"Percentage of points on hull: {100*len(hull)/n_points:.1f}%")
    
    # Visualization
    plot_convex_hull(points, hull, title=f"Convex Hull of {n_points} Random Points")


def demo_special_cases():
    """Demo με ειδικές περιπτώσεις"""
    print("\n=== Special Cases Demo ===\n")
    
    # Case 1: Σημεία σε κύκλο
    print("Case 1: Points on circle")
    circle_points = generate_circle_points(20)
    hull1 = compute_convex_hull(circle_points)
    print(f"  Points on circle: {len(circle_points)}, Hull vertices: {len(hull1)}")
    
    # Case 2: Σημεία σε κύκλο με θόρυβο
    print("\nCase 2: Points on noisy circle")
    noisy_circle = generate_circle_points(50, noise=10)
    hull2 = compute_convex_hull(noisy_circle)
    print(f"  Points on noisy circle: {len(noisy_circle)}, Hull vertices: {len(hull2)}")
    
    # Case 3: Clustered points
    print("\nCase 3: Clustered points")
    clusters = generate_clusters(3, 30)
    hull3 = compute_convex_hull(clusters)
    print(f"  Clustered points: {len(clusters)}, Hull vertices: {len(hull3)}")
    
    # Visualizations
    plot_convex_hull(circle_points, hull1, title="Convex Hull: Circle Points")
    plot_convex_hull(noisy_circle, hull2, title="Convex Hull: Noisy Circle")
    plot_convex_hull(clusters, hull3, title="Convex Hull: Clustered Points")


def demo_performance():
    """Demo για performance testing"""
    print("\n=== Performance Demo ===\n")
    
    sizes = [10, 50, 100, 500, 1000, 5000]
    
    print("Input Size | Time (seconds) | Hull Vertices")
    print("-" * 45)
    
    for size in sizes:
        points = generate_random_points(size, seed=42)
        
        with Timer(f"Size {size}") as timer:
            hull = compute_convex_hull(points)
        
        print(f"{size:10d} | {timer.elapsed:14.6f} | {len(hull):13d}")


def main():
    """Main demo function"""
    print("Convex Hull 2D Implementation Demo")
    print("=" * 50)
    
    # Επιλογή demo
    print("\nAvailable demos:")
    print("1. Basic demo (few points)")
    print("2. Random points demo")
    print("3. Special cases demo")
    print("4. Performance demo")
    print("5. Run all demos")
    
    choice = input("\nSelect demo (1-5): ")
    
    if choice == '1':
        demo_basic()
    elif choice == '2':
        demo_random_points()
    elif choice == '3':
        demo_special_cases()
    elif choice == '4':
        demo_performance()
    elif choice == '5':
        demo_basic()
        demo_random_points()
        demo_special_cases()
        demo_performance()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()