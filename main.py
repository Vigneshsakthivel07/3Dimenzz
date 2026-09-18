from shapely.geometry import Polygon
from shapely.validation import make_valid

# Importing our modular blocks
from core.geometry import build_fmb_polygon
from core.analytics import compare_polygons
from core.visuals import visualize_comparison

if __name__ == "__main__":
    # 1. Generate Data
    fmb_polygon = build_fmb_polygon(100.0, [
        (20, 15, 'left'), (50, 30, 'left'), (80, 10, 'left'),
        (30, 25, 'right'), (70, 20, 'right')
    ])
    
    gps_polygon = make_valid(Polygon([
        (-1, 2), (19, 17), (52, 28), (81, 11), (102, 1), 
        (72, -18), (28, -26), (-1, 2)
    ]))
    
    # 2. Run Analytics
    metrics = compare_polygons(fmb_polygon, gps_polygon)
    print("--- System Check: Engine is Modular ---")
    for key, value in metrics.items():
        print(f"{key}: {value}")
        
    # 3. Visualize
    visualize_comparison(fmb_polygon, gps_polygon)