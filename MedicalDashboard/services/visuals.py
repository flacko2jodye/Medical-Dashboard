import os
import matplotlib.pyplot as plt
import seaborn as sns

VISUALS_FOLDER = 'MedicalDashboard/static/visuals'
os.makedirs(VISUALS_FOLDER, exist_ok=True)

def generate_visuals(df):
    numerical_cols = df.select_dtypes(include=['number']).columns
    if len(numerical_cols) > 1:
        plt.figure(figsize=(8, 6))
        sns.heatmap(df[numerical_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Feature Correlation Heatmap")
        heatmap_path = os.path.join(VISUALS_FOLDER, 'heatmap.png')
        plt.savefig(heatmap_path)
        plt.close()
        return heatmap_path
    return None
