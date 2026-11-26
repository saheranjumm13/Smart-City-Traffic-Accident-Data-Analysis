from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

BASE_DIR = Path(".")
RAW_ACCIDENTS = BASE_DIR / "Dataset" / "Raw" / "indian_roads_dataset.csv"
RAW_TRAFFIC = BASE_DIR / "Dataset" / "Raw" / "smart_traffic_management_dataset.csv"
PROCESSED_DIR = BASE_DIR / "Dataset" / "Processed"
VIS_DIR = BASE_DIR / "Visualizations"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
VIS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load data
df = pd.read_csv(RAW_ACCIDENTS)
traffic_df = pd.read_csv(RAW_TRAFFIC)

# 2. Clean & engineer time features
df["festival"] = df["festival"].fillna("Non-Festival").astype(str).str.strip()
df["city"] = df["city"].astype(str).str.strip()
df["road_type"] = df["road_type"].astype(str).str.strip().str.lower()
df["accident_severity"] = df["accident_severity"].astype(str).str.strip().str.lower()

parsed_dt = pd.to_datetime(
    df["date"].astype(str) + " " + df["time"].astype(str),
    format="%d-%m-%Y %H:%M",
    errors="coerce",
)
df["year"] = parsed_dt.dt.year
df["month"] = parsed_dt.dt.month
df["time_period"] = pd.cut(
    df["hour"],
    bins=[-1, 5, 11, 17, 23],
    labels=["Night (0-5)", "Morning (6-11)", "Afternoon (12-17)", "Evening/Night (18-23)"],
)

cleaned_path = PROCESSED_DIR / "cleaned_indian_roads.csv"
df.to_csv(cleaned_path, index=False)

# 3. Statistical analysis
print("=== Casualties Descriptive Stats ===")
print(df["casualties"].describe())

# Peak vs Non-Peak hour casualties (Mann-Whitney U test)
peak_cas = df.loc[df["is_peak_hour"] == 1, "casualties"]
non_peak_cas = df.loc[df["is_peak_hour"] == 0, "casualties"]
u_stat, p_mw = stats.mannwhitneyu(peak_cas, non_peak_cas, alternative="two-sided")
print(f"\nPeak vs Non-Peak Casualties: U={u_stat:.2f}, p={p_mw:.4f}")

# Road type vs Accident severity (Chi-square test of independence)
ct = pd.crosstab(df["road_type"], df["accident_severity"])
chi2, p_chi, dof, _ = stats.chi2_contingency(ct)
print(f"Road Type vs Severity: chi2={chi2:.2f}, dof={dof}, p={p_chi:.4e}")

# Traffic dataset: Speed when accident_reported == 1 vs 0 (Welch's t-test)
spd_yes = traffic_df.loc[traffic_df["accident_reported"] == 1, "avg_vehicle_speed"]
spd_no = traffic_df.loc[traffic_df["accident_reported"] == 0, "avg_vehicle_speed"]
t_stat, p_t = stats.ttest_ind(spd_yes, spd_no, equal_var=False)
print(f"Avg Speed (Accident=1 vs 0): t={t_stat:.2f}, p={p_t:.4f}")

# 4. Location-wise & Accident-Prone Hotspot analysis
city_stats = (
    df.groupby(["city", "state"], as_index=False)
    .agg(
        total_accidents=("accident_id", "count"),
        total_casualties=("casualties", "sum"),
        fatal_accidents=("accident_severity", lambda s: (s == "fatal").sum()),
        avg_risk_score=("risk_score", "mean"),
    )
    .sort_values("total_accidents", ascending=False)
)
city_stats.to_csv(PROCESSED_DIR / "city_wise_summary.csv", index=False)

df["lat_grid"] = df["latitude"].round(2)
df["lon_grid"] = df["longitude"].round(2)

hotspots = (
    df.groupby(["city", "state", "road_type", "lat_grid", "lon_grid"], as_index=False)
    .agg(
        accidents=("accident_id", "count"),
        casualties=("casualties", "sum"),
        fatal_count=("accident_severity", lambda s: (s == "fatal").sum()),
        avg_risk_score=("risk_score", "mean"),
    )
)

# Filter to clusters with at least 5 accidents so small 1-row spikes don't skew rankings
hotspots = hotspots[hotspots["accidents"] >= 5].copy()
hotspots["hotspot_score"] = (
    0.5 * (hotspots["accidents"] / hotspots["accidents"].max())
    + 0.3 * (hotspots["casualties"] / hotspots["casualties"].max())
    + 0.2 * hotspots["avg_risk_score"]
)
hotspots = hotspots.sort_values("hotspot_score", ascending=False)
hotspots.to_csv(PROCESSED_DIR / "accident_hotspots.csv", index=False)

print("\n=== Top 10 Accident-Prone Hotspots ===")
print(hotspots.head(10).to_string(index=False))

# 5. Charts
plt.figure(figsize=(10, 5))
sns.barplot(data=city_stats, x="city", y="total_accidents")
plt.title("Total Accidents by City")
plt.xlabel("City")
plt.ylabel("Accidents")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig(VIS_DIR / "01_city_accidents.png", dpi=300)
plt.close()

hourly = df.groupby("hour", as_index=False)["accident_id"].count().rename(columns={"accident_id": "accidents"})
plt.figure(figsize=(10, 5))
sns.lineplot(data=hourly, x="hour", y="accidents", marker="o")
plt.title("Accidents by Hour of Day")
plt.xlabel("Hour (0-23)")
plt.ylabel("Accidents")
plt.xticks(range(0, 24))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(VIS_DIR / "02_hourly_trend.png", dpi=300)
plt.close()

top_hs = hotspots.head(10).copy()
top_hs["label"] = top_hs["city"] + " (" + top_hs["road_type"] + " " + top_hs["lat_grid"].astype(str) + "," + top_hs["lon_grid"].astype(str) + ")"
plt.figure(figsize=(11, 5))
sns.barplot(data=top_hs, y="label", x="hotspot_score")
plt.title("Top 10 Accident-Prone Hotspot Grids")
plt.xlabel("Composite Hotspot Score")
plt.ylabel("Location Grid")
plt.tight_layout()
plt.savefig(VIS_DIR / "03_top_hotspots.png", dpi=300)
plt.close()