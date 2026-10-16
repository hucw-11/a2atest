# 多通道测量噪声实验

目标：检验原 A2AFM 与直接回归对位置/速度测量噪声的敏感性，并比较混合噪声增强训练后的能力。保持原模型结构和过去→未来任务定义。本轮为开环估计，不改变真实状态或反馈控制器。

结果入口：[正式报告](../results/multichannel-20261016/REPORT.md)。

## 测量模型

`x_m=x+epsilon_x`，`v_m=v+epsilon_v`，`a_m=a+epsilon_a`。

观测残差为 `d_raw=m*a_m+c*v_m+kappa*x_m-u`。同一份测量用于残差与网络条件；真值标签仍是原始 d。三种传感器白噪声彼此独立。x/v 噪声在采样点间独立，不模拟从位置差分得到速度的相关噪声。

七种场景：x/v 准确；仅 x、仅 v、x/v 同时含 1% 噪声；对应三种 5% 噪声。百分比相对于**全部干净训练轨迹**中 x/v 的固定标准差，不使用测试真值来选择噪声尺度。`clean` 仅指 x/v 无噪，加速度仍有噪声。

原独立训练/验证/测试轨迹种子为 10000/20000/50000，默认数量 72/18/24。训练与验证加速度噪声沿用原实验的 σ∈[0.2,0.9]，测试固定 σ=0.5。同一数据划分内部的七种观测版本共享真实轨迹、加速度测量、x/v 标准正态抽样；不同划分独立。

训练数据是 72 条独立轨迹各自的七种观测版本，不是 504 条独立轨迹。噪声实现固定；不声称覆盖所有传感器噪声。验证也使用七种版本，按混合当前扰动 MSE 选择检查点。训练 stride=2，验证 stride=8，测试 stride=2，窗口长度24。新模型各训练3000步、种子11/22/33。

## 对照方法

- frozen_a2afm / frozen_regression：冻结 `results/main` 已有模型。
- mixed_a2afm / mixed_regression：从头训练的七场景混合噪声模型；每种方法/种子一份权重用于全部场景。
- raw：带噪测量构造的原始残差。
- ema：验证集选择低通系数。
- physics_backward：从测量速度做因果后向差分，展示数值微分的噪声敏感性。
- augmented_kalman：利用同样的 x/v/a 测量、已知 u 和系统参数，状态为 `[x,v,d,d_dot]`，连续模型经矩阵指数离散化。测量为原始 x/v/a，不把残差当成与 x/v 独立的额外测量。使用真实传感器噪声方差；过程噪声谱密度在每个场景的验证集上从 `[0.01,1,100,10000]` 选择。

EMA 与 Kalman 每场景单独调参，而神经网络在场景间共享权重。原模型与新模型的验证采样密度及训练样本构成不同，比较反映整个增强训练方案，并非单个因素的严格消融。原始残差和速度差分用于诊断，不将噪声敏感的差分基线当成最强物理方法。

## 运行

Python 3.12，依赖沿用仓库的 requirements-lock.txt。推荐已配置的 `.venv`。从仓库根目录执行：

```bash
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2
export MPLCONFIGDIR="$PWD/.mplconfig"
mkdir -p "$MPLCONFIGDIR"
.venv/bin/python -m unittest test_core closed_loop.test_core multichannel.test_core -v
.venv/bin/python -m multichannel.experiment --out /tmp/a2atest-multichannel-reproduction
```

默认参数就是本轮正式协议；本次归档的实际输出目录为 `results/multichannel-20261016`。输出目录已有内容时拒绝覆盖；上述复现命令使用新的输出目录。中断后可用相同参数加 `--resume`，源码与配置必须匹配。检查 `status.json` 为 `complete`，不能把部分模型检查点当作完整实验。

快速流程检查（不能用作研究结论）：

```bash
.venv/bin/python -m multichannel.experiment --out /tmp/multichannel-smoke \
  --steps 2 --seeds 11 --train-trajectories 3 --val-trajectories 3 --test-trajectories 3
```

复用原 `experiment.train`，将日志明确写入新实验目录；不修改根目录 WORK_LOG.md、原模型或原结果。新模型可通过原 `DisturbanceEstimator` 加载，传入测量的 x/v/a 历史即可。

## 评价与限制

当前扰动 RMSE/MAE、尾部误差、逐轨迹结果均保留。汇总 RMSE 对训练种子 MSE 取平均后开方；配对 Bootstrap 在轨迹层进行，不把重叠窗口或多模型种子当成独立轨迹。区间未作多重比较校正，只有一套独立测试轨迹和固定传感器噪声实现。

本轮没有测试闭环反馈噪声、偏置、有色/相关噪声、传感器延迟、参数失配或 5% 以上的强度，也没有修改流起点或针对重尾异常值做修复。完整预测、测试观测、调参记录、训练历史、源码及旧权重摘要均保存，以便后续复查。
