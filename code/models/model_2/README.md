# Model 2: Surface Defect Detector

YOLOv8s, exported to ONNX (`nusaqc_model2_defect_detector.onnx`, 42.7 MB Float32, plus an INT8 build from `quantize_int8.py`). It draws boxes around four kinds of visible surface defect on a fish.

This model was trained before the hackathon. The Receiving QC Room runs it on both conveyor views of every fish, and qc-agent posts the flagged photo with these boxes drawn on.

## Classes

The class ids are Indonesian and stay that way in storage. The chat, the photos and the dashboard show the English labels.

| Id | Stored id | Shown as | Covers |
|---|---|---|---|
| 0 | `sisik_sisa` | scale damage | Attached parasites (*Argulus*, anchor worm), loose or rough scales |
| 1 | `warna_abnormal` | red lesion | Red spots, hemorrhage, Aeromonas lesions, gill discoloration |
| 2 | `luka_robekan` | open wound | Ulcers, fin and tail rot, *Saprolegnia* fungus |
| 3 | `lendir_berlebih` | excess mucus | Thick cloudy mucus, white tail disease |

Visual criteria for each class and the edge-case rules are in [`ANNOTATION_GUIDE_MODEL2.md`](ANNOTATION_GUIDE_MODEL2.md).

## Data

| Dataset | Labels | Size |
|---|---|---|
| Roboflow Fish Disease | YOLO boxes, 7 classes (BDA, BGD, BRD, FDS, HF, PD, WTD) | 457 images |
| [`panda992/fish_disease_datasets`](https://huggingface.co/datasets/panda992/fish_disease_datasets) (Hugging Face, public) | Image-level, 7 disease classes | 2,450 images (2,082 train, 368 test) |
| Alaa Mahmoud Fish Disease (Kaggle) | Image-level, infected or not | 305 images |

SalmonScan (1,208 images) is set aside for later work.

The Hugging Face set replaced `Saon110/bd-fish-disease-dataset`, which is gated and failed on Kaggle with `DatasetNotFoundError`. `panda992` is the public original of the same BD fish data, without the unrelated shrimp images.

## Pipeline: seed model, pseudo-labels, retrain

Only the Roboflow set has boxes, so a seed model labels the other two.

1. **Seed model.** Train YOLOv8s on the 457 boxed Roboflow images with `03_model2_kaggle_pipeline.py` (Kaggle GPU). Output: `best.pt` and an ONNX export.
2. **Pseudo-labels.** `04_model2_kaggle_pseudolabeling.py` runs the seed model on `panda992` (downloaded automatically) and Alaa Mahmoud, and writes YOLO `.txt` labels. Inputs: the Roboflow set, notebook 03's `best.pt`, and optionally Alaa Mahmoud. Output: `nusaqc_extended_pseudo_dataset.zip`.
3. **Human check.** Review a random 10 to 15% of the pseudo-labels in Label Studio with [`02_label_studio_config.xml`](02_label_studio_config.xml). `05_label_studio_converter.py` turns the Label Studio export back into YOLO labels, and `06_sync_and_package_dataset.py` packages the dataset.
4. **Final model.** Run notebook 03 again with `DATASET_ROOT` pointing at the extended dataset.

Locally:

```bash
python code/models/model_2/01_prepare_model2_dataset.py --setup-dirs
python code/models/model_2/03_model2_kaggle_pipeline.py
```

### Hybrid class locking

To stop the seed model from drifting to the wrong class on outside data, each source is handled differently:

| Source | Handling |
|---|---|
| Roboflow (457, boxed) | Direct mapping of its 7 classes to the 4 NusaQC classes |
| `panda992` (2,450, known disease) | `lock_class = True`: the class comes from the dataset label, YOLO only finds the box |
| Alaa Mahmoud (305, infected or not) | `lock_class = False`: YOLO finds both the box and the class |

Result: **3,212 images and 3,509 boxes**, up from 457 images.

| Id | Class | Boxes (train) | Share |
|---|---|---|---|
| 0 | `sisik_sisa` | 434 | 12.4% |
| 1 | `warna_abnormal` | 1,511 | 43.1% |
| 2 | `luka_robekan` | 726 | 20.7% |
| 3 | `lendir_berlebih` | 489 | 13.9% |
| — | background (empty) | 549 | 15.6% |

## Seed model tuning

| Run | Val mAP@50 | Val recall | Test mAP@50 |
|---|---|---|---|
| Run 1, first settings (60 epochs) | 0.188 | 0.133 | — |
| Run 2, tuned | **0.409** (+117%) | **0.356** (+167%) | **0.287** (+53%) |

In Run 1 the validation classification loss blew up to about 80,000 in the early epochs. The causes were `lr0: 0.003` with too little warmup, a classification weight of `cls: 0.7` that was too low, and `mosaic: 0.2`, too weak for 457 images. Run 2's settings:

```python
HPARAMS = {
    'epochs': 100, 'batch': 16, 'imgsz': 640,
    'optimizer': 'AdamW', 'lr0': 0.001, 'lrf': 0.01,
    'momentum': 0.937, 'weight_decay': 0.001, 'warmup_epochs': 5.0,
    'mosaic': 1.0, 'close_mosaic': 15, 'mixup': 0.15, 'copy_paste': 0.2,
    'hsv_h': 0.015, 'hsv_s': 0.7, 'hsv_v': 0.4,
    'scale': 0.5, 'fliplr': 0.5, 'flipud': 0.1,
    'translate': 0.2, 'degrees': 10.0,
    'box': 7.5, 'cls': 1.5, 'dfl': 1.5, 'patience': 30
}
```

`output.txt` is the training log. `train_glare_aug.py` is a specular-glare augmentation experiment to cut false alarms on water and mucus reflections.

## Limits

- It is a visual screen. It never calls a fish safe or diseased.
- It mislabels the open ulcer in the demo image `hf_00811` as a red lesion (`warna_abnormal`) rather than an open wound. The demo keeps that on purpose: the model screens, the person decides.
