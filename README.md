Stop updates until 2024/08/09! (minor additions on 2024/10/04)

## Introduction

This repository stores the code for the Science Data Center (SDC) of Gamma-ray Transients Monitor (GTM), the secondary science payload on board the Formosat-8B (FS-8B) satellite of Taiwan.

## Key Architecture

```
├── better_trigger_localize
│   ├── 0.table
│   ├── 1.input
│   ├── 2.trigger
│   ├── 3.location
│   ├── 1.generate_input.py
│   ├── 2.report_trigger.py
│   └── 3.plot_location.py
├── efficiency_study
│   └── s/lgrb_pool.py
├── gtm_dashboard
│   └── dashboard.py
├── gtm_gui
│   ├── GTM_SDC_Start.py
│   ├── Makefile_Linux
│   ├── Makefile_MacOS
│   └── Makefile_Windows
└── website
    ├── gtm_backend
    ├── gtm_frontend
    └── nginx.conf
```

