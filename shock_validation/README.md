# 单步 FM 冲击验证代码

本目录执行 [原建议方案](../SINGLE_STEP_FM_SHOCK_PROTOCOL.md) 的同构核心消融、独立数据重复、闭环和软件延时阶段。正式结果入口为 [REPORT.md](../results/shock_validation/REPORT.md)，所有数值表在 [TABLES.md](../results/shock_validation/TABLES.md)。

## 当前状态（2026-10-25）

正式实验已完成并归档：

- 3 套独立训练数据 × 3 个配对权重种子；A/B/C 同构对照、A_time 等优化耗时、直接回归/中点 FM 工程参照、原始残差/EMA/增广 Kalman 基线。
- 共享 720 条测试轨迹；同观测流评分、固定权重闭环和自身 P50 软件延时复核均已完成。
- 主比较 B（单步 FM）对 A（同构残差）的冲击 RMSE 仅改善 **1.58%**（97.5% 区间 [0.43, 2.63]），背景恶化 **1.49%**，未达到预注册的“冲击改善至少 10%、背景恶化不超过 5%”门槛；B 对 C 也没有优势。
- 按预注册规则，**没有**启动零源噪声消融和 D 组追加实验，也没有做测试驱动的调参或重选。
- 归档验证：36 项单元测试通过；42 个检查点完成更新数、同初始化、验证选模和调用次数审计；数据划分无重叠；源码哈希一致。

完整结果、解释与限制见 [REPORT.md](../results/shock_validation/REPORT.md)。

## 复现

在仓库根目录、现有 requirements.txt 环境中运行：

```powershell
.venv/Scripts/python.exe shock_validation_experiment.py --workers 3 --stage all
.venv/Scripts/python.exe shock_validation_delay.py
.venv/Scripts/python.exe analyze_shock_validation.py
.venv/Scripts/python.exe -m unittest test_shock_validation test_core test_single_step test_adaptation test_delayed closed_loop.test_core -v
```

使用 `--out results/another_directory` 可在新目录从头运行；三个入口都要传相同目录。入口默认本地 CPU，每训练进程 1 个 PyTorch 线程。正式主训练和评分不依赖网络。

`--stage train` 只训练与验证选参，`--stage evaluate` 只执行冻结权重的同观测流和零延时闭环评分。最初运行冻结配置与源码 SHA-256；源码发生变化时拒绝直接接续，避免把不同实现的结果混在一起。断点缓存记录全部优化器、三个独立随机流与模型状态。训练完成的组用 `seed*_training.json` 标记；评估按单模型输出跳过已经完成的记录。

A_time 是额外的按实测优化耗时停止的控制，更新数随机器负载变化。中途停止其延长阶段会从完整主训练终点重新执行该补充阶段；主 A/B/C 的 15,000 次更新不受影响。只有完整保存的组视为完成。

## 实现边界

- `data.py`：分层矩形冲击、7 类背景、共同 PD/DOB 数据池、stride=1 窗口和哈希。
- `training.py`：同构 A/B/C 的共享初始化与采样，FM、重复端点、直接回归及多步参照，验证选模与等优化耗时 A_time。
- `metrics.py`：事件/分层等权评分、脉冲与拖尾积分、逐事件峰值绝对偏差；无未来观测用于推理。
- `filters.py`：EMA 与增广 Kalman。Kalman 使用已知模型和真实噪声尺度，是理想信息条件下的工程基线。
- `control.py`：经典补偿控制和固定 1 秒事件指标；神经网络沿用原 `closed_loop/core.py`，延时沿用 `closed_loop/delayed.py`。
- `EXECUTION_PROTOCOL.md`：训练启动后、正式测试评分前写下的执行细节和统计规则；在 `analysis_plan.json` 中记录哈希。

核心协议在训练开始前写入 `frozen_config.json`。流程检查使用两次更新的 seed=99 模型，检查了保存、读取、影子推理与闭环；该检查沿用了同一测试生成种子，仅用于代码接口核对，未据此调整训练配置、阈值、选择规则或报告子组。它不计入正式训练重复，也不作为性能证据。

## 结果文件

每个 `dataN/` 内保存：数据清单、训练与归一化哈希、各模型最佳 `.pt`、训练历史、验证选择信息、滤波选参网格、逐轨迹和逐事件评分、当前点预测 `.npz`、闭环及延时指标。

全局保存：冻结配置、环境/源码来源、测试清单、聚合表、配对 bootstrap、调用次数和选模审计、测试输出、图及中文分析。`*_resume.pt` 是可再生的本地训练恢复缓存，不上传；正式最佳权重和训练历史上传。

预测 NPZ 是每条轨迹×601 时刻的当前扰动预测；神经网络在不满足完整 24 点历史/目标窗口的边缘以 NaN 标记，评分不会使用这些边缘。目标未来值仅用于训练和评分，不进入网络部署条件。

本轮主实验只处理网格对齐矩形冲击、准确 x/v/模型和 Gaussian σ=0.5。噪声状态反馈、参数失配、亚周期冲击及硬件在环均不是本轮已完成的内容；零源增强与 D 组是满足预定主比较门槛后的条件追加实验。
