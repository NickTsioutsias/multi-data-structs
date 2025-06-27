# src/convex_hull/visualization.py
"""Visualization utilities για Convex Hull"""

import matplotlib.pyplot as plt
from typing import List, Optional
import numpy as np

from src.utils.geometry import Point2D


def plot_convex_hull(points: List[Point2D], 
                    hull: List[Point2D], 
                    title: str = "Convex Hull",
                    save_path: Optional[str] = None,
                    show_plot: bool = True):
    """
    Απεικονίζει τα σημεία και το convex hull τους.
    
    Args:
        points: Όλα τα σημεία
        hull: Τα σημεία του convex hull
        title: Τίτλος του plot
        save_path: Path για αποθήκευση (optional)
        show_plot: Αν θα εμφανιστεί το plot
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot όλα τα σημεία
    x_coords = [p.x for p in points]
    y_coords = [p.y for p in points]
    ax.scatter(x_coords, y_coords, c='blue', s=50, label='Points', zorder=5)
    
    # Plot το hull
    if hull:
        hull_x = [p.x for p in hull] + [hull[0].x]  # Κλείσιμο του polygon
        hull_y = [p.y for p in hull] + [hull[0].y]
        
        # Γέμισμα του hull
        ax.fill(hull_x, hull_y, alpha=0.3, c='green', label='Convex Hull')
        
        # Περίγραμμα του hull
        ax.plot(hull_x, hull_y, 'r-', linewidth=2, label='Hull Boundary')
        
        # Σημεία του hull
        hull_x_points = [p.x for p in hull]
        hull_y_points = [p.y for p in hull]
        ax.scatter(hull_x_points, hull_y_points, c='red', s=100, 
                  marker='o', edgecolors='black', linewidth=2, 
                  label='Hull Vertices', zorder=10)
    
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Equal aspect ratio
    ax.set_aspect('equal', adjustable='box')
    
    # Προσθήκη padding
    if points:
        x_min = min(p.x for p in points)
        x_max = max(p.x for p in points)
        y_min = min(p.y for p in points)
        y_max = max(p.y for p in points)
        
        x_range = x_max - x_min
        y_range = y_max - y_min
        padding = 0.1
        
        ax.set_xlim(x_min - padding * x_range, x_max + padding * x_range)
        ax.set_ylim(y_min - padding * y_range, y_max + padding * y_range)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    if show_plot:
        plt.show()
    else:
        plt.close()


def plot_algorithm_progress(points: List[Point2D], 
                          steps: List[List[Point2D]], 
                          save_dir: Optional[str] = None):
    """
    Δημιουργεί animation-style plots που δείχνουν την πρόοδο του αλγορίθμου.
    
    Args:
        points: Αρχικά σημεία
        steps: Λίστα με τα βήματα του hull σε κάθε iteration
        save_dir: Directory για αποθήκευση των plots
    """
    for i, hull_step in enumerate(steps):
        title = f"Graham Scan - Step {i+1}/{len(steps)}"
        save_path = f"{save_dir}/step_{i+1:03d}.png" if save_dir else None
        
        plot_convex_hull(points, hull_step, title=title, 
                        save_path=save_path, show_plot=False)


def create_comparison_plot(points: List[Point2D],
                         hulls: dict,
                         title: str = "Algorithm Comparison",
                         save_path: Optional[str] = None):
    """
    Συγκρίνει διαφορετικούς αλγορίθμους convex hull.
    
    Args:
        points: Input points
        hulls: Dictionary με {algorithm_name: hull_points}
    """
    n_algorithms = len(hulls)
    fig, axes = plt.subplots(1, n_algorithms, figsize=(6*n_algorithms, 5))
    
    if n_algorithms == 1:
        axes = [axes]
    
    for ax, (algo_name, hull) in zip(axes, hulls.items()):
        # Plot points
        x_coords = [p.x for p in points]
        y_coords = [p.y for p in points]
        ax.scatter(x_coords, y_coords, c='blue', s=30, alpha=0.6)
        
        # Plot hull
        if hull:
            hull_x = [p.x for p in hull] + [hull[0].x]
            hull_y = [p.y for p in hull] + [hull[0].y]
            ax.fill(hull_x, hull_y, alpha=0.3, c='green')
            ax.plot(hull_x, hull_y, 'r-', linewidth=2)
        
        ax.set_title(algo_name)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
    
    fig.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()