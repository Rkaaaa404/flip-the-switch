# NusaQC Baseline Evaluation Report

**What:** results of the automated test suite, phase 1 baseline
**Run on:** 26 September 2026, before the hackathon
**Harness:** `code/webdev/eval/` (ONNX Runtime on CPU, SNI 2729:2013 grades). Run everything with `python run_all.py`. Raw results are in `results/*.json`.
**Data:**
- **Model 1 (freshness):** `models/datasets/mobilenet/val`, 380 real validation images, grades A, B and C across 11 days on ice
- **Model 2 (defects):** `models/datasets/yolo8s/valid`, 642 real annotated validation images with 720 defect boxes

> **Read the freshness score with care.** [`code/models/model_1/README.md`](../../models/model_1/README.md) shows that splits sharing DaFiF sessions inflate accuracy to about 99%. The grouped-by-day split (75.75% accuracy, 84.6% Grade C recall) is the realistic estimate. This report is the evaluation of the vision models only. The Receiving QC Room treats their output as a screen that a named person reviews.

## 1. Summary

The suite has six parts: core accuracy, optical robustness, edge cases, agentic adjudication, async streaming and quantization. It ran on the full validation sets, without sampling.

- **Model 1 (MobileNetV3)** is perfect on this validation folder under good conditions, but degrades badly in poor light and with motion blur.
- **Model 2 (YOLOv8s FP32)** misses many defects (false negative rate **46.39%**), and is too slow in FP32 for an ARM Cortex-A72 edge CPU.

These results are the baseline that justified the phase 2 work.

## 2. Scorecard

| # | Script | What it measures | Key baseline numbers | Notes |
|---|---|---|---|---|
| 1 | `test_core_accuracy.py` | Freshness accuracy and defect detection | Freshness F1 **100.0%**; defect recall **53.61%**, FNR **46.39%**, precision **89.56%**, mAP@50 **50.41%** | All 380 freshness images correct. **Critical:** 334 of 720 defects missed |
| 2 | `test_optical_robustness.py` | Wet glare, low light (<50 lux), blur (>15 cm/s) | Glare false alarms **0.00%**; low-light F1 **41.58%**; blur recall retained **40.00%** | Robust to water and mucus glare. **Critical:** collapses in dim light and on a fast belt |
| 3 | `test_edge_cases.py` | Empty belt, out-of-distribution input, occlusion | Phantom defects **0.00%**; OOD confidence drop **34.92%**; recall at >50% occlusion **28.00%** | Empty belt is clean. **Critical:** heavy occlusion is a blind spot for a single camera |
| 4 | `test_agentic_adjudication.py` | Resolving CONDITIONAL cases (VLM review with fallback) | Resolved **100.0%**; agreement with experts **86.00%**; fallback **100.0%**; VLM latency **1.19 s** | Borderline cases resolve without stopping the line; fallback to the operator always works. 14% disagreement with QC experts |
| 5 | `test_async_stream.py` | Streaming load and memory | **4.40 FPS**; RAM growth **2.59 MB/min**; frame drops **0.00%** | Stable, no memory leak, but below the 10 FPS conveyor target |
| 6 | `test_quantization_performance.py` | FP32 size and edge readiness | **42.68 MB**; host latency **226.83 ms**; projected edge latency **1,315 ms (0.76 FPS)**; INT8 pending | FP32 is too heavy for a Raspberry Pi 4. **Critical:** INT8 quantization needed in phase 2 |

## 3. Detailed metrics

### Model 1: freshness classifier (MobileNetV3-Small FP32)

- 380 validation images. Accuracy, macro precision, macro recall and macro F1 are all 100.0%.
- Mean host CPU latency: 5.39 ms per frame.
- Per grade (SNI 2729:2013), all at 100% precision and recall: Grade A (days 1 to 2, 60 images), Grade B (days 3 to 6, 141 images), Grade C (days 7 to 11, 179 images).
- **Safety-critical:** Grade C predicted as Grade A: **0 cases**.

### Model 2: defect detector (YOLOv8s FP32)

- 642 validation images with 720 ground-truth boxes.
- Precision 89.56%, recall 53.61%, **false negative rate 46.39%**, false alarm rate 10.44%, mAP@50 50.41%.
- Mean host CPU latency: 255.34 ms per frame (about 3.9 FPS).

