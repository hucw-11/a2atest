# 独立闭环扩展

原 `a2afm/`、`results/main/` 保留。本扩展复用原网络与训练函数，但新增控制仿真、数据集、检查点和报告均单独保存。

已完成结果请先看 [CLOSED_LOOP_RESULTS.md](../CLOSED_LOOP_RESULTS.md)。

运行（项目根目录）：

```powershell
.\.venv\Scripts\python.exe -m unittest closed_loop.test_core -v
.\.venv\Scripts\python.exe -m closed_loop.experiment --steps 3000
.\.venv\Scripts\python.exe -m closed_loop.experiment --steps 3000 --resume
.\.venv\Scripts\python.exe -m closed_loop.analyze
```

输出：`results/closed_loop/REPORT.md` 和 `ANALYSIS.md`。

三个阶段：

1. `open_frozen`：原模型冻结，测试新的冲击扰动。固定正弦控制，估计不反馈。
2. `closed_frozen`：原模型冻结接入相同PD控制器，检验开环训练到闭环使用的迁移。
3. `closed_adapted`：使用独立闭环训练集重新训练的网络接入控制器。DOB和Kalman参数不变。

四种主要方法为残差Q滤波DOB、扰动/扰动导数Kalman观测器、直接回归网络、A2AFM。另加无扰动补偿PD作参照。

控制结构：

```text
参考 r,r_dot,r_ddot ─→ PD + 已知模型前馈 ─→ 减去 d_est ─→ 限幅 ─→ 二阶植物
                            ↑                                 │
                            x,v ←─────────────── 状态测量 ←────┤
                                                             │
旧控制 u_hold + x,v + 加速度测量 ─→ 物理残差 ─→ 观测器 ─→ d_est
```

采样顺序详见报告；测量中的u与控制执行中的新u分开存储。NPZ的`u_i`是第i条轨迹加速度采样时的旧控制，`command_i`是采样后执行的新控制。

配置与轨迹编号保存在 `config.json` 和 `test_manifest.json`，滤波调参完整记录位于 `filter_tuning.json`。所有新增权重在 `results/closed_loop/models/`。每阶段包含逐轨迹指标与全部状态/控制/估计时序。

模型选择沿用验证集当前扰动RMSE；经典滤波参数则按验证控制目标选择，因此并非所有方法均完成同等的闭环超参数搜索。网络按相同训练步数比较，也不代表等计算成本。

初始原系统快照：`snapshots/open_loop_20261013_234542/`；该目录含源码、依赖版本、全部原模型/结果与SHA-256清单，不重复保存虚拟环境或安装缓存。
