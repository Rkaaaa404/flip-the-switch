# NusaQC Evaluation — Ringkasan Skor Baseline (Fase 1)

| Skrip Test Suite | Fokus Evaluasi | Skor Saat Ini | Status / Keterangan |
| --- | --- | --- | --- |
| 1. test_core_accuracy.py | Freshness F1 & Defect Deteksi | Freshness F1: 100.0% \| Defect Recall: 53.6% (FNR: 46.4%) | Evaluasi seluruh dataset riil (380 Freshness, 642 Defect) |
| 2. test_optical_robustness.py | Wet Glare & Pencahayaan | Glare FAR: 0.00% \| Low-Light F1: 41.6% | Ketahanan optik: Tahan pantulan kilau air; degradasi pada redup <50 lux |
| 3. test_edge_cases.py | Empty Frame & Oklusi | Phantom: 0.0% \| Oklusi 50%: 28.0% | Konveyor kosong 100% bersih; oklusi berat >50% blind spot kamera tunggal |
| 4. test_agentic_adjudication.py | Resolusi Kasus CONDITIONAL | Resolusi: 100.0% \| Fallback: 100.0% | Penyelesaian otomatis kasus borderline via VLM & graceful fallback ke operator |
| 5. test_async_stream.py | Throughput Aliran Konveyor | 4.40 FPS \| 4697 ms Latency | Pipeline asinkronus kontinu; zero memory leak |
| 6. test_quantization_performance.py | Efisiensi Kuantisasi Model | FP32: 42.7 MB (226.8 ms) \| INT8: Belum Dilakukan | Baseline FP32 lambat untuk edge; Kuantisasi INT8 ditargetkan untuk Fase II |


*Dihasilkan secara otomatis oleh NusaQC Automated Test Suite orchestrator.*
