
- [2026-10-16 17:29:13 UTC+8] 开始实验 results；设备 cpu；计划训练 A2AFM/直接回归，评估滤波和物理基线

- [2026-10-16 17:29:17 UTC+8] 数据完成：训练窗口 4536，验证窗口 3402；滤波参数 {'ema': 0.2, 'local_poly': 23, 'kalman': 10000.0}

- [2026-10-16 17:29:19 UTC+8] a2afm seed=11 step=100/100 val_RMSE=0.30402 best=0.30402

- [2026-10-16 17:29:19 UTC+8] 完成 a2afm seed=11，本轮耗时 1.5 s，选择验证最优 step=100

- [2026-10-16 17:29:19 UTC+8] regression seed=11 step=100/100 val_RMSE=0.30815 best=0.30815

- [2026-10-16 17:29:19 UTC+8] 完成 regression seed=11，本轮耗时 0.3 s，选择验证最优 step=100

- [2026-10-16 17:29:20 UTC+8] fm_only seed=11 step=100/100 val_RMSE=0.37792 best=0.37792

- [2026-10-16 17:29:20 UTC+8] 完成 fm_only seed=11，本轮耗时 0.3 s，选择验证最优 step=100

- [2026-10-16 17:29:20 UTC+8] 训练完成，开始冻结测试集评估与积分步数检查

- [2026-10-16 17:29:24 UTC+8] 实验完成：/workspace/a2atest-runs/cloud-validation/results/REPORT.md
