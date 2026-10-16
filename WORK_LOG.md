# 工作日志（北京时间 UTC+8）

## 2026-10-13：需求确认与环境准备
- 已确认：主实验为过去到未来：d_hat[t-k:t] -> d[t:t+k]，只取首项作为当前扰动估计。
- 已确认：m*x''+c*x'+kappa*x=u+d，仅加速度含噪声；x、v、u、系统参数准确已知。
- 计划：建立可配置仿真、直接信号空间条件 FM、训练/评估、滤波与神经网络基线、图表和报告。
- 已完成：空目录检查；找到可用 Python 3.12；启动项目虚拟环境依赖安装。
- 已完成：读取参考仓库 README 与 a2a_policy.py，核对历史包含当前、未来从当前开始的索引。
- 问题：Git clone 因本机证书信任失败，使用公开源码页面核对；额度接口未返回数据。
- 实验注意：精确速度历史允许物理差分估计扰动，必须报告该强基线，不能预设 FM 最好。
- 后续每阶段由脚本自动追加精确时间戳；初始准备时未采集具体时分，不伪造时间。

- [2026-10-13T23:04:24.584176+08:00] 完成系统、FM、训练、评估、因果滤波基线、应用接口和检查脚本；语法检查通过；解析解最大误差 6.03e-12。依赖大文件传输慢，改用官方分块下载并验证哈希。

- [2026-10-13 23:09:30 UTC+8] 开始实验 results/smoke；设备 cpu；计划训练 A2AFM/直接回归，评估滤波和物理基线

- [2026-10-13 23:09:33 UTC+8] 数据完成：训练窗口 2268，验证窗口 3402；滤波参数 {'ema': 0.2, 'local_poly': 23, 'kalman': 10000.0}

- [2026-10-13 23:09:38 UTC+8] a2afm seed=11 step=100/100 val_RMSE=0.33180 best=0.33180

- [2026-10-13 23:09:38 UTC+8] 完成 a2afm seed=11，本轮耗时 2.3 s，选择验证最优 step=100

- [2026-10-13 23:09:38 UTC+8] regression seed=11 step=100/100 val_RMSE=0.32717 best=0.32717

- [2026-10-13 23:09:38 UTC+8] 完成 regression seed=11，本轮耗时 0.5 s，选择验证最优 step=100

- [2026-10-13 23:09:39 UTC+8] fm_only seed=11 step=100/100 val_RMSE=0.40763 best=0.40763

- [2026-10-13 23:09:39 UTC+8] 完成 fm_only seed=11，本轮耗时 0.5 s，选择验证最优 step=100

- [2026-10-13 23:09:39 UTC+8] 训练完成，开始冻结测试集评估与积分步数检查

- [2026-10-13 23:09:43 UTC+8] 实验完成：E:\desktop\MyDataBase\A2AFM\results\smoke\REPORT.md

- [2026-10-13 23:10:06 UTC+8] 开始实验 results/main；设备 cpu；计划训练 A2AFM/直接回归，评估滤波和物理基线

- [2026-10-13 23:10:16 UTC+8] 数据完成：训练窗口 27216，验证窗口 3402；滤波参数 {'ema': 0.2, 'local_poly': 23, 'kalman': 10000.0}

- [2026-10-13 23:10:20 UTC+8] a2afm seed=11 step=100/3000 val_RMSE=0.30125 best=0.30125

- [2026-10-13 23:10:22 UTC+8] a2afm seed=11 step=200/3000 val_RMSE=0.27800 best=0.27800

- [2026-10-13 23:10:24 UTC+8] a2afm seed=11 step=300/3000 val_RMSE=0.26789 best=0.26789

- [2026-10-13 23:10:26 UTC+8] a2afm seed=11 step=400/3000 val_RMSE=0.26859 best=0.26789

- [2026-10-13 23:10:28 UTC+8] a2afm seed=11 step=500/3000 val_RMSE=0.25768 best=0.25768

- [2026-10-13 23:10:31 UTC+8] a2afm seed=11 step=600/3000 val_RMSE=0.25250 best=0.25250

- [2026-10-13 23:10:33 UTC+8] a2afm seed=11 step=700/3000 val_RMSE=0.25875 best=0.25250

- [2026-10-13 23:10:35 UTC+8] a2afm seed=11 step=800/3000 val_RMSE=0.24028 best=0.24028

- [2026-10-13 23:10:37 UTC+8] a2afm seed=11 step=900/3000 val_RMSE=0.24810 best=0.24028

- [2026-10-13 23:10:39 UTC+8] a2afm seed=11 step=1000/3000 val_RMSE=0.23517 best=0.23517

- [2026-10-13 23:10:41 UTC+8] a2afm seed=11 step=1100/3000 val_RMSE=0.23567 best=0.23517

- [2026-10-13 23:10:43 UTC+8] a2afm seed=11 step=1200/3000 val_RMSE=0.22433 best=0.22433

- [2026-10-13 23:10:46 UTC+8] a2afm seed=11 step=1300/3000 val_RMSE=0.22085 best=0.22085

- [2026-10-13 23:10:51 UTC+8] 开始实验 results/main；设备 cpu；计划训练 A2AFM/直接回归，评估滤波和物理基线

- [2026-10-13 23:11:01 UTC+8] 数据完成：训练窗口 27216，验证窗口 3402；滤波参数 {'ema': 0.2, 'local_poly': 23, 'kalman': 10000.0}

- [2026-10-13 23:11:03 UTC+8] 恢复 a2afm seed=11，训练步数 1300

- [2026-10-13 23:11:05 UTC+8] a2afm seed=11 step=1400/3000 val_RMSE=0.21528 best=0.21528

- [2026-10-13 23:11:07 UTC+8] a2afm seed=11 step=1500/3000 val_RMSE=0.21889 best=0.21528

- [2026-10-13 23:11:09 UTC+8] a2afm seed=11 step=1600/3000 val_RMSE=0.21345 best=0.21345

- [2026-10-13 23:11:11 UTC+8] a2afm seed=11 step=1700/3000 val_RMSE=0.21325 best=0.21325

- [2026-10-13 23:11:14 UTC+8] a2afm seed=11 step=1800/3000 val_RMSE=0.20750 best=0.20750

- [2026-10-13 23:11:16 UTC+8] a2afm seed=11 step=1900/3000 val_RMSE=0.20418 best=0.20418

- [2026-10-13 23:11:18 UTC+8] a2afm seed=11 step=2000/3000 val_RMSE=0.19451 best=0.19451

- [2026-10-13 23:11:20 UTC+8] a2afm seed=11 step=2100/3000 val_RMSE=0.20652 best=0.19451

- [2026-10-13 23:11:22 UTC+8] a2afm seed=11 step=2200/3000 val_RMSE=0.19302 best=0.19302

- [2026-10-13 23:11:24 UTC+8] a2afm seed=11 step=2300/3000 val_RMSE=0.20857 best=0.19302

- [2026-10-13 23:11:26 UTC+8] a2afm seed=11 step=2400/3000 val_RMSE=0.19036 best=0.19036

- [2026-10-13 23:11:28 UTC+8] a2afm seed=11 step=2500/3000 val_RMSE=0.19034 best=0.19034

- [2026-10-13 23:11:30 UTC+8] a2afm seed=11 step=2600/3000 val_RMSE=0.19153 best=0.19034

- [2026-10-13 23:11:32 UTC+8] a2afm seed=11 step=2700/3000 val_RMSE=0.19109 best=0.19034

- [2026-10-13 23:11:35 UTC+8] a2afm seed=11 step=2800/3000 val_RMSE=0.18897 best=0.18897

- [2026-10-13 23:11:37 UTC+8] a2afm seed=11 step=2900/3000 val_RMSE=0.18798 best=0.18798

- [2026-10-13 23:11:39 UTC+8] a2afm seed=11 step=3000/3000 val_RMSE=0.18343 best=0.18343

- [2026-10-13 23:11:39 UTC+8] 完成 a2afm seed=11，本轮耗时 36.2 s，选择验证最优 step=3000

- [2026-10-13 23:11:39 UTC+8] regression seed=11 step=100/3000 val_RMSE=0.27859 best=0.27859

- [2026-10-13 23:11:40 UTC+8] regression seed=11 step=200/3000 val_RMSE=0.29040 best=0.27859

- [2026-10-13 23:11:40 UTC+8] regression seed=11 step=300/3000 val_RMSE=0.27326 best=0.27326

- [2026-10-13 23:11:41 UTC+8] regression seed=11 step=400/3000 val_RMSE=0.26818 best=0.26818

- [2026-10-13 23:11:41 UTC+8] regression seed=11 step=500/3000 val_RMSE=0.26402 best=0.26402

- [2026-10-13 23:11:42 UTC+8] regression seed=11 step=600/3000 val_RMSE=0.26843 best=0.26402

- [2026-10-13 23:11:42 UTC+8] regression seed=11 step=700/3000 val_RMSE=0.26191 best=0.26191

- [2026-10-13 23:11:43 UTC+8] regression seed=11 step=800/3000 val_RMSE=0.26227 best=0.26191

- [2026-10-13 23:11:43 UTC+8] regression seed=11 step=900/3000 val_RMSE=0.25991 best=0.25991

