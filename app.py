import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.validation import make_valid

def build_fmb_polygon(g_line_length, offsets):
    """
    Reconstructs an FMB polygon using the baseline (G-Line) and perpendicular offsets.
    
    :param g_line_length: Total length of the main survey line (e.g., in meters/links)
    :param offsets: List of tuples (chainage, offset_distance, 'left'/'right')
                    Chainage is the distance along the G-Line from the start (0,0).
    """
    left_points = []
    right_points = []
    
    # Start of the G-line
    start_point = (0.0, 0.0)
    # End of the G-line
    end_point = (float(g_line_length), 0.0)
    
    for chainage, offset, direction in offsets:
        x = float(chainage)
        # Left is typically positive Y, Right is negative Y in Cartesian
        y = float(offset) if direction.lower() == 'left' else -float(offset)
        
        if direction.lower() == 'left':
            left_points.append((x, y))
        else:
            right_points.append((x, y))
            
    # Sort points to form a proper closed ring
    # Left points go from start to end (ascending chainage)
    left_points.sort(key=lambda p: p[0])
    # Right points go from end back to start (descending chainage)
    right_points.sort(key=lambda p: p[0], reverse=True)
    
    # Combine to form the perimeter
    perimeter_coords = [start_point] + left_points + [end_point] + right_points + [start_point]
    
    fmb_poly = Polygon(perimeter_coords)
    return make_valid(fmb_poly)

def compare_polygons(fmb_poly, gps_poly):
    """
    Compares the reconstructed FMB polygon against the ground-truth GPS polygon.
    """
    # 1. Area Calculation
    fmb_area = fmb_poly.area
    gps_area = gps_poly.area
    area_diff = abs(fmb_area - gps_area)
    
    # 2. Intersection over Union (IoU)
    intersection_area = fmb_poly.intersection(gps_poly).area
    union_area = fmb_poly.union(gps_poly).area
    iou = (intersection_area / union_area) * 100 if union_area != 0 else 0
    
    # 3. Hausdorff Distance (Maximum deviation between the two shapes)
    max_deviation = fmb_poly.hausdorff_distance(gps_poly)
    
    return {
        "FMB Area": round(fmb_area, 2),
        "GPS Area": round(gps_area, 2),
        "Area Difference": round(area_diff, 2),
        "IoU Overlap (%)": round(iou, 2),
        "Max Deviation (Hausdorff)": round(max_deviation, 2)
    }

def visualize_comparison(fmb_poly, gps_poly):
    """Plots both polygons for visual inspection."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot FMB Polygon (Blue, Dashed)
    x_fmb, y_fmb = fmb_poly.exterior.xy
    ax.plot(x_fmb, y_fmb, color='blue', linestyle='--', linewidth=2, label='FMB (Paper Records)')
    ax.fill(x_fmb, y_fmb, color='blue', alpha=0.1)
    
    # Plot GPS/RTK Polygon (Red, Solid)
    x_gps, y_gps = gps_poly.exterior.xy
    ax.plot(x_gps, y_gps, color='red', linestyle='-', linewidth=2, label='GPS/RTK (Real-time)')
    ax.fill(x_gps, y_gps, color='red', alpha=0.1)
    
    # Formatting
    ax.set_aspect('equal')
    ax.set_title("FMB Sketch vs. RTK Survey Comparison")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Distance (m)")
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend()
    plt.show()

# ==========================================
# TEST RUN WITH MOCK DATA
# ==========================================
if __name__ == "__main__":
    # 1. Reconstruct FMB Polygon
    g_line = 100.0  # Main diagonal line is 100 meters
    # (chainage, offset, side)
    fmb_offsets = [
        (20, 15, 'left'),
        (50, 30, 'left'),
        (80, 10, 'left'),
        (30, 25, 'right'),
        (70, 20, 'right')
    ]
    fmb_polygon = build_fmb_polygon(g_line, fmb_offsets)
    
    # 2. Simulate incoming RTK GPS Data
    # In reality, you would convert WGS84 (Lat/Lon) to a local Cartesian plane (like UTM) first.
    # Here we simulate points with slight measurement deviations from the FMB.
    gps_coordinates = [
        (-1, 2),       # Start shifted slightly
        (19, 17),      # Left corner 1
        (52, 28),      # Left corner 2
        (81, 11),      # Left corner 3
        (102, 1),      # End shifted slightly
        (72, -18),     # Right corner 2
        (28, -26),     # Right corner 1
        (-1, 2)        # Close loop
    ]
    gps_polygon = make_valid(Polygon(gps_coordinates))
    
    # 3. Run Analytics
    metrics = compare_polygons(fmb_polygon, gps_polygon)
    print("--- Survey Comparison Results ---")
    for key, value in metrics.items():
        print(f"{key}: {value}")
        
    # 4. Show output
    visualize_comparison(fmb_polygon, gps_polygon)