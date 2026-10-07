GitHub repository: Cellula_1week
Link: https://github.com/HebaQasim/Cellula_1week
Description: No description
Main language: Jupyter Notebook

# Cellula Internship — Week 1: Toxic Comment Classification with RNN and LSTM

Multi-label classification of toxic comments using recurrent neural networks (TensorFlow / Keras).
Each comment can have any of six labels at the same time, or none:
`toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`.

## Dataset

The **Jigsaw Toxic Comment Classification** dataset: 159,571 Wikipedia talk-page comments.
About 90% of the comments have no label and the labels are very imbalanced (for example, `threat` is only 0.3%),
so F1 is used instead of accuracy. The official test set (test.csv + test_labels.csv, 63,978 scored comments)
was kept untouched until the final evaluation.

## Preprocessing

- Data inspection and quality checks: missing values, duplicate IDs, label values, near-duplicate comments, text issues.
- Removed near-duplicate comments (215 extra copies) and groups with conflicting labels (84 rows), leaving 159,272 comments.
- Text cleaning: lowercasing, URLs → `urltoken`, IP addresses → `iptoken`, control characters removed, extra whitespace collapsed.
- Stratified 80/20 train/validation split on the label combinations: 127,417 / 31,855 comments.
- Tokenizer fitted on the training text only (20,000-word vocabulary with an `<OOV>` token).
- Sequences padded and truncated to 250 tokens (pre-padding), with masking so padding is ignored.

## Models

**RNN** (`RNN/Task1_RNN.ipynb`)

- Baseline: Embedding (128) → SimpleRNN (64) → Dropout → Dense (6, sigmoid).
- Experiment 2: SimpleRNN returning all time steps + mask-aware global max pooling.

**LSTM** (`LSTM/Task1_LSTM.ipynb`)

- Embedding (128) → SpatialDropout → Bidirectional LSTM (64 per direction) → masked max pooling + average pooling → Dense (64) → Dropout → Dense (6, sigmoid). 2,675,654 parameters.

**Training (both):** weighted binary cross-entropy (positive weight √(negatives / positives) per label), Adam,
batch size 256, early stopping on validation PR-AUC. One decision threshold per label was tuned on the validation set.

## Results (F1 with tuned thresholds)

| Model | Validation Macro F1 | Validation Micro F1 | Test Macro F1 | Test Micro F1 |
|---|---|---|---|---|
| RNN baseline | 0.5447 | 0.6893 | 0.4364 | 0.5363 |
| RNN Experiment 2 (max pooling) | 0.6046 | 0.7296 | — | — |
| BiLSTM | 0.6396 | 0.7527 | 0.5400 | 0.6258 |

The BiLSTM is the best model. The rare labels (`threat`, `identity_hate`, `severe_toxic`) are the hardest.
Full results, training curves and confusion matrices are in `RNN/RNN_results.pdf` and `LSTM/LSTM_results.pdf`.

## Repository structure

```text
Cellula_1week/
├── RNN/
│   ├── Task1_RNN.ipynb
│   └── RNN_results.pdf
└── LSTM/
    ├── Task1_LSTM.ipynb
    └── LSTM_results.pdf
```

Each folder also contains the Jigsaw data files (`train.csv`, `test.csv`, `test_labels.csv`).

## How to run

Open a notebook in Google Colab, upload `train.csv`, `test.csv` and `test_labels.csv` next to it, and run all cells.
A GPU runtime is recommended for the LSTM.