- [2026-10-13 23:11:44 UTC+8] regression seed=11 step=1000/3000 val_RMSE=0.25010 best=0.25010

- [2026-10-13 23:11:44 UTC+8] regression seed=11 step=1100/3000 val_RMSE=0.23827 best=0.23827

- [2026-10-13 23:11:45 UTC+8] regression seed=11 step=1200/3000 val_RMSE=0.22994 best=0.22994

- [2026-10-13 23:11:45 UTC+8] regression seed=11 step=1300/3000 val_RMSE=0.22061 best=0.22061

- [2026-10-13 23:11:46 UTC+8] regression seed=11 step=1400/3000 val_RMSE=0.23470 best=0.22061

- [2026-10-13 23:11:46 UTC+8] regression seed=11 step=1500/3000 val_RMSE=0.21341 best=0.21341

- [2026-10-13 23:11:47 UTC+8] regression seed=11 step=1600/3000 val_RMSE=0.20903 best=0.20903

- [2026-10-13 23:11:47 UTC+8] regression seed=11 step=1700/3000 val_RMSE=0.21314 best=0.20903

- [2026-10-13 23:11:47 UTC+8] regression seed=11 step=1800/3000 val_RMSE=0.20227 best=0.20227

- [2026-10-13 23:11:48 UTC+8] regression seed=11 step=1900/3000 val_RMSE=0.21911 best=0.20227

- [2026-10-13 23:11:48 UTC+8] regression seed=11 step=2000/3000 val_RMSE=0.20137 best=0.20137

- [2026-10-13 23:11:49 UTC+8] regression seed=11 step=2100/3000 val_RMSE=0.20396 best=0.20137

- [2026-10-13 23:11:49 UTC+8] regression seed=11 step=2200/3000 val_RMSE=0.19784 best=0.19784

- [2026-10-13 23:11:50 UTC+8] regression seed=11 step=2300/3000 val_RMSE=0.19445 best=0.19445

- [2026-10-13 23:11:50 UTC+8] regression seed=11 step=2400/3000 val_RMSE=0.20042 best=0.19445

- [2026-10-13 23:11:51 UTC+8] regression seed=11 step=2500/3000 val_RMSE=0.18331 best=0.18331

- [2026-10-13 23:11:51 UTC+8] regression seed=11 step=2600/3000 val_RMSE=0.18435 best=0.18331

- [2026-10-13 23:11:52 UTC+8] regression seed=11 step=2700/3000 val_RMSE=0.19323 best=0.18331

- [2026-10-13 23:11:52 UTC+8] regression seed=11 step=2800/3000 val_RMSE=0.19916 best=0.18331

- [2026-10-13 23:11:53 UTC+8] regression seed=11 step=2900/3000 val_RMSE=0.20890 best=0.18331

- [2026-10-13 23:11:53 UTC+8] regression seed=11 step=3000/3000 val_RMSE=0.18028 best=0.18028

- [2026-10-13 23:11:53 UTC+8] 完成 regression seed=11，本轮耗时 14.2 s，选择验证最优 step=3000

- [2026-10-13 23:11:54 UTC+8] fm_only seed=11 step=100/3000 val_RMSE=0.36431 best=0.36431

- [2026-10-13 23:11:54 UTC+8] fm_only seed=11 step=200/3000 val_RMSE=0.32794 best=0.32794

- [2026-10-13 23:11:55 UTC+8] fm_only seed=11 step=300/3000 val_RMSE=0.32463 best=0.32463

- [2026-10-13 23:11:55 UTC+8] fm_only seed=11 step=400/3000 val_RMSE=0.35038 best=0.32463

- [2026-10-13 23:11:56 UTC+8] fm_only seed=11 step=500/3000 val_RMSE=0.30291 best=0.30291

- [2026-10-13 23:11:56 UTC+8] fm_only seed=11 step=600/3000 val_RMSE=0.30680 best=0.30291

- [2026-10-13 23:11:57 UTC+8] fm_only seed=11 step=700/3000 val_RMSE=0.30345 best=0.30291

- [2026-10-13 23:11:57 UTC+8] fm_only seed=11 step=800/3000 val_RMSE=0.33830 best=0.30291

- [2026-10-13 23:11:58 UTC+8] fm_only seed=11 step=900/3000 val_RMSE=0.32312 best=0.30291

- [2026-10-13 23:11:58 UTC+8] fm_only seed=11 step=1000/3000 val_RMSE=0.29842 best=0.29842

- [2026-10-13 23:11:59 UTC+8] fm_only seed=11 step=1100/3000 val_RMSE=0.30638 best=0.29842

- [2026-10-13 23:12:00 UTC+8] fm_only seed=11 step=1200/3000 val_RMSE=0.30276 best=0.29842

- [2026-10-13 23:12:00 UTC+8] fm_only seed=11 step=1300/3000 val_RMSE=0.29246 best=0.29246

- [2026-10-13 23:12:01 UTC+8] fm_only seed=11 step=1400/3000 val_RMSE=0.31361 best=0.29246

- [2026-10-13 23:12:01 UTC+8] fm_only seed=11 step=1500/3000 val_RMSE=0.41506 best=0.29246

- [2026-10-13 23:12:02 UTC+8] fm_only seed=11 step=1600/3000 val_RMSE=0.29383 best=0.29246

- [2026-10-13 23:12:02 UTC+8] fm_only seed=11 step=1700/3000 val_RMSE=0.27470 best=0.27470

- [2026-10-13 23:12:03 UTC+8] fm_only seed=11 step=1800/3000 val_RMSE=0.30113 best=0.27470

- [2026-10-13 23:12:03 UTC+8] fm_only seed=11 step=1900/3000 val_RMSE=0.29430 best=0.27470

- [2026-10-13 23:12:04 UTC+8] fm_only seed=11 step=2000/3000 val_RMSE=0.33004 best=0.27470

- [2026-10-13 23:12:04 UTC+8] fm_only seed=11 step=2100/3000 val_RMSE=0.30287 best=0.27470

- [2026-10-13 23:12:05 UTC+8] fm_only seed=11 step=2200/3000 val_RMSE=0.28891 best=0.27470

- [2026-10-13 23:12:06 UTC+8] fm_only seed=11 step=2300/3000 val_RMSE=0.27396 best=0.27396

- [2026-10-13 23:12:06 UTC+8] fm_only seed=11 step=2400/3000 val_RMSE=0.32098 best=0.27396

- [2026-10-13 23:12:07 UTC+8] fm_only seed=11 step=2500/3000 val_RMSE=0.27395 best=0.27395

- [2026-10-13 23:12:07 UTC+8] fm_only seed=11 step=2600/3000 val_RMSE=0.28385 best=0.27395

- [2026-10-13 23:12:08 UTC+8] fm_only seed=11 step=2700/3000 val_RMSE=0.27862 best=0.27395

- [2026-10-13 23:12:08 UTC+8] fm_only seed=11 step=2800/3000 val_RMSE=0.28527 best=0.27395

- [2026-10-13 23:12:09 UTC+8] fm_only seed=11 step=2900/3000 val_RMSE=0.25970 best=0.25970

- [2026-10-13 23:12:09 UTC+8] fm_only seed=11 step=3000/3000 val_RMSE=0.27978 best=0.25970

- [2026-10-13 23:12:09 UTC+8] 完成 fm_only seed=11，本轮耗时 16.3 s，选择验证最优 step=2900

- [2026-10-13 23:12:12 UTC+8] a2afm seed=22 step=100/3000 val_RMSE=0.29860 best=0.29860

- [2026-10-13 23:12:14 UTC+8] a2afm seed=22 step=200/3000 val_RMSE=0.28895 best=0.28895

- [2026-10-13 23:12:16 UTC+8] a2afm seed=22 step=300/3000 val_RMSE=0.28222 best=0.28222

- [2026-10-13 23:12:18 UTC+8] a2afm seed=22 step=400/3000 val_RMSE=0.26786 best=0.26786

- [2026-10-13 23:12:21 UTC+8] a2afm seed=22 step=500/3000 val_RMSE=0.27428 best=0.26786

- [2026-10-13 23:12:23 UTC+8] a2afm seed=22 step=600/3000 val_RMSE=0.26914 best=0.26786

- [2026-10-13 23:12:25 UTC+8] a2afm seed=22 step=700/3000 val_RMSE=0.25262 best=0.25262

- [2026-10-13 23:12:27 UTC+8] a2afm seed=22 step=800/3000 val_RMSE=0.24005 best=0.24005

- [2026-10-13 23:12:29 UTC+8] a2afm seed=22 step=900/3000 val_RMSE=0.23507 best=0.23507

- [2026-10-13 23:12:32 UTC+8] a2afm seed=22 step=1000/3000 val_RMSE=0.24428 best=0.23507

- [2026-10-13 23:12:34 UTC+8] a2afm seed=22 step=1100/3000 val_RMSE=0.23143 best=0.23143

- [2026-10-13 23:12:36 UTC+8] a2afm seed=22 step=1200/3000 val_RMSE=0.22365 best=0.22365

- [2026-10-13 23:12:38 UTC+8] a2afm seed=22 step=1300/3000 val_RMSE=0.24341 best=0.22365

- [2026-10-13 23:12:40 UTC+8] a2afm seed=22 step=1400/3000 val_RMSE=0.22596 best=0.22365

