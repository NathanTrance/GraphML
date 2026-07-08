# RP-GAAP Coding Agent and stuff Guide

## Goal

Implement a small, feasible improvement on **GAAP** for graph fraud detection.

Btw, this machine has no env or machine to run these experiments. so just code, git init and stuff to push stuff. Thank you

Proposed method:

**RP-GAAP = GAAP + focal loss + rare-pattern weighting**

The goal is not to redesign GAAP. Keep the original model mostly unchanged and modify the **training loss / sample weighting**.

---

## Base Project

Use the official GAAP repository as the base code.

Start with **YelpChi only**. Add Amazon only after YelpChi works.

---

## Main Tasks

### 1. Reproduce Original GAAP

First, run the original GAAP training script on YelpChi and save the baseline result.

Deliverable:

```text
Baseline GAAP result on YelpChi
```

Do not modify the model before this works.

---

### 2. Find the Training Loss

Search the codebase for:

```python
cross_entropy
```

or:

```python
loss =
```

Find the place where the model computes:

```text
logits -> loss -> backward
```

This is the main file to modify.

---

### 3. Add Focal Loss

Create:

```text
mycode/utils/losses.py
```

Add a `FocalLoss` class that supports:

```python
criterion(logits, labels, sample_weight=None)
```

Use this default setting:

```python
gamma = 2.0
alpha = [1.0, 3.0]   # class 0 = normal, class 1 = fraud
```

Purpose:

```text
Make the model focus more on hard fraud examples.
```

---

### 4. Add Rare-Pattern Weighting

Create:

```text
mycode/utils/rare_pattern.py
```

Implement a function:

```python
make_rare_pattern_weights(features, labels, train_mask)
```

Simple logic:

```text
1. Select top-k features by variance
2. Bin each selected feature into quantile bins
3. Treat each node's binned feature vector as a pattern
4. Count pattern frequency
5. Give higher weight to rarer patterns
6. Optionally boost fraud nodes
```

Suggested defaults:

```python
num_bins = 5
top_k_features = 10
max_weight = 3.0
fraud_boost = 1.5
```

Purpose:

```text
Make rare fraud-related patterns contribute more during training.
```

---

### 5. Integrate Four Experiment Modes

Support these four modes:

| Mode | Description |
|---|---|
| `baseline` | Original GAAP |
| `focal` | GAAP + focal loss |
| `rare` | GAAP + rare-pattern weighting |
| `both` | GAAP + focal loss + rare-pattern weighting |

The final method is:

```text
both = RP-GAAP
```

---

## Loss Logic

### Baseline

```python
loss = cross_entropy(logits[train_mask], labels[train_mask])
```

### Focal Loss Only

```python
loss = focal_loss(logits[train_mask], labels[train_mask])
```

### Rare-Pattern Weighting Only

```python
loss_each = cross_entropy(
    logits[train_mask],
    labels[train_mask],
    reduction="none"
)

loss = (loss_each * rare_weights[train_mask]).mean()
```

### RP-GAAP

```python
loss = focal_loss(
    logits[train_mask],
    labels[train_mask],
    sample_weight=rare_weights[train_mask]
)
```

---

## Metrics to Report

Report at least:

```text
AUC
AP / PR-AUC
Macro-F1
Fraud Recall
Fraud Precision
```

Accuracy alone is not enough because fraud detection is imbalanced.

---

## Expected Result Table

| Method | AUC | AP | Macro-F1 | Fraud Recall | Fraud Precision |
|---|---:|---:|---:|---:|---:|
| GAAP | | | | | |
| GAAP + Focal Loss | | | | | |
| GAAP + Rare Weighting | | | | | |
| RP-GAAP | | | | | |

---

## Important Constraints

- Do not rewrite the GAAP architecture unless necessary.
- Do not add too many new components.
- Do not tune too many hyperparameters.
- Prioritize reproducibility over complexity.
- Keep all baseline results unchanged and clearly recorded.
- Run YelpChi first. Amazon is optional.

---

## Suggested Git Workflow

Use separate commits:

```text
1. reproduce original GAAP
2. add focal loss
3. add rare-pattern weighting
4. add experiment modes
5. add result table / logging
```

---

## Final Project Story

GAAP learns attribute-association patterns for graph fraud detection, but rare fraud-related patterns may be underweighted because common benign patterns dominate training.

RP-GAAP improves this by:

```text
1. using focal loss to emphasize hard fraud examples
2. using rare-pattern weighting to emphasize uncommon suspicious patterns
```

This gives a small but meaningful novelty while keeping the project feasible.
