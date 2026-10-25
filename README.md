# 二阶系统扰动估计：无隐空间 A2A Flow Matching

## 项目复盘与下一轮实验

| 文档 | 内容与状态 |
|---|---|
| [项目完整复盘（2026-10-25）](PROJECT_REVIEW_20261025.md) | 汇总各实验分支中已经完成的尝试、结果、适用边界和后续优先级；不同协议的结果不直接横向排名。 |
| [单步FM冲击优势实验协议](SINGLE_STEP_FM_SHOCK_PROTOCOL.md) | 同构残差回归、单步FM和重复端点监督对照的预注册方案：先比较同一观测流的冲击估计，再验证闭环收益。 |
| [单步FM冲击验证正式报告](results/shock_validation/REPORT.md) | 2026-10-25 已完成：3 套数据 × 3 配对种子，A/B/C 同构对照、固定权重闭环与 P50 延时复核。主比较未达 10% 门槛，按预注册规则未启动条件追加实验。数值表见 [TABLES.md](results/shock_validation/TABLES.md)。 |

## 单步 FM 冲击验证正式结果（2026-10-25）

按 [预注册协议](SINGLE_STEP_FM_SHOCK_PROTOCOL.md) 完成 A（同构残差回归）、B（单步 FM）、C（重复端点监督）三组对照，另加等优化耗时 A_time、直接回归、中点 FM、原始残差、EMA 和增广 Kalman。3 套独立训练数据 × 3 个配对权重种子，共享 720 条测试轨迹；所有主模型再做固定权重闭环和自身 P50 软件延时复核。

核心结果：

- B 对 A 的冲击 RMSE 仅改善 **1.58%**（97.5% 区间 [0.43, 2.63]），远低于预注册的 10% 门槛；背景 RMSE 恶化 **1.49%**。
- B 对 C 的冲击改善为 **-0.19%**（略差），背景恶化 **3.01%**；没有证据支持随机路径速度监督的独立优势。
- 固定权重闭环中 B 的 tracking RMSE 为 **0.0046799**，差于 A 的 0.0043803 和 C 的 0.0041600；B 对 A 的事件后 1 秒误差能量变化为 **-4.80%**。
- 原始残差和增广 Kalman 的冲击 RMSE 约 **0.50**，仍明显优于所有学习模型（0.68–0.77），但背景 RMSE 约 0.50，闭环控制抖动也更大。
- A_time（等优化耗时，约 21.6k–23.4k 次更新）冲击 0.702175、背景 0.113798，优于 A/B/C，提示计算预算本身能解释部分差异。

按协议未满足门槛，因此没有执行零源噪声消融和 D 组追加实验，也没有做测试驱动的调参或重选。完整解释、限制与复现方式见 [正式报告](results/shock_validation/REPORT.md)。

```powershell
.\.venv\Scripts\python.exe shock_validation_experiment.py --workers 3 --stage all
.\.venv\Scripts\python.exe shock_validation_delay.py
.\.venv\Scripts\python.exe analyze_shock_validation.py
.\.venv\Scripts\python.exe -m unittest test_shock_validation test_core test_single_step test_adaptation test_delayed closed_loop.test_core -v
```

## 闭环适配与计算延时复核

新增[闭环适配报告](results/closed_adaptation/REPORT.md)：比较冻结权重、仅闭环状态适配、闭环并加入冲击适配。
单步FM、多步FM和直接回归各3个种子，共享两轮360条闭环采集数据；每模型额外更新5000次。
按独立闭环验证集的跟踪误差选择权重，另用全新的混合/冲击测试轨迹评估。

[延时报告](results/computation_delay/REPORT.md)在上述训练完成后单独复核软件计算延时。
计算期间植物继续受旧控制驱动；小于周期的延时采用分段精确ZOH推进，超周期按单工作线程跳过新任务处理。