- [2026-10-13 23:12:43 UTC+8] a2afm seed=22 step=1500/3000 val_RMSE=0.21656 best=0.21656

- [2026-10-13 23:12:45 UTC+8] a2afm seed=22 step=1600/3000 val_RMSE=0.23074 best=0.21656

- [2026-10-13 23:12:47 UTC+8] a2afm seed=22 step=1700/3000 val_RMSE=0.20308 best=0.20308

- [2026-10-13 23:12:49 UTC+8] a2afm seed=22 step=1800/3000 val_RMSE=0.22161 best=0.20308

- [2026-10-13 23:12:51 UTC+8] a2afm seed=22 step=1900/3000 val_RMSE=0.20952 best=0.20308

- [2026-10-13 23:12:53 UTC+8] a2afm seed=22 step=2000/3000 val_RMSE=0.22301 best=0.20308

- [2026-10-13 23:12:56 UTC+8] a2afm seed=22 step=2100/3000 val_RMSE=0.20395 best=0.20308

- [2026-10-13 23:12:58 UTC+8] a2afm seed=22 step=2200/3000 val_RMSE=0.19008 best=0.19008

- [2026-10-13 23:13:00 UTC+8] a2afm seed=22 step=2300/3000 val_RMSE=0.21119 best=0.19008

- [2026-10-13 23:13:02 UTC+8] a2afm seed=22 step=2400/3000 val_RMSE=0.21530 best=0.19008

- [2026-10-13 23:13:04 UTC+8] a2afm seed=22 step=2500/3000 val_RMSE=0.19618 best=0.19008

- [2026-10-13 23:13:06 UTC+8] a2afm seed=22 step=2600/3000 val_RMSE=0.18840 best=0.18840

- [2026-10-13 23:13:09 UTC+8] a2afm seed=22 step=2700/3000 val_RMSE=0.19356 best=0.18840

- [2026-10-13 23:13:11 UTC+8] a2afm seed=22 step=2800/3000 val_RMSE=0.19792 best=0.18840

- [2026-10-13 23:13:13 UTC+8] a2afm seed=22 step=2900/3000 val_RMSE=0.19925 best=0.18840

- [2026-10-13 23:13:15 UTC+8] a2afm seed=22 step=3000/3000 val_RMSE=0.18204 best=0.18204

- [2026-10-13 23:13:15 UTC+8] 完成 a2afm seed=22，本轮耗时 65.7 s，选择验证最优 step=3000

- [2026-10-13 23:13:16 UTC+8] regression seed=22 step=100/3000 val_RMSE=0.28279 best=0.28279

- [2026-10-13 23:13:16 UTC+8] regression seed=22 step=200/3000 val_RMSE=0.28039 best=0.28039

- [2026-10-13 23:13:16 UTC+8] regression seed=22 step=300/3000 val_RMSE=0.27367 best=0.27367

- [2026-10-13 23:13:17 UTC+8] regression seed=22 step=400/3000 val_RMSE=0.27522 best=0.27367

- [2026-10-13 23:13:17 UTC+8] regression seed=22 step=500/3000 val_RMSE=0.27064 best=0.27064

- [2026-10-13 23:13:18 UTC+8] regression seed=22 step=600/3000 val_RMSE=0.27029 best=0.27029

- [2026-10-13 23:13:18 UTC+8] regression seed=22 step=700/3000 val_RMSE=0.26044 best=0.26044

- [2026-10-13 23:13:19 UTC+8] regression seed=22 step=800/3000 val_RMSE=0.26119 best=0.26044

- [2026-10-13 23:13:19 UTC+8] regression seed=22 step=900/3000 val_RMSE=0.25576 best=0.25576

- [2026-10-13 23:13:20 UTC+8] regression seed=22 step=1000/3000 val_RMSE=0.24985 best=0.24985

- [2026-10-13 23:13:20 UTC+8] regression seed=22 step=1100/3000 val_RMSE=0.24379 best=0.24379

- [2026-10-13 23:13:21 UTC+8] regression seed=22 step=1200/3000 val_RMSE=0.24582 best=0.24379

- [2026-10-13 23:13:21 UTC+8] regression seed=22 step=1300/3000 val_RMSE=0.24246 best=0.24246

- [2026-10-13 23:13:22 UTC+8] regression seed=22 step=1400/3000 val_RMSE=0.21721 best=0.21721

- [2026-10-13 23:13:22 UTC+8] regression seed=22 step=1500/3000 val_RMSE=0.20876 best=0.20876

- [2026-10-13 23:13:23 UTC+8] regression seed=22 step=1600/3000 val_RMSE=0.21123 best=0.20876

- [2026-10-13 23:13:23 UTC+8] regression seed=22 step=1700/3000 val_RMSE=0.21103 best=0.20876

- [2026-10-13 23:13:23 UTC+8] regression seed=22 step=1800/3000 val_RMSE=0.21059 best=0.20876

- [2026-10-13 23:13:24 UTC+8] regression seed=22 step=1900/3000 val_RMSE=0.20564 best=0.20564

- [2026-10-13 23:13:24 UTC+8] regression seed=22 step=2000/3000 val_RMSE=0.19883 best=0.19883

- [2026-10-13 23:13:25 UTC+8] regression seed=22 step=2100/3000 val_RMSE=0.19659 best=0.19659

- [2026-10-13 23:13:25 UTC+8] regression seed=22 step=2200/3000 val_RMSE=0.19025 best=0.19025

- [2026-10-13 23:13:26 UTC+8] regression seed=22 step=2300/3000 val_RMSE=0.18833 best=0.18833

- [2026-10-13 23:13:26 UTC+8] regression seed=22 step=2400/3000 val_RMSE=0.21636 best=0.18833

- [2026-10-13 23:13:27 UTC+8] regression seed=22 step=2500/3000 val_RMSE=0.19051 best=0.18833

- [2026-10-13 23:13:27 UTC+8] regression seed=22 step=2600/3000 val_RMSE=0.18656 best=0.18656

- [2026-10-13 23:13:28 UTC+8] regression seed=22 step=2700/3000 val_RMSE=0.19634 best=0.18656

- [2026-10-13 23:13:28 UTC+8] regression seed=22 step=2800/3000 val_RMSE=0.18458 best=0.18458

- [2026-10-13 23:13:29 UTC+8] regression seed=22 step=2900/3000 val_RMSE=0.18148 best=0.18148

- [2026-10-13 23:13:29 UTC+8] regression seed=22 step=3000/3000 val_RMSE=0.18374 best=0.18148

- [2026-10-13 23:13:29 UTC+8] 完成 regression seed=22，本轮耗时 13.9 s，选择验证最优 step=2900

- [2026-10-13 23:13:30 UTC+8] fm_only seed=22 step=100/3000 val_RMSE=0.38047 best=0.38047

- [2026-10-13 23:13:30 UTC+8] fm_only seed=22 step=200/3000 val_RMSE=0.34644 best=0.34644

- [2026-10-13 23:13:31 UTC+8] fm_only seed=22 step=300/3000 val_RMSE=0.34027 best=0.34027

- [2026-10-13 23:13:31 UTC+8] fm_only seed=22 step=400/3000 val_RMSE=0.34499 best=0.34027

- [2026-10-13 23:13:32 UTC+8] fm_only seed=22 step=500/3000 val_RMSE=0.32408 best=0.32408

- [2026-10-13 23:13:32 UTC+8] fm_only seed=22 step=600/3000 val_RMSE=0.31371 best=0.31371

- [2026-10-13 23:13:33 UTC+8] fm_only seed=22 step=700/3000 val_RMSE=0.32392 best=0.31371

- [2026-10-13 23:13:33 UTC+8] fm_only seed=22 step=800/3000 val_RMSE=0.33127 best=0.31371

- [2026-10-13 23:13:34 UTC+8] fm_only seed=22 step=900/3000 val_RMSE=0.32019 best=0.31371

- [2026-10-13 23:13:35 UTC+8] fm_only seed=22 step=1000/3000 val_RMSE=0.30827 best=0.30827

- [2026-10-13 23:13:35 UTC+8] fm_only seed=22 step=1100/3000 val_RMSE=0.30433 best=0.30433

- [2026-10-13 23:13:36 UTC+8] fm_only seed=22 step=1200/3000 val_RMSE=0.30259 best=0.30259

- [2026-10-13 23:13:36 UTC+8] fm_only seed=22 step=1300/3000 val_RMSE=0.28828 best=0.28828

- [2026-10-13 23:13:37 UTC+8] fm_only seed=22 step=1400/3000 val_RMSE=0.29573 best=0.28828

- [2026-10-13 23:13:37 UTC+8] fm_only seed=22 step=1500/3000 val_RMSE=0.32966 best=0.28828

- [2026-10-13 23:13:38 UTC+8] fm_only seed=22 step=1600/3000 val_RMSE=0.29586 best=0.28828

- [2026-10-13 23:13:38 UTC+8] fm_only seed=22 step=1700/3000 val_RMSE=0.29948 best=0.28828

- [2026-10-13 23:13:39 UTC+8] fm_only seed=22 step=1800/3000 val_RMSE=0.31795 best=0.28828

- [2026-10-13 23:13:39 UTC+8] fm_only seed=22 step=1900/3000 val_RMSE=0.27324 best=0.27324