| Class | TP | FP | Precision | Failure pattern |
|---|---|---|---|---|
| `sisik_sisa` (scale damage) | 51 | 9 | 85.0% | Often missed when scales are thin or translucent |
| `warna_abnormal` (red lesion) | 229 | 8 | 96.6% | Stable on large bruises and red patches |
| `luka_robekan` (open wound) | 45 | 8 | 84.9% | Misses narrow tears (<15 px) |
| `lendir_berlebih` (excess mucus) | 61 | 20 | 75.3% | Most false alarms, from water reflections |

## 4. Six weaknesses found

### 🔴 1. Many missed defects (FNR 46.39%, recall 53.61%)

- **Finding:** of 720 real defects in 642 images, **334 were missed**.
- **Causes:** standard cross-entropy with no weighting for minority classes; tiny defects (<20 px) lose spatial detail in the CSPDarknet backbone's pooling layers.
- **Impact:** fish with tears or scale damage could reach an export container and trigger a quality rejection.

### 🔴 2. FP32 latency and size on an edge CPU (0.76 FPS)

- **Finding:** the FP32 YOLOv8s weights are **42.68 MB**. Host latency is **226.83 to 255.34 ms** (about 4 FPS). On a Raspberry Pi 4 (ARM Cortex-A72) the projection is **1,315 ms per frame (0.76 FPS)**.
- **Cause:** full 32-bit floating point on a CPU with no NPU or GPU.
- **Impact:** at a standard belt speed of 15 cm/s the camera produces 10 frames per second. At 0.76 FPS the frame queue overflows and the system falls 5 to 10 seconds behind.

### 🔴 3. Freshness accuracy collapses in dim light (<50 lux)

- **Finding:** in dim light or under an operator's shadow, MobileNetV3's **macro F1 drops from 100.0% to 41.58%**.
- **Cause:** the pixel histogram squeezes into the dark range, and the gill and eye colors the model relies on lose contrast.
- **Impact:** changing light on the sorting floor can grade a Grade A fish as B or C.

### 🟡 4. Motion blur cuts detection (>15 cm/s)

- **Finding:** with linear motion blur from a fast belt, defect recall retained drops to **40.00%** and freshness macro F1 to **67.29%**.
- **Cause:** blur smears the edges of tears and scale damage, so confidence falls below the operating threshold (0.55).

### 🟡 5. Blind spot under heavy occlusion (>50% overlap)

- **Finding:** when more than half of a fish is covered by others, defect recall drops to **28.00%**.
- **Cause:** a single top-down 2D camera can't see the underside or covered areas. (The delivery traceability feature added during the hackathon captures a second, ventral view of each fish for this reason.)

### 🟡 6. Mucus false alarms and AI agent disagreement (14%)

- `lendir_berlebih` has the most false positives (20 of 81 predictions, precision 75.3%): wet ice and water reflections are read as abnormal mucus.
- On borderline cases sent to the VLM agent (`test_agentic_adjudication.py`), the agent disagreed with human QC experts **14.0%** of the time.

## 5. Phase 2 plan

| Priority | Work | Target | Method |
|---|---|---|---|
| P1 | Retrain YOLOv8s with focal loss and weighted boxes | Recall **≥ 75%**, FNR **≤ 25%** (from 46.39%) | Weighted loss on open wound and scale damage; copy-paste augmentation of tiny defects |
| P2 | Dynamic INT8 quantization of the defect model | **~10.8 MB**, host latency **< 80 ms**, edge **> 2.5 FPS** | `onnxruntime.quantization.quantize_dynamic` with `QuantType.QUInt8` (done: `code/models/model_2/quantize_int8.py`, 11.5 MB) |
| P3 | Adaptive CLAHE preprocessing | Low-light macro F1 **≥ 70%** (from 41.58%) | Contrast-limited adaptive histogram equalization on the luminance channel before MobileNetV3 |
| P4 | Synthetic motion-blur and glare augmentation | Blur recall retained **≥ 65%** (from 40.00%) | Retrain with linear blur kernels for 15 to 20 cm/s belts |
| P5 | Occlusion handling with a hardware diverter | **100%** of occluded cases diverted | Mark >50% occlusion as `CONDITIONAL` and trigger a GPIO diverter to a re-orientation lane |

Also planned: IoU 0.45 and confidence 0.50 threshold tuning, to cut mucus false alarms.