```powershell
.\.venv\Scripts\python.exe adaptation_experiment.py
.\.venv\Scripts\python.exe delay_experiment.py
.\.venv\Scripts\python.exe analyze_adaptation.py
.\.venv\Scripts\python.exe -m unittest test_adaptation test_delayed test_single_step test_core closed_loop.test_core -v
```

## 本分支：单次调用 FM 与五倍混合训练集

本分支新增独立实验 `single_step_experiment.py`。正式结果与完整报告位于
[`results/single_step_mixed/REPORT.md`](results/single_step_mixed/REPORT.md)，原 `results/main` 保留用于历史参考。

新预测为 `source + v_theta(source, condition, source, tau=0)`，结果损失和实际部署均只调用一次网络。
速度损失保持随机 tau 的线性插值监督。训练时，归一化后的 source 每次加入标准差 0.01 的独立高斯白噪声；
插值、目标速度和结果预测共用该 source，验证、测试与部署不加额外噪声。

训练轨迹从72条增至360条，包含原三类及两两/三者同时叠加的混合轨迹；验证90条，每噪声场景测试56条。
全部使用本地CPU。比较单次FM、原4步中点FM、直接回归、残差回归，均为宽128、两个残差块；
每个模型训练15000次更新、三个随机种子。另有因果滤波/物理基线、冻结权重闭环冲击测试和batch=1实测延迟。

```powershell
.\.venv\Scripts\python.exe -m unittest test_core test_single_step closed_loop.test_core -v
.\.venv\Scripts\python.exe single_step_experiment.py
.\.venv\Scripts\python.exe analyze_single_step.py
# 中断后：相同配置加 --resume；重评估：相同配置加 --evaluate-only
.\.venv\Scripts\python.exe demo.py --checkpoint results/single_step_mixed/single_fm/a2afm_seed11.pt
```

`DisturbanceEstimator`从检查点自动选择单步或中点预测，也支持残差回归；旧检查点保持原行为。
下面内容描述原有多步实验及其运行方式。

已完成的实验请先看 [RESULTS.md](RESULTS.md)。正式结果位于 `results/main`；`results/smoke` 仅供安装/流程调试，不作为结论依据。

## 研究问题

系统为 `m*x'' + c*x' + kappa*x = u(t,x,v) + d(t,x,v)`。仅加速度测量加入独立传感器噪声，准确可测的 x/v/u 和已知系统参数用于得到 `d_hat=m*a_measured+c*v+kappa*x-u`。

本实现严格采用用户指定的过去到未来映射：`source=[d_hat(t-k),...,d_hat(t)]`，`target=[d(t),...,d(t+k)]`，两者长度均为 L=k+1。训练、应用的条件只有截至 t 的 x/v/u 历史以及 `[m,c,kappa]`。应用取输出索引 0，即当前 d(t)。其余分量是辅助预测任务。默认 dt=0.02 s，L=24（历史覆盖 0.46 秒，未来覆盖 0.46 秒）。

