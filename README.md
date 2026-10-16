# 二阶系统扰动估计：无隐空间 A2A Flow Matching

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
