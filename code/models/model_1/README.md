# Model 1: Fish Freshness Classifier

MobileNetV3-Small, exported to Float32 ONNX (opset 18): a 0.28 MB graph plus about 6 MB of external weights (`.onnx.data`). It grades a fish photo as **Grade A** (prime), **Grade B** (fresh, domestic market) or **Grade C** (reject), following the visual organoleptic criteria of Indonesian standard SNI 2729:2013.

This model was trained before the hackathon. The Receiving QC Room uses its exported weights as they are (`code/webdev/backend/models_weights/mobilenetv3_freshness.onnx`).

## Data

| Dataset | Use | Notes |
|---|---|---|
| **DaFiF** (*Data in Brief* 57, 2024, 111016) | Training and test | 2,536 photos of 3 species over 11 days on ice, graded with SNI 2729:2013 |
| **FFE**, fish-eye freshness (*Ecological Informatics* 95, 2026) | Secondary test only | Macro close-ups of the eye |

Kaggle inputs: `raykapranandita/dataset-for-fishs-freshness-problems` and `raykapranandita/the-freshness-of-the-fish-eyes-dataset-ffe`.

## Pipeline

Everything runs from one file, [`01_model1_full_pipeline.py`](01_model1_full_pipeline.py): EDA, two train/test splits, class-weighted training, the FFE check, plots, ONNX export and a CPU latency benchmark.

- **In-memory preload** (`FastRAMFishDataset`): resizes the whole dataset into RAM at start (~15 s), so 12 epochs take under 2 minutes on a Kaggle T4 or P100.
- **Dataset autodiscovery:** works with Kaggle input paths, symlinks or local folders.
- **Class-weighted cross-entropy:** Grade A is only 15.8% of the data and Grade C is 47.2%.
- **Anti-leakage augmentation:** `RandomErasing` (cutout), `ColorJitter` and `RandomResizedCrop`, so the CNN learns the fish and not DaFiF's lab tray.
- **ONNX opset 18 export:** native with PyTorch 2.x, no version-conversion warnings, about 6 MB in total.
- **Latency benchmark:** 2.44 ms per frame (about 409 FPS) on a multi-threaded CPU, well under the 150 ms budget for an edge device such as a Raspberry Pi 5.

`train_weighted_loss.py` and `train_focal_loss.py` are the earlier loss experiments. `output.txt` is the log of the final run.

### Run it on Kaggle

1. Create a notebook with a **T4 or P100 GPU** and add the two datasets above.
2. Paste `01_model1_full_pipeline.py` into a cell and **Run All** (about 2 minutes).
3. Download `/kaggle/working/output_model1/`: the plots (300 DPI) and `mobilenetv3_freshness.onnx`.

| Output | Contents |
|---|---|
| `eda_dataset_distribution.png` | Class distribution, per-species distribution, grade decline by day (1 to 11), DaFiF vs. FFE |
| `eda_sample_images_by_grade.png` | Sample photos per grade, with species, day and session |
| `training_curves_comparison.png` | Loss, accuracy and macro F1 per epoch, random vs. grouped split |
| `confusion_matrices_all.png` | Raw and normalized confusion matrices for the random split, grouped split and FFE |
| `sample_test_predictions_grid.png` | Test predictions with confidence, correct in green and wrong in red |
| `mobilenetv3_freshness.onnx` | The deployable model |

## Results: leakage and domain shift

| Metric | Random split | Grouped by day/session | FFE (secondary) |
|---|---|---|---|
| Accuracy | 99.48% | **75.75%** | 41.70% |
| Macro F1 | 0.9958 | **0.6648** | 0.3032 |
| Grade C recall (safety-critical) | 1.0000 | **0.8464** | 0.0352 |
| Reading | Inflated by leakage | **Honest production estimate** | Domain mismatch |

- **Random split is leaked.** DaFiF photographs the same 10 fish per species again and again in one session, on numbered trays. A random split puts photos of the same fish under the same light in both train and test, so the model memorizes specimens and backgrounds.
- **The grouped split is the honest number.** With whole days and sessions held out, accuracy is 75.75%. Grade A recall is 95.0%. Grade C recall is 84.64%: of 280 spoiled fish, 237 are caught, and only 2.5% are graded A. Grade B (35.0% recall) is the biochemical transition between days 3 and 6, and is the hardest class.
- **FFE shows a modality gap.** DaFiF shows the whole fish, while FFE is a close-up of the eye. Features learned from body, gills and background don't transfer to an eye close-up. Eye-based grading would need a macro camera and an eye-localization step.

## Limits in the Receiving QC Room

Species outside the model's scope come back `UNSUPPORTED` and count as unscreened. The grade is a visual screen, not a safety verdict: a named person decides.