参考：[A2A 仓库](https://github.com/JIAjindou/A2A_Flow_Matching) 的 `roboverse_learn/il/policies/a2a/a2a_policy.py`，重点核对 `compute_loss` 的未来起点 `n_obs_steps-1` 和 `predict_action`。原实现包含历史/动作编码器；本项目独立重写为直接扰动空间，不使用其机器人仿真依赖。网页读取日期 2026-10-13；Git clone 因证书信任错误未成功，因此未声称固定了上游 commit。

## FM 定义

用 tau 表示流时间，避免与物理时间 t 混淆：

```
z_tau=(1-tau)*source+tau*target
v_target=target-source
L_FM = mean((v_theta(z_tau,tau,source,condition)-v_target)^2)
prediction = MidpointODE(v_theta, initial=source, tau=0..1)
L_result = MSE(prediction,target)+4*MSE(prediction[:,0],target[:,0])
L_total = L_FM+L_result
```

ODE 默认中点积分 4 步（8 次网络求值），训练时允许梯度穿过积分器；结果损失不是把真值混入推理输入的单步代理。网络是 128 宽、两个残差块的全连接时序窗口网络，所有历史位置可交互；流状态始终为 R^L。网络内部隐藏层不代表单独的潜空间流。归一化只拟合训练数据。

给定一份完整观测历史后，当前实现的输出是确定性的；它用于点估计，不声称提供真实条件后验采样或校准的不确定度。与参考仓库的 Euler 积分不同，这里选用中点积分，并额外报告 1/2/4/8/16 步的一致性检查。

直接回归网络采用同宽同深结构、同一输入信息和相同结果损失，直接输出未来片段。它与 FM 使用相同训练更新数，但 FM 每次更新计算量更大，不能称为等算力比较。`fm_only` 消融去掉结果损失。

## 运行

推荐 Python 3.12，依赖见 requirements.txt。当前项目使用 `.venv`。

```powershell
.\.venv\Scripts\python.exe -m unittest test_core -v
.\.venv\Scripts\python.exe experiment.py --out results/main --steps 3000 --seeds 11 22 33 --ablation
.\.venv\Scripts\python.exe experiment.py --out results/main --steps 3000 --seeds 11 22 33 --ablation --resume
.\.venv\Scripts\python.exe demo.py --checkpoint results/main/a2afm_seed11.pt
.\.venv\Scripts\python.exe analyze_results.py --out results/main
```

检查点每 100 步保存，包括优化器和随机数状态；最佳模型只按验证集当前时刻 RMSE 选择。恢复时使用原训练参数。训练不需要在线模型服务；代码执行与 Codex 对话额度是不同资源，但本机必须保持运行。

## 自定义方程

`a2afm.system.Plant` 提供 m/c/kappa 和等价状态矩阵 `A=[[0,1],[-kappa/m,-c/m]]`。同时保留 m 是必要的，因为输入增益为 1/m，单独 A 不能唯一确定它。

```python
from a2afm.system import Plant, simulate
import numpy as np
u = lambda t,x,v: np.sin(t) - 0.2*v
d = lambda t,x,v: 0.5*np.cos(2*t)
trajectory = simulate(Plant(m=1,c=.6,kappa=2),u,d,sigma_a=.5)
```

修改扰动/控制分布后，需要生成相应训练轨迹再训练；支持传入函数不意味着已训练模型能泛化到任意函数。非线性植物需要同时修改动力学、反演公式和条件编码，当前版本只承诺线性带阻尼系统。

## 评价与边界

- 72 条训练、18 条验证、24 条测试轨迹（默认），按完整轨迹隔离；多正弦、chirp、阶跃加正弦均在训练中出现。
- 高斯加速度噪声标准差 0.2/0.5/0.9，另测试同方差 Student-t(3) 噪声；后者是噪声分布 OOD。
- EMA、因果局部多项式和扰动/扰动导数 Kalman 滤波在验证集上调参。Kalman 使用已知传感器噪声尺度。
- `physics_backward` 用准确速度的二阶后向差分估计加速度。这一强基线可能优于所有去噪网络，必须如实报告。
- 主要指标只针对当前 d(t)，不把未来预测误差混入去噪 RMSE；曲线没有使用未来观测或零相位滤波。
- 训练种子重复共享同一数据集；报告均值/标准差，不等于独立数据集重复或显著性检验。
- EMA/Kalman 持续保留过去的滤波状态，神经网络只使用固定长度窗口；所有方法均因果，但有效历史长度不同。此处比较的是实际可用估计器，不宣称完全相同的计算量或内存预算。

输出目录包含配置、环境信息、训练曲线、最佳和末次权重、逐轨迹/分类指标、预测 NPZ、积分步数检查和中文 REPORT.md。WORK_LOG.md 自动记录阶段、训练进度和完成时间（UTC+8）。
