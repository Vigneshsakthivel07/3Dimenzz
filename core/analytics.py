def compare_polygons(fmb_poly, gps_poly):
    """Calculates disputes: Area, Overlap (IoU), and Max Deviation."""
    fmb_area = fmb_poly.area
    gps_area = gps_poly.area
    area_diff = abs(fmb_area - gps_area)
    
    intersection_area = fmb_poly.intersection(gps_poly).area
    union_area = fmb_poly.union(gps_poly).area
    iou = (intersection_area / union_area) * 100 if union_area != 0 else 0
    
    max_deviation = fmb_poly.hausdorff_distance(gps_poly)
    
    return {
        "FMB Area": round(fmb_area, 2),
        "GPS Area": round(gps_area, 2),
        "Area Difference": round(area_diff, 2),
        "IoU Overlap (%)": round(iou, 2),
        "Max Deviation (Hausdorff)": round(max_deviation, 2)
    }