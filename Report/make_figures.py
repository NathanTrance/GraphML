import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

os.makedirs('Figures', exist_ok=True)

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'figure.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

# ══════ Figure 1: Recall@K bar chart ══════
datasets = ['YelpChi', 'T-Finance', 'Elliptic', 'Tolokers']
methods = ['GAAP', '+Focal', 'RP-GAAP', '+Both']
colors  = ['#011f4b', '#03396c', '#005b96', '#6497b1']

data = {
    'YelpChi':   [0.8839, 0.8823, 0.8862, 0.8700],
    'T-Finance': [0.8488, 0.8530, 0.8585, 0.8571],
    'Elliptic':  [0.7322, 0.7359, 0.7313, 0.7322],
    'Tolokers':  [0.5498, 0.5296, 0.5467, 0.5576],
}

fig, ax = plt.subplots(figsize=(6.0, 3.4))
x = np.arange(len(datasets))
w = 0.18
offsets = [-1.5*w, -0.5*w, 0.5*w, 1.5*w]

for i, method in enumerate(methods):
    vals = [data[d][i] for d in datasets]
    bars = ax.bar(x + offsets[i], vals, w, label=method, color=colors[i], edgecolor='white', linewidth=0.4)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{v:.4f}', ha='center', va='bottom', fontsize=6, rotation=90)

ax.set_xticks(x)
ax.set_xticklabels(datasets)
ax.set_ylabel('Recall@K')
ax.set_ylim(0.45, 0.96)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
ax.legend(ncols=4, loc='upper right', framealpha=0.9)
ax.grid(axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig('Figures/recall_at_k_comparison.pdf')
plt.close(fig)
print('[1/2] recall_at_k_comparison.pdf saved')

# ══════ Figure 2: Sweep subplots ══════
sweeps = {
    'rare_num_bins':       {3: 0.5561, 5: 0.5608, 7: 0.5608},
    'rare_top_k_features': {5: 0.5608, 10: 0.5514, 15: 0.5623},
    'rare_max_weight':     {1.5: 0.5561, 2.0: 0.5358, 3.0: 0.5623, 5.0: 0.5530},
    'rare_fraud_boost':    {1.0: 0.5483, 1.5: 0.5483, 2.0: 0.5545, 3.0: 0.5514},
    'focal_alpha_class1':  {1.5: 0.5364, 2.0: 0.5530, 3.0: 0.5514, 4.0: 0.5483},
}

titles = [
    r'rare_num_bins',
    r'rare_top_k_features',
    r'rare_max_weight',
    r'rare_fraud_boost',
    r'focal_alpha (class 1)',
]

baseline = 0.5498

fig, axes = plt.subplots(2, 3, figsize=(7.5, 4.5))
axes = axes.flatten()

for idx, (param, values) in enumerate(sweeps.items()):
    ax = axes[idx]
    kv = sorted(values.items())
    x_labels = [str(k) for k, _ in kv]
    y_vals  = [v for _, v in kv]
    xs = range(len(x_labels))

    bars = ax.bar(xs, y_vals, color='#b3cde0', edgecolor='white', linewidth=0.3)

    best_y = max(y_vals)
    for i, (k, yv) in enumerate(kv):
        if yv == best_y:
            bars[i].set_color('#005b96')

    ax.axhline(y=baseline, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.set_xticks(xs)
    ax.set_xticklabels(x_labels)
    ax.set_title(titles[idx], fontsize=9)
    ax.set_ylabel('Recall@K')
    ax.set_ylim(0.49, 0.59)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f'))
    ax.grid(axis='y', alpha=0.3)

axes[-1].set_visible(False)
fig.tight_layout()
fig.savefig('Figures/sweep_tolokers.pdf')
plt.close(fig)
print('[2/2] sweep_tolokers.pdf saved')
print('Done.')