- [2026-10-13 23:13:40 UTC+8] fm_only seed=22 step=2000/3000 val_RMSE=0.30116 best=0.27324

- [2026-10-13 23:13:41 UTC+8] fm_only seed=22 step=2100/3000 val_RMSE=0.29743 best=0.27324

- [2026-10-13 23:13:41 UTC+8] fm_only seed=22 step=2200/3000 val_RMSE=0.30069 best=0.27324

- [2026-10-13 23:13:42 UTC+8] fm_only seed=22 step=2300/3000 val_RMSE=0.33760 best=0.27324

- [2026-10-13 23:13:42 UTC+8] fm_only seed=22 step=2400/3000 val_RMSE=0.29608 best=0.27324

- [2026-10-13 23:13:43 UTC+8] fm_only seed=22 step=2500/3000 val_RMSE=0.29143 best=0.27324

- [2026-10-13 23:13:44 UTC+8] fm_only seed=22 step=2600/3000 val_RMSE=0.33220 best=0.27324

- [2026-10-13 23:13:44 UTC+8] fm_only seed=22 step=2700/3000 val_RMSE=0.29339 best=0.27324

- [2026-10-13 23:13:45 UTC+8] fm_only seed=22 step=2800/3000 val_RMSE=0.32992 best=0.27324

- [2026-10-13 23:13:45 UTC+8] fm_only seed=22 step=2900/3000 val_RMSE=0.30887 best=0.27324

- [2026-10-13 23:13:46 UTC+8] fm_only seed=22 step=3000/3000 val_RMSE=0.28847 best=0.27324

- [2026-10-13 23:13:46 UTC+8] 完成 fm_only seed=22，本轮耗时 16.7 s，选择验证最优 step=1900

- [2026-10-13 23:13:48 UTC+8] a2afm seed=33 step=100/3000 val_RMSE=0.29728 best=0.29728

- [2026-10-13 23:13:50 UTC+8] a2afm seed=33 step=200/3000 val_RMSE=0.28965 best=0.28965

- [2026-10-13 23:13:52 UTC+8] a2afm seed=33 step=300/3000 val_RMSE=0.27626 best=0.27626

- [2026-10-13 23:13:54 UTC+8] a2afm seed=33 step=400/3000 val_RMSE=0.27197 best=0.27197

- [2026-10-13 23:13:56 UTC+8] a2afm seed=33 step=500/3000 val_RMSE=0.25569 best=0.25569

- [2026-10-13 23:13:59 UTC+8] a2afm seed=33 step=600/3000 val_RMSE=0.26346 best=0.25569

- [2026-10-13 23:14:01 UTC+8] a2afm seed=33 step=700/3000 val_RMSE=0.26048 best=0.25569

- [2026-10-13 23:14:03 UTC+8] a2afm seed=33 step=800/3000 val_RMSE=0.24507 best=0.24507

- [2026-10-13 23:14:06 UTC+8] a2afm seed=33 step=900/3000 val_RMSE=0.23916 best=0.23916

- [2026-10-13 23:14:08 UTC+8] a2afm seed=33 step=1000/3000 val_RMSE=0.23761 best=0.23761

- [2026-10-13 23:14:10 UTC+8] a2afm seed=33 step=1100/3000 val_RMSE=0.22927 best=0.22927

- [2026-10-13 23:14:13 UTC+8] a2afm seed=33 step=1200/3000 val_RMSE=0.21801 best=0.21801

- [2026-10-13 23:14:15 UTC+8] a2afm seed=33 step=1300/3000 val_RMSE=0.22733 best=0.21801

- [2026-10-13 23:14:18 UTC+8] a2afm seed=33 step=1400/3000 val_RMSE=0.21987 best=0.21801

- [2026-10-13 23:14:21 UTC+8] a2afm seed=33 step=1500/3000 val_RMSE=0.21077 best=0.21077

- [2026-10-13 23:14:23 UTC+8] a2afm seed=33 step=1600/3000 val_RMSE=0.21360 best=0.21077

- [2026-10-13 23:14:25 UTC+8] a2afm seed=33 step=1700/3000 val_RMSE=0.20865 best=0.20865

- [2026-10-13 23:14:27 UTC+8] a2afm seed=33 step=1800/3000 val_RMSE=0.20365 best=0.20365

- [2026-10-13 23:14:29 UTC+8] a2afm seed=33 step=1900/3000 val_RMSE=0.19632 best=0.19632

- [2026-10-13 23:14:32 UTC+8] a2afm seed=33 step=2000/3000 val_RMSE=0.20802 best=0.19632

- [2026-10-13 23:14:34 UTC+8] a2afm seed=33 step=2100/3000 val_RMSE=0.19114 best=0.19114

- [2026-10-13 23:14:36 UTC+8] a2afm seed=33 step=2200/3000 val_RMSE=0.20003 best=0.19114

- [2026-10-13 23:14:38 UTC+8] a2afm seed=33 step=2300/3000 val_RMSE=0.18602 best=0.18602

- [2026-10-13 23:14:40 UTC+8] a2afm seed=33 step=2400/3000 val_RMSE=0.19543 best=0.18602

- [2026-10-13 23:14:43 UTC+8] a2afm seed=33 step=2500/3000 val_RMSE=0.20489 best=0.18602

- [2026-10-13 23:14:45 UTC+8] a2afm seed=33 step=2600/3000 val_RMSE=0.20107 best=0.18602

- [2026-10-13 23:14:47 UTC+8] a2afm seed=33 step=2700/3000 val_RMSE=0.18211 best=0.18211

- [2026-10-13 23:14:49 UTC+8] a2afm seed=33 step=2800/3000 val_RMSE=0.18086 best=0.18086

- [2026-10-13 23:14:51 UTC+8] a2afm seed=33 step=2900/3000 val_RMSE=0.20948 best=0.18086

- [2026-10-13 23:14:54 UTC+8] a2afm seed=33 step=3000/3000 val_RMSE=0.19729 best=0.18086

- [2026-10-13 23:14:54 UTC+8] 完成 a2afm seed=33，本轮耗时 67.9 s，选择验证最优 step=2800

- [2026-10-13 23:14:54 UTC+8] regression seed=33 step=100/3000 val_RMSE=0.27684 best=0.27684

- [2026-10-13 23:14:55 UTC+8] regression seed=33 step=200/3000 val_RMSE=0.27935 best=0.27684

- [2026-10-13 23:14:55 UTC+8] regression seed=33 step=300/3000 val_RMSE=0.27189 best=0.27189

- [2026-10-13 23:14:55 UTC+8] regression seed=33 step=400/3000 val_RMSE=0.26901 best=0.26901

- [2026-10-13 23:14:56 UTC+8] regression seed=33 step=500/3000 val_RMSE=0.27040 best=0.26901

- [2026-10-13 23:14:56 UTC+8] regression seed=33 step=600/3000 val_RMSE=0.25744 best=0.25744

- [2026-10-13 23:14:57 UTC+8] regression seed=33 step=700/3000 val_RMSE=0.25576 best=0.25576

- [2026-10-13 23:14:58 UTC+8] regression seed=33 step=800/3000 val_RMSE=0.26017 best=0.25576

- [2026-10-13 23:14:58 UTC+8] regression seed=33 step=900/3000 val_RMSE=0.25316 best=0.25316

- [2026-10-13 23:14:58 UTC+8] regression seed=33 step=1000/3000 val_RMSE=0.24560 best=0.24560

- [2026-10-13 23:14:59 UTC+8] regression seed=33 step=1100/3000 val_RMSE=0.24879 best=0.24560

- [2026-10-13 23:14:59 UTC+8] regression seed=33 step=1200/3000 val_RMSE=0.23218 best=0.23218

- [2026-10-13 23:15:00 UTC+8] regression seed=33 step=1300/3000 val_RMSE=0.22676 best=0.22676

- [2026-10-13 23:15:00 UTC+8] regression seed=33 step=1400/3000 val_RMSE=0.22068 best=0.22068

- [2026-10-13 23:15:01 UTC+8] regression seed=33 step=1500/3000 val_RMSE=0.21550 best=0.21550

- [2026-10-13 23:15:01 UTC+8] regression seed=33 step=1600/3000 val_RMSE=0.21604 best=0.21550

- [2026-10-13 23:15:02 UTC+8] regression seed=33 step=1700/3000 val_RMSE=0.22139 best=0.21550

- [2026-10-13 23:15:02 UTC+8] regression seed=33 step=1800/3000 val_RMSE=0.21007 best=0.21007

- [2026-10-13 23:15:03 UTC+8] regression seed=33 step=1900/3000 val_RMSE=0.20828 best=0.20828

- [2026-10-13 23:15:03 UTC+8] regression seed=33 step=2000/3000 val_RMSE=0.19175 best=0.19175

- [2026-10-13 23:15:04 UTC+8] regression seed=33 step=2100/3000 val_RMSE=0.19717 best=0.19175

- [2026-10-13 23:15:04 UTC+8] regression seed=33 step=2200/3000 val_RMSE=0.18977 best=0.18977

- [2026-10-13 23:15:05 UTC+8] regression seed=33 step=2300/3000 val_RMSE=0.18997 best=0.18977

