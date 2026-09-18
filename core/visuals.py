import matplotlib.pyplot as plt

def visualize_comparison(fmb_poly, gps_poly):
    """Plots both polygons for visual inspection."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x_fmb, y_fmb = fmb_poly.exterior.xy
    ax.plot(x_fmb, y_fmb, color='blue', linestyle='--', linewidth=2, label='FMB (Paper Records)')
    ax.fill(x_fmb, y_fmb, color='blue', alpha=0.1)
    
    x_gps, y_gps = gps_poly.exterior.xy
    ax.plot(x_gps, y_gps, color='red', linestyle='-', linewidth=2, label='GPS/RTK (Real-time)')
    ax.fill(x_gps, y_gps, color='red', alpha=0.1)
    
    ax.set_aspect('equal')
    ax.set_title("FMB Sketch vs. RTK Survey Comparison")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Distance (m)")
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend()
    plt.show()