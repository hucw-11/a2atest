# CNN A2AFM 与全连接网络：冲击扰动估计

## 问题与对照

比较CNN能否改善A2AFM的扰动估计，特别是短脉冲。四组模型均从头训练：

| 模型 | 特征网络 | 目标 | 参数量 | 每次估计网络调用 |
|---|---|---|---:|---:|
| mlp_a2afm | 原128宽全连接残差网络 | FM+结果损失 | 86,296 | 8 |
| mlp_regression | 原128宽全连接残差网络 | 结果损失 | 82,712 | 1 |
| cnn_a2afm | 32通道时序CNN+全连接读出 | FM+结果损失 | 82,888 | 8 |
| cnn_regression | 同款CNN+全连接读出 | 结果损失 | 82,728 | 1 |

CNN包含3个残差块，每块两层kernel=3因果卷积，dilation依次1/2/4。仅左侧填充，感受野29覆盖24点历史。条件包括位置、速度、控制历史及已知物理参数；流模型额外输入中间状态和流时间特征。增加固定位置通道，保留窗口内时间位置。

卷积特征展平后经过80宽读出层映射到24点目标：输入是过去窗口，输出是当前至未来窗口，不能把卷积位置直接解释成同一物理时间的目标。因此这是CNN特征网络+全连接读出，不是纯全卷积输出。末端保留LayerNorm，源序列与FM损失完全沿用原定义，没有同时修改之前讨论的重尾起点问题。

流积分仍是**4步中点法、8次速度网络调用**。两种FM模型使用相同的流时间随机抽样；同一种子的四组模型使用相同批次索引顺序。相同训练步数、相近参数量，不等于相同FLOPs或训练耗时。

## 数据与冲击

- 系统：已知参数的二阶线性系统，采样dt=0.02s，每条轨迹12s；控制和扰动采样区间内保持常值，以矩阵指数精确推进状态。
- 控制是预先已知的正弦开环输入；测量a[k]使用u[k]，下一状态使用u[k]+d[k]推进，避免错用一拍前控制的残差。
- 背景为随机频率/相位的0.3幅值正弦。每条冲击轨迹含一正一负矩形脉冲，发生时刻随机；每次冲量绝对值J∈[0.15,0.35]，幅值=J/宽度。
- 训练96条、验证24条独立轨迹，均衡包含平滑、20ms、80ms、200ms四类。
- 测试72条独立轨迹，每类12条，包含平滑、20ms、40ms、80ms、120ms、200ms六类；40/120ms宽度不参与训练和验证。
- 未见宽度是脉冲宽度插值测试，不是对从未见过冲击的模型做零样本测试。
- 两种测量条件：x/v准确；x/v联合高斯噪声，σ为干净训练通道标准差的5%。加速度高斯噪声始终σ=0.5。相同的测量同时构造源残差与条件，真实状态和标签不被污染。
- 独立物理轨迹种子91000/92000/93000；传感器噪声种子基数101000/102000/103000。噪声实现固定，所有方法共享。
- 训练/验证/测试均用stride=1，避免漏评单采样脉冲。历史/目标长度仍为24；按未来标签长度省略轨迹末23点，但所有脉冲都完整位于评分区间。

每条训练轨迹产生两种观测版本，共106,560窗口，仍只有96条独立轨迹；验证26,640窗口，测试每条件39,960窗口。

## 训练与评价

三个模型种子11/22/33，每模型3000次AdamW更新，batch=128，lr=0.001，weight_decay=0.0001，梯度范数上限5。当前分量结果损失额外权重4；没有额外事件重采样或事件权重。每500步计算全部混合验证集当前扰动MSE并保存最佳模型。

新增对照保留原始残差、EMA、多传感器增广Kalman。EMA/Kalman仅在验证轨迹上按每个测量条件调参；其参数范围沿用multichannel模块。Kalman知道真实参数与测量噪声方差，神经网络不显式输入噪声幅度。

报告全时段RMSE、脉冲持续点RMSE、起点误差、冲击积分误差、峰值比例、冲击后0.5s误差和其余背景误差。脉冲指标按轨迹等权，不按宽度给长脉冲更大权重。峰值比例包含小幅背景，非纯脉冲增益。

对模型种子MSE平均后，在每个测试波形类别内部按轨迹配对Bootstrap 5000次。保持类别比例，不对重叠窗口独立重采样，区间未作多重比较校正。

在线耗时在全部训练worker退出后单独测量，CPU2线程、batch=1，预热30次，逐点处理两条完整轨迹（包含20ms与200ms脉冲）。包括历史更新、残差、归一化、网络/流积分、反归一化及输出；不含传感器/执行器通信与模型加载。报告median/P95/P99/max及超过20ms比例，不能据此证明硬实时或闭环稳定性。

## 运行与恢复

沿用现有Python3.12与requirements-lock.txt依赖。从项目根目录运行：

```bash
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export MPLCONFIGDIR="$PWD/.mplconfig"
mkdir -p "$MPLCONFIGDIR"
.venv/bin/python -m unittest test_core closed_loop.test_core multichannel.test_core cnn_experiment.test_core -v
.venv/bin/python -m cnn_experiment.experiment --out /tmp/cnn-impulses-reproduction
```

默认最多3个独立种子进程，每进程训练1线程；可用`--workers 1`顺序运行。输出目录必须为空。中断后以原参数加`--resume`恢复优化器、批次和流时间随机状态；源码及配置必须匹配。

快速流程检查（不能用于研究结论）：

```bash
.venv/bin/python -m cnn_experiment.experiment --out /tmp/cnn-impulses-smoke \
  --steps 2 --seeds 11 --train-trajectories 4 --val-trajectories 4 --test-trajectories 6 --workers 1
```

正式归档：[报告](../results/cnn-impulses-20261019/REPORT.md)、[结果解读](../results/cnn-impulses-20261019/ANALYSIS.md)。`status.json`应为complete。

核验本次正式归档可运行`.venv/bin/python scripts/validate_cnn_results.py`，检查源码摘要、12个模型的训练步数及最佳检查点、批次/流时间随机状态一致性、全部逐轨迹指标、完整脉冲采样覆盖，以及逐时刻接口与批量预测的一致性。该脚本针对本次固定的正式配置；单元测试另行运行，记录见结果目录的tests.log。

加载新模型使用专用接口（原有检查点接口保持不变）：

```python
from cnn_experiment.models import Estimator
est = Estimator('results/cnn-impulses-20261019/models/cnn_a2afm_seed11.pt')
# 每个数组是按时间排列的24点测量历史，params=[m,c,kappa]。
d_current, future = est.estimate(x_measured, v_measured, u, a_measured, params)
```

## 适用范围

本轮为开环估计，无闭环噪声反馈、无计算延迟注入、无异步/亚采样脉冲、无参数失配、无重尾噪声。20ms脉冲仍是有限宽度而非Dirac冲量。保持原有源码、模型及结果；只新增本模块及独立输出目录。