- [2026-10-13 23:15:05 UTC+8] regression seed=33 step=2400/3000 val_RMSE=0.19942 best=0.18977

- [2026-10-13 23:15:06 UTC+8] regression seed=33 step=2500/3000 val_RMSE=0.18368 best=0.18368

- [2026-10-13 23:15:06 UTC+8] regression seed=33 step=2600/3000 val_RMSE=0.19960 best=0.18368

- [2026-10-13 23:15:07 UTC+8] regression seed=33 step=2700/3000 val_RMSE=0.19032 best=0.18368

- [2026-10-13 23:15:07 UTC+8] regression seed=33 step=2800/3000 val_RMSE=0.18416 best=0.18368

- [2026-10-13 23:15:08 UTC+8] regression seed=33 step=2900/3000 val_RMSE=0.18568 best=0.18368

- [2026-10-13 23:15:08 UTC+8] regression seed=33 step=3000/3000 val_RMSE=0.18899 best=0.18368

- [2026-10-13 23:15:08 UTC+8] 完成 regression seed=33，本轮耗时 14.6 s，选择验证最优 step=2500

- [2026-10-13 23:15:09 UTC+8] fm_only seed=33 step=100/3000 val_RMSE=0.37730 best=0.37730

- [2026-10-13 23:15:09 UTC+8] fm_only seed=33 step=200/3000 val_RMSE=0.34706 best=0.34706

- [2026-10-13 23:15:10 UTC+8] fm_only seed=33 step=300/3000 val_RMSE=0.33239 best=0.33239

- [2026-10-13 23:15:10 UTC+8] fm_only seed=33 step=400/3000 val_RMSE=0.31880 best=0.31880

- [2026-10-13 23:15:11 UTC+8] fm_only seed=33 step=500/3000 val_RMSE=0.31013 best=0.31013

- [2026-10-13 23:15:12 UTC+8] fm_only seed=33 step=600/3000 val_RMSE=0.31484 best=0.31013

- [2026-10-13 23:15:12 UTC+8] fm_only seed=33 step=700/3000 val_RMSE=0.37062 best=0.31013

- [2026-10-13 23:15:13 UTC+8] fm_only seed=33 step=800/3000 val_RMSE=0.33076 best=0.31013

- [2026-10-13 23:15:13 UTC+8] fm_only seed=33 step=900/3000 val_RMSE=0.35638 best=0.31013

- [2026-10-13 23:15:14 UTC+8] fm_only seed=33 step=1000/3000 val_RMSE=0.30864 best=0.30864

- [2026-10-13 23:15:14 UTC+8] fm_only seed=33 step=1100/3000 val_RMSE=0.32910 best=0.30864

- [2026-10-13 23:15:15 UTC+8] fm_only seed=33 step=1200/3000 val_RMSE=0.28996 best=0.28996

- [2026-10-13 23:15:15 UTC+8] fm_only seed=33 step=1300/3000 val_RMSE=0.28984 best=0.28984

- [2026-10-13 23:15:16 UTC+8] fm_only seed=33 step=1400/3000 val_RMSE=0.35074 best=0.28984

- [2026-10-13 23:15:17 UTC+8] fm_only seed=33 step=1500/3000 val_RMSE=0.31177 best=0.28984

- [2026-10-13 23:15:17 UTC+8] fm_only seed=33 step=1600/3000 val_RMSE=0.29103 best=0.28984

- [2026-10-13 23:15:18 UTC+8] fm_only seed=33 step=1700/3000 val_RMSE=0.30279 best=0.28984

- [2026-10-13 23:15:18 UTC+8] fm_only seed=33 step=1800/3000 val_RMSE=0.28936 best=0.28936

- [2026-10-13 23:15:19 UTC+8] fm_only seed=33 step=1900/3000 val_RMSE=0.34888 best=0.28936

- [2026-10-13 23:15:19 UTC+8] fm_only seed=33 step=2000/3000 val_RMSE=0.31565 best=0.28936

- [2026-10-13 23:15:20 UTC+8] fm_only seed=33 step=2100/3000 val_RMSE=0.28147 best=0.28147

- [2026-10-13 23:15:21 UTC+8] fm_only seed=33 step=2200/3000 val_RMSE=0.34708 best=0.28147

- [2026-10-13 23:15:21 UTC+8] fm_only seed=33 step=2300/3000 val_RMSE=0.30052 best=0.28147

- [2026-10-13 23:15:22 UTC+8] fm_only seed=33 step=2400/3000 val_RMSE=0.27343 best=0.27343

- [2026-10-13 23:15:22 UTC+8] fm_only seed=33 step=2500/3000 val_RMSE=0.28011 best=0.27343

- [2026-10-13 23:15:23 UTC+8] fm_only seed=33 step=2600/3000 val_RMSE=0.27033 best=0.27033

- [2026-10-13 23:15:24 UTC+8] fm_only seed=33 step=2700/3000 val_RMSE=0.31285 best=0.27033

- [2026-10-13 23:15:24 UTC+8] fm_only seed=33 step=2800/3000 val_RMSE=0.27049 best=0.27033

- [2026-10-13 23:15:25 UTC+8] fm_only seed=33 step=2900/3000 val_RMSE=0.26827 best=0.26827

- [2026-10-13 23:15:26 UTC+8] fm_only seed=33 step=3000/3000 val_RMSE=0.30363 best=0.26827

- [2026-10-13 23:15:26 UTC+8] 完成 fm_only seed=33，本轮耗时 17.7 s，选择验证最优 step=2900

- [2026-10-13 23:15:26 UTC+8] 训练完成，开始冻结测试集评估与积分步数检查

- [2026-10-13 23:15:45 UTC+8] 实验完成：E:\desktop\MyDataBase\A2AFM\results\main\REPORT.md

- [2026-10-13 23:19:15 UTC+8] 完成交付：9 个模型（3 方法×3 种子）、4 噪声场景、3 信号族、5 项核心测试、应用演示、配对轨迹 Bootstrap、CPU 时延测试与图表视觉检查。

- [2026-10-13 23:19:15 UTC+8] 结果：中等高斯噪声 A2AFM RMSE=0.15951，原始=0.49073，降低67.50%；回归=0.16153，差异区间包含0；精确速度差分=0.03944。重尾噪声下直接回归更优。如实记录于 RESULTS.md。

- [2026-10-13 23:19:15 UTC+8] 验证补充：应用与批处理最大差1.79e-7；训练源码哈希一致；Kalman验证网格外1e5/1e6/1e7均不优于1e4；安装尚在写入NumPy时曾提前运行一次测试导致导入失败，安装完成后全部测试通过。

- [2026-10-13 23:19:15 UTC+8] 运行情况：正式测试种子50000，与调试测试种子30000分开；seed11在1300步恢复继续，已验证恢复机制；训练和评估均结束，无须等待夜间任务。

- [20261013_234542 UTC+8] 新任务：冲击扰动测试及闭环比较 DOB/Kalman/回归/A2AFM。已备份原代码、全部权重和结果至 snapshots\open_loop_20261013_234542，89 文件哈希验证通过。虚拟环境及安装缓存不重复复制，依赖版本在备份中保留。

- [2026-10-13 23:50:50 UTC+8] 计划：先冻结原权重测试冲击，再建立并训练闭环版本，比较四种观测器及无补偿参照

- [2026-10-13 23:50:51 UTC+8] 闭环扩展 open_frozen none seed=-1 完成

- [2026-10-13 23:50:51 UTC+8] 闭环扩展 open_frozen dob seed=-1 完成

- [2026-10-13 23:50:51 UTC+8] 闭环扩展 open_frozen kalman seed=-1 完成

- [2026-10-13 23:50:52 UTC+8] 闭环扩展 open_frozen regression seed=11 完成

- [2026-10-13 23:50:52 UTC+8] 闭环扩展 open_frozen regression seed=22 完成

- [2026-10-13 23:50:52 UTC+8] 闭环扩展 open_frozen regression seed=33 完成

- [2026-10-13 23:50:55 UTC+8] 闭环扩展 open_frozen a2afm seed=11 完成

- [2026-10-13 23:50:57 UTC+8] 闭环扩展 open_frozen a2afm seed=22 完成

- [2026-10-13 23:51:00 UTC+8] 闭环扩展 open_frozen a2afm seed=33 完成

- [2026-10-13 23:51:01 UTC+8] 闭环扩展 closed_frozen none seed=-1 完成

- [2026-10-13 23:51:01 UTC+8] 闭环扩展 closed_frozen dob seed=-1 完成

- [2026-10-13 23:51:01 UTC+8] 闭环扩展 closed_frozen kalman seed=-1 完成

- [2026-10-13 23:51:01 UTC+8] 闭环扩展 closed_frozen regression seed=11 完成

- [2026-10-13 23:51:02 UTC+8] 闭环扩展 closed_frozen regression seed=22 完成

- [2026-10-13 23:51:02 UTC+8] 闭环扩展 closed_frozen regression seed=33 完成

- [2026-10-13 23:51:05 UTC+8] 闭环扩展 closed_frozen a2afm seed=11 完成

- [2026-10-13 23:51:07 UTC+8] 闭环扩展 closed_frozen a2afm seed=22 完成

- [2026-10-13 23:51:09 UTC+8] 闭环扩展 closed_frozen a2afm seed=33 完成

