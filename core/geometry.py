from shapely.geometry import Polygon
from shapely.validation import make_valid

def build_fmb_polygon(g_line_length, offsets):
    """Reconstructs an FMB polygon using the baseline (G-Line) and offsets."""
    left_points = []
    right_points = []
    start_point = (0.0, 0.0)
    end_point = (float(g_line_length), 0.0)
    
    for chainage, offset, direction in offsets:
        x = float(chainage)
        y = float(offset) if direction.lower() == 'left' else -float(offset)
        
        if direction.lower() == 'left':
            left_points.append((x, y))
        else:
            right_points.append((x, y))
            
    left_points.sort(key=lambda p: p[0])
    right_points.sort(key=lambda p: p[0], reverse=True)
    
    perimeter_coords = [start_point] + left_points + [end_point] + right_points + [start_point]
    return make_valid(Polygon(perimeter_coords))