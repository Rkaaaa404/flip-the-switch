# NusaQC Code

Everything that runs. For what the Receiving QC Room is, how to set it up and the demo, see the [main README](../README.md).

NusaQC is a computer-vision QC system for Indonesian export fish processing plants. It combines two models:

1. **Freshness (Model 1):** MobileNetV3-Small grades a fish A, B or C against the visual criteria of SNI 2729:2013.
2. **Surface defects (Model 2):** YOLOv8s, trained on 3,200+ images with pseudo-labels, boxes scale damage, red lesions, open wounds and excess mucus.

## Layout

```text
code/
├── switch/                 # The Switch layer (built during the hackathon)
│   ├── agent/              # qcctl.py (qc-agent's only tool) and CLAUDE.md (its instructions)
│   ├── gate/               # qc-gate relay, no LLM
│   ├── setup/              # setup_switch.py: accounts, identities, room, gate policy, agent install
│   └── demo/images/        # real fish images used by the demo seed
│
├── webdev/                 # FastAPI backend and Next.js dashboard, see webdev/README.md
│   ├── backend/            # ONNX inference, SQLite records, delivery traceability, Switch room API
│   ├── frontend/           # dashboard (read-only for decisions)
│   └── eval/               # model evaluation suite and baseline report
│
├── models/                 # model training (before the hackathon)
│   ├── model_1/            # freshness classifier, see model_1/README.md
│   ├── model_2/            # defect detector, see model_2/README.md and ANNOTATION_GUIDE_MODEL2.md
│   └── datasets/           # local datasets, gitignored
│
├── AI/                     # exported ONNX models (freshness; defects in FP32 and INT8)
├── edge/                   # Raspberry Pi edge runtime: camera and MJPEG server, inference, GPIO, sorting decision, telemetry
├── default_yolo.yaml       # default YOLO config
├── requirements.txt        # Python dependencies for training and edge scripts
├── run.sh                  # edge node launcher (Raspberry Pi)
├── test_hardware.py        # local hardware check
└── test_rpi_remote.py      # Raspberry Pi check over SSH
```

## Where to start

| To understand | Read |
|---|---|
| The Switch room: agent, gate, signing | [`switch/agent/CLAUDE.md`](switch/agent/CLAUDE.md), [`switch/gate/main.py`](switch/gate/main.py), [`webdev/backend/app/services/switchroom_service.py`](webdev/backend/app/services/switchroom_service.py) |
| The backend and its API | [`webdev/README.md`](webdev/README.md) |
| Delivery traceability design | [`../docs/designs/nusaqc_delivery_traceability.md`](../docs/designs/nusaqc_delivery_traceability.md) |
| The models and their measured limits | [`models/model_1/README.md`](models/model_1/README.md), [`models/model_2/README.md`](models/model_2/README.md), [`webdev/eval/BASELINE_EVALUATION_REPORT.md`](webdev/eval/BASELINE_EVALUATION_REPORT.md) |