- [2026-10-13 23:51:15 UTC+8] a2afm seed=11 step=100/3000 val_RMSE=0.47332 best=0.47332

- [2026-10-13 23:51:17 UTC+8] a2afm seed=11 step=200/3000 val_RMSE=0.40076 best=0.40076

- [2026-10-13 23:51:19 UTC+8] a2afm seed=11 step=300/3000 val_RMSE=0.34500 best=0.34500

- [2026-10-13 23:51:21 UTC+8] a2afm seed=11 step=400/3000 val_RMSE=0.30796 best=0.30796

- [2026-10-13 23:51:23 UTC+8] a2afm seed=11 step=500/3000 val_RMSE=0.26389 best=0.26389

- [2026-10-13 23:51:25 UTC+8] a2afm seed=11 step=600/3000 val_RMSE=0.21887 best=0.21887

- [2026-10-13 23:51:27 UTC+8] a2afm seed=11 step=700/3000 val_RMSE=0.20755 best=0.20755

- [2026-10-13 23:51:30 UTC+8] a2afm seed=11 step=800/3000 val_RMSE=0.18396 best=0.18396

- [2026-10-13 23:51:32 UTC+8] a2afm seed=11 step=900/3000 val_RMSE=0.16056 best=0.16056

- [2026-10-13 23:51:34 UTC+8] a2afm seed=11 step=1000/3000 val_RMSE=0.14828 best=0.14828

- [2026-10-13 23:51:36 UTC+8] a2afm seed=11 step=1100/3000 val_RMSE=0.14843 best=0.14828

- [2026-10-13 23:51:38 UTC+8] a2afm seed=11 step=1200/3000 val_RMSE=0.15721 best=0.14828

- [2026-10-13 23:51:41 UTC+8] a2afm seed=11 step=1300/3000 val_RMSE=0.14721 best=0.14721

- [2026-10-13 23:51:43 UTC+8] a2afm seed=11 step=1400/3000 val_RMSE=0.15116 best=0.14721

- [2026-10-13 23:51:45 UTC+8] a2afm seed=11 step=1500/3000 val_RMSE=0.12852 best=0.12852

- [2026-10-13 23:51:47 UTC+8] a2afm seed=11 step=1600/3000 val_RMSE=0.14219 best=0.12852

- [2026-10-13 23:51:49 UTC+8] a2afm seed=11 step=1700/3000 val_RMSE=0.14564 best=0.12852

- [2026-10-13 23:51:51 UTC+8] a2afm seed=11 step=1800/3000 val_RMSE=0.13842 best=0.12852

- [2026-10-13 23:51:53 UTC+8] a2afm seed=11 step=1900/3000 val_RMSE=0.13362 best=0.12852

- [2026-10-13 23:51:55 UTC+8] a2afm seed=11 step=2000/3000 val_RMSE=0.12787 best=0.12787

- [2026-10-13 23:51:58 UTC+8] a2afm seed=11 step=2100/3000 val_RMSE=0.13754 best=0.12787

- [2026-10-13 23:52:00 UTC+8] a2afm seed=11 step=2200/3000 val_RMSE=0.14857 best=0.12787

- [2026-10-13 23:52:02 UTC+8] a2afm seed=11 step=2300/3000 val_RMSE=0.14145 best=0.12787

- [2026-10-13 23:52:04 UTC+8] a2afm seed=11 step=2400/3000 val_RMSE=0.12374 best=0.12374

- [2026-10-13 23:52:06 UTC+8] a2afm seed=11 step=2500/3000 val_RMSE=0.13202 best=0.12374

- [2026-10-13 23:52:08 UTC+8] a2afm seed=11 step=2600/3000 val_RMSE=0.12647 best=0.12374

- [2026-10-13 23:52:11 UTC+8] a2afm seed=11 step=2700/3000 val_RMSE=0.12967 best=0.12374

- [2026-10-13 23:52:13 UTC+8] a2afm seed=11 step=2800/3000 val_RMSE=0.13872 best=0.12374

- [2026-10-13 23:52:15 UTC+8] a2afm seed=11 step=2900/3000 val_RMSE=0.13797 best=0.12374

- [2026-10-13 23:52:17 UTC+8] a2afm seed=11 step=3000/3000 val_RMSE=0.12635 best=0.12374

- [2026-10-13 23:52:17 UTC+8] 完成 a2afm seed=11，本轮耗时 64.8 s，选择验证最优 step=2400

- [2026-10-13 23:52:18 UTC+8] regression seed=11 step=100/3000 val_RMSE=0.49171 best=0.49171

- [2026-10-13 23:52:18 UTC+8] regression seed=11 step=200/3000 val_RMSE=0.42489 best=0.42489

- [2026-10-13 23:52:19 UTC+8] regression seed=11 step=300/3000 val_RMSE=0.39344 best=0.39344

- [2026-10-13 23:52:19 UTC+8] regression seed=11 step=400/3000 val_RMSE=0.36838 best=0.36838

- [2026-10-13 23:52:20 UTC+8] regression seed=11 step=500/3000 val_RMSE=0.35404 best=0.35404

- [2026-10-13 23:52:20 UTC+8] regression seed=11 step=600/3000 val_RMSE=0.31905 best=0.31905

- [2026-10-13 23:52:21 UTC+8] regression seed=11 step=700/3000 val_RMSE=0.31814 best=0.31814

- [2026-10-13 23:52:21 UTC+8] regression seed=11 step=800/3000 val_RMSE=0.29620 best=0.29620

- [2026-10-13 23:52:22 UTC+8] regression seed=11 step=900/3000 val_RMSE=0.27808 best=0.27808

- [2026-10-13 23:52:22 UTC+8] regression seed=11 step=1000/3000 val_RMSE=0.25027 best=0.25027

- [2026-10-13 23:52:23 UTC+8] regression seed=11 step=1100/3000 val_RMSE=0.24387 best=0.24387

- [2026-10-13 23:52:23 UTC+8] regression seed=11 step=1200/3000 val_RMSE=0.21588 best=0.21588

- [2026-10-13 23:52:23 UTC+8] regression seed=11 step=1300/3000 val_RMSE=0.21293 best=0.21293

- [2026-10-13 23:52:24 UTC+8] regression seed=11 step=1400/3000 val_RMSE=0.21233 best=0.21233

- [2026-10-13 23:52:24 UTC+8] regression seed=11 step=1500/3000 val_RMSE=0.19903 best=0.19903

- [2026-10-13 23:52:25 UTC+8] regression seed=11 step=1600/3000 val_RMSE=0.18606 best=0.18606

- [2026-10-13 23:52:25 UTC+8] regression seed=11 step=1700/3000 val_RMSE=0.17503 best=0.17503

- [2026-10-13 23:52:26 UTC+8] regression seed=11 step=1800/3000 val_RMSE=0.17599 best=0.17503

- [2026-10-13 23:52:26 UTC+8] regression seed=11 step=1900/3000 val_RMSE=0.17698 best=0.17503

- [2026-10-13 23:52:27 UTC+8] regression seed=11 step=2000/3000 val_RMSE=0.17506 best=0.17503

- [2026-10-13 23:52:27 UTC+8] regression seed=11 step=2100/3000 val_RMSE=0.16514 best=0.16514

- [2026-10-13 23:52:28 UTC+8] regression seed=11 step=2200/3000 val_RMSE=0.16522 best=0.16514

- [2026-10-13 23:52:28 UTC+8] regression seed=11 step=2300/3000 val_RMSE=0.15674 best=0.15674

- [2026-10-13 23:52:29 UTC+8] regression seed=11 step=2400/3000 val_RMSE=0.15636 best=0.15636

- [2026-10-13 23:52:29 UTC+8] regression seed=11 step=2500/3000 val_RMSE=0.15596 best=0.15596

- [2026-10-13 23:52:29 UTC+8] regression seed=11 step=2600/3000 val_RMSE=0.16800 best=0.15596

- [2026-10-13 23:52:30 UTC+8] regression seed=11 step=2700/3000 val_RMSE=0.15561 best=0.15561

- [2026-10-13 23:52:30 UTC+8] regression seed=11 step=2800/3000 val_RMSE=0.15013 best=0.15013

- [2026-10-13 23:52:31 UTC+8] regression seed=11 step=2900/3000 val_RMSE=0.14372 best=0.14372

- [2026-10-13 23:52:31 UTC+8] regression seed=11 step=3000/3000 val_RMSE=0.13510 best=0.13510

- [2026-10-13 23:52:31 UTC+8] 完成 regression seed=11，本轮耗时 14.0 s，选择验证最优 step=3000

- [2026-10-13 23:52:34 UTC+8] a2afm seed=22 step=100/3000 val_RMSE=0.48790 best=0.48790

- [2026-10-13 23:52:36 UTC+8] a2afm seed=22 step=200/3000 val_RMSE=0.39268 best=0.39268

- [2026-10-13 23:52:38 UTC+8] a2afm seed=22 step=300/3000 val_RMSE=0.34745 best=0.34745

- [2026-10-13 23:52:40 UTC+8] a2afm seed=22 step=400/3000 val_RMSE=0.27451 best=0.27451

- [2026-10-13 23:52:42 UTC+8] a2afm seed=22 step=500/3000 val_RMSE=0.23861 best=0.23861

- [2026-10-13 23:52:44 UTC+8] a2afm seed=22 step=600/3000 val_RMSE=0.21687 best=0.21687

- [2026-10-13 23:52:46 UTC+8] a2afm seed=22 step=700/3000 val_RMSE=0.17885 best=0.17885

- [2026-10-13 23:52:48 UTC+8] a2afm seed=22 step=800/3000 val_RMSE=0.18361 best=0.17885

- [2026-10-13 23:52:51 UTC+8] a2afm seed=22 step=900/3000 val_RMSE=0.15799 best=0.15799

- [2026-10-13 23:52:53 UTC+8] a2afm seed=22 step=1000/3000 val_RMSE=0.15831 best=0.15799

- [2026-10-13 23:52:55 UTC+8] a2afm seed=22 step=1100/3000 val_RMSE=0.15679 best=0.15679

- [2026-10-13 23:52:57 UTC+8] a2afm seed=22 step=1200/3000 val_RMSE=0.14306 best=0.14306

- [2026-10-13 23:52:59 UTC+8] a2afm seed=22 step=1300/3000 val_RMSE=0.15604 best=0.14306

- [2026-10-13 23:53:01 UTC+8] a2afm seed=22 step=1400/3000 val_RMSE=0.13768 best=0.13768

- [2026-10-13 23:53:03 UTC+8] a2afm seed=22 step=1500/3000 val_RMSE=0.13488 best=0.13488

- [2026-10-13 23:53:06 UTC+8] a2afm seed=22 step=1600/3000 val_RMSE=0.14800 best=0.13488

- [2026-10-13 23:53:08 UTC+8] a2afm seed=22 step=1700/3000 val_RMSE=0.13439 best=0.13439

- [2026-10-13 23:53:10 UTC+8] a2afm seed=22 step=1800/3000 val_RMSE=0.14318 best=0.13439

- [2026-10-13 23:53:12 UTC+8] a2afm seed=22 step=1900/3000 val_RMSE=0.13646 best=0.13439

- [2026-10-13 23:53:14 UTC+8] a2afm seed=22 step=2000/3000 val_RMSE=0.12411 best=0.12411

- [2026-10-13 23:53:16 UTC+8] a2afm seed=22 step=2100/3000 val_RMSE=0.12775 best=0.12411

- [2026-10-13 23:53:18 UTC+8] a2afm seed=22 step=2200/3000 val_RMSE=0.12899 best=0.12411

- [2026-10-13 23:53:21 UTC+8] a2afm seed=22 step=2300/3000 val_RMSE=0.12118 best=0.12118

- [2026-10-13 23:53:23 UTC+8] a2afm seed=22 step=2400/3000 val_RMSE=0.12200 best=0.12118

- [2026-10-13 23:53:25 UTC+8] a2afm seed=22 step=2500/3000 val_RMSE=0.11848 best=0.11848

- [2026-10-13 23:53:27 UTC+8] a2afm seed=22 step=2600/3000 val_RMSE=0.12265 best=0.11848

- [2026-10-13 23:53:29 UTC+8] a2afm seed=22 step=2700/3000 val_RMSE=0.12629 best=0.11848

- [2026-10-13 23:53:31 UTC+8] a2afm seed=22 step=2800/3000 val_RMSE=0.13325 best=0.11848

- [2026-10-13 23:53:33 UTC+8] a2afm seed=22 step=2900/3000 val_RMSE=0.12635 best=0.11848

- [2026-10-13 23:53:35 UTC+8] a2afm seed=22 step=3000/3000 val_RMSE=0.12737 best=0.11848

- [2026-10-13 23:53:35 UTC+8] 完成 a2afm seed=22，本轮耗时 64.1 s，选择验证最优 step=2500

- [2026-10-13 23:53:36 UTC+8] regression seed=22 step=100/3000 val_RMSE=0.46037 best=0.46037

- [2026-10-13 23:53:36 UTC+8] regression seed=22 step=200/3000 val_RMSE=0.43403 best=0.43403

- [2026-10-13 23:53:37 UTC+8] regression seed=22 step=300/3000 val_RMSE=0.38911 best=0.38911

- [2026-10-13 23:53:37 UTC+8] regression seed=22 step=400/3000 val_RMSE=0.36349 best=0.36349

- [2026-10-13 23:53:38 UTC+8] regression seed=22 step=500/3000 val_RMSE=0.33409 best=0.33409

- [2026-10-13 23:53:38 UTC+8] regression seed=22 step=600/3000 val_RMSE=0.32280 best=0.32280

- [2026-10-13 23:53:39 UTC+8] regression seed=22 step=700/3000 val_RMSE=0.31489 best=0.31489

- [2026-10-13 23:53:39 UTC+8] regression seed=22 step=800/3000 val_RMSE=0.28775 best=0.28775

- [2026-10-13 23:53:40 UTC+8] regression seed=22 step=900/3000 val_RMSE=0.26788 best=0.26788

- [2026-10-13 23:53:40 UTC+8] regression seed=22 step=1000/3000 val_RMSE=0.24705 best=0.24705

- [2026-10-13 23:53:41 UTC+8] regression seed=22 step=1100/3000 val_RMSE=0.22972 best=0.22972

- [2026-10-13 23:53:41 UTC+8] regression seed=22 step=1200/3000 val_RMSE=0.23623 best=0.22972

- [2026-10-13 23:53:42 UTC+8] regression seed=22 step=1300/3000 val_RMSE=0.21015 best=0.21015

- [2026-10-13 23:53:42 UTC+8] regression seed=22 step=1400/3000 val_RMSE=0.19908 best=0.19908

- [2026-10-13 23:53:43 UTC+8] regression seed=22 step=1500/3000 val_RMSE=0.19975 best=0.19908

- [2026-10-13 23:53:43 UTC+8] regression seed=22 step=1600/3000 val_RMSE=0.20783 best=0.19908

- [2026-10-13 23:53:44 UTC+8] regression seed=22 step=1700/3000 val_RMSE=0.17986 best=0.17986

- [2026-10-13 23:53:44 UTC+8] regression seed=22 step=1800/3000 val_RMSE=0.18538 best=0.17986

- [2026-10-13 23:53:44 UTC+8] regression seed=22 step=1900/3000 val_RMSE=0.17531 best=0.17531

- [2026-10-13 23:53:45 UTC+8] regression seed=22 step=2000/3000 val_RMSE=0.18611 best=0.17531

- [2026-10-13 23:53:45 UTC+8] regression seed=22 step=2100/3000 val_RMSE=0.15864 best=0.15864

- [2026-10-13 23:53:46 UTC+8] regression seed=22 step=2200/3000 val_RMSE=0.15681 best=0.15681

- [2026-10-13 23:53:46 UTC+8] regression seed=22 step=2300/3000 val_RMSE=0.15697 best=0.15681

- [2026-10-13 23:53:47 UTC+8] regression seed=22 step=2400/3000 val_RMSE=0.17617 best=0.15681

- [2026-10-13 23:53:47 UTC+8] regression seed=22 step=2500/3000 val_RMSE=0.15392 best=0.15392

- [2026-10-13 23:53:48 UTC+8] regression seed=22 step=2600/3000 val_RMSE=0.15214 best=0.15214

- [2026-10-13 23:53:48 UTC+8] regression seed=22 step=2700/3000 val_RMSE=0.14822 best=0.14822

- [2026-10-13 23:53:49 UTC+8] regression seed=22 step=2800/3000 val_RMSE=0.16582 best=0.14822

- [2026-10-13 23:53:49 UTC+8] regression seed=22 step=2900/3000 val_RMSE=0.14653 best=0.14653

- [2026-10-13 23:53:50 UTC+8] regression seed=22 step=3000/3000 val_RMSE=0.14068 best=0.14068

- [2026-10-13 23:53:50 UTC+8] 完成 regression seed=22，本轮耗时 14.2 s，选择验证最优 step=3000

- [2026-10-13 23:53:52 UTC+8] a2afm seed=33 step=100/3000 val_RMSE=0.49249 best=0.49249

- [2026-10-13 23:53:54 UTC+8] a2afm seed=33 step=200/3000 val_RMSE=0.40688 best=0.40688

- [2026-10-13 23:53:56 UTC+8] a2afm seed=33 step=300/3000 val_RMSE=0.35302 best=0.35302

- [2026-10-13 23:53:59 UTC+8] a2afm seed=33 step=400/3000 val_RMSE=0.29188 best=0.29188

- [2026-10-13 23:54:01 UTC+8] a2afm seed=33 step=500/3000 val_RMSE=0.23937 best=0.23937

- [2026-10-13 23:54:03 UTC+8] a2afm seed=33 step=600/3000 val_RMSE=0.19183 best=0.19183

- [2026-10-13 23:54:05 UTC+8] a2afm seed=33 step=700/3000 val_RMSE=0.17861 best=0.17861

- [2026-10-13 23:54:08 UTC+8] a2afm seed=33 step=800/3000 val_RMSE=0.17378 best=0.17378

- [2026-10-13 23:54:10 UTC+8] a2afm seed=33 step=900/3000 val_RMSE=0.15525 best=0.15525

- [2026-10-13 23:54:12 UTC+8] a2afm seed=33 step=1000/3000 val_RMSE=0.15905 best=0.15525

- [2026-10-13 23:54:14 UTC+8] a2afm seed=33 step=1100/3000 val_RMSE=0.16689 best=0.15525

- [2026-10-13 23:54:16 UTC+8] a2afm seed=33 step=1200/3000 val_RMSE=0.14522 best=0.14522

- [2026-10-13 23:54:19 UTC+8] a2afm seed=33 step=1300/3000 val_RMSE=0.14807 best=0.14522

- [2026-10-13 23:54:21 UTC+8] a2afm seed=33 step=1400/3000 val_RMSE=0.15017 best=0.14522

- [2026-10-13 23:54:23 UTC+8] a2afm seed=33 step=1500/3000 val_RMSE=0.13357 best=0.13357

- [2026-10-13 23:54:25 UTC+8] a2afm seed=33 step=1600/3000 val_RMSE=0.13663 best=0.13357

- [2026-10-13 23:54:28 UTC+8] a2afm seed=33 step=1700/3000 val_RMSE=0.14534 best=0.13357

- [2026-10-13 23:54:30 UTC+8] a2afm seed=33 step=1800/3000 val_RMSE=0.11883 best=0.11883

- [2026-10-13 23:54:32 UTC+8] a2afm seed=33 step=1900/3000 val_RMSE=0.12639 best=0.11883

- [2026-10-13 23:54:34 UTC+8] a2afm seed=33 step=2000/3000 val_RMSE=0.13947 best=0.11883

- [2026-10-13 23:54:36 UTC+8] a2afm seed=33 step=2100/3000 val_RMSE=0.12213 best=0.11883

- [2026-10-13 23:54:38 UTC+8] a2afm seed=33 step=2200/3000 val_RMSE=0.12716 best=0.11883

- [2026-10-13 23:54:41 UTC+8] a2afm seed=33 step=2300/3000 val_RMSE=0.11845 best=0.11845

- [2026-10-13 23:54:43 UTC+8] a2afm seed=33 step=2400/3000 val_RMSE=0.11934 best=0.11845

- [2026-10-13 23:54:45 UTC+8] a2afm seed=33 step=2500/3000 val_RMSE=0.13230 best=0.11845

- [2026-10-13 23:54:47 UTC+8] a2afm seed=33 step=2600/3000 val_RMSE=0.15453 best=0.11845

- [2026-10-13 23:54:49 UTC+8] a2afm seed=33 step=2700/3000 val_RMSE=0.11662 best=0.11662

- [2026-10-13 23:54:52 UTC+8] a2afm seed=33 step=2800/3000 val_RMSE=0.12980 best=0.11662

- [2026-10-13 23:54:54 UTC+8] a2afm seed=33 step=2900/3000 val_RMSE=0.12455 best=0.11662

- [2026-10-13 23:54:56 UTC+8] a2afm seed=33 step=3000/3000 val_RMSE=0.12070 best=0.11662

- [2026-10-13 23:54:56 UTC+8] 完成 a2afm seed=33，本轮耗时 66.6 s，选择验证最优 step=2700

- [2026-10-13 23:54:57 UTC+8] regression seed=33 step=100/3000 val_RMSE=0.48852 best=0.48852

- [2026-10-13 23:54:57 UTC+8] regression seed=33 step=200/3000 val_RMSE=0.43675 best=0.43675

- [2026-10-13 23:54:58 UTC+8] regression seed=33 step=300/3000 val_RMSE=0.42191 best=0.42191

- [2026-10-13 23:54:58 UTC+8] regression seed=33 step=400/3000 val_RMSE=0.38762 best=0.38762

- [2026-10-13 23:54:59 UTC+8] regression seed=33 step=500/3000 val_RMSE=0.38023 best=0.38023

- [2026-10-13 23:54:59 UTC+8] regression seed=33 step=600/3000 val_RMSE=0.35410 best=0.35410

- [2026-10-13 23:55:00 UTC+8] regression seed=33 step=700/3000 val_RMSE=0.34527 best=0.34527

- [2026-10-13 23:55:00 UTC+8] regression seed=33 step=800/3000 val_RMSE=0.31332 best=0.31332

- [2026-10-13 23:55:01 UTC+8] regression seed=33 step=900/3000 val_RMSE=0.29852 best=0.29852

- [2026-10-13 23:55:01 UTC+8] regression seed=33 step=1000/3000 val_RMSE=0.27384 best=0.27384

- [2026-10-13 23:55:02 UTC+8] regression seed=33 step=1100/3000 val_RMSE=0.24546 best=0.24546

- [2026-10-13 23:55:02 UTC+8] regression seed=33 step=1200/3000 val_RMSE=0.23445 best=0.23445

- [2026-10-13 23:55:03 UTC+8] regression seed=33 step=1300/3000 val_RMSE=0.22388 best=0.22388

- [2026-10-13 23:55:03 UTC+8] regression seed=33 step=1400/3000 val_RMSE=0.21618 best=0.21618

- [2026-10-13 23:55:04 UTC+8] regression seed=33 step=1500/3000 val_RMSE=0.20120 best=0.20120

- [2026-10-13 23:55:04 UTC+8] regression seed=33 step=1600/3000 val_RMSE=0.19128 best=0.19128

- [2026-10-13 23:55:04 UTC+8] regression seed=33 step=1700/3000 val_RMSE=0.18438 best=0.18438

- [2026-10-13 23:55:05 UTC+8] regression seed=33 step=1800/3000 val_RMSE=0.17808 best=0.17808

- [2026-10-13 23:55:05 UTC+8] regression seed=33 step=1900/3000 val_RMSE=0.18922 best=0.17808

- [2026-10-13 23:55:06 UTC+8] regression seed=33 step=2000/3000 val_RMSE=0.20262 best=0.17808

- [2026-10-13 23:55:06 UTC+8] regression seed=33 step=2100/3000 val_RMSE=0.16656 best=0.16656

- [2026-10-13 23:55:07 UTC+8] regression seed=33 step=2200/3000 val_RMSE=0.17409 best=0.16656

- [2026-10-13 23:55:07 UTC+8] regression seed=33 step=2300/3000 val_RMSE=0.15721 best=0.15721

- [2026-10-13 23:55:08 UTC+8] regression seed=33 step=2400/3000 val_RMSE=0.16090 best=0.15721

- [2026-10-13 23:55:08 UTC+8] regression seed=33 step=2500/3000 val_RMSE=0.15068 best=0.15068

- [2026-10-13 23:55:09 UTC+8] regression seed=33 step=2600/3000 val_RMSE=0.15485 best=0.15068

- [2026-10-13 23:55:09 UTC+8] regression seed=33 step=2700/3000 val_RMSE=0.14840 best=0.14840

- [2026-10-13 23:55:10 UTC+8] regression seed=33 step=2800/3000 val_RMSE=0.15635 best=0.14840

- [2026-10-13 23:55:10 UTC+8] regression seed=33 step=2900/3000 val_RMSE=0.13611 best=0.13611

- [2026-10-13 23:55:11 UTC+8] regression seed=33 step=3000/3000 val_RMSE=0.13956 best=0.13611

- [2026-10-13 23:55:11 UTC+8] 完成 regression seed=33，本轮耗时 14.5 s，选择验证最优 step=2900

- [2026-10-13 23:55:11 UTC+8] 闭环扩展 closed_adapted none seed=-1 完成

- [2026-10-13 23:55:11 UTC+8] 闭环扩展 closed_adapted dob seed=-1 完成

- [2026-10-13 23:55:11 UTC+8] 闭环扩展 closed_adapted kalman seed=-1 完成

- [2026-10-13 23:55:11 UTC+8] 闭环扩展 closed_adapted regression seed=11 完成

- [2026-10-13 23:55:12 UTC+8] 闭环扩展 closed_adapted regression seed=22 完成

- [2026-10-13 23:55:12 UTC+8] 闭环扩展 closed_adapted regression seed=33 完成

- [2026-10-13 23:55:15 UTC+8] 闭环扩展 closed_adapted a2afm seed=11 完成

- [2026-10-13 23:55:17 UTC+8] 闭环扩展 closed_adapted a2afm seed=22 完成

- [2026-10-13 23:55:20 UTC+8] 闭环扩展 closed_adapted a2afm seed=33 完成

- [2026-10-13 23:55:21 UTC+8] 冲击及闭环实验完成：E:\desktop\MyDataBase\A2AFM\results\closed_loop\REPORT.md

- [2026-10-13 23:59:44 UTC+8] 完成冲击及闭环扩展：旧权重开环/闭环与新权重闭环三阶段，24独立测试轨迹、3种脉冲宽度、两种网络各3训练种子。新增4项测试通过；原89文件快照哈希再次核对通过，原代码/权重/结果均未改动（日志追加除外）。

- [2026-10-13 23:59:44 UTC+8] 新闭环跟踪RMSE：DOB 0.004779，Kalman 0.004771，回归0.003233，A2AFM 0.003117；无补偿0.011208。新版A2AFM冲击区间RMSE1.06708，仍大于原始残差0.45241，报告已说明幅值失真与同步采样限制。

- [2026-10-13 23:59:44 UTC+8] 配对轨迹统计、三阶段图表检查及颜色/局部坐标轴修正完成。交付入口 CLOSED_LOOP_RESULTS.md；完整数据 results/closed_loop。
