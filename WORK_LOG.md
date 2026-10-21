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

- [2026-10-21 17:47:19 UTC+8] 单步混合实验开始：CPU，训练轨迹=7，每模型更新=2

- [2026-10-21 17:47:21 UTC+8] 混合数据完成：训练窗口=2646，验证窗口=1323

- [2026-10-21 17:47:22 UTC+8] a2afm seed=11 step=2/2 val_RMSE=0.76757 best=0.76757

- [2026-10-21 17:47:22 UTC+8] 完成 a2afm seed=11，本轮耗时 0.0 s，选择验证最优 step=2

- [2026-10-21 17:47:22 UTC+8] a2afm seed=11 step=2/2 val_RMSE=0.76889 best=0.76889

- [2026-10-21 17:47:22 UTC+8] 完成 a2afm seed=11，本轮耗时 0.0 s，选择验证最优 step=2

- [2026-10-21 17:47:22 UTC+8] regression seed=11 step=2/2 val_RMSE=0.54686 best=0.54686

- [2026-10-21 17:47:22 UTC+8] 完成 regression seed=11，本轮耗时 0.0 s，选择验证最优 step=2

- [2026-10-21 17:47:22 UTC+8] residual seed=11 step=2/2 val_RMSE=0.93756 best=0.93756

- [2026-10-21 17:47:22 UTC+8] 完成 residual seed=11，本轮耗时 0.0 s，选择验证最优 step=2

- [2026-10-21 17:47:22 UTC+8] 单步实验评估 gaussian_low

- [2026-10-21 17:47:23 UTC+8] 单步实验评估 gaussian_mid

- [2026-10-21 17:47:24 UTC+8] 单步实验评估 gaussian_high

- [2026-10-21 17:47:25 UTC+8] 单步实验评估 student_ood

- [2026-10-21 17:47:26 UTC+8] 冻结权重闭环冲击测试完成 none

- [2026-10-21 17:47:26 UTC+8] 冻结权重闭环冲击测试完成 dob

- [2026-10-21 17:47:26 UTC+8] 冻结权重闭环冲击测试完成 kalman

- [2026-10-21 17:47:26 UTC+8] 冻结权重闭环冲击测试完成 single_fm

- [2026-10-21 17:47:27 UTC+8] 冻结权重闭环冲击测试完成 midpoint_fm

- [2026-10-21 17:47:27 UTC+8] 冻结权重闭环冲击测试完成 regression

- [2026-10-21 17:47:28 UTC+8] 冻结权重闭环冲击测试完成 residual

- [2026-10-21 17:47:28 UTC+8] 单步混合实验完成：E:\Desktop\MyCode\A2AFM\results\single_step_smoke\REPORT.md

- [2026-10-21 17:48:09 UTC+8] 单步混合实验开始：CPU，训练轨迹=360，每模型更新=15000

- [2026-10-21 17:48:55 UTC+8] 混合数据完成：训练窗口=136080，验证窗口=17010

- [2026-10-21 17:48:56 UTC+8] a2afm seed=11 step=100/15000 val_RMSE=0.28323 best=0.28323

- [2026-10-21 17:48:56 UTC+8] a2afm seed=11 step=200/15000 val_RMSE=0.26161 best=0.26161

- [2026-10-21 17:48:56 UTC+8] a2afm seed=11 step=300/15000 val_RMSE=0.25052 best=0.25052

- [2026-10-21 17:48:57 UTC+8] a2afm seed=11 step=400/15000 val_RMSE=0.25415 best=0.25052

- [2026-10-21 17:48:57 UTC+8] a2afm seed=11 step=500/15000 val_RMSE=0.26104 best=0.25052

- [2026-10-21 17:48:57 UTC+8] a2afm seed=11 step=600/15000 val_RMSE=0.23641 best=0.23641

- [2026-10-21 17:48:57 UTC+8] a2afm seed=11 step=700/15000 val_RMSE=0.23302 best=0.23302

- [2026-10-21 17:48:58 UTC+8] a2afm seed=11 step=800/15000 val_RMSE=0.22926 best=0.22926

- [2026-10-21 17:48:58 UTC+8] a2afm seed=11 step=900/15000 val_RMSE=0.23033 best=0.22926

- [2026-10-21 17:48:58 UTC+8] a2afm seed=11 step=1000/15000 val_RMSE=0.23244 best=0.22926

- [2026-10-21 17:48:58 UTC+8] a2afm seed=11 step=1100/15000 val_RMSE=0.22878 best=0.22878

- [2026-10-21 17:48:58 UTC+8] a2afm seed=11 step=1200/15000 val_RMSE=0.21576 best=0.21576

- [2026-10-21 17:48:59 UTC+8] a2afm seed=11 step=1300/15000 val_RMSE=0.21099 best=0.21099

- [2026-10-21 17:48:59 UTC+8] a2afm seed=11 step=1400/15000 val_RMSE=0.21613 best=0.21099

- [2026-10-21 17:48:59 UTC+8] a2afm seed=11 step=1500/15000 val_RMSE=0.22436 best=0.21099

- [2026-10-21 17:48:59 UTC+8] a2afm seed=11 step=1600/15000 val_RMSE=0.19458 best=0.19458

- [2026-10-21 17:48:59 UTC+8] a2afm seed=11 step=1700/15000 val_RMSE=0.19923 best=0.19458

- [2026-10-21 17:49:00 UTC+8] a2afm seed=11 step=1800/15000 val_RMSE=0.20093 best=0.19458

- [2026-10-21 17:49:00 UTC+8] a2afm seed=11 step=1900/15000 val_RMSE=0.19338 best=0.19338

- [2026-10-21 17:49:00 UTC+8] a2afm seed=11 step=2000/15000 val_RMSE=0.19583 best=0.19338

- [2026-10-21 17:49:00 UTC+8] a2afm seed=11 step=2100/15000 val_RMSE=0.18903 best=0.18903

- [2026-10-21 17:49:01 UTC+8] a2afm seed=11 step=2200/15000 val_RMSE=0.18298 best=0.18298

- [2026-10-21 17:49:01 UTC+8] a2afm seed=11 step=2300/15000 val_RMSE=0.20134 best=0.18298

- [2026-10-21 17:49:01 UTC+8] a2afm seed=11 step=2400/15000 val_RMSE=0.18740 best=0.18298

- [2026-10-21 17:49:01 UTC+8] a2afm seed=11 step=2500/15000 val_RMSE=0.18190 best=0.18190

- [2026-10-21 17:49:01 UTC+8] a2afm seed=11 step=2600/15000 val_RMSE=0.18959 best=0.18190

- [2026-10-21 17:49:02 UTC+8] a2afm seed=11 step=2700/15000 val_RMSE=0.18762 best=0.18190

- [2026-10-21 17:49:02 UTC+8] a2afm seed=11 step=2800/15000 val_RMSE=0.19417 best=0.18190

- [2026-10-21 17:49:02 UTC+8] a2afm seed=11 step=2900/15000 val_RMSE=0.18738 best=0.18190

- [2026-10-21 17:49:02 UTC+8] a2afm seed=11 step=3000/15000 val_RMSE=0.17571 best=0.17571

- [2026-10-21 17:49:02 UTC+8] a2afm seed=11 step=3100/15000 val_RMSE=0.17609 best=0.17571

- [2026-10-21 17:49:03 UTC+8] a2afm seed=11 step=3200/15000 val_RMSE=0.17151 best=0.17151

- [2026-10-21 17:49:03 UTC+8] a2afm seed=11 step=3300/15000 val_RMSE=0.17867 best=0.17151

- [2026-10-21 17:49:03 UTC+8] a2afm seed=11 step=3400/15000 val_RMSE=0.18308 best=0.17151

- [2026-10-21 17:49:03 UTC+8] a2afm seed=11 step=3500/15000 val_RMSE=0.17168 best=0.17151

- [2026-10-21 17:49:04 UTC+8] a2afm seed=11 step=3600/15000 val_RMSE=0.15912 best=0.15912

- [2026-10-21 17:49:04 UTC+8] a2afm seed=11 step=3700/15000 val_RMSE=0.16658 best=0.15912

- [2026-10-21 17:49:04 UTC+8] a2afm seed=11 step=3800/15000 val_RMSE=0.17630 best=0.15912

- [2026-10-21 17:49:04 UTC+8] a2afm seed=11 step=3900/15000 val_RMSE=0.15540 best=0.15540

- [2026-10-21 17:49:04 UTC+8] a2afm seed=11 step=4000/15000 val_RMSE=0.15709 best=0.15540

- [2026-10-21 17:49:05 UTC+8] a2afm seed=11 step=4100/15000 val_RMSE=0.17224 best=0.15540

- [2026-10-21 17:49:05 UTC+8] a2afm seed=11 step=4200/15000 val_RMSE=0.14819 best=0.14819

- [2026-10-21 17:49:05 UTC+8] a2afm seed=11 step=4300/15000 val_RMSE=0.16066 best=0.14819

- [2026-10-21 17:49:05 UTC+8] a2afm seed=11 step=4400/15000 val_RMSE=0.15196 best=0.14819

- [2026-10-21 17:49:05 UTC+8] a2afm seed=11 step=4500/15000 val_RMSE=0.15390 best=0.14819

- [2026-10-21 17:49:06 UTC+8] a2afm seed=11 step=4600/15000 val_RMSE=0.16261 best=0.14819

- [2026-10-21 17:49:06 UTC+8] a2afm seed=11 step=4700/15000 val_RMSE=0.15510 best=0.14819

- [2026-10-21 17:49:06 UTC+8] a2afm seed=11 step=4800/15000 val_RMSE=0.15376 best=0.14819

- [2026-10-21 17:49:06 UTC+8] a2afm seed=11 step=4900/15000 val_RMSE=0.16020 best=0.14819

- [2026-10-21 17:49:07 UTC+8] a2afm seed=11 step=5000/15000 val_RMSE=0.20586 best=0.14819

- [2026-10-21 17:49:07 UTC+8] a2afm seed=11 step=5100/15000 val_RMSE=0.16196 best=0.14819

- [2026-10-21 17:49:07 UTC+8] a2afm seed=11 step=5200/15000 val_RMSE=0.15408 best=0.14819

- [2026-10-21 17:49:07 UTC+8] a2afm seed=11 step=5300/15000 val_RMSE=0.15040 best=0.14819

- [2026-10-21 17:49:07 UTC+8] a2afm seed=11 step=5400/15000 val_RMSE=0.15149 best=0.14819

- [2026-10-21 17:49:08 UTC+8] a2afm seed=11 step=5500/15000 val_RMSE=0.15106 best=0.14819

- [2026-10-21 17:49:08 UTC+8] a2afm seed=11 step=5600/15000 val_RMSE=0.14422 best=0.14422

- [2026-10-21 17:49:08 UTC+8] a2afm seed=11 step=5700/15000 val_RMSE=0.15782 best=0.14422

- [2026-10-21 17:49:08 UTC+8] a2afm seed=11 step=5800/15000 val_RMSE=0.14723 best=0.14422

- [2026-10-21 17:49:08 UTC+8] a2afm seed=11 step=5900/15000 val_RMSE=0.15467 best=0.14422

- [2026-10-21 17:49:09 UTC+8] a2afm seed=11 step=6000/15000 val_RMSE=0.14221 best=0.14221

- [2026-10-21 17:49:09 UTC+8] a2afm seed=11 step=6100/15000 val_RMSE=0.15679 best=0.14221

- [2026-10-21 17:49:09 UTC+8] a2afm seed=11 step=6200/15000 val_RMSE=0.15205 best=0.14221

- [2026-10-21 17:49:09 UTC+8] a2afm seed=11 step=6300/15000 val_RMSE=0.14619 best=0.14221

- [2026-10-21 17:49:09 UTC+8] a2afm seed=11 step=6400/15000 val_RMSE=0.16894 best=0.14221

- [2026-10-21 17:49:10 UTC+8] a2afm seed=11 step=6500/15000 val_RMSE=0.15937 best=0.14221

- [2026-10-21 17:49:10 UTC+8] a2afm seed=11 step=6600/15000 val_RMSE=0.16130 best=0.14221

- [2026-10-21 17:49:10 UTC+8] a2afm seed=11 step=6700/15000 val_RMSE=0.15979 best=0.14221

- [2026-10-21 17:49:10 UTC+8] a2afm seed=11 step=6800/15000 val_RMSE=0.14941 best=0.14221

- [2026-10-21 17:49:11 UTC+8] a2afm seed=11 step=6900/15000 val_RMSE=0.14271 best=0.14221

- [2026-10-21 17:49:11 UTC+8] a2afm seed=11 step=7000/15000 val_RMSE=0.16105 best=0.14221

- [2026-10-21 17:49:11 UTC+8] a2afm seed=11 step=7100/15000 val_RMSE=0.14113 best=0.14113

- [2026-10-21 17:49:11 UTC+8] a2afm seed=11 step=7200/15000 val_RMSE=0.15737 best=0.14113

- [2026-10-21 17:49:11 UTC+8] a2afm seed=11 step=7300/15000 val_RMSE=0.14410 best=0.14113

- [2026-10-21 17:49:12 UTC+8] a2afm seed=11 step=7400/15000 val_RMSE=0.13732 best=0.13732

- [2026-10-21 17:49:12 UTC+8] a2afm seed=11 step=7500/15000 val_RMSE=0.13446 best=0.13446

- [2026-10-21 17:49:12 UTC+8] a2afm seed=11 step=7600/15000 val_RMSE=0.14438 best=0.13446

- [2026-10-21 17:49:12 UTC+8] a2afm seed=11 step=7700/15000 val_RMSE=0.14368 best=0.13446

- [2026-10-21 17:49:12 UTC+8] a2afm seed=11 step=7800/15000 val_RMSE=0.14924 best=0.13446

- [2026-10-21 17:49:13 UTC+8] a2afm seed=11 step=7900/15000 val_RMSE=0.13973 best=0.13446

- [2026-10-21 17:49:13 UTC+8] a2afm seed=11 step=8000/15000 val_RMSE=0.14630 best=0.13446

- [2026-10-21 17:49:13 UTC+8] a2afm seed=11 step=8100/15000 val_RMSE=0.14374 best=0.13446

- [2026-10-21 17:49:13 UTC+8] a2afm seed=11 step=8200/15000 val_RMSE=0.13472 best=0.13446

- [2026-10-21 17:49:14 UTC+8] a2afm seed=11 step=8300/15000 val_RMSE=0.13909 best=0.13446

- [2026-10-21 17:49:14 UTC+8] a2afm seed=11 step=8400/15000 val_RMSE=0.14978 best=0.13446

- [2026-10-21 17:49:14 UTC+8] a2afm seed=11 step=8500/15000 val_RMSE=0.13249 best=0.13249

- [2026-10-21 17:49:14 UTC+8] a2afm seed=11 step=8600/15000 val_RMSE=0.13740 best=0.13249

- [2026-10-21 17:49:14 UTC+8] a2afm seed=11 step=8700/15000 val_RMSE=0.14411 best=0.13249

- [2026-10-21 17:49:15 UTC+8] a2afm seed=11 step=8800/15000 val_RMSE=0.13573 best=0.13249

- [2026-10-21 17:49:15 UTC+8] a2afm seed=11 step=8900/15000 val_RMSE=0.15666 best=0.13249

- [2026-10-21 17:49:15 UTC+8] a2afm seed=11 step=9000/15000 val_RMSE=0.14720 best=0.13249

- [2026-10-21 17:49:15 UTC+8] a2afm seed=11 step=9100/15000 val_RMSE=0.14659 best=0.13249

- [2026-10-21 17:49:15 UTC+8] a2afm seed=11 step=9200/15000 val_RMSE=0.14774 best=0.13249

- [2026-10-21 17:49:16 UTC+8] a2afm seed=11 step=9300/15000 val_RMSE=0.15661 best=0.13249

- [2026-10-21 17:49:16 UTC+8] a2afm seed=11 step=9400/15000 val_RMSE=0.14439 best=0.13249

- [2026-10-21 17:49:16 UTC+8] a2afm seed=11 step=9500/15000 val_RMSE=0.15965 best=0.13249

- [2026-10-21 17:49:16 UTC+8] a2afm seed=11 step=9600/15000 val_RMSE=0.12723 best=0.12723

- [2026-10-21 17:49:17 UTC+8] a2afm seed=11 step=9700/15000 val_RMSE=0.13437 best=0.12723

- [2026-10-21 17:49:17 UTC+8] a2afm seed=11 step=9800/15000 val_RMSE=0.14060 best=0.12723

- [2026-10-21 17:49:17 UTC+8] a2afm seed=11 step=9900/15000 val_RMSE=0.16213 best=0.12723

- [2026-10-21 17:49:17 UTC+8] a2afm seed=11 step=10000/15000 val_RMSE=0.13110 best=0.12723

- [2026-10-21 17:49:17 UTC+8] a2afm seed=11 step=10100/15000 val_RMSE=0.13545 best=0.12723

- [2026-10-21 17:49:18 UTC+8] a2afm seed=11 step=10200/15000 val_RMSE=0.14047 best=0.12723

- [2026-10-21 17:49:18 UTC+8] a2afm seed=11 step=10300/15000 val_RMSE=0.12313 best=0.12313

- [2026-10-21 17:49:18 UTC+8] a2afm seed=11 step=10400/15000 val_RMSE=0.15109 best=0.12313

- [2026-10-21 17:49:18 UTC+8] a2afm seed=11 step=10500/15000 val_RMSE=0.14014 best=0.12313

- [2026-10-21 17:49:19 UTC+8] a2afm seed=11 step=10600/15000 val_RMSE=0.12761 best=0.12313

- [2026-10-21 17:49:19 UTC+8] a2afm seed=11 step=10700/15000 val_RMSE=0.13821 best=0.12313

- [2026-10-21 17:49:19 UTC+8] a2afm seed=11 step=10800/15000 val_RMSE=0.13029 best=0.12313

- [2026-10-21 17:49:19 UTC+8] a2afm seed=11 step=10900/15000 val_RMSE=0.13867 best=0.12313

- [2026-10-21 17:49:19 UTC+8] a2afm seed=11 step=11000/15000 val_RMSE=0.14022 best=0.12313

- [2026-10-21 17:49:20 UTC+8] a2afm seed=11 step=11100/15000 val_RMSE=0.15954 best=0.12313

- [2026-10-21 17:49:20 UTC+8] a2afm seed=11 step=11200/15000 val_RMSE=0.14543 best=0.12313

- [2026-10-21 17:49:20 UTC+8] a2afm seed=11 step=11300/15000 val_RMSE=0.14055 best=0.12313

- [2026-10-21 17:49:20 UTC+8] a2afm seed=11 step=11400/15000 val_RMSE=0.12827 best=0.12313

- [2026-10-21 17:49:20 UTC+8] a2afm seed=11 step=11500/15000 val_RMSE=0.14008 best=0.12313

- [2026-10-21 17:49:21 UTC+8] a2afm seed=11 step=11600/15000 val_RMSE=0.13381 best=0.12313

- [2026-10-21 17:49:21 UTC+8] a2afm seed=11 step=11700/15000 val_RMSE=0.12950 best=0.12313

- [2026-10-21 17:49:21 UTC+8] a2afm seed=11 step=11800/15000 val_RMSE=0.11795 best=0.11795

- [2026-10-21 17:49:21 UTC+8] a2afm seed=11 step=11900/15000 val_RMSE=0.13753 best=0.11795

- [2026-10-21 17:49:21 UTC+8] a2afm seed=11 step=12000/15000 val_RMSE=0.14664 best=0.11795

- [2026-10-21 17:49:22 UTC+8] a2afm seed=11 step=12100/15000 val_RMSE=0.13558 best=0.11795

- [2026-10-21 17:49:22 UTC+8] a2afm seed=11 step=12200/15000 val_RMSE=0.13959 best=0.11795

- [2026-10-21 17:49:22 UTC+8] a2afm seed=11 step=12300/15000 val_RMSE=0.14148 best=0.11795

- [2026-10-21 17:49:22 UTC+8] a2afm seed=11 step=12400/15000 val_RMSE=0.12781 best=0.11795

- [2026-10-21 17:49:23 UTC+8] a2afm seed=11 step=12500/15000 val_RMSE=0.14274 best=0.11795

- [2026-10-21 17:49:23 UTC+8] a2afm seed=11 step=12600/15000 val_RMSE=0.12706 best=0.11795

- [2026-10-21 17:49:23 UTC+8] a2afm seed=11 step=12700/15000 val_RMSE=0.14821 best=0.11795

- [2026-10-21 17:49:23 UTC+8] a2afm seed=11 step=12800/15000 val_RMSE=0.12496 best=0.11795

- [2026-10-21 17:49:23 UTC+8] a2afm seed=11 step=12900/15000 val_RMSE=0.12356 best=0.11795

- [2026-10-21 17:49:24 UTC+8] a2afm seed=11 step=13000/15000 val_RMSE=0.15099 best=0.11795

- [2026-10-21 17:49:24 UTC+8] a2afm seed=11 step=13100/15000 val_RMSE=0.12804 best=0.11795

- [2026-10-21 17:49:24 UTC+8] a2afm seed=11 step=13200/15000 val_RMSE=0.13424 best=0.11795

- [2026-10-21 17:49:24 UTC+8] a2afm seed=11 step=13300/15000 val_RMSE=0.15201 best=0.11795

- [2026-10-21 17:49:25 UTC+8] a2afm seed=11 step=13400/15000 val_RMSE=0.13063 best=0.11795

- [2026-10-21 17:49:25 UTC+8] a2afm seed=11 step=13500/15000 val_RMSE=0.13713 best=0.11795

- [2026-10-21 17:49:25 UTC+8] a2afm seed=11 step=13600/15000 val_RMSE=0.13297 best=0.11795

- [2026-10-21 17:49:25 UTC+8] a2afm seed=11 step=13700/15000 val_RMSE=0.14515 best=0.11795

- [2026-10-21 17:49:25 UTC+8] a2afm seed=11 step=13800/15000 val_RMSE=0.12590 best=0.11795

- [2026-10-21 17:49:26 UTC+8] a2afm seed=11 step=13900/15000 val_RMSE=0.12703 best=0.11795

- [2026-10-21 17:49:26 UTC+8] a2afm seed=11 step=14000/15000 val_RMSE=0.12881 best=0.11795

- [2026-10-21 17:49:26 UTC+8] a2afm seed=11 step=14100/15000 val_RMSE=0.13712 best=0.11795

- [2026-10-21 17:49:26 UTC+8] a2afm seed=11 step=14200/15000 val_RMSE=0.13315 best=0.11795

- [2026-10-21 17:49:26 UTC+8] a2afm seed=11 step=14300/15000 val_RMSE=0.12637 best=0.11795

- [2026-10-21 17:49:27 UTC+8] a2afm seed=11 step=14400/15000 val_RMSE=0.12401 best=0.11795

- [2026-10-21 17:49:27 UTC+8] a2afm seed=11 step=14500/15000 val_RMSE=0.13037 best=0.11795

- [2026-10-21 17:49:27 UTC+8] a2afm seed=11 step=14600/15000 val_RMSE=0.14375 best=0.11795

- [2026-10-21 17:49:27 UTC+8] a2afm seed=11 step=14700/15000 val_RMSE=0.13211 best=0.11795

- [2026-10-21 17:49:28 UTC+8] a2afm seed=11 step=14800/15000 val_RMSE=0.13909 best=0.11795

- [2026-10-21 17:49:28 UTC+8] a2afm seed=11 step=14900/15000 val_RMSE=0.12286 best=0.11795

- [2026-10-21 17:49:28 UTC+8] a2afm seed=11 step=15000/15000 val_RMSE=0.15031 best=0.11795

- [2026-10-21 17:49:28 UTC+8] 完成 a2afm seed=11，本轮耗时 32.1 s，选择验证最优 step=11800

- [2026-10-21 17:49:28 UTC+8] a2afm seed=22 step=100/15000 val_RMSE=0.30016 best=0.30016

- [2026-10-21 17:49:28 UTC+8] a2afm seed=22 step=200/15000 val_RMSE=0.26089 best=0.26089

- [2026-10-21 17:49:29 UTC+8] a2afm seed=22 step=300/15000 val_RMSE=0.25230 best=0.25230

- [2026-10-21 17:49:29 UTC+8] a2afm seed=22 step=400/15000 val_RMSE=0.25038 best=0.25038

- [2026-10-21 17:49:29 UTC+8] a2afm seed=22 step=500/15000 val_RMSE=0.24309 best=0.24309

- [2026-10-21 17:49:29 UTC+8] a2afm seed=22 step=600/15000 val_RMSE=0.24109 best=0.24109

- [2026-10-21 17:49:29 UTC+8] a2afm seed=22 step=700/15000 val_RMSE=0.23191 best=0.23191

- [2026-10-21 17:49:30 UTC+8] a2afm seed=22 step=800/15000 val_RMSE=0.23057 best=0.23057

- [2026-10-21 17:49:30 UTC+8] a2afm seed=22 step=900/15000 val_RMSE=0.22535 best=0.22535

- [2026-10-21 17:49:30 UTC+8] a2afm seed=22 step=1000/15000 val_RMSE=0.23957 best=0.22535

- [2026-10-21 17:49:30 UTC+8] a2afm seed=22 step=1100/15000 val_RMSE=0.21894 best=0.21894

- [2026-10-21 17:49:31 UTC+8] a2afm seed=22 step=1200/15000 val_RMSE=0.22368 best=0.21894

- [2026-10-21 17:49:31 UTC+8] a2afm seed=22 step=1300/15000 val_RMSE=0.21459 best=0.21459

- [2026-10-21 17:49:31 UTC+8] a2afm seed=22 step=1400/15000 val_RMSE=0.21298 best=0.21298

- [2026-10-21 17:49:31 UTC+8] a2afm seed=22 step=1500/15000 val_RMSE=0.20496 best=0.20496

- [2026-10-21 17:49:31 UTC+8] a2afm seed=22 step=1600/15000 val_RMSE=0.21842 best=0.20496

- [2026-10-21 17:49:32 UTC+8] a2afm seed=22 step=1700/15000 val_RMSE=0.20558 best=0.20496

- [2026-10-21 17:49:32 UTC+8] a2afm seed=22 step=1800/15000 val_RMSE=0.19937 best=0.19937

- [2026-10-21 17:49:32 UTC+8] a2afm seed=22 step=1900/15000 val_RMSE=0.20430 best=0.19937

- [2026-10-21 17:49:32 UTC+8] a2afm seed=22 step=2000/15000 val_RMSE=0.19558 best=0.19558

- [2026-10-21 17:49:32 UTC+8] a2afm seed=22 step=2100/15000 val_RMSE=0.18600 best=0.18600

- [2026-10-21 17:49:33 UTC+8] a2afm seed=22 step=2200/15000 val_RMSE=0.22037 best=0.18600

- [2026-10-21 17:49:33 UTC+8] a2afm seed=22 step=2300/15000 val_RMSE=0.20455 best=0.18600

- [2026-10-21 17:49:33 UTC+8] a2afm seed=22 step=2400/15000 val_RMSE=0.18095 best=0.18095

- [2026-10-21 17:49:33 UTC+8] a2afm seed=22 step=2500/15000 val_RMSE=0.19099 best=0.18095

- [2026-10-21 17:49:34 UTC+8] a2afm seed=22 step=2600/15000 val_RMSE=0.18614 best=0.18095

- [2026-10-21 17:49:34 UTC+8] a2afm seed=22 step=2700/15000 val_RMSE=0.18151 best=0.18095

- [2026-10-21 17:49:34 UTC+8] a2afm seed=22 step=2800/15000 val_RMSE=0.19453 best=0.18095

- [2026-10-21 17:49:34 UTC+8] a2afm seed=22 step=2900/15000 val_RMSE=0.18283 best=0.18095

- [2026-10-21 17:49:34 UTC+8] a2afm seed=22 step=3000/15000 val_RMSE=0.18823 best=0.18095

- [2026-10-21 17:49:35 UTC+8] a2afm seed=22 step=3100/15000 val_RMSE=0.17039 best=0.17039

- [2026-10-21 17:49:35 UTC+8] a2afm seed=22 step=3200/15000 val_RMSE=0.17756 best=0.17039

- [2026-10-21 17:49:35 UTC+8] a2afm seed=22 step=3300/15000 val_RMSE=0.18135 best=0.17039

- [2026-10-21 17:49:35 UTC+8] a2afm seed=22 step=3400/15000 val_RMSE=0.18373 best=0.17039

- [2026-10-21 17:49:36 UTC+8] a2afm seed=22 step=3500/15000 val_RMSE=0.16653 best=0.16653

- [2026-10-21 17:49:36 UTC+8] a2afm seed=22 step=3600/15000 val_RMSE=0.17455 best=0.16653

- [2026-10-21 17:49:36 UTC+8] a2afm seed=22 step=3700/15000 val_RMSE=0.17575 best=0.16653

- [2026-10-21 17:49:36 UTC+8] a2afm seed=22 step=3800/15000 val_RMSE=0.19311 best=0.16653

- [2026-10-21 17:49:36 UTC+8] a2afm seed=22 step=3900/15000 val_RMSE=0.17237 best=0.16653

- [2026-10-21 17:49:37 UTC+8] a2afm seed=22 step=4000/15000 val_RMSE=0.17882 best=0.16653

- [2026-10-21 17:49:37 UTC+8] a2afm seed=22 step=4100/15000 val_RMSE=0.19024 best=0.16653

- [2026-10-21 17:49:37 UTC+8] a2afm seed=22 step=4200/15000 val_RMSE=0.18922 best=0.16653

- [2026-10-21 17:49:37 UTC+8] a2afm seed=22 step=4300/15000 val_RMSE=0.16382 best=0.16382

- [2026-10-21 17:49:38 UTC+8] a2afm seed=22 step=4400/15000 val_RMSE=0.16633 best=0.16382

- [2026-10-21 17:49:38 UTC+8] a2afm seed=22 step=4500/15000 val_RMSE=0.16798 best=0.16382

- [2026-10-21 17:49:38 UTC+8] a2afm seed=22 step=4600/15000 val_RMSE=0.16462 best=0.16382

- [2026-10-21 17:49:38 UTC+8] a2afm seed=22 step=4700/15000 val_RMSE=0.15479 best=0.15479

- [2026-10-21 17:49:38 UTC+8] a2afm seed=22 step=4800/15000 val_RMSE=0.14967 best=0.14967

- [2026-10-21 17:49:39 UTC+8] a2afm seed=22 step=4900/15000 val_RMSE=0.15937 best=0.14967

- [2026-10-21 17:49:39 UTC+8] a2afm seed=22 step=5000/15000 val_RMSE=0.19654 best=0.14967

- [2026-10-21 17:49:39 UTC+8] a2afm seed=22 step=5100/15000 val_RMSE=0.15749 best=0.14967

- [2026-10-21 17:49:39 UTC+8] a2afm seed=22 step=5200/15000 val_RMSE=0.17179 best=0.14967

- [2026-10-21 17:49:39 UTC+8] a2afm seed=22 step=5300/15000 val_RMSE=0.16053 best=0.14967

- [2026-10-21 17:49:40 UTC+8] a2afm seed=22 step=5400/15000 val_RMSE=0.15721 best=0.14967

- [2026-10-21 17:49:40 UTC+8] a2afm seed=22 step=5500/15000 val_RMSE=0.15145 best=0.14967

- [2026-10-21 17:49:40 UTC+8] a2afm seed=22 step=5600/15000 val_RMSE=0.14920 best=0.14920

- [2026-10-21 17:49:40 UTC+8] a2afm seed=22 step=5700/15000 val_RMSE=0.15981 best=0.14920

- [2026-10-21 17:49:41 UTC+8] a2afm seed=22 step=5800/15000 val_RMSE=0.16437 best=0.14920

- [2026-10-21 17:49:41 UTC+8] a2afm seed=22 step=5900/15000 val_RMSE=0.15477 best=0.14920

- [2026-10-21 17:49:41 UTC+8] a2afm seed=22 step=6000/15000 val_RMSE=0.16589 best=0.14920

- [2026-10-21 17:49:41 UTC+8] a2afm seed=22 step=6100/15000 val_RMSE=0.14474 best=0.14474

- [2026-10-21 17:49:41 UTC+8] a2afm seed=22 step=6200/15000 val_RMSE=0.17739 best=0.14474

- [2026-10-21 17:49:42 UTC+8] a2afm seed=22 step=6300/15000 val_RMSE=0.14309 best=0.14309

- [2026-10-21 17:49:42 UTC+8] a2afm seed=22 step=6400/15000 val_RMSE=0.14593 best=0.14309

- [2026-10-21 17:49:42 UTC+8] a2afm seed=22 step=6500/15000 val_RMSE=0.15336 best=0.14309

- [2026-10-21 17:49:42 UTC+8] a2afm seed=22 step=6600/15000 val_RMSE=0.16667 best=0.14309

- [2026-10-21 17:49:42 UTC+8] a2afm seed=22 step=6700/15000 val_RMSE=0.14625 best=0.14309

- [2026-10-21 17:49:43 UTC+8] a2afm seed=22 step=6800/15000 val_RMSE=0.14669 best=0.14309

- [2026-10-21 17:49:43 UTC+8] a2afm seed=22 step=6900/15000 val_RMSE=0.14554 best=0.14309

- [2026-10-21 17:49:43 UTC+8] a2afm seed=22 step=7000/15000 val_RMSE=0.14455 best=0.14309

- [2026-10-21 17:49:43 UTC+8] a2afm seed=22 step=7100/15000 val_RMSE=0.15248 best=0.14309

- [2026-10-21 17:49:44 UTC+8] a2afm seed=22 step=7200/15000 val_RMSE=0.14243 best=0.14243

- [2026-10-21 17:49:44 UTC+8] a2afm seed=22 step=7300/15000 val_RMSE=0.14660 best=0.14243

- [2026-10-21 17:49:44 UTC+8] a2afm seed=22 step=7400/15000 val_RMSE=0.14754 best=0.14243

- [2026-10-21 17:49:44 UTC+8] a2afm seed=22 step=7500/15000 val_RMSE=0.15453 best=0.14243

- [2026-10-21 17:49:44 UTC+8] a2afm seed=22 step=7600/15000 val_RMSE=0.13732 best=0.13732

- [2026-10-21 17:49:45 UTC+8] a2afm seed=22 step=7700/15000 val_RMSE=0.14573 best=0.13732

- [2026-10-21 17:49:45 UTC+8] a2afm seed=22 step=7800/15000 val_RMSE=0.15151 best=0.13732

- [2026-10-21 17:49:45 UTC+8] a2afm seed=22 step=7900/15000 val_RMSE=0.16537 best=0.13732

- [2026-10-21 17:49:45 UTC+8] a2afm seed=22 step=8000/15000 val_RMSE=0.14661 best=0.13732

- [2026-10-21 17:49:46 UTC+8] a2afm seed=22 step=8100/15000 val_RMSE=0.13516 best=0.13516

- [2026-10-21 17:49:46 UTC+8] a2afm seed=22 step=8200/15000 val_RMSE=0.14946 best=0.13516

- [2026-10-21 17:49:46 UTC+8] a2afm seed=22 step=8300/15000 val_RMSE=0.16607 best=0.13516

- [2026-10-21 17:49:46 UTC+8] a2afm seed=22 step=8400/15000 val_RMSE=0.13017 best=0.13017

- [2026-10-21 17:49:46 UTC+8] a2afm seed=22 step=8500/15000 val_RMSE=0.15981 best=0.13017

- [2026-10-21 17:49:47 UTC+8] a2afm seed=22 step=8600/15000 val_RMSE=0.15079 best=0.13017

- [2026-10-21 17:49:47 UTC+8] a2afm seed=22 step=8700/15000 val_RMSE=0.14370 best=0.13017

- [2026-10-21 17:49:47 UTC+8] a2afm seed=22 step=8800/15000 val_RMSE=0.15123 best=0.13017

- [2026-10-21 17:49:47 UTC+8] a2afm seed=22 step=8900/15000 val_RMSE=0.13890 best=0.13017

- [2026-10-21 17:49:47 UTC+8] a2afm seed=22 step=9000/15000 val_RMSE=0.15643 best=0.13017

- [2026-10-21 17:49:48 UTC+8] a2afm seed=22 step=9100/15000 val_RMSE=0.15523 best=0.13017

- [2026-10-21 17:49:48 UTC+8] a2afm seed=22 step=9200/15000 val_RMSE=0.15147 best=0.13017

- [2026-10-21 17:49:48 UTC+8] a2afm seed=22 step=9300/15000 val_RMSE=0.15558 best=0.13017

- [2026-10-21 17:49:48 UTC+8] a2afm seed=22 step=9400/15000 val_RMSE=0.14464 best=0.13017

- [2026-10-21 17:49:49 UTC+8] a2afm seed=22 step=9500/15000 val_RMSE=0.14831 best=0.13017

- [2026-10-21 17:49:49 UTC+8] a2afm seed=22 step=9600/15000 val_RMSE=0.13651 best=0.13017

- [2026-10-21 17:49:49 UTC+8] a2afm seed=22 step=9700/15000 val_RMSE=0.14080 best=0.13017

- [2026-10-21 17:49:49 UTC+8] a2afm seed=22 step=9800/15000 val_RMSE=0.13070 best=0.13017

- [2026-10-21 17:49:49 UTC+8] a2afm seed=22 step=9900/15000 val_RMSE=0.13939 best=0.13017

- [2026-10-21 17:49:50 UTC+8] a2afm seed=22 step=10000/15000 val_RMSE=0.16918 best=0.13017

- [2026-10-21 17:49:50 UTC+8] a2afm seed=22 step=10100/15000 val_RMSE=0.14405 best=0.13017

- [2026-10-21 17:49:50 UTC+8] a2afm seed=22 step=10200/15000 val_RMSE=0.12874 best=0.12874

- [2026-10-21 17:49:50 UTC+8] a2afm seed=22 step=10300/15000 val_RMSE=0.13423 best=0.12874

- [2026-10-21 17:49:50 UTC+8] a2afm seed=22 step=10400/15000 val_RMSE=0.12997 best=0.12874

- [2026-10-21 17:49:51 UTC+8] a2afm seed=22 step=10500/15000 val_RMSE=0.12537 best=0.12537

- [2026-10-21 17:49:51 UTC+8] a2afm seed=22 step=10600/15000 val_RMSE=0.13662 best=0.12537

- [2026-10-21 17:49:51 UTC+8] a2afm seed=22 step=10700/15000 val_RMSE=0.14081 best=0.12537

- [2026-10-21 17:49:51 UTC+8] a2afm seed=22 step=10800/15000 val_RMSE=0.12658 best=0.12537

- [2026-10-21 17:49:52 UTC+8] a2afm seed=22 step=10900/15000 val_RMSE=0.13199 best=0.12537

- [2026-10-21 17:49:52 UTC+8] a2afm seed=22 step=11000/15000 val_RMSE=0.15207 best=0.12537

- [2026-10-21 17:49:52 UTC+8] a2afm seed=22 step=11100/15000 val_RMSE=0.15427 best=0.12537

- [2026-10-21 17:49:52 UTC+8] a2afm seed=22 step=11200/15000 val_RMSE=0.13740 best=0.12537

- [2026-10-21 17:49:52 UTC+8] a2afm seed=22 step=11300/15000 val_RMSE=0.14447 best=0.12537

- [2026-10-21 17:49:53 UTC+8] a2afm seed=22 step=11400/15000 val_RMSE=0.13867 best=0.12537

- [2026-10-21 17:49:53 UTC+8] a2afm seed=22 step=11500/15000 val_RMSE=0.13602 best=0.12537

- [2026-10-21 17:49:53 UTC+8] a2afm seed=22 step=11600/15000 val_RMSE=0.13272 best=0.12537

- [2026-10-21 17:49:53 UTC+8] a2afm seed=22 step=11700/15000 val_RMSE=0.12249 best=0.12249

- [2026-10-21 17:49:54 UTC+8] a2afm seed=22 step=11800/15000 val_RMSE=0.17474 best=0.12249

- [2026-10-21 17:49:54 UTC+8] a2afm seed=22 step=11900/15000 val_RMSE=0.12313 best=0.12249

- [2026-10-21 17:49:54 UTC+8] a2afm seed=22 step=12000/15000 val_RMSE=0.13559 best=0.12249

- [2026-10-21 17:49:54 UTC+8] a2afm seed=22 step=12100/15000 val_RMSE=0.12753 best=0.12249

- [2026-10-21 17:49:54 UTC+8] a2afm seed=22 step=12200/15000 val_RMSE=0.13351 best=0.12249

- [2026-10-21 17:49:55 UTC+8] a2afm seed=22 step=12300/15000 val_RMSE=0.16232 best=0.12249

- [2026-10-21 17:49:55 UTC+8] a2afm seed=22 step=12400/15000 val_RMSE=0.14465 best=0.12249

- [2026-10-21 17:49:55 UTC+8] a2afm seed=22 step=12500/15000 val_RMSE=0.13937 best=0.12249

- [2026-10-21 17:49:55 UTC+8] a2afm seed=22 step=12600/15000 val_RMSE=0.13454 best=0.12249

- [2026-10-21 17:49:56 UTC+8] a2afm seed=22 step=12700/15000 val_RMSE=0.12877 best=0.12249

- [2026-10-21 17:49:56 UTC+8] a2afm seed=22 step=12800/15000 val_RMSE=0.13013 best=0.12249

- [2026-10-21 17:49:56 UTC+8] a2afm seed=22 step=12900/15000 val_RMSE=0.13356 best=0.12249

- [2026-10-21 17:49:56 UTC+8] a2afm seed=22 step=13000/15000 val_RMSE=0.14545 best=0.12249

- [2026-10-21 17:49:56 UTC+8] a2afm seed=22 step=13100/15000 val_RMSE=0.13923 best=0.12249

- [2026-10-21 17:49:57 UTC+8] a2afm seed=22 step=13200/15000 val_RMSE=0.12421 best=0.12249

- [2026-10-21 17:49:57 UTC+8] a2afm seed=22 step=13300/15000 val_RMSE=0.12280 best=0.12249

- [2026-10-21 17:49:57 UTC+8] a2afm seed=22 step=13400/15000 val_RMSE=0.13172 best=0.12249

- [2026-10-21 17:49:57 UTC+8] a2afm seed=22 step=13500/15000 val_RMSE=0.14845 best=0.12249

- [2026-10-21 17:49:57 UTC+8] a2afm seed=22 step=13600/15000 val_RMSE=0.14221 best=0.12249

- [2026-10-21 17:49:58 UTC+8] a2afm seed=22 step=13700/15000 val_RMSE=0.13377 best=0.12249

- [2026-10-21 17:49:58 UTC+8] a2afm seed=22 step=13800/15000 val_RMSE=0.12275 best=0.12249

- [2026-10-21 17:49:58 UTC+8] a2afm seed=22 step=13900/15000 val_RMSE=0.13223 best=0.12249

- [2026-10-21 17:49:58 UTC+8] a2afm seed=22 step=14000/15000 val_RMSE=0.12770 best=0.12249

- [2026-10-21 17:49:59 UTC+8] a2afm seed=22 step=14100/15000 val_RMSE=0.14730 best=0.12249

- [2026-10-21 17:49:59 UTC+8] a2afm seed=22 step=14200/15000 val_RMSE=0.12650 best=0.12249

- [2026-10-21 17:49:59 UTC+8] a2afm seed=22 step=14300/15000 val_RMSE=0.12013 best=0.12013

- [2026-10-21 17:49:59 UTC+8] a2afm seed=22 step=14400/15000 val_RMSE=0.12431 best=0.12013

- [2026-10-21 17:49:59 UTC+8] a2afm seed=22 step=14500/15000 val_RMSE=0.12308 best=0.12013

- [2026-10-21 17:50:00 UTC+8] a2afm seed=22 step=14600/15000 val_RMSE=0.14591 best=0.12013

- [2026-10-21 17:50:00 UTC+8] a2afm seed=22 step=14700/15000 val_RMSE=0.13555 best=0.12013

- [2026-10-21 17:50:00 UTC+8] a2afm seed=22 step=14800/15000 val_RMSE=0.12736 best=0.12013

- [2026-10-21 17:50:00 UTC+8] a2afm seed=22 step=14900/15000 val_RMSE=0.13014 best=0.12013

- [2026-10-21 17:50:01 UTC+8] a2afm seed=22 step=15000/15000 val_RMSE=0.12140 best=0.12013

- [2026-10-21 17:50:01 UTC+8] 完成 a2afm seed=22，本轮耗时 32.6 s，选择验证最优 step=14300

- [2026-10-21 17:50:01 UTC+8] a2afm seed=33 step=100/15000 val_RMSE=0.28103 best=0.28103

- [2026-10-21 17:50:01 UTC+8] a2afm seed=33 step=200/15000 val_RMSE=0.25971 best=0.25971

- [2026-10-21 17:50:01 UTC+8] a2afm seed=33 step=300/15000 val_RMSE=0.24914 best=0.24914

- [2026-10-21 17:50:02 UTC+8] a2afm seed=33 step=400/15000 val_RMSE=0.25386 best=0.24914

- [2026-10-21 17:50:02 UTC+8] a2afm seed=33 step=500/15000 val_RMSE=0.25194 best=0.24914

- [2026-10-21 17:50:02 UTC+8] a2afm seed=33 step=600/15000 val_RMSE=0.25508 best=0.24914

- [2026-10-21 17:50:02 UTC+8] a2afm seed=33 step=700/15000 val_RMSE=0.24097 best=0.24097

- [2026-10-21 17:50:03 UTC+8] a2afm seed=33 step=800/15000 val_RMSE=0.24444 best=0.24097

- [2026-10-21 17:50:03 UTC+8] a2afm seed=33 step=900/15000 val_RMSE=0.23307 best=0.23307

- [2026-10-21 17:50:03 UTC+8] a2afm seed=33 step=1000/15000 val_RMSE=0.23231 best=0.23231

- [2026-10-21 17:50:04 UTC+8] a2afm seed=33 step=1100/15000 val_RMSE=0.24846 best=0.23231

- [2026-10-21 17:50:04 UTC+8] a2afm seed=33 step=1200/15000 val_RMSE=0.23044 best=0.23044

- [2026-10-21 17:50:04 UTC+8] a2afm seed=33 step=1300/15000 val_RMSE=0.21776 best=0.21776

- [2026-10-21 17:50:04 UTC+8] a2afm seed=33 step=1400/15000 val_RMSE=0.22864 best=0.21776

- [2026-10-21 17:50:05 UTC+8] a2afm seed=33 step=1500/15000 val_RMSE=0.21390 best=0.21390

- [2026-10-21 17:50:05 UTC+8] a2afm seed=33 step=1600/15000 val_RMSE=0.21957 best=0.21390

- [2026-10-21 17:50:05 UTC+8] a2afm seed=33 step=1700/15000 val_RMSE=0.20695 best=0.20695

- [2026-10-21 17:50:06 UTC+8] a2afm seed=33 step=1800/15000 val_RMSE=0.20522 best=0.20522

- [2026-10-21 17:50:06 UTC+8] a2afm seed=33 step=1900/15000 val_RMSE=0.19478 best=0.19478

- [2026-10-21 17:50:06 UTC+8] a2afm seed=33 step=2000/15000 val_RMSE=0.18766 best=0.18766

- [2026-10-21 17:50:07 UTC+8] a2afm seed=33 step=2100/15000 val_RMSE=0.19770 best=0.18766

- [2026-10-21 17:50:07 UTC+8] a2afm seed=33 step=2200/15000 val_RMSE=0.18206 best=0.18206

- [2026-10-21 17:50:07 UTC+8] a2afm seed=33 step=2300/15000 val_RMSE=0.20053 best=0.18206

- [2026-10-21 17:50:07 UTC+8] a2afm seed=33 step=2400/15000 val_RMSE=0.19932 best=0.18206

- [2026-10-21 17:50:08 UTC+8] a2afm seed=33 step=2500/15000 val_RMSE=0.20506 best=0.18206

- [2026-10-21 17:50:08 UTC+8] a2afm seed=33 step=2600/15000 val_RMSE=0.20449 best=0.18206

- [2026-10-21 17:50:08 UTC+8] a2afm seed=33 step=2700/15000 val_RMSE=0.18268 best=0.18206

- [2026-10-21 17:50:09 UTC+8] a2afm seed=33 step=2800/15000 val_RMSE=0.20493 best=0.18206

- [2026-10-21 17:50:09 UTC+8] a2afm seed=33 step=2900/15000 val_RMSE=0.17561 best=0.17561

- [2026-10-21 17:50:09 UTC+8] a2afm seed=33 step=3000/15000 val_RMSE=0.18312 best=0.17561

- [2026-10-21 17:50:10 UTC+8] a2afm seed=33 step=3100/15000 val_RMSE=0.17369 best=0.17369

- [2026-10-21 17:50:10 UTC+8] a2afm seed=33 step=3200/15000 val_RMSE=0.18138 best=0.17369

- [2026-10-21 17:50:10 UTC+8] a2afm seed=33 step=3300/15000 val_RMSE=0.17280 best=0.17280

- [2026-10-21 17:50:11 UTC+8] a2afm seed=33 step=3400/15000 val_RMSE=0.17890 best=0.17280

- [2026-10-21 17:50:11 UTC+8] a2afm seed=33 step=3500/15000 val_RMSE=0.19041 best=0.17280

- [2026-10-21 17:50:11 UTC+8] a2afm seed=33 step=3600/15000 val_RMSE=0.17857 best=0.17280

- [2026-10-21 17:50:12 UTC+8] a2afm seed=33 step=3700/15000 val_RMSE=0.16939 best=0.16939

- [2026-10-21 17:50:12 UTC+8] a2afm seed=33 step=3800/15000 val_RMSE=0.16401 best=0.16401

- [2026-10-21 17:50:12 UTC+8] a2afm seed=33 step=3900/15000 val_RMSE=0.15785 best=0.15785

- [2026-10-21 17:50:12 UTC+8] a2afm seed=33 step=4000/15000 val_RMSE=0.15970 best=0.15785

- [2026-10-21 17:50:13 UTC+8] a2afm seed=33 step=4100/15000 val_RMSE=0.16731 best=0.15785

- [2026-10-21 17:50:13 UTC+8] a2afm seed=33 step=4200/15000 val_RMSE=0.16892 best=0.15785

- [2026-10-21 17:50:13 UTC+8] a2afm seed=33 step=4300/15000 val_RMSE=0.19559 best=0.15785

- [2026-10-21 17:50:14 UTC+8] a2afm seed=33 step=4400/15000 val_RMSE=0.16521 best=0.15785

- [2026-10-21 17:50:14 UTC+8] a2afm seed=33 step=4500/15000 val_RMSE=0.16595 best=0.15785

- [2026-10-21 17:50:14 UTC+8] a2afm seed=33 step=4600/15000 val_RMSE=0.15571 best=0.15571

- [2026-10-21 17:50:15 UTC+8] a2afm seed=33 step=4700/15000 val_RMSE=0.15293 best=0.15293

- [2026-10-21 17:50:15 UTC+8] a2afm seed=33 step=4800/15000 val_RMSE=0.17389 best=0.15293

- [2026-10-21 17:50:15 UTC+8] a2afm seed=33 step=4900/15000 val_RMSE=0.16525 best=0.15293

- [2026-10-21 17:50:16 UTC+8] a2afm seed=33 step=5000/15000 val_RMSE=0.15510 best=0.15293

- [2026-10-21 17:50:16 UTC+8] a2afm seed=33 step=5100/15000 val_RMSE=0.17914 best=0.15293

- [2026-10-21 17:50:16 UTC+8] a2afm seed=33 step=5200/15000 val_RMSE=0.14838 best=0.14838

- [2026-10-21 17:50:16 UTC+8] a2afm seed=33 step=5300/15000 val_RMSE=0.16326 best=0.14838

- [2026-10-21 17:50:17 UTC+8] a2afm seed=33 step=5400/15000 val_RMSE=0.15840 best=0.14838

- [2026-10-21 17:50:17 UTC+8] a2afm seed=33 step=5500/15000 val_RMSE=0.16169 best=0.14838

- [2026-10-21 17:50:17 UTC+8] a2afm seed=33 step=5600/15000 val_RMSE=0.16579 best=0.14838

- [2026-10-21 17:50:18 UTC+8] a2afm seed=33 step=5700/15000 val_RMSE=0.15420 best=0.14838

- [2026-10-21 17:50:18 UTC+8] a2afm seed=33 step=5800/15000 val_RMSE=0.14974 best=0.14838

- [2026-10-21 17:50:18 UTC+8] a2afm seed=33 step=5900/15000 val_RMSE=0.14538 best=0.14538

- [2026-10-21 17:50:19 UTC+8] a2afm seed=33 step=6000/15000 val_RMSE=0.15927 best=0.14538

- [2026-10-21 17:50:19 UTC+8] a2afm seed=33 step=6100/15000 val_RMSE=0.15608 best=0.14538

- [2026-10-21 17:50:19 UTC+8] a2afm seed=33 step=6200/15000 val_RMSE=0.15967 best=0.14538

- [2026-10-21 17:50:19 UTC+8] a2afm seed=33 step=6300/15000 val_RMSE=0.14379 best=0.14379

- [2026-10-21 17:50:20 UTC+8] a2afm seed=33 step=6400/15000 val_RMSE=0.14238 best=0.14238

- [2026-10-21 17:50:20 UTC+8] a2afm seed=33 step=6500/15000 val_RMSE=0.14182 best=0.14182

- [2026-10-21 17:50:20 UTC+8] a2afm seed=33 step=6600/15000 val_RMSE=0.15140 best=0.14182

- [2026-10-21 17:50:21 UTC+8] a2afm seed=33 step=6700/15000 val_RMSE=0.15647 best=0.14182

- [2026-10-21 17:50:21 UTC+8] a2afm seed=33 step=6800/15000 val_RMSE=0.16631 best=0.14182

- [2026-10-21 17:50:21 UTC+8] a2afm seed=33 step=6900/15000 val_RMSE=0.18383 best=0.14182

- [2026-10-21 17:50:22 UTC+8] a2afm seed=33 step=7000/15000 val_RMSE=0.14748 best=0.14182

- [2026-10-21 17:50:22 UTC+8] a2afm seed=33 step=7100/15000 val_RMSE=0.13359 best=0.13359

- [2026-10-21 17:50:22 UTC+8] a2afm seed=33 step=7200/15000 val_RMSE=0.13471 best=0.13359

- [2026-10-21 17:50:23 UTC+8] a2afm seed=33 step=7300/15000 val_RMSE=0.15916 best=0.13359

- [2026-10-21 17:50:23 UTC+8] a2afm seed=33 step=7400/15000 val_RMSE=0.14452 best=0.13359

- [2026-10-21 17:50:23 UTC+8] a2afm seed=33 step=7500/15000 val_RMSE=0.14685 best=0.13359

- [2026-10-21 17:50:23 UTC+8] a2afm seed=33 step=7600/15000 val_RMSE=0.14352 best=0.13359

- [2026-10-21 17:50:24 UTC+8] a2afm seed=33 step=7700/15000 val_RMSE=0.15384 best=0.13359

- [2026-10-21 17:51:29 UTC+8] 单步混合实验开始：CPU，训练轨迹=360，每模型更新=15000

- [2026-10-21 17:52:14 UTC+8] 混合数据完成：训练窗口=136080，验证窗口=17010

- [2026-10-21 17:52:14 UTC+8] 恢复 a2afm seed=33，训练步数 7700

- [2026-10-21 17:52:14 UTC+8] a2afm seed=33 step=7800/15000 val_RMSE=0.13996 best=0.13359

- [2026-10-21 17:52:15 UTC+8] a2afm seed=33 step=7900/15000 val_RMSE=0.15012 best=0.13359

- [2026-10-21 17:52:15 UTC+8] a2afm seed=33 step=8000/15000 val_RMSE=0.14358 best=0.13359

- [2026-10-21 17:52:15 UTC+8] a2afm seed=33 step=8100/15000 val_RMSE=0.18706 best=0.13359

- [2026-10-21 17:52:15 UTC+8] a2afm seed=33 step=8200/15000 val_RMSE=0.13310 best=0.13310

- [2026-10-21 17:52:15 UTC+8] a2afm seed=33 step=8300/15000 val_RMSE=0.13922 best=0.13310

- [2026-10-21 17:52:16 UTC+8] a2afm seed=33 step=8400/15000 val_RMSE=0.14430 best=0.13310

- [2026-10-21 17:52:16 UTC+8] a2afm seed=33 step=8500/15000 val_RMSE=0.15723 best=0.13310

- [2026-10-21 17:52:16 UTC+8] a2afm seed=33 step=8600/15000 val_RMSE=0.15321 best=0.13310

- [2026-10-21 17:52:16 UTC+8] a2afm seed=33 step=8700/15000 val_RMSE=0.14092 best=0.13310

- [2026-10-21 17:52:16 UTC+8] a2afm seed=33 step=8800/15000 val_RMSE=0.12927 best=0.12927

- [2026-10-21 17:52:17 UTC+8] a2afm seed=33 step=8900/15000 val_RMSE=0.12620 best=0.12620

- [2026-10-21 17:52:17 UTC+8] a2afm seed=33 step=9000/15000 val_RMSE=0.14450 best=0.12620

- [2026-10-21 17:52:17 UTC+8] a2afm seed=33 step=9100/15000 val_RMSE=0.14200 best=0.12620

- [2026-10-21 17:52:17 UTC+8] a2afm seed=33 step=9200/15000 val_RMSE=0.13388 best=0.12620

- [2026-10-21 17:52:18 UTC+8] a2afm seed=33 step=9300/15000 val_RMSE=0.15936 best=0.12620

- [2026-10-21 17:52:18 UTC+8] a2afm seed=33 step=9400/15000 val_RMSE=0.15255 best=0.12620

- [2026-10-21 17:52:18 UTC+8] a2afm seed=33 step=9500/15000 val_RMSE=0.13935 best=0.12620

- [2026-10-21 17:52:18 UTC+8] a2afm seed=33 step=9600/15000 val_RMSE=0.13782 best=0.12620

- [2026-10-21 17:52:18 UTC+8] a2afm seed=33 step=9700/15000 val_RMSE=0.13741 best=0.12620

- [2026-10-21 17:52:19 UTC+8] a2afm seed=33 step=9800/15000 val_RMSE=0.12694 best=0.12620

- [2026-10-21 17:52:19 UTC+8] a2afm seed=33 step=9900/15000 val_RMSE=0.15590 best=0.12620

- [2026-10-21 17:52:19 UTC+8] a2afm seed=33 step=10000/15000 val_RMSE=0.14144 best=0.12620

- [2026-10-21 17:52:19 UTC+8] a2afm seed=33 step=10100/15000 val_RMSE=0.13129 best=0.12620

- [2026-10-21 17:52:19 UTC+8] a2afm seed=33 step=10200/15000 val_RMSE=0.13220 best=0.12620

- [2026-10-21 17:52:20 UTC+8] a2afm seed=33 step=10300/15000 val_RMSE=0.13600 best=0.12620

- [2026-10-21 17:52:20 UTC+8] a2afm seed=33 step=10400/15000 val_RMSE=0.12483 best=0.12483

- [2026-10-21 17:52:20 UTC+8] a2afm seed=33 step=10500/15000 val_RMSE=0.13376 best=0.12483

- [2026-10-21 17:52:20 UTC+8] a2afm seed=33 step=10600/15000 val_RMSE=0.17761 best=0.12483

- [2026-10-21 17:52:21 UTC+8] a2afm seed=33 step=10700/15000 val_RMSE=0.13983 best=0.12483

- [2026-10-21 17:52:21 UTC+8] a2afm seed=33 step=10800/15000 val_RMSE=0.13022 best=0.12483

- [2026-10-21 17:52:21 UTC+8] a2afm seed=33 step=10900/15000 val_RMSE=0.13872 best=0.12483

- [2026-10-21 17:52:21 UTC+8] a2afm seed=33 step=11000/15000 val_RMSE=0.12821 best=0.12483

- [2026-10-21 17:52:21 UTC+8] a2afm seed=33 step=11100/15000 val_RMSE=0.12678 best=0.12483

- [2026-10-21 17:52:22 UTC+8] a2afm seed=33 step=11200/15000 val_RMSE=0.14680 best=0.12483

- [2026-10-21 17:52:22 UTC+8] a2afm seed=33 step=11300/15000 val_RMSE=0.14806 best=0.12483

- [2026-10-21 17:52:22 UTC+8] a2afm seed=33 step=11400/15000 val_RMSE=0.14227 best=0.12483

- [2026-10-21 17:52:22 UTC+8] a2afm seed=33 step=11500/15000 val_RMSE=0.13405 best=0.12483

- [2026-10-21 17:52:22 UTC+8] a2afm seed=33 step=11600/15000 val_RMSE=0.13047 best=0.12483

- [2026-10-21 17:52:23 UTC+8] a2afm seed=33 step=11700/15000 val_RMSE=0.14681 best=0.12483

- [2026-10-21 17:52:23 UTC+8] a2afm seed=33 step=11800/15000 val_RMSE=0.12791 best=0.12483

- [2026-10-21 17:52:23 UTC+8] a2afm seed=33 step=11900/15000 val_RMSE=0.16757 best=0.12483

- [2026-10-21 17:52:23 UTC+8] a2afm seed=33 step=12000/15000 val_RMSE=0.14075 best=0.12483

- [2026-10-21 17:52:24 UTC+8] a2afm seed=33 step=12100/15000 val_RMSE=0.14377 best=0.12483

- [2026-10-21 17:52:24 UTC+8] a2afm seed=33 step=12200/15000 val_RMSE=0.13300 best=0.12483

- [2026-10-21 17:52:24 UTC+8] a2afm seed=33 step=12300/15000 val_RMSE=0.12927 best=0.12483

- [2026-10-21 17:55:44 UTC+8] 单步混合实验开始：CPU，训练轨迹=360，每模型更新=15000

- [2026-10-21 17:56:29 UTC+8] 混合数据完成：训练窗口=136080，验证窗口=17010

- [2026-10-21 17:56:29 UTC+8] 恢复 a2afm seed=33，训练步数 12300

- [2026-10-21 17:56:30 UTC+8] a2afm seed=33 step=12400/15000 val_RMSE=0.12718 best=0.12483

- [2026-10-21 17:56:30 UTC+8] a2afm seed=33 step=12500/15000 val_RMSE=0.14981 best=0.12483

- [2026-10-21 17:56:30 UTC+8] a2afm seed=33 step=12600/15000 val_RMSE=0.14481 best=0.12483

- [2026-10-21 17:56:30 UTC+8] a2afm seed=33 step=12700/15000 val_RMSE=0.13604 best=0.12483

- [2026-10-21 17:56:30 UTC+8] a2afm seed=33 step=12800/15000 val_RMSE=0.12795 best=0.12483

- [2026-10-21 17:56:31 UTC+8] a2afm seed=33 step=12900/15000 val_RMSE=0.14467 best=0.12483

- [2026-10-21 17:56:31 UTC+8] a2afm seed=33 step=13000/15000 val_RMSE=0.13850 best=0.12483

- [2026-10-21 17:56:31 UTC+8] a2afm seed=33 step=13100/15000 val_RMSE=0.13171 best=0.12483

- [2026-10-21 17:56:31 UTC+8] a2afm seed=33 step=13200/15000 val_RMSE=0.13515 best=0.12483

- [2026-10-21 17:56:32 UTC+8] a2afm seed=33 step=13300/15000 val_RMSE=0.15241 best=0.12483

- [2026-10-21 17:56:32 UTC+8] a2afm seed=33 step=13400/15000 val_RMSE=0.12264 best=0.12264

- [2026-10-21 17:56:32 UTC+8] a2afm seed=33 step=13500/15000 val_RMSE=0.13015 best=0.12264

- [2026-10-21 17:56:32 UTC+8] a2afm seed=33 step=13600/15000 val_RMSE=0.14484 best=0.12264

- [2026-10-21 17:56:32 UTC+8] a2afm seed=33 step=13700/15000 val_RMSE=0.13731 best=0.12264

- [2026-10-21 17:56:33 UTC+8] a2afm seed=33 step=13800/15000 val_RMSE=0.12767 best=0.12264

- [2026-10-21 17:56:33 UTC+8] a2afm seed=33 step=13900/15000 val_RMSE=0.13347 best=0.12264

- [2026-10-21 17:56:33 UTC+8] a2afm seed=33 step=14000/15000 val_RMSE=0.12815 best=0.12264

- [2026-10-21 17:56:33 UTC+8] a2afm seed=33 step=14100/15000 val_RMSE=0.16003 best=0.12264

- [2026-10-21 17:56:33 UTC+8] a2afm seed=33 step=14200/15000 val_RMSE=0.12413 best=0.12264

- [2026-10-21 17:56:34 UTC+8] a2afm seed=33 step=14300/15000 val_RMSE=0.15493 best=0.12264

- [2026-10-21 17:56:34 UTC+8] a2afm seed=33 step=14400/15000 val_RMSE=0.12317 best=0.12264

- [2026-10-21 17:56:34 UTC+8] a2afm seed=33 step=14500/15000 val_RMSE=0.14572 best=0.12264

- [2026-10-21 17:56:34 UTC+8] a2afm seed=33 step=14600/15000 val_RMSE=0.13380 best=0.12264

- [2026-10-21 17:56:35 UTC+8] a2afm seed=33 step=14700/15000 val_RMSE=0.12664 best=0.12264

- [2026-10-21 17:56:35 UTC+8] a2afm seed=33 step=14800/15000 val_RMSE=0.12275 best=0.12264

- [2026-10-21 17:56:35 UTC+8] a2afm seed=33 step=14900/15000 val_RMSE=0.13326 best=0.12264

- [2026-10-21 17:56:35 UTC+8] a2afm seed=33 step=15000/15000 val_RMSE=0.13948 best=0.12264

- [2026-10-21 17:56:35 UTC+8] 完成 a2afm seed=33，本轮耗时 5.8 s，选择验证最优 step=13400

- [2026-10-21 17:56:36 UTC+8] a2afm seed=11 step=100/15000 val_RMSE=0.26641 best=0.26641

- [2026-10-21 17:56:37 UTC+8] a2afm seed=11 step=200/15000 val_RMSE=0.24802 best=0.24802

- [2026-10-21 17:56:37 UTC+8] a2afm seed=11 step=300/15000 val_RMSE=0.24499 best=0.24499

- [2026-10-21 17:56:38 UTC+8] a2afm seed=11 step=400/15000 val_RMSE=0.24892 best=0.24499

- [2026-10-21 17:56:39 UTC+8] a2afm seed=11 step=500/15000 val_RMSE=0.24596 best=0.24499

- [2026-10-21 17:56:39 UTC+8] a2afm seed=11 step=600/15000 val_RMSE=0.22752 best=0.22752

- [2026-10-21 17:56:40 UTC+8] a2afm seed=11 step=700/15000 val_RMSE=0.22683 best=0.22683

- [2026-10-21 17:56:41 UTC+8] a2afm seed=11 step=800/15000 val_RMSE=0.22031 best=0.22031

- [2026-10-21 17:56:42 UTC+8] a2afm seed=11 step=900/15000 val_RMSE=0.21933 best=0.21933

- [2026-10-21 17:56:42 UTC+8] a2afm seed=11 step=1000/15000 val_RMSE=0.21586 best=0.21586

- [2026-10-21 17:56:43 UTC+8] a2afm seed=11 step=1100/15000 val_RMSE=0.22284 best=0.21586

- [2026-10-21 17:56:44 UTC+8] a2afm seed=11 step=1200/15000 val_RMSE=0.19899 best=0.19899

- [2026-10-21 17:56:44 UTC+8] a2afm seed=11 step=1300/15000 val_RMSE=0.20554 best=0.19899

- [2026-10-21 17:56:45 UTC+8] a2afm seed=11 step=1400/15000 val_RMSE=0.20104 best=0.19899

- [2026-10-21 17:56:46 UTC+8] a2afm seed=11 step=1500/15000 val_RMSE=0.20686 best=0.19899

- [2026-10-21 17:56:46 UTC+8] a2afm seed=11 step=1600/15000 val_RMSE=0.18696 best=0.18696

- [2026-10-21 17:56:47 UTC+8] a2afm seed=11 step=1700/15000 val_RMSE=0.19128 best=0.18696

- [2026-10-21 17:56:48 UTC+8] a2afm seed=11 step=1800/15000 val_RMSE=0.18188 best=0.18188

- [2026-10-21 17:56:48 UTC+8] a2afm seed=11 step=1900/15000 val_RMSE=0.19152 best=0.18188

- [2026-10-21 17:56:49 UTC+8] a2afm seed=11 step=2000/15000 val_RMSE=0.21868 best=0.18188

- [2026-10-21 17:56:50 UTC+8] a2afm seed=11 step=2100/15000 val_RMSE=0.18536 best=0.18188

- [2026-10-21 17:56:51 UTC+8] a2afm seed=11 step=2200/15000 val_RMSE=0.17983 best=0.17983

- [2026-10-21 17:56:51 UTC+8] a2afm seed=11 step=2300/15000 val_RMSE=0.18591 best=0.17983

- [2026-10-21 17:56:52 UTC+8] a2afm seed=11 step=2400/15000 val_RMSE=0.18101 best=0.17983

- [2026-10-21 17:56:53 UTC+8] a2afm seed=11 step=2500/15000 val_RMSE=0.17447 best=0.17447

- [2026-10-21 17:56:53 UTC+8] a2afm seed=11 step=2600/15000 val_RMSE=0.17738 best=0.17447

- [2026-10-21 17:56:54 UTC+8] a2afm seed=11 step=2700/15000 val_RMSE=0.18266 best=0.17447

- [2026-10-21 17:56:55 UTC+8] a2afm seed=11 step=2800/15000 val_RMSE=0.16710 best=0.16710

- [2026-10-21 17:56:56 UTC+8] a2afm seed=11 step=2900/15000 val_RMSE=0.16729 best=0.16710

- [2026-10-21 17:56:56 UTC+8] a2afm seed=11 step=3000/15000 val_RMSE=0.16905 best=0.16710

- [2026-10-21 17:56:57 UTC+8] a2afm seed=11 step=3100/15000 val_RMSE=0.16430 best=0.16430

- [2026-10-21 17:56:58 UTC+8] a2afm seed=11 step=3200/15000 val_RMSE=0.16540 best=0.16430

- [2026-10-21 17:56:58 UTC+8] a2afm seed=11 step=3300/15000 val_RMSE=0.19718 best=0.16430

- [2026-10-21 17:56:59 UTC+8] a2afm seed=11 step=3400/15000 val_RMSE=0.19034 best=0.16430

- [2026-10-21 17:57:00 UTC+8] a2afm seed=11 step=3500/15000 val_RMSE=0.17150 best=0.16430

- [2026-10-21 17:57:00 UTC+8] a2afm seed=11 step=3600/15000 val_RMSE=0.15865 best=0.15865

- [2026-10-21 17:57:01 UTC+8] a2afm seed=11 step=3700/15000 val_RMSE=0.18289 best=0.15865

- [2026-10-21 17:57:02 UTC+8] a2afm seed=11 step=3800/15000 val_RMSE=0.17495 best=0.15865

- [2026-10-21 17:57:02 UTC+8] a2afm seed=11 step=3900/15000 val_RMSE=0.15132 best=0.15132

- [2026-10-21 17:57:03 UTC+8] a2afm seed=11 step=4000/15000 val_RMSE=0.15843 best=0.15132

- [2026-10-21 17:57:04 UTC+8] a2afm seed=11 step=4100/15000 val_RMSE=0.18118 best=0.15132

- [2026-10-21 17:57:05 UTC+8] a2afm seed=11 step=4200/15000 val_RMSE=0.16086 best=0.15132

- [2026-10-21 17:57:05 UTC+8] a2afm seed=11 step=4300/15000 val_RMSE=0.15751 best=0.15132

- [2026-10-21 17:57:06 UTC+8] a2afm seed=11 step=4400/15000 val_RMSE=0.15603 best=0.15132

- [2026-10-21 17:57:07 UTC+8] a2afm seed=11 step=4500/15000 val_RMSE=0.16748 best=0.15132

- [2026-10-21 17:57:07 UTC+8] a2afm seed=11 step=4600/15000 val_RMSE=0.15377 best=0.15132

- [2026-10-21 17:57:08 UTC+8] a2afm seed=11 step=4700/15000 val_RMSE=0.14998 best=0.14998

- [2026-10-21 17:57:09 UTC+8] a2afm seed=11 step=4800/15000 val_RMSE=0.15425 best=0.14998

- [2026-10-21 17:57:10 UTC+8] a2afm seed=11 step=4900/15000 val_RMSE=0.14851 best=0.14851

- [2026-10-21 17:57:10 UTC+8] a2afm seed=11 step=5000/15000 val_RMSE=0.18427 best=0.14851

- [2026-10-21 17:57:11 UTC+8] a2afm seed=11 step=5100/15000 val_RMSE=0.15573 best=0.14851

- [2026-10-21 17:57:12 UTC+8] a2afm seed=11 step=5200/15000 val_RMSE=0.16775 best=0.14851

- [2026-10-21 17:57:12 UTC+8] a2afm seed=11 step=5300/15000 val_RMSE=0.14268 best=0.14268

- [2026-10-21 17:57:13 UTC+8] a2afm seed=11 step=5400/15000 val_RMSE=0.16107 best=0.14268

- [2026-10-21 17:57:14 UTC+8] a2afm seed=11 step=5500/15000 val_RMSE=0.14856 best=0.14268

- [2026-10-21 17:57:14 UTC+8] a2afm seed=11 step=5600/15000 val_RMSE=0.14772 best=0.14268

- [2026-10-21 17:57:15 UTC+8] a2afm seed=11 step=5700/15000 val_RMSE=0.15403 best=0.14268

- [2026-10-21 17:57:16 UTC+8] a2afm seed=11 step=5800/15000 val_RMSE=0.13818 best=0.13818

- [2026-10-21 17:57:17 UTC+8] a2afm seed=11 step=5900/15000 val_RMSE=0.16916 best=0.13818

- [2026-10-21 17:57:17 UTC+8] a2afm seed=11 step=6000/15000 val_RMSE=0.15434 best=0.13818

- [2026-10-21 17:57:18 UTC+8] a2afm seed=11 step=6100/15000 val_RMSE=0.14024 best=0.13818

- [2026-10-21 17:57:19 UTC+8] a2afm seed=11 step=6200/15000 val_RMSE=0.14851 best=0.13818

- [2026-10-21 17:57:19 UTC+8] a2afm seed=11 step=6300/15000 val_RMSE=0.15472 best=0.13818

- [2026-10-21 17:57:20 UTC+8] a2afm seed=11 step=6400/15000 val_RMSE=0.15523 best=0.13818

- [2026-10-21 17:57:21 UTC+8] a2afm seed=11 step=6500/15000 val_RMSE=0.14975 best=0.13818

- [2026-10-21 17:57:21 UTC+8] a2afm seed=11 step=6600/15000 val_RMSE=0.16052 best=0.13818

- [2026-10-21 17:57:22 UTC+8] a2afm seed=11 step=6700/15000 val_RMSE=0.14701 best=0.13818

- [2026-10-21 17:57:23 UTC+8] a2afm seed=11 step=6800/15000 val_RMSE=0.14939 best=0.13818

- [2026-10-21 17:57:24 UTC+8] a2afm seed=11 step=6900/15000 val_RMSE=0.14507 best=0.13818

- [2026-10-21 17:57:24 UTC+8] a2afm seed=11 step=7000/15000 val_RMSE=0.14200 best=0.13818

- [2026-10-21 17:57:25 UTC+8] a2afm seed=11 step=7100/15000 val_RMSE=0.13750 best=0.13750

- [2026-10-21 17:57:26 UTC+8] a2afm seed=11 step=7200/15000 val_RMSE=0.17037 best=0.13750

- [2026-10-21 17:57:26 UTC+8] a2afm seed=11 step=7300/15000 val_RMSE=0.14915 best=0.13750

- [2026-10-21 17:57:27 UTC+8] a2afm seed=11 step=7400/15000 val_RMSE=0.13416 best=0.13416

- [2026-10-21 17:57:28 UTC+8] a2afm seed=11 step=7500/15000 val_RMSE=0.13720 best=0.13416

- [2026-10-21 17:57:28 UTC+8] a2afm seed=11 step=7600/15000 val_RMSE=0.14576 best=0.13416

- [2026-10-21 17:57:29 UTC+8] a2afm seed=11 step=7700/15000 val_RMSE=0.15234 best=0.13416

- [2026-10-21 17:57:30 UTC+8] a2afm seed=11 step=7800/15000 val_RMSE=0.14855 best=0.13416

- [2026-10-21 17:57:31 UTC+8] a2afm seed=11 step=7900/15000 val_RMSE=0.12978 best=0.12978

- [2026-10-21 17:57:31 UTC+8] a2afm seed=11 step=8000/15000 val_RMSE=0.12937 best=0.12937

- [2026-10-21 17:57:32 UTC+8] a2afm seed=11 step=8100/15000 val_RMSE=0.14369 best=0.12937

- [2026-10-21 17:57:33 UTC+8] a2afm seed=11 step=8200/15000 val_RMSE=0.12726 best=0.12726

- [2026-10-21 17:57:33 UTC+8] a2afm seed=11 step=8300/15000 val_RMSE=0.12918 best=0.12726

- [2026-10-21 17:57:34 UTC+8] a2afm seed=11 step=8400/15000 val_RMSE=0.14216 best=0.12726

- [2026-10-21 17:57:35 UTC+8] a2afm seed=11 step=8500/15000 val_RMSE=0.13928 best=0.12726

- [2026-10-21 17:57:35 UTC+8] a2afm seed=11 step=8600/15000 val_RMSE=0.13669 best=0.12726

- [2026-10-21 17:57:36 UTC+8] a2afm seed=11 step=8700/15000 val_RMSE=0.14107 best=0.12726

- [2026-10-21 17:57:37 UTC+8] a2afm seed=11 step=8800/15000 val_RMSE=0.13282 best=0.12726

- [2026-10-21 17:57:38 UTC+8] a2afm seed=11 step=8900/15000 val_RMSE=0.15150 best=0.12726

- [2026-10-21 17:57:38 UTC+8] a2afm seed=11 step=9000/15000 val_RMSE=0.15059 best=0.12726

- [2026-10-21 17:57:39 UTC+8] a2afm seed=11 step=9100/15000 val_RMSE=0.15198 best=0.12726

- [2026-10-21 17:57:40 UTC+8] a2afm seed=11 step=9200/15000 val_RMSE=0.14157 best=0.12726

- [2026-10-21 17:57:40 UTC+8] a2afm seed=11 step=9300/15000 val_RMSE=0.13655 best=0.12726

- [2026-10-21 17:57:41 UTC+8] a2afm seed=11 step=9400/15000 val_RMSE=0.15482 best=0.12726

- [2026-10-21 17:57:42 UTC+8] a2afm seed=11 step=9500/15000 val_RMSE=0.15351 best=0.12726

- [2026-10-21 17:57:42 UTC+8] a2afm seed=11 step=9600/15000 val_RMSE=0.13648 best=0.12726

- [2026-10-21 17:57:43 UTC+8] a2afm seed=11 step=9700/15000 val_RMSE=0.12999 best=0.12726

- [2026-10-21 17:57:44 UTC+8] a2afm seed=11 step=9800/15000 val_RMSE=0.13647 best=0.12726

- [2026-10-21 17:57:45 UTC+8] a2afm seed=11 step=9900/15000 val_RMSE=0.17805 best=0.12726

- [2026-10-21 17:57:45 UTC+8] a2afm seed=11 step=10000/15000 val_RMSE=0.13354 best=0.12726

- [2026-10-21 17:57:46 UTC+8] a2afm seed=11 step=10100/15000 val_RMSE=0.12741 best=0.12726

- [2026-10-21 17:57:47 UTC+8] a2afm seed=11 step=10200/15000 val_RMSE=0.12592 best=0.12592

- [2026-10-21 17:57:47 UTC+8] a2afm seed=11 step=10300/15000 val_RMSE=0.13848 best=0.12592

- [2026-10-21 17:57:48 UTC+8] a2afm seed=11 step=10400/15000 val_RMSE=0.12804 best=0.12592

- [2026-10-21 17:57:49 UTC+8] a2afm seed=11 step=10500/15000 val_RMSE=0.13589 best=0.12592

- [2026-10-21 17:57:49 UTC+8] a2afm seed=11 step=10600/15000 val_RMSE=0.14825 best=0.12592

- [2026-10-21 17:57:50 UTC+8] a2afm seed=11 step=10700/15000 val_RMSE=0.12983 best=0.12592

- [2026-10-21 17:57:51 UTC+8] a2afm seed=11 step=10800/15000 val_RMSE=0.14903 best=0.12592

- [2026-10-21 17:57:52 UTC+8] a2afm seed=11 step=10900/15000 val_RMSE=0.13054 best=0.12592

- [2026-10-21 17:57:52 UTC+8] a2afm seed=11 step=11000/15000 val_RMSE=0.14508 best=0.12592

- [2026-10-21 17:57:53 UTC+8] a2afm seed=11 step=11100/15000 val_RMSE=0.13361 best=0.12592

- [2026-10-21 17:57:54 UTC+8] a2afm seed=11 step=11200/15000 val_RMSE=0.14386 best=0.12592

- [2026-10-21 17:57:54 UTC+8] a2afm seed=11 step=11300/15000 val_RMSE=0.14008 best=0.12592

- [2026-10-21 17:57:55 UTC+8] a2afm seed=11 step=11400/15000 val_RMSE=0.14115 best=0.12592

- [2026-10-21 17:57:56 UTC+8] a2afm seed=11 step=11500/15000 val_RMSE=0.14699 best=0.12592

- [2026-10-21 17:57:56 UTC+8] a2afm seed=11 step=11600/15000 val_RMSE=0.12694 best=0.12592

- [2026-10-21 17:57:57 UTC+8] a2afm seed=11 step=11700/15000 val_RMSE=0.15352 best=0.12592

- [2026-10-21 17:57:58 UTC+8] a2afm seed=11 step=11800/15000 val_RMSE=0.12210 best=0.12210

- [2026-10-21 17:57:59 UTC+8] a2afm seed=11 step=11900/15000 val_RMSE=0.13872 best=0.12210

- [2026-10-21 17:57:59 UTC+8] a2afm seed=11 step=12000/15000 val_RMSE=0.14194 best=0.12210

- [2026-10-21 17:58:00 UTC+8] a2afm seed=11 step=12100/15000 val_RMSE=0.12010 best=0.12010

- [2026-10-21 17:58:01 UTC+8] a2afm seed=11 step=12200/15000 val_RMSE=0.15872 best=0.12010

- [2026-10-21 17:58:01 UTC+8] a2afm seed=11 step=12300/15000 val_RMSE=0.12816 best=0.12010

- [2026-10-21 17:58:02 UTC+8] a2afm seed=11 step=12400/15000 val_RMSE=0.12420 best=0.12010

- [2026-10-21 17:58:03 UTC+8] a2afm seed=11 step=12500/15000 val_RMSE=0.12513 best=0.12010

- [2026-10-21 17:58:04 UTC+8] a2afm seed=11 step=12600/15000 val_RMSE=0.12688 best=0.12010

- [2026-10-21 17:58:04 UTC+8] a2afm seed=11 step=12700/15000 val_RMSE=0.13288 best=0.12010

- [2026-10-21 17:58:05 UTC+8] a2afm seed=11 step=12800/15000 val_RMSE=0.13391 best=0.12010

- [2026-10-21 17:58:06 UTC+8] a2afm seed=11 step=12900/15000 val_RMSE=0.13120 best=0.12010

- [2026-10-21 17:58:06 UTC+8] a2afm seed=11 step=13000/15000 val_RMSE=0.12362 best=0.12010

- [2026-10-21 17:58:07 UTC+8] a2afm seed=11 step=13100/15000 val_RMSE=0.14056 best=0.12010

- [2026-10-21 17:58:08 UTC+8] a2afm seed=11 step=13200/15000 val_RMSE=0.15369 best=0.12010

- [2026-10-21 17:58:08 UTC+8] a2afm seed=11 step=13300/15000 val_RMSE=0.16224 best=0.12010

- [2026-10-21 17:58:09 UTC+8] a2afm seed=11 step=13400/15000 val_RMSE=0.11987 best=0.11987

- [2026-10-21 17:58:10 UTC+8] a2afm seed=11 step=13500/15000 val_RMSE=0.11979 best=0.11979

- [2026-10-21 17:58:11 UTC+8] a2afm seed=11 step=13600/15000 val_RMSE=0.13982 best=0.11979

- [2026-10-21 17:58:11 UTC+8] a2afm seed=11 step=13700/15000 val_RMSE=0.12736 best=0.11979

- [2026-10-21 17:58:12 UTC+8] a2afm seed=11 step=13800/15000 val_RMSE=0.13166 best=0.11979

- [2026-10-21 17:58:13 UTC+8] a2afm seed=11 step=13900/15000 val_RMSE=0.14021 best=0.11979

- [2026-10-21 17:58:13 UTC+8] a2afm seed=11 step=14000/15000 val_RMSE=0.12831 best=0.11979

- [2026-10-21 17:58:14 UTC+8] a2afm seed=11 step=14100/15000 val_RMSE=0.14633 best=0.11979

- [2026-10-21 17:58:15 UTC+8] a2afm seed=11 step=14200/15000 val_RMSE=0.12328 best=0.11979

- [2026-10-21 17:58:15 UTC+8] a2afm seed=11 step=14300/15000 val_RMSE=0.13217 best=0.11979

- [2026-10-21 17:58:16 UTC+8] a2afm seed=11 step=14400/15000 val_RMSE=0.13019 best=0.11979

- [2026-10-21 17:58:17 UTC+8] a2afm seed=11 step=14500/15000 val_RMSE=0.13749 best=0.11979

- [2026-10-21 17:58:18 UTC+8] a2afm seed=11 step=14600/15000 val_RMSE=0.13252 best=0.11979

- [2026-10-21 17:58:18 UTC+8] a2afm seed=11 step=14700/15000 val_RMSE=0.12986 best=0.11979

- [2026-10-21 17:58:19 UTC+8] a2afm seed=11 step=14800/15000 val_RMSE=0.14128 best=0.11979

- [2026-10-21 17:58:20 UTC+8] a2afm seed=11 step=14900/15000 val_RMSE=0.12902 best=0.11979

- [2026-10-21 17:58:20 UTC+8] a2afm seed=11 step=15000/15000 val_RMSE=0.14158 best=0.11979

- [2026-10-21 17:58:20 UTC+8] 完成 a2afm seed=11，本轮耗时 105.1 s，选择验证最优 step=13500

- [2026-10-21 17:58:21 UTC+8] a2afm seed=22 step=100/15000 val_RMSE=0.27555 best=0.27555

- [2026-10-21 17:58:22 UTC+8] a2afm seed=22 step=200/15000 val_RMSE=0.24783 best=0.24783

- [2026-10-21 17:58:23 UTC+8] a2afm seed=22 step=300/15000 val_RMSE=0.24328 best=0.24328

- [2026-10-21 17:58:23 UTC+8] a2afm seed=22 step=400/15000 val_RMSE=0.24773 best=0.24328

- [2026-10-21 17:58:24 UTC+8] a2afm seed=22 step=500/15000 val_RMSE=0.23199 best=0.23199

- [2026-10-21 17:58:25 UTC+8] a2afm seed=22 step=600/15000 val_RMSE=0.22985 best=0.22985

- [2026-10-21 17:58:25 UTC+8] a2afm seed=22 step=700/15000 val_RMSE=0.23428 best=0.22985

- [2026-10-21 17:58:26 UTC+8] a2afm seed=22 step=800/15000 val_RMSE=0.22889 best=0.22889

- [2026-10-21 17:58:27 UTC+8] a2afm seed=22 step=900/15000 val_RMSE=0.21022 best=0.21022

- [2026-10-21 17:58:27 UTC+8] a2afm seed=22 step=1000/15000 val_RMSE=0.20933 best=0.20933

- [2026-10-21 17:58:28 UTC+8] a2afm seed=22 step=1100/15000 val_RMSE=0.19802 best=0.19802

- [2026-10-21 17:58:29 UTC+8] a2afm seed=22 step=1200/15000 val_RMSE=0.22584 best=0.19802

- [2026-10-21 17:58:30 UTC+8] a2afm seed=22 step=1300/15000 val_RMSE=0.21294 best=0.19802

- [2026-10-21 17:58:30 UTC+8] a2afm seed=22 step=1400/15000 val_RMSE=0.19777 best=0.19777

- [2026-10-21 17:58:31 UTC+8] a2afm seed=22 step=1500/15000 val_RMSE=0.19676 best=0.19676

- [2026-10-21 17:58:32 UTC+8] a2afm seed=22 step=1600/15000 val_RMSE=0.21371 best=0.19676

- [2026-10-21 17:58:32 UTC+8] a2afm seed=22 step=1700/15000 val_RMSE=0.20076 best=0.19676

- [2026-10-21 17:58:33 UTC+8] a2afm seed=22 step=1800/15000 val_RMSE=0.18836 best=0.18836

- [2026-10-21 17:58:34 UTC+8] a2afm seed=22 step=1900/15000 val_RMSE=0.18915 best=0.18836

- [2026-10-21 17:58:34 UTC+8] a2afm seed=22 step=2000/15000 val_RMSE=0.19581 best=0.18836

- [2026-10-21 17:58:35 UTC+8] a2afm seed=22 step=2100/15000 val_RMSE=0.18007 best=0.18007

- [2026-10-21 17:58:36 UTC+8] a2afm seed=22 step=2200/15000 val_RMSE=0.20649 best=0.18007

- [2026-10-21 17:58:37 UTC+8] a2afm seed=22 step=2300/15000 val_RMSE=0.17566 best=0.17566

- [2026-10-21 17:58:37 UTC+8] a2afm seed=22 step=2400/15000 val_RMSE=0.18601 best=0.17566

- [2026-10-21 17:58:38 UTC+8] a2afm seed=22 step=2500/15000 val_RMSE=0.17039 best=0.17039

- [2026-10-21 17:58:39 UTC+8] a2afm seed=22 step=2600/15000 val_RMSE=0.17972 best=0.17039

- [2026-10-21 17:58:39 UTC+8] a2afm seed=22 step=2700/15000 val_RMSE=0.16926 best=0.16926

- [2026-10-21 17:58:40 UTC+8] a2afm seed=22 step=2800/15000 val_RMSE=0.18719 best=0.16926

- [2026-10-21 17:58:41 UTC+8] a2afm seed=22 step=2900/15000 val_RMSE=0.16447 best=0.16447

- [2026-10-21 17:58:41 UTC+8] a2afm seed=22 step=3000/15000 val_RMSE=0.16812 best=0.16447

- [2026-10-21 17:58:42 UTC+8] a2afm seed=22 step=3100/15000 val_RMSE=0.16765 best=0.16447

- [2026-10-21 17:58:43 UTC+8] a2afm seed=22 step=3200/15000 val_RMSE=0.17861 best=0.16447

- [2026-10-21 17:58:44 UTC+8] a2afm seed=22 step=3300/15000 val_RMSE=0.15890 best=0.15890

- [2026-10-21 17:58:44 UTC+8] a2afm seed=22 step=3400/15000 val_RMSE=0.17995 best=0.15890

- [2026-10-21 17:58:45 UTC+8] a2afm seed=22 step=3500/15000 val_RMSE=0.16217 best=0.15890

- [2026-10-21 17:58:46 UTC+8] a2afm seed=22 step=3600/15000 val_RMSE=0.16475 best=0.15890

- [2026-10-21 17:58:46 UTC+8] a2afm seed=22 step=3700/15000 val_RMSE=0.16678 best=0.15890

- [2026-10-21 17:58:47 UTC+8] a2afm seed=22 step=3800/15000 val_RMSE=0.17587 best=0.15890

- [2026-10-21 17:58:48 UTC+8] a2afm seed=22 step=3900/15000 val_RMSE=0.15712 best=0.15712

- [2026-10-21 17:58:48 UTC+8] a2afm seed=22 step=4000/15000 val_RMSE=0.16893 best=0.15712

- [2026-10-21 17:58:49 UTC+8] a2afm seed=22 step=4100/15000 val_RMSE=0.16225 best=0.15712

- [2026-10-21 17:58:50 UTC+8] a2afm seed=22 step=4200/15000 val_RMSE=0.15031 best=0.15031

- [2026-10-21 17:58:51 UTC+8] a2afm seed=22 step=4300/15000 val_RMSE=0.15038 best=0.15031

- [2026-10-21 17:58:51 UTC+8] a2afm seed=22 step=4400/15000 val_RMSE=0.15883 best=0.15031

- [2026-10-21 17:58:52 UTC+8] a2afm seed=22 step=4500/15000 val_RMSE=0.15088 best=0.15031

- [2026-10-21 17:58:53 UTC+8] a2afm seed=22 step=4600/15000 val_RMSE=0.15771 best=0.15031

- [2026-10-21 17:58:53 UTC+8] a2afm seed=22 step=4700/15000 val_RMSE=0.15639 best=0.15031

- [2026-10-21 17:58:54 UTC+8] a2afm seed=22 step=4800/15000 val_RMSE=0.15474 best=0.15031

- [2026-10-21 17:58:55 UTC+8] a2afm seed=22 step=4900/15000 val_RMSE=0.15546 best=0.15031

- [2026-10-21 17:58:56 UTC+8] a2afm seed=22 step=5000/15000 val_RMSE=0.17788 best=0.15031

- [2026-10-21 17:58:56 UTC+8] a2afm seed=22 step=5100/15000 val_RMSE=0.15500 best=0.15031

- [2026-10-21 17:58:57 UTC+8] a2afm seed=22 step=5200/15000 val_RMSE=0.18020 best=0.15031

- [2026-10-21 17:58:58 UTC+8] a2afm seed=22 step=5300/15000 val_RMSE=0.17313 best=0.15031

- [2026-10-21 17:58:58 UTC+8] a2afm seed=22 step=5400/15000 val_RMSE=0.17206 best=0.15031

- [2026-10-21 17:58:59 UTC+8] a2afm seed=22 step=5500/15000 val_RMSE=0.14259 best=0.14259

- [2026-10-21 17:59:00 UTC+8] a2afm seed=22 step=5600/15000 val_RMSE=0.16144 best=0.14259

- [2026-10-21 17:59:00 UTC+8] a2afm seed=22 step=5700/15000 val_RMSE=0.15327 best=0.14259

- [2026-10-21 17:59:01 UTC+8] a2afm seed=22 step=5800/15000 val_RMSE=0.14761 best=0.14259

- [2026-10-21 17:59:02 UTC+8] a2afm seed=22 step=5900/15000 val_RMSE=0.14889 best=0.14259

- [2026-10-21 17:59:03 UTC+8] a2afm seed=22 step=6000/15000 val_RMSE=0.16809 best=0.14259

- [2026-10-21 17:59:03 UTC+8] a2afm seed=22 step=6100/15000 val_RMSE=0.13548 best=0.13548

- [2026-10-21 17:59:04 UTC+8] a2afm seed=22 step=6200/15000 val_RMSE=0.15429 best=0.13548

- [2026-10-21 17:59:05 UTC+8] a2afm seed=22 step=6300/15000 val_RMSE=0.14440 best=0.13548

- [2026-10-21 17:59:05 UTC+8] a2afm seed=22 step=6400/15000 val_RMSE=0.14650 best=0.13548

- [2026-10-21 17:59:06 UTC+8] a2afm seed=22 step=6500/15000 val_RMSE=0.14136 best=0.13548

- [2026-10-21 17:59:07 UTC+8] a2afm seed=22 step=6600/15000 val_RMSE=0.15057 best=0.13548

- [2026-10-21 17:59:07 UTC+8] a2afm seed=22 step=6700/15000 val_RMSE=0.13849 best=0.13548

- [2026-10-21 17:59:08 UTC+8] a2afm seed=22 step=6800/15000 val_RMSE=0.15357 best=0.13548

- [2026-10-21 17:59:09 UTC+8] a2afm seed=22 step=6900/15000 val_RMSE=0.14040 best=0.13548

- [2026-10-21 17:59:10 UTC+8] a2afm seed=22 step=7000/15000 val_RMSE=0.14644 best=0.13548

- [2026-10-21 17:59:10 UTC+8] a2afm seed=22 step=7100/15000 val_RMSE=0.13489 best=0.13489

- [2026-10-21 17:59:11 UTC+8] a2afm seed=22 step=7200/15000 val_RMSE=0.14516 best=0.13489

- [2026-10-21 17:59:12 UTC+8] a2afm seed=22 step=7300/15000 val_RMSE=0.14842 best=0.13489

- [2026-10-21 17:59:12 UTC+8] a2afm seed=22 step=7400/15000 val_RMSE=0.13751 best=0.13489

- [2026-10-21 17:59:13 UTC+8] a2afm seed=22 step=7500/15000 val_RMSE=0.13303 best=0.13303

- [2026-10-21 17:59:14 UTC+8] a2afm seed=22 step=7600/15000 val_RMSE=0.14119 best=0.13303

- [2026-10-21 17:59:14 UTC+8] a2afm seed=22 step=7700/15000 val_RMSE=0.15188 best=0.13303

- [2026-10-21 17:59:15 UTC+8] a2afm seed=22 step=7800/15000 val_RMSE=0.15448 best=0.13303

- [2026-10-21 17:59:16 UTC+8] a2afm seed=22 step=7900/15000 val_RMSE=0.15765 best=0.13303

- [2026-10-21 17:59:17 UTC+8] a2afm seed=22 step=8000/15000 val_RMSE=0.14031 best=0.13303

- [2026-10-21 17:59:17 UTC+8] a2afm seed=22 step=8100/15000 val_RMSE=0.14173 best=0.13303

- [2026-10-21 17:59:18 UTC+8] a2afm seed=22 step=8200/15000 val_RMSE=0.14144 best=0.13303

- [2026-10-21 17:59:19 UTC+8] a2afm seed=22 step=8300/15000 val_RMSE=0.13669 best=0.13303

- [2026-10-21 17:59:19 UTC+8] a2afm seed=22 step=8400/15000 val_RMSE=0.13729 best=0.13303

- [2026-10-21 17:59:20 UTC+8] a2afm seed=22 step=8500/15000 val_RMSE=0.15186 best=0.13303

- [2026-10-21 17:59:21 UTC+8] a2afm seed=22 step=8600/15000 val_RMSE=0.13891 best=0.13303

- [2026-10-21 17:59:21 UTC+8] a2afm seed=22 step=8700/15000 val_RMSE=0.13596 best=0.13303

- [2026-10-21 17:59:22 UTC+8] a2afm seed=22 step=8800/15000 val_RMSE=0.14328 best=0.13303

- [2026-10-21 17:59:23 UTC+8] a2afm seed=22 step=8900/15000 val_RMSE=0.15902 best=0.13303

- [2026-10-21 17:59:24 UTC+8] a2afm seed=22 step=9000/15000 val_RMSE=0.15126 best=0.13303

- [2026-10-21 17:59:24 UTC+8] a2afm seed=22 step=9100/15000 val_RMSE=0.14183 best=0.13303

- [2026-10-21 17:59:25 UTC+8] a2afm seed=22 step=9200/15000 val_RMSE=0.15742 best=0.13303

- [2026-10-21 17:59:26 UTC+8] a2afm seed=22 step=9300/15000 val_RMSE=0.13229 best=0.13229

- [2026-10-21 17:59:26 UTC+8] a2afm seed=22 step=9400/15000 val_RMSE=0.15085 best=0.13229

- [2026-10-21 17:59:27 UTC+8] a2afm seed=22 step=9500/15000 val_RMSE=0.13944 best=0.13229

- [2026-10-21 17:59:28 UTC+8] a2afm seed=22 step=9600/15000 val_RMSE=0.14094 best=0.13229

- [2026-10-21 17:59:28 UTC+8] a2afm seed=22 step=9700/15000 val_RMSE=0.12780 best=0.12780

- [2026-10-21 17:59:29 UTC+8] a2afm seed=22 step=9800/15000 val_RMSE=0.13511 best=0.12780

- [2026-10-21 17:59:30 UTC+8] a2afm seed=22 step=9900/15000 val_RMSE=0.13099 best=0.12780

- [2026-10-21 17:59:31 UTC+8] a2afm seed=22 step=10000/15000 val_RMSE=0.12558 best=0.12558

- [2026-10-21 17:59:31 UTC+8] a2afm seed=22 step=10100/15000 val_RMSE=0.15673 best=0.12558

- [2026-10-21 17:59:32 UTC+8] a2afm seed=22 step=10200/15000 val_RMSE=0.12736 best=0.12558

- [2026-10-21 17:59:33 UTC+8] a2afm seed=22 step=10300/15000 val_RMSE=0.13210 best=0.12558

- [2026-10-21 17:59:33 UTC+8] a2afm seed=22 step=10400/15000 val_RMSE=0.13026 best=0.12558

- [2026-10-21 17:59:34 UTC+8] a2afm seed=22 step=10500/15000 val_RMSE=0.14429 best=0.12558

- [2026-10-21 17:59:35 UTC+8] a2afm seed=22 step=10600/15000 val_RMSE=0.13619 best=0.12558

- [2026-10-21 17:59:35 UTC+8] a2afm seed=22 step=10700/15000 val_RMSE=0.13550 best=0.12558

- [2026-10-21 17:59:36 UTC+8] a2afm seed=22 step=10800/15000 val_RMSE=0.11809 best=0.11809

- [2026-10-21 17:59:37 UTC+8] a2afm seed=22 step=10900/15000 val_RMSE=0.13561 best=0.11809

- [2026-10-21 17:59:38 UTC+8] a2afm seed=22 step=11000/15000 val_RMSE=0.14116 best=0.11809

- [2026-10-21 17:59:38 UTC+8] a2afm seed=22 step=11100/15000 val_RMSE=0.14198 best=0.11809

- [2026-10-21 17:59:39 UTC+8] a2afm seed=22 step=11200/15000 val_RMSE=0.15730 best=0.11809

- [2026-10-21 17:59:40 UTC+8] a2afm seed=22 step=11300/15000 val_RMSE=0.13266 best=0.11809

- [2026-10-21 17:59:40 UTC+8] a2afm seed=22 step=11400/15000 val_RMSE=0.12061 best=0.11809

- [2026-10-21 17:59:41 UTC+8] a2afm seed=22 step=11500/15000 val_RMSE=0.13626 best=0.11809

- [2026-10-21 17:59:42 UTC+8] a2afm seed=22 step=11600/15000 val_RMSE=0.12371 best=0.11809

- [2026-10-21 17:59:42 UTC+8] a2afm seed=22 step=11700/15000 val_RMSE=0.15205 best=0.11809

- [2026-10-21 17:59:43 UTC+8] a2afm seed=22 step=11800/15000 val_RMSE=0.13771 best=0.11809

- [2026-10-21 17:59:44 UTC+8] a2afm seed=22 step=11900/15000 val_RMSE=0.12560 best=0.11809

- [2026-10-21 17:59:45 UTC+8] a2afm seed=22 step=12000/15000 val_RMSE=0.12332 best=0.11809

- [2026-10-21 17:59:45 UTC+8] a2afm seed=22 step=12100/15000 val_RMSE=0.13675 best=0.11809

- [2026-10-21 17:59:46 UTC+8] a2afm seed=22 step=12200/15000 val_RMSE=0.12974 best=0.11809

- [2026-10-21 17:59:47 UTC+8] a2afm seed=22 step=12300/15000 val_RMSE=0.14929 best=0.11809

- [2026-10-21 17:59:47 UTC+8] a2afm seed=22 step=12400/15000 val_RMSE=0.14114 best=0.11809

- [2026-10-21 17:59:48 UTC+8] a2afm seed=22 step=12500/15000 val_RMSE=0.13585 best=0.11809

- [2026-10-21 17:59:49 UTC+8] a2afm seed=22 step=12600/15000 val_RMSE=0.12709 best=0.11809

- [2026-10-21 17:59:49 UTC+8] a2afm seed=22 step=12700/15000 val_RMSE=0.12381 best=0.11809

- [2026-10-21 17:59:50 UTC+8] a2afm seed=22 step=12800/15000 val_RMSE=0.12492 best=0.11809

- [2026-10-21 17:59:51 UTC+8] a2afm seed=22 step=12900/15000 val_RMSE=0.12440 best=0.11809

- [2026-10-21 17:59:52 UTC+8] a2afm seed=22 step=13000/15000 val_RMSE=0.14001 best=0.11809

- [2026-10-21 17:59:52 UTC+8] a2afm seed=22 step=13100/15000 val_RMSE=0.12526 best=0.11809

- [2026-10-21 17:59:53 UTC+8] a2afm seed=22 step=13200/15000 val_RMSE=0.13264 best=0.11809

- [2026-10-21 17:59:54 UTC+8] a2afm seed=22 step=13300/15000 val_RMSE=0.11745 best=0.11745

- [2026-10-21 17:59:54 UTC+8] a2afm seed=22 step=13400/15000 val_RMSE=0.12968 best=0.11745

- [2026-10-21 17:59:55 UTC+8] a2afm seed=22 step=13500/15000 val_RMSE=0.14042 best=0.11745

- [2026-10-21 17:59:56 UTC+8] a2afm seed=22 step=13600/15000 val_RMSE=0.13947 best=0.11745

- [2026-10-21 17:59:57 UTC+8] a2afm seed=22 step=13700/15000 val_RMSE=0.13683 best=0.11745

- [2026-10-21 17:59:58 UTC+8] a2afm seed=22 step=13800/15000 val_RMSE=0.12660 best=0.11745

- [2026-10-21 17:59:59 UTC+8] a2afm seed=22 step=13900/15000 val_RMSE=0.14649 best=0.11745

- [2026-10-21 18:00:00 UTC+8] a2afm seed=22 step=14000/15000 val_RMSE=0.12824 best=0.11745

- [2026-10-21 18:00:01 UTC+8] a2afm seed=22 step=14100/15000 val_RMSE=0.14928 best=0.11745

- [2026-10-21 18:00:02 UTC+8] a2afm seed=22 step=14200/15000 val_RMSE=0.13517 best=0.11745

- [2026-10-21 18:00:03 UTC+8] a2afm seed=22 step=14300/15000 val_RMSE=0.12791 best=0.11745

- [2026-10-21 18:00:03 UTC+8] a2afm seed=22 step=14400/15000 val_RMSE=0.12694 best=0.11745

- [2026-10-21 18:00:04 UTC+8] a2afm seed=22 step=14500/15000 val_RMSE=0.12502 best=0.11745

- [2026-10-21 18:00:05 UTC+8] a2afm seed=22 step=14600/15000 val_RMSE=0.12556 best=0.11745

- [2026-10-21 18:00:06 UTC+8] a2afm seed=22 step=14700/15000 val_RMSE=0.14616 best=0.11745

- [2026-10-21 18:00:06 UTC+8] a2afm seed=22 step=14800/15000 val_RMSE=0.12419 best=0.11745

- [2026-10-21 18:00:07 UTC+8] a2afm seed=22 step=14900/15000 val_RMSE=0.13205 best=0.11745

- [2026-10-21 18:00:08 UTC+8] a2afm seed=22 step=15000/15000 val_RMSE=0.12436 best=0.11745

- [2026-10-21 18:00:08 UTC+8] 完成 a2afm seed=22，本轮耗时 107.2 s，选择验证最优 step=13300

- [2026-10-21 18:00:08 UTC+8] a2afm seed=33 step=100/15000 val_RMSE=0.26099 best=0.26099

- [2026-10-21 18:00:09 UTC+8] a2afm seed=33 step=200/15000 val_RMSE=0.26052 best=0.26052

- [2026-10-21 18:00:10 UTC+8] a2afm seed=33 step=300/15000 val_RMSE=0.24253 best=0.24253

- [2026-10-21 18:00:10 UTC+8] a2afm seed=33 step=400/15000 val_RMSE=0.24828 best=0.24253

- [2026-10-21 18:00:11 UTC+8] a2afm seed=33 step=500/15000 val_RMSE=0.24514 best=0.24253

- [2026-10-21 18:00:12 UTC+8] a2afm seed=33 step=600/15000 val_RMSE=0.24363 best=0.24253

- [2026-10-21 18:00:13 UTC+8] a2afm seed=33 step=700/15000 val_RMSE=0.22486 best=0.22486

- [2026-10-21 18:00:13 UTC+8] a2afm seed=33 step=800/15000 val_RMSE=0.23051 best=0.22486

- [2026-10-21 18:00:14 UTC+8] a2afm seed=33 step=900/15000 val_RMSE=0.22123 best=0.22123

- [2026-10-21 18:00:15 UTC+8] a2afm seed=33 step=1000/15000 val_RMSE=0.22915 best=0.22123

- [2026-10-21 18:00:15 UTC+8] a2afm seed=33 step=1100/15000 val_RMSE=0.22371 best=0.22123

- [2026-10-21 18:00:16 UTC+8] a2afm seed=33 step=1200/15000 val_RMSE=0.21591 best=0.21591

- [2026-10-21 18:00:17 UTC+8] a2afm seed=33 step=1300/15000 val_RMSE=0.19936 best=0.19936

- [2026-10-21 18:00:17 UTC+8] a2afm seed=33 step=1400/15000 val_RMSE=0.19263 best=0.19263

- [2026-10-21 18:00:18 UTC+8] a2afm seed=33 step=1500/15000 val_RMSE=0.20437 best=0.19263

- [2026-10-21 18:00:19 UTC+8] a2afm seed=33 step=1600/15000 val_RMSE=0.19486 best=0.19263

- [2026-10-21 18:00:20 UTC+8] a2afm seed=33 step=1700/15000 val_RMSE=0.19006 best=0.19006

- [2026-10-21 18:00:20 UTC+8] a2afm seed=33 step=1800/15000 val_RMSE=0.20177 best=0.19006

- [2026-10-21 18:00:21 UTC+8] a2afm seed=33 step=1900/15000 val_RMSE=0.19362 best=0.19006

- [2026-10-21 18:00:22 UTC+8] a2afm seed=33 step=2000/15000 val_RMSE=0.19028 best=0.19006

- [2026-10-21 18:00:22 UTC+8] a2afm seed=33 step=2100/15000 val_RMSE=0.18957 best=0.18957

- [2026-10-21 18:00:23 UTC+8] a2afm seed=33 step=2200/15000 val_RMSE=0.18898 best=0.18898

- [2026-10-21 18:00:24 UTC+8] a2afm seed=33 step=2300/15000 val_RMSE=0.18040 best=0.18040

- [2026-10-21 18:00:24 UTC+8] a2afm seed=33 step=2400/15000 val_RMSE=0.18230 best=0.18040

- [2026-10-21 18:00:25 UTC+8] a2afm seed=33 step=2500/15000 val_RMSE=0.19716 best=0.18040

- [2026-10-21 18:00:26 UTC+8] a2afm seed=33 step=2600/15000 val_RMSE=0.16289 best=0.16289

- [2026-10-21 18:00:27 UTC+8] a2afm seed=33 step=2700/15000 val_RMSE=0.17980 best=0.16289

- [2026-10-21 18:00:27 UTC+8] a2afm seed=33 step=2800/15000 val_RMSE=0.16802 best=0.16289

- [2026-10-21 18:00:28 UTC+8] a2afm seed=33 step=2900/15000 val_RMSE=0.16325 best=0.16289

- [2026-10-21 18:00:29 UTC+8] a2afm seed=33 step=3000/15000 val_RMSE=0.15831 best=0.15831

- [2026-10-21 18:00:29 UTC+8] a2afm seed=33 step=3100/15000 val_RMSE=0.16696 best=0.15831

- [2026-10-21 18:00:30 UTC+8] a2afm seed=33 step=3200/15000 val_RMSE=0.16489 best=0.15831

- [2026-10-21 18:00:31 UTC+8] a2afm seed=33 step=3300/15000 val_RMSE=0.17043 best=0.15831

- [2026-10-21 18:00:31 UTC+8] a2afm seed=33 step=3400/15000 val_RMSE=0.17770 best=0.15831

- [2026-10-21 18:00:32 UTC+8] a2afm seed=33 step=3500/15000 val_RMSE=0.17158 best=0.15831

- [2026-10-21 18:00:33 UTC+8] a2afm seed=33 step=3600/15000 val_RMSE=0.15952 best=0.15831

- [2026-10-21 18:00:33 UTC+8] a2afm seed=33 step=3700/15000 val_RMSE=0.15189 best=0.15189

- [2026-10-21 18:00:34 UTC+8] a2afm seed=33 step=3800/15000 val_RMSE=0.16586 best=0.15189

- [2026-10-21 18:00:35 UTC+8] a2afm seed=33 step=3900/15000 val_RMSE=0.16223 best=0.15189

- [2026-10-21 18:00:36 UTC+8] a2afm seed=33 step=4000/15000 val_RMSE=0.15628 best=0.15189

- [2026-10-21 18:00:36 UTC+8] a2afm seed=33 step=4100/15000 val_RMSE=0.17226 best=0.15189

- [2026-10-21 18:00:37 UTC+8] a2afm seed=33 step=4200/15000 val_RMSE=0.16727 best=0.15189

- [2026-10-21 18:00:38 UTC+8] a2afm seed=33 step=4300/15000 val_RMSE=0.18388 best=0.15189

- [2026-10-21 18:00:38 UTC+8] a2afm seed=33 step=4400/15000 val_RMSE=0.19651 best=0.15189

- [2026-10-21 18:00:39 UTC+8] a2afm seed=33 step=4500/15000 val_RMSE=0.16707 best=0.15189

- [2026-10-21 18:00:40 UTC+8] a2afm seed=33 step=4600/15000 val_RMSE=0.15221 best=0.15189

- [2026-10-21 18:00:40 UTC+8] a2afm seed=33 step=4700/15000 val_RMSE=0.15141 best=0.15141

- [2026-10-21 18:00:41 UTC+8] a2afm seed=33 step=4800/15000 val_RMSE=0.15245 best=0.15141

- [2026-10-21 18:00:42 UTC+8] a2afm seed=33 step=4900/15000 val_RMSE=0.15764 best=0.15141

- [2026-10-21 18:00:43 UTC+8] a2afm seed=33 step=5000/15000 val_RMSE=0.15250 best=0.15141

- [2026-10-21 18:00:43 UTC+8] a2afm seed=33 step=5100/15000 val_RMSE=0.16109 best=0.15141

- [2026-10-21 18:00:44 UTC+8] a2afm seed=33 step=5200/15000 val_RMSE=0.15261 best=0.15141

- [2026-10-21 18:00:45 UTC+8] a2afm seed=33 step=5300/15000 val_RMSE=0.15005 best=0.15005

- [2026-10-21 18:00:45 UTC+8] a2afm seed=33 step=5400/15000 val_RMSE=0.13836 best=0.13836

- [2026-10-21 18:00:46 UTC+8] a2afm seed=33 step=5500/15000 val_RMSE=0.14863 best=0.13836

- [2026-10-21 18:00:47 UTC+8] a2afm seed=33 step=5600/15000 val_RMSE=0.15485 best=0.13836

- [2026-10-21 18:00:47 UTC+8] a2afm seed=33 step=5700/15000 val_RMSE=0.14745 best=0.13836

- [2026-10-21 18:00:48 UTC+8] a2afm seed=33 step=5800/15000 val_RMSE=0.16552 best=0.13836

- [2026-10-21 18:00:49 UTC+8] a2afm seed=33 step=5900/15000 val_RMSE=0.13817 best=0.13817

- [2026-10-21 18:00:50 UTC+8] a2afm seed=33 step=6000/15000 val_RMSE=0.14811 best=0.13817

- [2026-10-21 18:00:50 UTC+8] a2afm seed=33 step=6100/15000 val_RMSE=0.15492 best=0.13817

- [2026-10-21 18:00:51 UTC+8] a2afm seed=33 step=6200/15000 val_RMSE=0.16225 best=0.13817

- [2026-10-21 18:00:52 UTC+8] a2afm seed=33 step=6300/15000 val_RMSE=0.14417 best=0.13817

- [2026-10-21 18:00:52 UTC+8] a2afm seed=33 step=6400/15000 val_RMSE=0.14152 best=0.13817

- [2026-10-21 18:00:53 UTC+8] a2afm seed=33 step=6500/15000 val_RMSE=0.14445 best=0.13817

- [2026-10-21 18:00:54 UTC+8] a2afm seed=33 step=6600/15000 val_RMSE=0.14741 best=0.13817

- [2026-10-21 18:00:54 UTC+8] a2afm seed=33 step=6700/15000 val_RMSE=0.14044 best=0.13817

- [2026-10-21 18:00:55 UTC+8] a2afm seed=33 step=6800/15000 val_RMSE=0.13560 best=0.13560

- [2026-10-21 18:00:56 UTC+8] a2afm seed=33 step=6900/15000 val_RMSE=0.16411 best=0.13560

- [2026-10-21 18:00:57 UTC+8] a2afm seed=33 step=7000/15000 val_RMSE=0.13637 best=0.13560

- [2026-10-21 18:00:57 UTC+8] a2afm seed=33 step=7100/15000 val_RMSE=0.13147 best=0.13147

- [2026-10-21 18:00:58 UTC+8] a2afm seed=33 step=7200/15000 val_RMSE=0.13576 best=0.13147

- [2026-10-21 18:00:59 UTC+8] a2afm seed=33 step=7300/15000 val_RMSE=0.13646 best=0.13147

- [2026-10-21 18:00:59 UTC+8] a2afm seed=33 step=7400/15000 val_RMSE=0.14356 best=0.13147

- [2026-10-21 18:01:00 UTC+8] a2afm seed=33 step=7500/15000 val_RMSE=0.14647 best=0.13147

- [2026-10-21 18:01:01 UTC+8] a2afm seed=33 step=7600/15000 val_RMSE=0.15000 best=0.13147

- [2026-10-21 18:01:01 UTC+8] a2afm seed=33 step=7700/15000 val_RMSE=0.14997 best=0.13147

- [2026-10-21 18:01:02 UTC+8] a2afm seed=33 step=7800/15000 val_RMSE=0.14408 best=0.13147

- [2026-10-21 18:01:03 UTC+8] a2afm seed=33 step=7900/15000 val_RMSE=0.15030 best=0.13147

- [2026-10-21 18:01:04 UTC+8] a2afm seed=33 step=8000/15000 val_RMSE=0.14362 best=0.13147

- [2026-10-21 18:01:04 UTC+8] a2afm seed=33 step=8100/15000 val_RMSE=0.15358 best=0.13147

- [2026-10-21 18:01:05 UTC+8] a2afm seed=33 step=8200/15000 val_RMSE=0.14479 best=0.13147

- [2026-10-21 18:01:06 UTC+8] a2afm seed=33 step=8300/15000 val_RMSE=0.14322 best=0.13147

- [2026-10-21 18:01:06 UTC+8] a2afm seed=33 step=8400/15000 val_RMSE=0.14550 best=0.13147

- [2026-10-21 18:01:07 UTC+8] a2afm seed=33 step=8500/15000 val_RMSE=0.16178 best=0.13147

- [2026-10-21 18:01:08 UTC+8] a2afm seed=33 step=8600/15000 val_RMSE=0.14218 best=0.13147

- [2026-10-21 18:01:08 UTC+8] a2afm seed=33 step=8700/15000 val_RMSE=0.13494 best=0.13147

- [2026-10-21 18:01:09 UTC+8] a2afm seed=33 step=8800/15000 val_RMSE=0.13554 best=0.13147

- [2026-10-21 18:01:10 UTC+8] a2afm seed=33 step=8900/15000 val_RMSE=0.13937 best=0.13147

- [2026-10-21 18:01:10 UTC+8] a2afm seed=33 step=9000/15000 val_RMSE=0.14456 best=0.13147

- [2026-10-21 18:01:11 UTC+8] a2afm seed=33 step=9100/15000 val_RMSE=0.12734 best=0.12734

- [2026-10-21 18:01:12 UTC+8] a2afm seed=33 step=9200/15000 val_RMSE=0.13088 best=0.12734

- [2026-10-21 18:01:13 UTC+8] a2afm seed=33 step=9300/15000 val_RMSE=0.13511 best=0.12734

- [2026-10-21 18:01:13 UTC+8] a2afm seed=33 step=9400/15000 val_RMSE=0.15203 best=0.12734

- [2026-10-21 18:01:14 UTC+8] a2afm seed=33 step=9500/15000 val_RMSE=0.12530 best=0.12530

- [2026-10-21 18:01:15 UTC+8] a2afm seed=33 step=9600/15000 val_RMSE=0.14129 best=0.12530

- [2026-10-21 18:01:15 UTC+8] a2afm seed=33 step=9700/15000 val_RMSE=0.12915 best=0.12530

- [2026-10-21 18:01:16 UTC+8] a2afm seed=33 step=9800/15000 val_RMSE=0.14368 best=0.12530

- [2026-10-21 18:01:17 UTC+8] a2afm seed=33 step=9900/15000 val_RMSE=0.16512 best=0.12530

- [2026-10-21 18:01:17 UTC+8] a2afm seed=33 step=10000/15000 val_RMSE=0.13917 best=0.12530

- [2026-10-21 18:01:18 UTC+8] a2afm seed=33 step=10100/15000 val_RMSE=0.12627 best=0.12530

- [2026-10-21 18:01:19 UTC+8] a2afm seed=33 step=10200/15000 val_RMSE=0.15351 best=0.12530

- [2026-10-21 18:01:19 UTC+8] a2afm seed=33 step=10300/15000 val_RMSE=0.13154 best=0.12530

- [2026-10-21 18:01:20 UTC+8] a2afm seed=33 step=10400/15000 val_RMSE=0.13909 best=0.12530

- [2026-10-21 18:01:21 UTC+8] a2afm seed=33 step=10500/15000 val_RMSE=0.13471 best=0.12530

- [2026-10-21 18:01:22 UTC+8] a2afm seed=33 step=10600/15000 val_RMSE=0.13522 best=0.12530

- [2026-10-21 18:01:22 UTC+8] a2afm seed=33 step=10700/15000 val_RMSE=0.13785 best=0.12530

- [2026-10-21 18:01:23 UTC+8] a2afm seed=33 step=10800/15000 val_RMSE=0.13385 best=0.12530

- [2026-10-21 18:01:24 UTC+8] a2afm seed=33 step=10900/15000 val_RMSE=0.13333 best=0.12530

- [2026-10-21 18:01:24 UTC+8] a2afm seed=33 step=11000/15000 val_RMSE=0.13390 best=0.12530

- [2026-10-21 18:01:25 UTC+8] a2afm seed=33 step=11100/15000 val_RMSE=0.12632 best=0.12530

- [2026-10-21 18:01:26 UTC+8] a2afm seed=33 step=11200/15000 val_RMSE=0.14096 best=0.12530

- [2026-10-21 18:01:26 UTC+8] a2afm seed=33 step=11300/15000 val_RMSE=0.12236 best=0.12236

- [2026-10-21 18:01:27 UTC+8] a2afm seed=33 step=11400/15000 val_RMSE=0.15436 best=0.12236

- [2026-10-21 18:01:28 UTC+8] a2afm seed=33 step=11500/15000 val_RMSE=0.13115 best=0.12236

- [2026-10-21 18:01:29 UTC+8] a2afm seed=33 step=11600/15000 val_RMSE=0.13461 best=0.12236

- [2026-10-21 18:01:29 UTC+8] a2afm seed=33 step=11700/15000 val_RMSE=0.13993 best=0.12236

- [2026-10-21 18:01:30 UTC+8] a2afm seed=33 step=11800/15000 val_RMSE=0.13119 best=0.12236

- [2026-10-21 18:01:31 UTC+8] a2afm seed=33 step=11900/15000 val_RMSE=0.14022 best=0.12236

- [2026-10-21 18:01:31 UTC+8] a2afm seed=33 step=12000/15000 val_RMSE=0.13346 best=0.12236

- [2026-10-21 18:01:32 UTC+8] a2afm seed=33 step=12100/15000 val_RMSE=0.13241 best=0.12236

- [2026-10-21 18:01:33 UTC+8] a2afm seed=33 step=12200/15000 val_RMSE=0.12606 best=0.12236

- [2026-10-21 18:01:33 UTC+8] a2afm seed=33 step=12300/15000 val_RMSE=0.14268 best=0.12236

- [2026-10-21 18:01:34 UTC+8] a2afm seed=33 step=12400/15000 val_RMSE=0.12056 best=0.12056

- [2026-10-21 18:01:35 UTC+8] a2afm seed=33 step=12500/15000 val_RMSE=0.14210 best=0.12056

- [2026-10-21 18:01:35 UTC+8] a2afm seed=33 step=12600/15000 val_RMSE=0.13242 best=0.12056

- [2026-10-21 18:01:36 UTC+8] a2afm seed=33 step=12700/15000 val_RMSE=0.12664 best=0.12056

- [2026-10-21 18:01:37 UTC+8] a2afm seed=33 step=12800/15000 val_RMSE=0.12735 best=0.12056

- [2026-10-21 18:01:38 UTC+8] a2afm seed=33 step=12900/15000 val_RMSE=0.14086 best=0.12056

- [2026-10-21 18:01:38 UTC+8] a2afm seed=33 step=13000/15000 val_RMSE=0.13418 best=0.12056

- [2026-10-21 18:01:39 UTC+8] a2afm seed=33 step=13100/15000 val_RMSE=0.13369 best=0.12056

- [2026-10-21 18:01:40 UTC+8] a2afm seed=33 step=13200/15000 val_RMSE=0.12897 best=0.12056

- [2026-10-21 18:01:40 UTC+8] a2afm seed=33 step=13300/15000 val_RMSE=0.13621 best=0.12056

- [2026-10-21 18:01:41 UTC+8] a2afm seed=33 step=13400/15000 val_RMSE=0.12969 best=0.12056

- [2026-10-21 18:01:42 UTC+8] a2afm seed=33 step=13500/15000 val_RMSE=0.13577 best=0.12056

- [2026-10-21 18:01:42 UTC+8] a2afm seed=33 step=13600/15000 val_RMSE=0.14381 best=0.12056

- [2026-10-21 18:01:43 UTC+8] a2afm seed=33 step=13700/15000 val_RMSE=0.13136 best=0.12056

- [2026-10-21 18:01:44 UTC+8] a2afm seed=33 step=13800/15000 val_RMSE=0.13484 best=0.12056

- [2026-10-21 18:01:45 UTC+8] a2afm seed=33 step=13900/15000 val_RMSE=0.13989 best=0.12056

- [2026-10-21 18:01:45 UTC+8] a2afm seed=33 step=14000/15000 val_RMSE=0.12638 best=0.12056

- [2026-10-21 18:01:46 UTC+8] a2afm seed=33 step=14100/15000 val_RMSE=0.13263 best=0.12056

- [2026-10-21 18:01:47 UTC+8] a2afm seed=33 step=14200/15000 val_RMSE=0.13371 best=0.12056

- [2026-10-21 18:01:47 UTC+8] a2afm seed=33 step=14300/15000 val_RMSE=0.15186 best=0.12056

- [2026-10-21 18:01:48 UTC+8] a2afm seed=33 step=14400/15000 val_RMSE=0.12390 best=0.12056

- [2026-10-21 18:01:49 UTC+8] a2afm seed=33 step=14500/15000 val_RMSE=0.12526 best=0.12056

- [2026-10-21 18:01:49 UTC+8] a2afm seed=33 step=14600/15000 val_RMSE=0.12514 best=0.12056

- [2026-10-21 18:01:50 UTC+8] a2afm seed=33 step=14700/15000 val_RMSE=0.12136 best=0.12056

- [2026-10-21 18:01:51 UTC+8] a2afm seed=33 step=14800/15000 val_RMSE=0.13060 best=0.12056

- [2026-10-21 18:01:52 UTC+8] a2afm seed=33 step=14900/15000 val_RMSE=0.12016 best=0.12016

- [2026-10-21 18:01:52 UTC+8] a2afm seed=33 step=15000/15000 val_RMSE=0.13933 best=0.12016

- [2026-10-21 18:01:52 UTC+8] 完成 a2afm seed=33，本轮耗时 104.6 s，选择验证最优 step=14900

- [2026-10-21 18:01:52 UTC+8] regression seed=11 step=100/15000 val_RMSE=0.25567 best=0.25567

- [2026-10-21 18:01:53 UTC+8] regression seed=11 step=200/15000 val_RMSE=0.25205 best=0.25205

- [2026-10-21 18:01:53 UTC+8] regression seed=11 step=300/15000 val_RMSE=0.25161 best=0.25161

- [2026-10-21 18:01:53 UTC+8] regression seed=11 step=400/15000 val_RMSE=0.24336 best=0.24336

- [2026-10-21 18:01:53 UTC+8] regression seed=11 step=500/15000 val_RMSE=0.24905 best=0.24336

- [2026-10-21 18:01:53 UTC+8] regression seed=11 step=600/15000 val_RMSE=0.23942 best=0.23942

- [2026-10-21 18:01:53 UTC+8] regression seed=11 step=700/15000 val_RMSE=0.23679 best=0.23679

- [2026-10-21 18:01:53 UTC+8] regression seed=11 step=800/15000 val_RMSE=0.23210 best=0.23210

- [2026-10-21 18:01:54 UTC+8] regression seed=11 step=900/15000 val_RMSE=0.21969 best=0.21969

- [2026-10-21 18:01:54 UTC+8] regression seed=11 step=1000/15000 val_RMSE=0.21533 best=0.21533

- [2026-10-21 18:01:54 UTC+8] regression seed=11 step=1100/15000 val_RMSE=0.21441 best=0.21441

- [2026-10-21 18:01:54 UTC+8] regression seed=11 step=1200/15000 val_RMSE=0.20270 best=0.20270

- [2026-10-21 18:01:54 UTC+8] regression seed=11 step=1300/15000 val_RMSE=0.21132 best=0.20270

- [2026-10-21 18:01:54 UTC+8] regression seed=11 step=1400/15000 val_RMSE=0.19403 best=0.19403

- [2026-10-21 18:01:55 UTC+8] regression seed=11 step=1500/15000 val_RMSE=0.18297 best=0.18297

- [2026-10-21 18:01:55 UTC+8] regression seed=11 step=1600/15000 val_RMSE=0.19469 best=0.18297

- [2026-10-21 18:01:55 UTC+8] regression seed=11 step=1700/15000 val_RMSE=0.20319 best=0.18297

- [2026-10-21 18:01:55 UTC+8] regression seed=11 step=1800/15000 val_RMSE=0.18200 best=0.18200

- [2026-10-21 18:01:55 UTC+8] regression seed=11 step=1900/15000 val_RMSE=0.17558 best=0.17558

- [2026-10-21 18:01:55 UTC+8] regression seed=11 step=2000/15000 val_RMSE=0.17308 best=0.17308

- [2026-10-21 18:01:56 UTC+8] regression seed=11 step=2100/15000 val_RMSE=0.18514 best=0.17308

- [2026-10-21 18:01:56 UTC+8] regression seed=11 step=2200/15000 val_RMSE=0.17620 best=0.17308

- [2026-10-21 18:01:56 UTC+8] regression seed=11 step=2300/15000 val_RMSE=0.17960 best=0.17308

- [2026-10-21 18:01:56 UTC+8] regression seed=11 step=2400/15000 val_RMSE=0.19513 best=0.17308

- [2026-10-21 18:01:56 UTC+8] regression seed=11 step=2500/15000 val_RMSE=0.17804 best=0.17308

- [2026-10-21 18:01:56 UTC+8] regression seed=11 step=2600/15000 val_RMSE=0.17120 best=0.17120

- [2026-10-21 18:01:56 UTC+8] regression seed=11 step=2700/15000 val_RMSE=0.16953 best=0.16953

- [2026-10-21 18:01:57 UTC+8] regression seed=11 step=2800/15000 val_RMSE=0.16563 best=0.16563

- [2026-10-21 18:01:57 UTC+8] regression seed=11 step=2900/15000 val_RMSE=0.16031 best=0.16031

- [2026-10-21 18:01:57 UTC+8] regression seed=11 step=3000/15000 val_RMSE=0.16385 best=0.16031

- [2026-10-21 18:01:57 UTC+8] regression seed=11 step=3100/15000 val_RMSE=0.16164 best=0.16031

- [2026-10-21 18:01:57 UTC+8] regression seed=11 step=3200/15000 val_RMSE=0.17176 best=0.16031

- [2026-10-21 18:01:57 UTC+8] regression seed=11 step=3300/15000 val_RMSE=0.16674 best=0.16031

- [2026-10-21 18:01:58 UTC+8] regression seed=11 step=3400/15000 val_RMSE=0.15448 best=0.15448

- [2026-10-21 18:01:58 UTC+8] regression seed=11 step=3500/15000 val_RMSE=0.16633 best=0.15448

- [2026-10-21 18:01:58 UTC+8] regression seed=11 step=3600/15000 val_RMSE=0.15050 best=0.15050

- [2026-10-21 18:01:58 UTC+8] regression seed=11 step=3700/15000 val_RMSE=0.15688 best=0.15050

- [2026-10-21 18:01:58 UTC+8] regression seed=11 step=3800/15000 val_RMSE=0.16006 best=0.15050

- [2026-10-21 18:01:58 UTC+8] regression seed=11 step=3900/15000 val_RMSE=0.15872 best=0.15050

- [2026-10-21 18:01:58 UTC+8] regression seed=11 step=4000/15000 val_RMSE=0.15918 best=0.15050

- [2026-10-21 18:01:59 UTC+8] regression seed=11 step=4100/15000 val_RMSE=0.15737 best=0.15050

- [2026-10-21 18:01:59 UTC+8] regression seed=11 step=4200/15000 val_RMSE=0.14972 best=0.14972

- [2026-10-21 18:01:59 UTC+8] regression seed=11 step=4300/15000 val_RMSE=0.14081 best=0.14081

- [2026-10-21 18:01:59 UTC+8] regression seed=11 step=4400/15000 val_RMSE=0.15203 best=0.14081

- [2026-10-21 18:01:59 UTC+8] regression seed=11 step=4500/15000 val_RMSE=0.14044 best=0.14044

- [2026-10-21 18:01:59 UTC+8] regression seed=11 step=4600/15000 val_RMSE=0.15379 best=0.14044

- [2026-10-21 18:02:00 UTC+8] regression seed=11 step=4700/15000 val_RMSE=0.14515 best=0.14044

- [2026-10-21 18:02:00 UTC+8] regression seed=11 step=4800/15000 val_RMSE=0.14738 best=0.14044

- [2026-10-21 18:02:00 UTC+8] regression seed=11 step=4900/15000 val_RMSE=0.13824 best=0.13824

- [2026-10-21 18:02:00 UTC+8] regression seed=11 step=5000/15000 val_RMSE=0.15149 best=0.13824

- [2026-10-21 18:02:00 UTC+8] regression seed=11 step=5100/15000 val_RMSE=0.13509 best=0.13509

- [2026-10-21 18:02:00 UTC+8] regression seed=11 step=5200/15000 val_RMSE=0.13068 best=0.13068

- [2026-10-21 18:02:00 UTC+8] regression seed=11 step=5300/15000 val_RMSE=0.13188 best=0.13068

- [2026-10-21 18:02:01 UTC+8] regression seed=11 step=5400/15000 val_RMSE=0.14254 best=0.13068

- [2026-10-21 18:02:01 UTC+8] regression seed=11 step=5500/15000 val_RMSE=0.13899 best=0.13068

- [2026-10-21 18:02:01 UTC+8] regression seed=11 step=5600/15000 val_RMSE=0.14853 best=0.13068

- [2026-10-21 18:02:01 UTC+8] regression seed=11 step=5700/15000 val_RMSE=0.14149 best=0.13068

- [2026-10-21 18:02:01 UTC+8] regression seed=11 step=5800/15000 val_RMSE=0.16463 best=0.13068

- [2026-10-21 18:02:01 UTC+8] regression seed=11 step=5900/15000 val_RMSE=0.13751 best=0.13068

- [2026-10-21 18:02:02 UTC+8] regression seed=11 step=6000/15000 val_RMSE=0.13457 best=0.13068

- [2026-10-21 18:02:02 UTC+8] regression seed=11 step=6100/15000 val_RMSE=0.13323 best=0.13068

- [2026-10-21 18:02:02 UTC+8] regression seed=11 step=6200/15000 val_RMSE=0.13670 best=0.13068

- [2026-10-21 18:02:02 UTC+8] regression seed=11 step=6300/15000 val_RMSE=0.15644 best=0.13068

- [2026-10-21 18:02:02 UTC+8] regression seed=11 step=6400/15000 val_RMSE=0.13420 best=0.13068

- [2026-10-21 18:02:02 UTC+8] regression seed=11 step=6500/15000 val_RMSE=0.13468 best=0.13068

- [2026-10-21 18:02:03 UTC+8] regression seed=11 step=6600/15000 val_RMSE=0.13616 best=0.13068

- [2026-10-21 18:02:03 UTC+8] regression seed=11 step=6700/15000 val_RMSE=0.13695 best=0.13068

- [2026-10-21 18:02:03 UTC+8] regression seed=11 step=6800/15000 val_RMSE=0.13379 best=0.13068

- [2026-10-21 18:02:03 UTC+8] regression seed=11 step=6900/15000 val_RMSE=0.13530 best=0.13068

- [2026-10-21 18:02:03 UTC+8] regression seed=11 step=7000/15000 val_RMSE=0.15029 best=0.13068

- [2026-10-21 18:02:04 UTC+8] regression seed=11 step=7100/15000 val_RMSE=0.12839 best=0.12839

- [2026-10-21 18:02:04 UTC+8] regression seed=11 step=7200/15000 val_RMSE=0.13097 best=0.12839

- [2026-10-21 18:02:04 UTC+8] regression seed=11 step=7300/15000 val_RMSE=0.14047 best=0.12839

- [2026-10-21 18:02:04 UTC+8] regression seed=11 step=7400/15000 val_RMSE=0.13481 best=0.12839

- [2026-10-21 18:02:05 UTC+8] regression seed=11 step=7500/15000 val_RMSE=0.15010 best=0.12839

- [2026-10-21 18:02:05 UTC+8] regression seed=11 step=7600/15000 val_RMSE=0.14113 best=0.12839

- [2026-10-21 18:02:05 UTC+8] regression seed=11 step=7700/15000 val_RMSE=0.13416 best=0.12839

- [2026-10-21 18:02:05 UTC+8] regression seed=11 step=7800/15000 val_RMSE=0.14500 best=0.12839

- [2026-10-21 18:02:05 UTC+8] regression seed=11 step=7900/15000 val_RMSE=0.12785 best=0.12785

- [2026-10-21 18:02:06 UTC+8] regression seed=11 step=8000/15000 val_RMSE=0.13186 best=0.12785

- [2026-10-21 18:02:06 UTC+8] regression seed=11 step=8100/15000 val_RMSE=0.12670 best=0.12670

- [2026-10-21 18:02:06 UTC+8] regression seed=11 step=8200/15000 val_RMSE=0.17686 best=0.12670

- [2026-10-21 18:02:06 UTC+8] regression seed=11 step=8300/15000 val_RMSE=0.12664 best=0.12664

- [2026-10-21 18:02:07 UTC+8] regression seed=11 step=8400/15000 val_RMSE=0.12930 best=0.12664

- [2026-10-21 18:02:07 UTC+8] regression seed=11 step=8500/15000 val_RMSE=0.13075 best=0.12664

- [2026-10-21 18:02:07 UTC+8] regression seed=11 step=8600/15000 val_RMSE=0.12825 best=0.12664

- [2026-10-21 18:02:07 UTC+8] regression seed=11 step=8700/15000 val_RMSE=0.13744 best=0.12664

- [2026-10-21 18:02:07 UTC+8] regression seed=11 step=8800/15000 val_RMSE=0.13976 best=0.12664

- [2026-10-21 18:02:08 UTC+8] regression seed=11 step=8900/15000 val_RMSE=0.13198 best=0.12664

- [2026-10-21 18:02:08 UTC+8] regression seed=11 step=9000/15000 val_RMSE=0.14080 best=0.12664

- [2026-10-21 18:02:08 UTC+8] regression seed=11 step=9100/15000 val_RMSE=0.14827 best=0.12664

- [2026-10-21 18:02:08 UTC+8] regression seed=11 step=9200/15000 val_RMSE=0.14173 best=0.12664

- [2026-10-21 18:02:08 UTC+8] regression seed=11 step=9300/15000 val_RMSE=0.13891 best=0.12664

- [2026-10-21 18:02:09 UTC+8] regression seed=11 step=9400/15000 val_RMSE=0.12556 best=0.12556

- [2026-10-21 18:02:09 UTC+8] regression seed=11 step=9500/15000 val_RMSE=0.13373 best=0.12556

- [2026-10-21 18:02:09 UTC+8] regression seed=11 step=9600/15000 val_RMSE=0.12189 best=0.12189

- [2026-10-21 18:02:09 UTC+8] regression seed=11 step=9700/15000 val_RMSE=0.14323 best=0.12189

- [2026-10-21 18:02:10 UTC+8] regression seed=11 step=9800/15000 val_RMSE=0.13820 best=0.12189

- [2026-10-21 18:02:10 UTC+8] regression seed=11 step=9900/15000 val_RMSE=0.12074 best=0.12074

- [2026-10-21 18:02:10 UTC+8] regression seed=11 step=10000/15000 val_RMSE=0.13670 best=0.12074

- [2026-10-21 18:02:10 UTC+8] regression seed=11 step=10100/15000 val_RMSE=0.13797 best=0.12074

- [2026-10-21 18:02:10 UTC+8] regression seed=11 step=10200/15000 val_RMSE=0.12322 best=0.12074

- [2026-10-21 18:02:11 UTC+8] regression seed=11 step=10300/15000 val_RMSE=0.13791 best=0.12074

- [2026-10-21 18:02:11 UTC+8] regression seed=11 step=10400/15000 val_RMSE=0.12595 best=0.12074

- [2026-10-21 18:02:11 UTC+8] regression seed=11 step=10500/15000 val_RMSE=0.12967 best=0.12074

- [2026-10-21 18:02:11 UTC+8] regression seed=11 step=10600/15000 val_RMSE=0.12802 best=0.12074

- [2026-10-21 18:02:12 UTC+8] regression seed=11 step=10700/15000 val_RMSE=0.13127 best=0.12074

- [2026-10-21 18:02:12 UTC+8] regression seed=11 step=10800/15000 val_RMSE=0.14600 best=0.12074

- [2026-10-21 18:02:12 UTC+8] regression seed=11 step=10900/15000 val_RMSE=0.12159 best=0.12074

- [2026-10-21 18:02:12 UTC+8] regression seed=11 step=11000/15000 val_RMSE=0.12919 best=0.12074

- [2026-10-21 18:02:12 UTC+8] regression seed=11 step=11100/15000 val_RMSE=0.13278 best=0.12074

- [2026-10-21 18:02:13 UTC+8] regression seed=11 step=11200/15000 val_RMSE=0.12659 best=0.12074

- [2026-10-21 18:02:13 UTC+8] regression seed=11 step=11300/15000 val_RMSE=0.14001 best=0.12074

- [2026-10-21 18:02:13 UTC+8] regression seed=11 step=11400/15000 val_RMSE=0.13000 best=0.12074

- [2026-10-21 18:02:13 UTC+8] regression seed=11 step=11500/15000 val_RMSE=0.12880 best=0.12074

- [2026-10-21 18:02:13 UTC+8] regression seed=11 step=11600/15000 val_RMSE=0.13522 best=0.12074

- [2026-10-21 18:02:14 UTC+8] regression seed=11 step=11700/15000 val_RMSE=0.13492 best=0.12074

- [2026-10-21 18:02:14 UTC+8] regression seed=11 step=11800/15000 val_RMSE=0.12925 best=0.12074

- [2026-10-21 18:02:14 UTC+8] regression seed=11 step=11900/15000 val_RMSE=0.11925 best=0.11925

- [2026-10-21 18:02:14 UTC+8] regression seed=11 step=12000/15000 val_RMSE=0.12677 best=0.11925

- [2026-10-21 18:02:14 UTC+8] regression seed=11 step=12100/15000 val_RMSE=0.12126 best=0.11925

- [2026-10-21 18:02:15 UTC+8] regression seed=11 step=12200/15000 val_RMSE=0.12666 best=0.11925

- [2026-10-21 18:02:15 UTC+8] regression seed=11 step=12300/15000 val_RMSE=0.11871 best=0.11871

- [2026-10-21 18:02:15 UTC+8] regression seed=11 step=12400/15000 val_RMSE=0.14307 best=0.11871

- [2026-10-21 18:02:15 UTC+8] regression seed=11 step=12500/15000 val_RMSE=0.12390 best=0.11871

- [2026-10-21 18:02:16 UTC+8] regression seed=11 step=12600/15000 val_RMSE=0.12506 best=0.11871

- [2026-10-21 18:02:16 UTC+8] regression seed=11 step=12700/15000 val_RMSE=0.12816 best=0.11871

- [2026-10-21 18:02:16 UTC+8] regression seed=11 step=12800/15000 val_RMSE=0.12204 best=0.11871

- [2026-10-21 18:02:16 UTC+8] regression seed=11 step=12900/15000 val_RMSE=0.11869 best=0.11869

- [2026-10-21 18:02:16 UTC+8] regression seed=11 step=13000/15000 val_RMSE=0.12515 best=0.11869

- [2026-10-21 18:02:17 UTC+8] regression seed=11 step=13100/15000 val_RMSE=0.13670 best=0.11869

- [2026-10-21 18:02:17 UTC+8] regression seed=11 step=13200/15000 val_RMSE=0.12081 best=0.11869

- [2026-10-21 18:02:17 UTC+8] regression seed=11 step=13300/15000 val_RMSE=0.13015 best=0.11869

- [2026-10-21 18:02:17 UTC+8] regression seed=11 step=13400/15000 val_RMSE=0.14651 best=0.11869

- [2026-10-21 18:02:17 UTC+8] regression seed=11 step=13500/15000 val_RMSE=0.12181 best=0.11869

- [2026-10-21 18:02:18 UTC+8] regression seed=11 step=13600/15000 val_RMSE=0.12129 best=0.11869

- [2026-10-21 18:02:18 UTC+8] regression seed=11 step=13700/15000 val_RMSE=0.12842 best=0.11869

- [2026-10-21 18:02:18 UTC+8] regression seed=11 step=13800/15000 val_RMSE=0.12689 best=0.11869

- [2026-10-21 18:02:18 UTC+8] regression seed=11 step=13900/15000 val_RMSE=0.11519 best=0.11519

- [2026-10-21 18:02:18 UTC+8] regression seed=11 step=14000/15000 val_RMSE=0.13204 best=0.11519

- [2026-10-21 18:02:19 UTC+8] regression seed=11 step=14100/15000 val_RMSE=0.12796 best=0.11519

- [2026-10-21 18:02:19 UTC+8] regression seed=11 step=14200/15000 val_RMSE=0.13506 best=0.11519

- [2026-10-21 18:02:19 UTC+8] regression seed=11 step=14300/15000 val_RMSE=0.11891 best=0.11519

- [2026-10-21 18:02:19 UTC+8] regression seed=11 step=14400/15000 val_RMSE=0.12581 best=0.11519

- [2026-10-21 18:02:20 UTC+8] regression seed=11 step=14500/15000 val_RMSE=0.12606 best=0.11519

- [2026-10-21 18:02:20 UTC+8] regression seed=11 step=14600/15000 val_RMSE=0.12241 best=0.11519

- [2026-10-21 18:02:20 UTC+8] regression seed=11 step=14700/15000 val_RMSE=0.12711 best=0.11519

- [2026-10-21 18:02:20 UTC+8] regression seed=11 step=14800/15000 val_RMSE=0.12090 best=0.11519

- [2026-10-21 18:02:20 UTC+8] regression seed=11 step=14900/15000 val_RMSE=0.12189 best=0.11519

- [2026-10-21 18:02:21 UTC+8] regression seed=11 step=15000/15000 val_RMSE=0.13344 best=0.11519

- [2026-10-21 18:02:21 UTC+8] 完成 regression seed=11，本轮耗时 28.3 s，选择验证最优 step=13900

- [2026-10-21 18:02:21 UTC+8] regression seed=22 step=100/15000 val_RMSE=0.27055 best=0.27055

- [2026-10-21 18:02:21 UTC+8] regression seed=22 step=200/15000 val_RMSE=0.26133 best=0.26133

- [2026-10-21 18:02:21 UTC+8] regression seed=22 step=300/15000 val_RMSE=0.24961 best=0.24961

- [2026-10-21 18:02:21 UTC+8] regression seed=22 step=400/15000 val_RMSE=0.24765 best=0.24765

- [2026-10-21 18:02:22 UTC+8] regression seed=22 step=500/15000 val_RMSE=0.24858 best=0.24765

- [2026-10-21 18:02:22 UTC+8] regression seed=22 step=600/15000 val_RMSE=0.23740 best=0.23740

- [2026-10-21 18:02:22 UTC+8] regression seed=22 step=700/15000 val_RMSE=0.25157 best=0.23740

- [2026-10-21 18:02:22 UTC+8] regression seed=22 step=800/15000 val_RMSE=0.22937 best=0.22937

- [2026-10-21 18:02:23 UTC+8] regression seed=22 step=900/15000 val_RMSE=0.23136 best=0.22937

- [2026-10-21 18:02:23 UTC+8] regression seed=22 step=1000/15000 val_RMSE=0.22701 best=0.22701

- [2026-10-21 18:02:23 UTC+8] regression seed=22 step=1100/15000 val_RMSE=0.21969 best=0.21969

- [2026-10-21 18:02:23 UTC+8] regression seed=22 step=1200/15000 val_RMSE=0.20697 best=0.20697

- [2026-10-21 18:02:23 UTC+8] regression seed=22 step=1300/15000 val_RMSE=0.19834 best=0.19834

- [2026-10-21 18:02:24 UTC+8] regression seed=22 step=1400/15000 val_RMSE=0.20712 best=0.19834

- [2026-10-21 18:02:24 UTC+8] regression seed=22 step=1500/15000 val_RMSE=0.18419 best=0.18419

- [2026-10-21 18:02:24 UTC+8] regression seed=22 step=1600/15000 val_RMSE=0.18307 best=0.18307

- [2026-10-21 18:02:24 UTC+8] regression seed=22 step=1700/15000 val_RMSE=0.17828 best=0.17828

- [2026-10-21 18:02:24 UTC+8] regression seed=22 step=1800/15000 val_RMSE=0.18026 best=0.17828

- [2026-10-21 18:02:25 UTC+8] regression seed=22 step=1900/15000 val_RMSE=0.18043 best=0.17828

- [2026-10-21 18:02:25 UTC+8] regression seed=22 step=2000/15000 val_RMSE=0.18116 best=0.17828

- [2026-10-21 18:02:25 UTC+8] regression seed=22 step=2100/15000 val_RMSE=0.18173 best=0.17828

- [2026-10-21 18:02:25 UTC+8] regression seed=22 step=2200/15000 val_RMSE=0.16723 best=0.16723

- [2026-10-21 18:02:25 UTC+8] regression seed=22 step=2300/15000 val_RMSE=0.16990 best=0.16723

- [2026-10-21 18:02:26 UTC+8] regression seed=22 step=2400/15000 val_RMSE=0.16659 best=0.16659

- [2026-10-21 18:02:26 UTC+8] regression seed=22 step=2500/15000 val_RMSE=0.16113 best=0.16113

- [2026-10-21 18:02:26 UTC+8] regression seed=22 step=2600/15000 val_RMSE=0.16407 best=0.16113

- [2026-10-21 18:02:26 UTC+8] regression seed=22 step=2700/15000 val_RMSE=0.16095 best=0.16095

- [2026-10-21 18:02:27 UTC+8] regression seed=22 step=2800/15000 val_RMSE=0.15606 best=0.15606

- [2026-10-21 18:02:27 UTC+8] regression seed=22 step=2900/15000 val_RMSE=0.16084 best=0.15606

- [2026-10-21 18:02:27 UTC+8] regression seed=22 step=3000/15000 val_RMSE=0.16113 best=0.15606

- [2026-10-21 18:02:27 UTC+8] regression seed=22 step=3100/15000 val_RMSE=0.15964 best=0.15606

- [2026-10-21 18:02:27 UTC+8] regression seed=22 step=3200/15000 val_RMSE=0.16099 best=0.15606

- [2026-10-21 18:02:28 UTC+8] regression seed=22 step=3300/15000 val_RMSE=0.15865 best=0.15606

- [2026-10-21 18:02:28 UTC+8] regression seed=22 step=3400/15000 val_RMSE=0.16029 best=0.15606

- [2026-10-21 18:02:28 UTC+8] regression seed=22 step=3500/15000 val_RMSE=0.15272 best=0.15272

- [2026-10-21 18:02:28 UTC+8] regression seed=22 step=3600/15000 val_RMSE=0.16248 best=0.15272

- [2026-10-21 18:02:28 UTC+8] regression seed=22 step=3700/15000 val_RMSE=0.15281 best=0.15272

- [2026-10-21 18:02:29 UTC+8] regression seed=22 step=3800/15000 val_RMSE=0.14077 best=0.14077

- [2026-10-21 18:02:29 UTC+8] regression seed=22 step=3900/15000 val_RMSE=0.14791 best=0.14077

- [2026-10-21 18:02:29 UTC+8] regression seed=22 step=4000/15000 val_RMSE=0.14188 best=0.14077

- [2026-10-21 18:02:29 UTC+8] regression seed=22 step=4100/15000 val_RMSE=0.16791 best=0.14077

- [2026-10-21 18:02:29 UTC+8] regression seed=22 step=4200/15000 val_RMSE=0.16045 best=0.14077

- [2026-10-21 18:02:30 UTC+8] regression seed=22 step=4300/15000 val_RMSE=0.14167 best=0.14077

- [2026-10-21 18:02:30 UTC+8] regression seed=22 step=4400/15000 val_RMSE=0.13706 best=0.13706

- [2026-10-21 18:02:30 UTC+8] regression seed=22 step=4500/15000 val_RMSE=0.14498 best=0.13706

- [2026-10-21 18:02:30 UTC+8] regression seed=22 step=4600/15000 val_RMSE=0.16264 best=0.13706

- [2026-10-21 18:02:30 UTC+8] regression seed=22 step=4700/15000 val_RMSE=0.14882 best=0.13706

- [2026-10-21 18:02:31 UTC+8] regression seed=22 step=4800/15000 val_RMSE=0.14764 best=0.13706

- [2026-10-21 18:02:31 UTC+8] regression seed=22 step=4900/15000 val_RMSE=0.14252 best=0.13706

- [2026-10-21 18:02:31 UTC+8] regression seed=22 step=5000/15000 val_RMSE=0.13757 best=0.13706

- [2026-10-21 18:02:31 UTC+8] regression seed=22 step=5100/15000 val_RMSE=0.14120 best=0.13706

- [2026-10-21 18:02:31 UTC+8] regression seed=22 step=5200/15000 val_RMSE=0.15115 best=0.13706

- [2026-10-21 18:02:32 UTC+8] regression seed=22 step=5300/15000 val_RMSE=0.14050 best=0.13706

- [2026-10-21 18:02:32 UTC+8] regression seed=22 step=5400/15000 val_RMSE=0.13674 best=0.13674

- [2026-10-21 18:02:32 UTC+8] regression seed=22 step=5500/15000 val_RMSE=0.13818 best=0.13674

- [2026-10-21 18:02:32 UTC+8] regression seed=22 step=5600/15000 val_RMSE=0.13853 best=0.13674

- [2026-10-21 18:02:32 UTC+8] regression seed=22 step=5700/15000 val_RMSE=0.13568 best=0.13568

- [2026-10-21 18:02:33 UTC+8] regression seed=22 step=5800/15000 val_RMSE=0.14191 best=0.13568

- [2026-10-21 18:02:33 UTC+8] regression seed=22 step=5900/15000 val_RMSE=0.15180 best=0.13568

- [2026-10-21 18:02:33 UTC+8] regression seed=22 step=6000/15000 val_RMSE=0.13268 best=0.13268

- [2026-10-21 18:02:33 UTC+8] regression seed=22 step=6100/15000 val_RMSE=0.14486 best=0.13268

- [2026-10-21 18:02:33 UTC+8] regression seed=22 step=6200/15000 val_RMSE=0.15183 best=0.13268

- [2026-10-21 18:02:33 UTC+8] regression seed=22 step=6300/15000 val_RMSE=0.13564 best=0.13268

- [2026-10-21 18:02:33 UTC+8] regression seed=22 step=6400/15000 val_RMSE=0.14702 best=0.13268

- [2026-10-21 18:02:34 UTC+8] regression seed=22 step=6500/15000 val_RMSE=0.13035 best=0.13035

- [2026-10-21 18:02:34 UTC+8] regression seed=22 step=6600/15000 val_RMSE=0.12580 best=0.12580

- [2026-10-21 18:02:34 UTC+8] regression seed=22 step=6700/15000 val_RMSE=0.13903 best=0.12580

- [2026-10-21 18:02:34 UTC+8] regression seed=22 step=6800/15000 val_RMSE=0.13706 best=0.12580

- [2026-10-21 18:02:34 UTC+8] regression seed=22 step=6900/15000 val_RMSE=0.13512 best=0.12580

- [2026-10-21 18:02:34 UTC+8] regression seed=22 step=7000/15000 val_RMSE=0.13116 best=0.12580

- [2026-10-21 18:02:35 UTC+8] regression seed=22 step=7100/15000 val_RMSE=0.13830 best=0.12580

- [2026-10-21 18:02:35 UTC+8] regression seed=22 step=7200/15000 val_RMSE=0.13491 best=0.12580

- [2026-10-21 18:02:35 UTC+8] regression seed=22 step=7300/15000 val_RMSE=0.13633 best=0.12580

- [2026-10-21 18:02:35 UTC+8] regression seed=22 step=7400/15000 val_RMSE=0.13508 best=0.12580

- [2026-10-21 18:02:35 UTC+8] regression seed=22 step=7500/15000 val_RMSE=0.12874 best=0.12580

- [2026-10-21 18:02:35 UTC+8] regression seed=22 step=7600/15000 val_RMSE=0.13467 best=0.12580

- [2026-10-21 18:02:36 UTC+8] regression seed=22 step=7700/15000 val_RMSE=0.13796 best=0.12580

- [2026-10-21 18:02:36 UTC+8] regression seed=22 step=7800/15000 val_RMSE=0.16122 best=0.12580

- [2026-10-21 18:02:36 UTC+8] regression seed=22 step=7900/15000 val_RMSE=0.12969 best=0.12580

- [2026-10-21 18:02:36 UTC+8] regression seed=22 step=8000/15000 val_RMSE=0.12985 best=0.12580

- [2026-10-21 18:02:36 UTC+8] regression seed=22 step=8100/15000 val_RMSE=0.13307 best=0.12580

- [2026-10-21 18:02:36 UTC+8] regression seed=22 step=8200/15000 val_RMSE=0.13978 best=0.12580

- [2026-10-21 18:02:36 UTC+8] regression seed=22 step=8300/15000 val_RMSE=0.13293 best=0.12580

- [2026-10-21 18:02:37 UTC+8] regression seed=22 step=8400/15000 val_RMSE=0.13787 best=0.12580

- [2026-10-21 18:02:37 UTC+8] regression seed=22 step=8500/15000 val_RMSE=0.13084 best=0.12580

- [2026-10-21 18:02:37 UTC+8] regression seed=22 step=8600/15000 val_RMSE=0.12350 best=0.12350

- [2026-10-21 18:02:37 UTC+8] regression seed=22 step=8700/15000 val_RMSE=0.12162 best=0.12162

- [2026-10-21 18:02:37 UTC+8] regression seed=22 step=8800/15000 val_RMSE=0.13199 best=0.12162

- [2026-10-21 18:02:37 UTC+8] regression seed=22 step=8900/15000 val_RMSE=0.13047 best=0.12162

- [2026-10-21 18:02:38 UTC+8] regression seed=22 step=9000/15000 val_RMSE=0.12977 best=0.12162

- [2026-10-21 18:02:38 UTC+8] regression seed=22 step=9100/15000 val_RMSE=0.12959 best=0.12162

- [2026-10-21 18:02:38 UTC+8] regression seed=22 step=9200/15000 val_RMSE=0.13305 best=0.12162

- [2026-10-21 18:02:38 UTC+8] regression seed=22 step=9300/15000 val_RMSE=0.12226 best=0.12162

- [2026-10-21 18:02:38 UTC+8] regression seed=22 step=9400/15000 val_RMSE=0.13497 best=0.12162

- [2026-10-21 18:02:38 UTC+8] regression seed=22 step=9500/15000 val_RMSE=0.11796 best=0.11796

- [2026-10-21 18:02:38 UTC+8] regression seed=22 step=9600/15000 val_RMSE=0.12756 best=0.11796

- [2026-10-21 18:02:39 UTC+8] regression seed=22 step=9700/15000 val_RMSE=0.13591 best=0.11796

- [2026-10-21 18:02:39 UTC+8] regression seed=22 step=9800/15000 val_RMSE=0.12374 best=0.11796

- [2026-10-21 18:02:39 UTC+8] regression seed=22 step=9900/15000 val_RMSE=0.12274 best=0.11796

- [2026-10-21 18:02:39 UTC+8] regression seed=22 step=10000/15000 val_RMSE=0.14015 best=0.11796

- [2026-10-21 18:02:39 UTC+8] regression seed=22 step=10100/15000 val_RMSE=0.13420 best=0.11796

- [2026-10-21 18:02:40 UTC+8] regression seed=22 step=10200/15000 val_RMSE=0.13496 best=0.11796

- [2026-10-21 18:02:40 UTC+8] regression seed=22 step=10300/15000 val_RMSE=0.12476 best=0.11796

- [2026-10-21 18:02:40 UTC+8] regression seed=22 step=10400/15000 val_RMSE=0.12243 best=0.11796

- [2026-10-21 18:02:40 UTC+8] regression seed=22 step=10500/15000 val_RMSE=0.12159 best=0.11796

- [2026-10-21 18:02:40 UTC+8] regression seed=22 step=10600/15000 val_RMSE=0.12631 best=0.11796

- [2026-10-21 18:02:40 UTC+8] regression seed=22 step=10700/15000 val_RMSE=0.14200 best=0.11796

- [2026-10-21 18:02:40 UTC+8] regression seed=22 step=10800/15000 val_RMSE=0.12467 best=0.11796

- [2026-10-21 18:02:41 UTC+8] regression seed=22 step=10900/15000 val_RMSE=0.13014 best=0.11796

- [2026-10-21 18:02:41 UTC+8] regression seed=22 step=11000/15000 val_RMSE=0.11945 best=0.11796

- [2026-10-21 18:02:41 UTC+8] regression seed=22 step=11100/15000 val_RMSE=0.13302 best=0.11796

- [2026-10-21 18:02:41 UTC+8] regression seed=22 step=11200/15000 val_RMSE=0.14506 best=0.11796

- [2026-10-21 18:02:41 UTC+8] regression seed=22 step=11300/15000 val_RMSE=0.12798 best=0.11796

- [2026-10-21 18:02:41 UTC+8] regression seed=22 step=11400/15000 val_RMSE=0.12334 best=0.11796

- [2026-10-21 18:02:42 UTC+8] regression seed=22 step=11500/15000 val_RMSE=0.12384 best=0.11796

- [2026-10-21 18:02:42 UTC+8] regression seed=22 step=11600/15000 val_RMSE=0.12883 best=0.11796

- [2026-10-21 18:02:42 UTC+8] regression seed=22 step=11700/15000 val_RMSE=0.12410 best=0.11796

- [2026-10-21 18:02:42 UTC+8] regression seed=22 step=11800/15000 val_RMSE=0.12123 best=0.11796

- [2026-10-21 18:02:42 UTC+8] regression seed=22 step=11900/15000 val_RMSE=0.11929 best=0.11796

- [2026-10-21 18:02:42 UTC+8] regression seed=22 step=12000/15000 val_RMSE=0.13006 best=0.11796

- [2026-10-21 18:02:42 UTC+8] regression seed=22 step=12100/15000 val_RMSE=0.12986 best=0.11796

- [2026-10-21 18:02:43 UTC+8] regression seed=22 step=12200/15000 val_RMSE=0.14081 best=0.11796

- [2026-10-21 18:02:43 UTC+8] regression seed=22 step=12300/15000 val_RMSE=0.12367 best=0.11796

- [2026-10-21 18:02:43 UTC+8] regression seed=22 step=12400/15000 val_RMSE=0.12241 best=0.11796

- [2026-10-21 18:02:43 UTC+8] regression seed=22 step=12500/15000 val_RMSE=0.14063 best=0.11796

- [2026-10-21 18:02:43 UTC+8] regression seed=22 step=12600/15000 val_RMSE=0.12366 best=0.11796

- [2026-10-21 18:02:43 UTC+8] regression seed=22 step=12700/15000 val_RMSE=0.12784 best=0.11796

- [2026-10-21 18:02:44 UTC+8] regression seed=22 step=12800/15000 val_RMSE=0.11587 best=0.11587

- [2026-10-21 18:02:44 UTC+8] regression seed=22 step=12900/15000 val_RMSE=0.13181 best=0.11587

- [2026-10-21 18:02:44 UTC+8] regression seed=22 step=13000/15000 val_RMSE=0.12042 best=0.11587

- [2026-10-21 18:02:44 UTC+8] regression seed=22 step=13100/15000 val_RMSE=0.12437 best=0.11587

- [2026-10-21 18:02:44 UTC+8] regression seed=22 step=13200/15000 val_RMSE=0.12101 best=0.11587

- [2026-10-21 18:02:44 UTC+8] regression seed=22 step=13300/15000 val_RMSE=0.12742 best=0.11587

- [2026-10-21 18:02:44 UTC+8] regression seed=22 step=13400/15000 val_RMSE=0.13016 best=0.11587

- [2026-10-21 18:02:45 UTC+8] regression seed=22 step=13500/15000 val_RMSE=0.14655 best=0.11587

- [2026-10-21 18:02:45 UTC+8] regression seed=22 step=13600/15000 val_RMSE=0.11392 best=0.11392

- [2026-10-21 18:02:45 UTC+8] regression seed=22 step=13700/15000 val_RMSE=0.13892 best=0.11392

- [2026-10-21 18:02:45 UTC+8] regression seed=22 step=13800/15000 val_RMSE=0.12978 best=0.11392

- [2026-10-21 18:02:45 UTC+8] regression seed=22 step=13900/15000 val_RMSE=0.13256 best=0.11392

- [2026-10-21 18:02:45 UTC+8] regression seed=22 step=14000/15000 val_RMSE=0.13075 best=0.11392

- [2026-10-21 18:02:46 UTC+8] regression seed=22 step=14100/15000 val_RMSE=0.11985 best=0.11392

- [2026-10-21 18:02:46 UTC+8] regression seed=22 step=14200/15000 val_RMSE=0.12884 best=0.11392

- [2026-10-21 18:02:46 UTC+8] regression seed=22 step=14300/15000 val_RMSE=0.12499 best=0.11392

- [2026-10-21 18:02:46 UTC+8] regression seed=22 step=14400/15000 val_RMSE=0.12205 best=0.11392

- [2026-10-21 18:02:46 UTC+8] regression seed=22 step=14500/15000 val_RMSE=0.11967 best=0.11392

- [2026-10-21 18:02:46 UTC+8] regression seed=22 step=14600/15000 val_RMSE=0.11572 best=0.11392

- [2026-10-21 18:02:47 UTC+8] regression seed=22 step=14700/15000 val_RMSE=0.12200 best=0.11392

- [2026-10-21 18:02:47 UTC+8] regression seed=22 step=14800/15000 val_RMSE=0.12299 best=0.11392

- [2026-10-21 18:02:47 UTC+8] regression seed=22 step=14900/15000 val_RMSE=0.11854 best=0.11392

- [2026-10-21 18:02:47 UTC+8] regression seed=22 step=15000/15000 val_RMSE=0.13279 best=0.11392

- [2026-10-21 18:02:47 UTC+8] 完成 regression seed=22，本轮耗时 26.4 s，选择验证最优 step=13600

- [2026-10-21 18:02:47 UTC+8] regression seed=33 step=100/15000 val_RMSE=0.25476 best=0.25476

- [2026-10-21 18:02:47 UTC+8] regression seed=33 step=200/15000 val_RMSE=0.25408 best=0.25408

- [2026-10-21 18:02:47 UTC+8] regression seed=33 step=300/15000 val_RMSE=0.25393 best=0.25393

- [2026-10-21 18:02:48 UTC+8] regression seed=33 step=400/15000 val_RMSE=0.24870 best=0.24870

- [2026-10-21 18:02:48 UTC+8] regression seed=33 step=500/15000 val_RMSE=0.24238 best=0.24238

- [2026-10-21 18:02:48 UTC+8] regression seed=33 step=600/15000 val_RMSE=0.24122 best=0.24122

- [2026-10-21 18:02:48 UTC+8] regression seed=33 step=700/15000 val_RMSE=0.23623 best=0.23623

- [2026-10-21 18:02:48 UTC+8] regression seed=33 step=800/15000 val_RMSE=0.23035 best=0.23035

- [2026-10-21 18:02:48 UTC+8] regression seed=33 step=900/15000 val_RMSE=0.23706 best=0.23035

- [2026-10-21 18:02:49 UTC+8] regression seed=33 step=1000/15000 val_RMSE=0.22053 best=0.22053

- [2026-10-21 18:02:49 UTC+8] regression seed=33 step=1100/15000 val_RMSE=0.22949 best=0.22053

- [2026-10-21 18:02:49 UTC+8] regression seed=33 step=1200/15000 val_RMSE=0.23246 best=0.22053

- [2026-10-21 18:02:49 UTC+8] regression seed=33 step=1300/15000 val_RMSE=0.20065 best=0.20065

- [2026-10-21 18:02:49 UTC+8] regression seed=33 step=1400/15000 val_RMSE=0.19339 best=0.19339

- [2026-10-21 18:02:49 UTC+8] regression seed=33 step=1500/15000 val_RMSE=0.18652 best=0.18652

- [2026-10-21 18:02:50 UTC+8] regression seed=33 step=1600/15000 val_RMSE=0.19352 best=0.18652

- [2026-10-21 18:02:50 UTC+8] regression seed=33 step=1700/15000 val_RMSE=0.18625 best=0.18625

- [2026-10-21 18:02:50 UTC+8] regression seed=33 step=1800/15000 val_RMSE=0.18475 best=0.18475

- [2026-10-21 18:02:50 UTC+8] regression seed=33 step=1900/15000 val_RMSE=0.17180 best=0.17180

- [2026-10-21 18:02:50 UTC+8] regression seed=33 step=2000/15000 val_RMSE=0.18606 best=0.17180

- [2026-10-21 18:02:50 UTC+8] regression seed=33 step=2100/15000 val_RMSE=0.16830 best=0.16830

- [2026-10-21 18:02:50 UTC+8] regression seed=33 step=2200/15000 val_RMSE=0.18154 best=0.16830

- [2026-10-21 18:02:51 UTC+8] regression seed=33 step=2300/15000 val_RMSE=0.17166 best=0.16830

- [2026-10-21 18:02:51 UTC+8] regression seed=33 step=2400/15000 val_RMSE=0.16990 best=0.16830

- [2026-10-21 18:02:51 UTC+8] regression seed=33 step=2500/15000 val_RMSE=0.18710 best=0.16830

- [2026-10-21 18:02:51 UTC+8] regression seed=33 step=2600/15000 val_RMSE=0.16588 best=0.16588

- [2026-10-21 18:02:51 UTC+8] regression seed=33 step=2700/15000 val_RMSE=0.17480 best=0.16588

- [2026-10-21 18:02:51 UTC+8] regression seed=33 step=2800/15000 val_RMSE=0.15697 best=0.15697

- [2026-10-21 18:02:52 UTC+8] regression seed=33 step=2900/15000 val_RMSE=0.15438 best=0.15438

- [2026-10-21 18:02:52 UTC+8] regression seed=33 step=3000/15000 val_RMSE=0.16584 best=0.15438

- [2026-10-21 18:02:52 UTC+8] regression seed=33 step=3100/15000 val_RMSE=0.16020 best=0.15438

- [2026-10-21 18:02:52 UTC+8] regression seed=33 step=3200/15000 val_RMSE=0.16221 best=0.15438

- [2026-10-21 18:02:52 UTC+8] regression seed=33 step=3300/15000 val_RMSE=0.15090 best=0.15090

- [2026-10-21 18:02:52 UTC+8] regression seed=33 step=3400/15000 val_RMSE=0.15063 best=0.15063

- [2026-10-21 18:02:52 UTC+8] regression seed=33 step=3500/15000 val_RMSE=0.16396 best=0.15063

- [2026-10-21 18:02:53 UTC+8] regression seed=33 step=3600/15000 val_RMSE=0.16639 best=0.15063

- [2026-10-21 18:02:53 UTC+8] regression seed=33 step=3700/15000 val_RMSE=0.16748 best=0.15063

- [2026-10-21 18:02:53 UTC+8] regression seed=33 step=3800/15000 val_RMSE=0.16263 best=0.15063

- [2026-10-21 18:02:53 UTC+8] regression seed=33 step=3900/15000 val_RMSE=0.15374 best=0.15063

- [2026-10-21 18:02:53 UTC+8] regression seed=33 step=4000/15000 val_RMSE=0.16462 best=0.15063

- [2026-10-21 18:02:53 UTC+8] regression seed=33 step=4100/15000 val_RMSE=0.14307 best=0.14307

- [2026-10-21 18:02:54 UTC+8] regression seed=33 step=4200/15000 val_RMSE=0.14823 best=0.14307

- [2026-10-21 18:02:54 UTC+8] regression seed=33 step=4300/15000 val_RMSE=0.14133 best=0.14133

- [2026-10-21 18:02:54 UTC+8] regression seed=33 step=4400/15000 val_RMSE=0.14657 best=0.14133

- [2026-10-21 18:02:54 UTC+8] regression seed=33 step=4500/15000 val_RMSE=0.14909 best=0.14133

- [2026-10-21 18:02:54 UTC+8] regression seed=33 step=4600/15000 val_RMSE=0.15350 best=0.14133

- [2026-10-21 18:02:54 UTC+8] regression seed=33 step=4700/15000 val_RMSE=0.15072 best=0.14133

- [2026-10-21 18:02:54 UTC+8] regression seed=33 step=4800/15000 val_RMSE=0.14152 best=0.14133

- [2026-10-21 18:02:55 UTC+8] regression seed=33 step=4900/15000 val_RMSE=0.15246 best=0.14133

- [2026-10-21 18:02:55 UTC+8] regression seed=33 step=5000/15000 val_RMSE=0.14600 best=0.14133

- [2026-10-21 18:02:55 UTC+8] regression seed=33 step=5100/15000 val_RMSE=0.15009 best=0.14133

- [2026-10-21 18:02:55 UTC+8] regression seed=33 step=5200/15000 val_RMSE=0.14863 best=0.14133

- [2026-10-21 18:02:55 UTC+8] regression seed=33 step=5300/15000 val_RMSE=0.14399 best=0.14133

- [2026-10-21 18:02:55 UTC+8] regression seed=33 step=5400/15000 val_RMSE=0.14839 best=0.14133

- [2026-10-21 18:02:56 UTC+8] regression seed=33 step=5500/15000 val_RMSE=0.13629 best=0.13629

- [2026-10-21 18:02:56 UTC+8] regression seed=33 step=5600/15000 val_RMSE=0.14556 best=0.13629

- [2026-10-21 18:02:56 UTC+8] regression seed=33 step=5700/15000 val_RMSE=0.13344 best=0.13344

- [2026-10-21 18:02:56 UTC+8] regression seed=33 step=5800/15000 val_RMSE=0.14912 best=0.13344

- [2026-10-21 18:02:56 UTC+8] regression seed=33 step=5900/15000 val_RMSE=0.15823 best=0.13344

- [2026-10-21 18:02:56 UTC+8] regression seed=33 step=6000/15000 val_RMSE=0.13559 best=0.13344

- [2026-10-21 18:02:57 UTC+8] regression seed=33 step=6100/15000 val_RMSE=0.14305 best=0.13344

- [2026-10-21 18:02:57 UTC+8] regression seed=33 step=6200/15000 val_RMSE=0.16402 best=0.13344

- [2026-10-21 18:02:57 UTC+8] regression seed=33 step=6300/15000 val_RMSE=0.13387 best=0.13344

- [2026-10-21 18:02:57 UTC+8] regression seed=33 step=6400/15000 val_RMSE=0.13696 best=0.13344

- [2026-10-21 18:02:57 UTC+8] regression seed=33 step=6500/15000 val_RMSE=0.17649 best=0.13344

- [2026-10-21 18:02:57 UTC+8] regression seed=33 step=6600/15000 val_RMSE=0.14402 best=0.13344

- [2026-10-21 18:02:57 UTC+8] regression seed=33 step=6700/15000 val_RMSE=0.14356 best=0.13344

- [2026-10-21 18:02:58 UTC+8] regression seed=33 step=6800/15000 val_RMSE=0.14005 best=0.13344

- [2026-10-21 18:02:58 UTC+8] regression seed=33 step=6900/15000 val_RMSE=0.13527 best=0.13344

- [2026-10-21 18:02:58 UTC+8] regression seed=33 step=7000/15000 val_RMSE=0.14209 best=0.13344

- [2026-10-21 18:02:58 UTC+8] regression seed=33 step=7100/15000 val_RMSE=0.13189 best=0.13189

- [2026-10-21 18:02:58 UTC+8] regression seed=33 step=7200/15000 val_RMSE=0.13293 best=0.13189

- [2026-10-21 18:02:58 UTC+8] regression seed=33 step=7300/15000 val_RMSE=0.13901 best=0.13189

- [2026-10-21 18:02:59 UTC+8] regression seed=33 step=7400/15000 val_RMSE=0.14510 best=0.13189

- [2026-10-21 18:02:59 UTC+8] regression seed=33 step=7500/15000 val_RMSE=0.14252 best=0.13189

- [2026-10-21 18:02:59 UTC+8] regression seed=33 step=7600/15000 val_RMSE=0.15056 best=0.13189

- [2026-10-21 18:02:59 UTC+8] regression seed=33 step=7700/15000 val_RMSE=0.12919 best=0.12919

- [2026-10-21 18:02:59 UTC+8] regression seed=33 step=7800/15000 val_RMSE=0.13361 best=0.12919

- [2026-10-21 18:02:59 UTC+8] regression seed=33 step=7900/15000 val_RMSE=0.13119 best=0.12919

- [2026-10-21 18:02:59 UTC+8] regression seed=33 step=8000/15000 val_RMSE=0.12306 best=0.12306

- [2026-10-21 18:03:00 UTC+8] regression seed=33 step=8100/15000 val_RMSE=0.12598 best=0.12306

- [2026-10-21 18:03:00 UTC+8] regression seed=33 step=8200/15000 val_RMSE=0.12516 best=0.12306

- [2026-10-21 18:03:00 UTC+8] regression seed=33 step=8300/15000 val_RMSE=0.14791 best=0.12306

- [2026-10-21 18:03:00 UTC+8] regression seed=33 step=8400/15000 val_RMSE=0.12544 best=0.12306

- [2026-10-21 18:03:00 UTC+8] regression seed=33 step=8500/15000 val_RMSE=0.12499 best=0.12306

- [2026-10-21 18:03:00 UTC+8] regression seed=33 step=8600/15000 val_RMSE=0.12519 best=0.12306

- [2026-10-21 18:03:01 UTC+8] regression seed=33 step=8700/15000 val_RMSE=0.12971 best=0.12306

- [2026-10-21 18:03:01 UTC+8] regression seed=33 step=8800/15000 val_RMSE=0.13987 best=0.12306

- [2026-10-21 18:03:01 UTC+8] regression seed=33 step=8900/15000 val_RMSE=0.13675 best=0.12306

- [2026-10-21 18:03:01 UTC+8] regression seed=33 step=9000/15000 val_RMSE=0.13870 best=0.12306

- [2026-10-21 18:03:01 UTC+8] regression seed=33 step=9100/15000 val_RMSE=0.12949 best=0.12306

- [2026-10-21 18:03:01 UTC+8] regression seed=33 step=9200/15000 val_RMSE=0.13155 best=0.12306

- [2026-10-21 18:03:01 UTC+8] regression seed=33 step=9300/15000 val_RMSE=0.12987 best=0.12306

- [2026-10-21 18:03:02 UTC+8] regression seed=33 step=9400/15000 val_RMSE=0.12406 best=0.12306

- [2026-10-21 18:03:02 UTC+8] regression seed=33 step=9500/15000 val_RMSE=0.14613 best=0.12306

- [2026-10-21 18:03:02 UTC+8] regression seed=33 step=9600/15000 val_RMSE=0.12847 best=0.12306

- [2026-10-21 18:03:02 UTC+8] regression seed=33 step=9700/15000 val_RMSE=0.13189 best=0.12306

- [2026-10-21 18:03:02 UTC+8] regression seed=33 step=9800/15000 val_RMSE=0.13853 best=0.12306

- [2026-10-21 18:03:02 UTC+8] regression seed=33 step=9900/15000 val_RMSE=0.12408 best=0.12306

- [2026-10-21 18:03:03 UTC+8] regression seed=33 step=10000/15000 val_RMSE=0.12168 best=0.12168

- [2026-10-21 18:03:03 UTC+8] regression seed=33 step=10100/15000 val_RMSE=0.14291 best=0.12168

- [2026-10-21 18:03:03 UTC+8] regression seed=33 step=10200/15000 val_RMSE=0.13872 best=0.12168

- [2026-10-21 18:03:03 UTC+8] regression seed=33 step=10300/15000 val_RMSE=0.12029 best=0.12029

- [2026-10-21 18:03:03 UTC+8] regression seed=33 step=10400/15000 val_RMSE=0.13253 best=0.12029

- [2026-10-21 18:03:03 UTC+8] regression seed=33 step=10500/15000 val_RMSE=0.12564 best=0.12029

- [2026-10-21 18:03:04 UTC+8] regression seed=33 step=10600/15000 val_RMSE=0.12693 best=0.12029

- [2026-10-21 18:03:04 UTC+8] regression seed=33 step=10700/15000 val_RMSE=0.12191 best=0.12029

- [2026-10-21 18:03:04 UTC+8] regression seed=33 step=10800/15000 val_RMSE=0.13215 best=0.12029

- [2026-10-21 18:03:04 UTC+8] regression seed=33 step=10900/15000 val_RMSE=0.12473 best=0.12029

- [2026-10-21 18:03:04 UTC+8] regression seed=33 step=11000/15000 val_RMSE=0.13172 best=0.12029

- [2026-10-21 18:03:04 UTC+8] regression seed=33 step=11100/15000 val_RMSE=0.12424 best=0.12029

- [2026-10-21 18:03:04 UTC+8] regression seed=33 step=11200/15000 val_RMSE=0.12638 best=0.12029

- [2026-10-21 18:03:05 UTC+8] regression seed=33 step=11300/15000 val_RMSE=0.14071 best=0.12029

- [2026-10-21 18:03:05 UTC+8] regression seed=33 step=11400/15000 val_RMSE=0.12837 best=0.12029

- [2026-10-21 18:03:05 UTC+8] regression seed=33 step=11500/15000 val_RMSE=0.13201 best=0.12029

- [2026-10-21 18:03:05 UTC+8] regression seed=33 step=11600/15000 val_RMSE=0.12803 best=0.12029

- [2026-10-21 18:03:05 UTC+8] regression seed=33 step=11700/15000 val_RMSE=0.14176 best=0.12029

- [2026-10-21 18:03:05 UTC+8] regression seed=33 step=11800/15000 val_RMSE=0.12301 best=0.12029

- [2026-10-21 18:03:06 UTC+8] regression seed=33 step=11900/15000 val_RMSE=0.14846 best=0.12029

- [2026-10-21 18:03:06 UTC+8] regression seed=33 step=12000/15000 val_RMSE=0.12260 best=0.12029

- [2026-10-21 18:03:06 UTC+8] regression seed=33 step=12100/15000 val_RMSE=0.12361 best=0.12029

- [2026-10-21 18:03:06 UTC+8] regression seed=33 step=12200/15000 val_RMSE=0.11967 best=0.11967

- [2026-10-21 18:03:06 UTC+8] regression seed=33 step=12300/15000 val_RMSE=0.12403 best=0.11967

- [2026-10-21 18:03:06 UTC+8] regression seed=33 step=12400/15000 val_RMSE=0.11812 best=0.11812

- [2026-10-21 18:03:06 UTC+8] regression seed=33 step=12500/15000 val_RMSE=0.12859 best=0.11812

- [2026-10-21 18:03:07 UTC+8] regression seed=33 step=12600/15000 val_RMSE=0.11945 best=0.11812

- [2026-10-21 18:03:07 UTC+8] regression seed=33 step=12700/15000 val_RMSE=0.12771 best=0.11812

- [2026-10-21 18:03:07 UTC+8] regression seed=33 step=12800/15000 val_RMSE=0.13576 best=0.11812

- [2026-10-21 18:03:07 UTC+8] regression seed=33 step=12900/15000 val_RMSE=0.12257 best=0.11812

- [2026-10-21 18:03:07 UTC+8] regression seed=33 step=13000/15000 val_RMSE=0.12415 best=0.11812

- [2026-10-21 18:03:08 UTC+8] regression seed=33 step=13100/15000 val_RMSE=0.12382 best=0.11812

- [2026-10-21 18:03:08 UTC+8] regression seed=33 step=13200/15000 val_RMSE=0.11720 best=0.11720

- [2026-10-21 18:03:08 UTC+8] regression seed=33 step=13300/15000 val_RMSE=0.12587 best=0.11720

- [2026-10-21 18:03:08 UTC+8] regression seed=33 step=13400/15000 val_RMSE=0.13393 best=0.11720

- [2026-10-21 18:03:08 UTC+8] regression seed=33 step=13500/15000 val_RMSE=0.12237 best=0.11720

- [2026-10-21 18:03:08 UTC+8] regression seed=33 step=13600/15000 val_RMSE=0.11814 best=0.11720

- [2026-10-21 18:03:08 UTC+8] regression seed=33 step=13700/15000 val_RMSE=0.11742 best=0.11720

- [2026-10-21 18:03:09 UTC+8] regression seed=33 step=13800/15000 val_RMSE=0.12787 best=0.11720

- [2026-10-21 18:03:09 UTC+8] regression seed=33 step=13900/15000 val_RMSE=0.13306 best=0.11720

- [2026-10-21 18:03:09 UTC+8] regression seed=33 step=14000/15000 val_RMSE=0.12408 best=0.11720

- [2026-10-21 18:03:09 UTC+8] regression seed=33 step=14100/15000 val_RMSE=0.12114 best=0.11720

- [2026-10-21 18:03:09 UTC+8] regression seed=33 step=14200/15000 val_RMSE=0.12194 best=0.11720

- [2026-10-21 18:03:09 UTC+8] regression seed=33 step=14300/15000 val_RMSE=0.12246 best=0.11720

- [2026-10-21 18:03:10 UTC+8] regression seed=33 step=14400/15000 val_RMSE=0.11728 best=0.11720

- [2026-10-21 18:03:10 UTC+8] regression seed=33 step=14500/15000 val_RMSE=0.12094 best=0.11720

- [2026-10-21 18:03:10 UTC+8] regression seed=33 step=14600/15000 val_RMSE=0.11651 best=0.11651

- [2026-10-21 18:03:10 UTC+8] regression seed=33 step=14700/15000 val_RMSE=0.13456 best=0.11651

- [2026-10-21 18:03:10 UTC+8] regression seed=33 step=14800/15000 val_RMSE=0.13107 best=0.11651

- [2026-10-21 18:03:10 UTC+8] regression seed=33 step=14900/15000 val_RMSE=0.13253 best=0.11651

- [2026-10-21 18:03:10 UTC+8] regression seed=33 step=15000/15000 val_RMSE=0.12539 best=0.11651

- [2026-10-21 18:03:10 UTC+8] 完成 regression seed=33，本轮耗时 23.5 s，选择验证最优 step=14600

- [2026-10-21 18:03:11 UTC+8] residual seed=11 step=100/15000 val_RMSE=0.27637 best=0.27637

- [2026-10-21 18:03:11 UTC+8] residual seed=11 step=200/15000 val_RMSE=0.25848 best=0.25848

- [2026-10-21 18:03:11 UTC+8] residual seed=11 step=300/15000 val_RMSE=0.25501 best=0.25501

- [2026-10-21 18:03:11 UTC+8] residual seed=11 step=400/15000 val_RMSE=0.25036 best=0.25036

- [2026-10-21 18:03:11 UTC+8] residual seed=11 step=500/15000 val_RMSE=0.25292 best=0.25036

- [2026-10-21 18:03:11 UTC+8] residual seed=11 step=600/15000 val_RMSE=0.25910 best=0.25036

- [2026-10-21 18:03:12 UTC+8] residual seed=11 step=700/15000 val_RMSE=0.24178 best=0.24178

- [2026-10-21 18:03:12 UTC+8] residual seed=11 step=800/15000 val_RMSE=0.23928 best=0.23928

- [2026-10-21 18:03:12 UTC+8] residual seed=11 step=900/15000 val_RMSE=0.22738 best=0.22738

- [2026-10-21 18:03:12 UTC+8] residual seed=11 step=1000/15000 val_RMSE=0.21280 best=0.21280

- [2026-10-21 18:03:12 UTC+8] residual seed=11 step=1100/15000 val_RMSE=0.23736 best=0.21280

- [2026-10-21 18:03:12 UTC+8] residual seed=11 step=1200/15000 val_RMSE=0.20462 best=0.20462

- [2026-10-21 18:03:13 UTC+8] residual seed=11 step=1300/15000 val_RMSE=0.21286 best=0.20462

- [2026-10-21 18:03:13 UTC+8] residual seed=11 step=1400/15000 val_RMSE=0.20460 best=0.20460

- [2026-10-21 18:03:13 UTC+8] residual seed=11 step=1500/15000 val_RMSE=0.21794 best=0.20460

- [2026-10-21 18:03:13 UTC+8] residual seed=11 step=1600/15000 val_RMSE=0.19484 best=0.19484

- [2026-10-21 18:03:13 UTC+8] residual seed=11 step=1700/15000 val_RMSE=0.20070 best=0.19484

- [2026-10-21 18:03:13 UTC+8] residual seed=11 step=1800/15000 val_RMSE=0.19849 best=0.19484

- [2026-10-21 18:03:13 UTC+8] residual seed=11 step=1900/15000 val_RMSE=0.19555 best=0.19484

- [2026-10-21 18:03:14 UTC+8] residual seed=11 step=2000/15000 val_RMSE=0.19391 best=0.19391

- [2026-10-21 18:03:14 UTC+8] residual seed=11 step=2100/15000 val_RMSE=0.20543 best=0.19391

- [2026-10-21 18:03:14 UTC+8] residual seed=11 step=2200/15000 val_RMSE=0.19720 best=0.19391

- [2026-10-21 18:03:14 UTC+8] residual seed=11 step=2300/15000 val_RMSE=0.17235 best=0.17235

- [2026-10-21 18:03:14 UTC+8] residual seed=11 step=2400/15000 val_RMSE=0.20002 best=0.17235

- [2026-10-21 18:03:14 UTC+8] residual seed=11 step=2500/15000 val_RMSE=0.17931 best=0.17235

- [2026-10-21 18:03:15 UTC+8] residual seed=11 step=2600/15000 val_RMSE=0.19425 best=0.17235

- [2026-10-21 18:03:15 UTC+8] residual seed=11 step=2700/15000 val_RMSE=0.17865 best=0.17235

- [2026-10-21 18:03:15 UTC+8] residual seed=11 step=2800/15000 val_RMSE=0.17737 best=0.17235

- [2026-10-21 18:03:15 UTC+8] residual seed=11 step=2900/15000 val_RMSE=0.17379 best=0.17235

- [2026-10-21 18:03:15 UTC+8] residual seed=11 step=3000/15000 val_RMSE=0.18027 best=0.17235

- [2026-10-21 18:03:15 UTC+8] residual seed=11 step=3100/15000 val_RMSE=0.16835 best=0.16835

- [2026-10-21 18:03:15 UTC+8] residual seed=11 step=3200/15000 val_RMSE=0.17359 best=0.16835

- [2026-10-21 18:03:16 UTC+8] residual seed=11 step=3300/15000 val_RMSE=0.16838 best=0.16835

- [2026-10-21 18:03:16 UTC+8] residual seed=11 step=3400/15000 val_RMSE=0.16675 best=0.16675

- [2026-10-21 18:03:16 UTC+8] residual seed=11 step=3500/15000 val_RMSE=0.17369 best=0.16675

- [2026-10-21 18:03:16 UTC+8] residual seed=11 step=3600/15000 val_RMSE=0.16661 best=0.16661

- [2026-10-21 18:03:16 UTC+8] residual seed=11 step=3700/15000 val_RMSE=0.16218 best=0.16218

- [2026-10-21 18:03:16 UTC+8] residual seed=11 step=3800/15000 val_RMSE=0.17481 best=0.16218

- [2026-10-21 18:03:17 UTC+8] residual seed=11 step=3900/15000 val_RMSE=0.16286 best=0.16218

- [2026-10-21 18:03:17 UTC+8] residual seed=11 step=4000/15000 val_RMSE=0.15732 best=0.15732

- [2026-10-21 18:03:17 UTC+8] residual seed=11 step=4100/15000 val_RMSE=0.16895 best=0.15732

- [2026-10-21 18:03:17 UTC+8] residual seed=11 step=4200/15000 val_RMSE=0.16560 best=0.15732

- [2026-10-21 18:03:17 UTC+8] residual seed=11 step=4300/15000 val_RMSE=0.15697 best=0.15697

- [2026-10-21 18:03:17 UTC+8] residual seed=11 step=4400/15000 val_RMSE=0.15220 best=0.15220

- [2026-10-21 18:03:18 UTC+8] residual seed=11 step=4500/15000 val_RMSE=0.13728 best=0.13728

- [2026-10-21 18:03:18 UTC+8] residual seed=11 step=4600/15000 val_RMSE=0.17317 best=0.13728

- [2026-10-21 18:03:18 UTC+8] residual seed=11 step=4700/15000 val_RMSE=0.15530 best=0.13728

- [2026-10-21 18:03:18 UTC+8] residual seed=11 step=4800/15000 val_RMSE=0.15763 best=0.13728

- [2026-10-21 18:03:18 UTC+8] residual seed=11 step=4900/15000 val_RMSE=0.14540 best=0.13728

- [2026-10-21 18:03:18 UTC+8] residual seed=11 step=5000/15000 val_RMSE=0.13368 best=0.13368

- [2026-10-21 18:03:18 UTC+8] residual seed=11 step=5100/15000 val_RMSE=0.14660 best=0.13368

- [2026-10-21 18:03:19 UTC+8] residual seed=11 step=5200/15000 val_RMSE=0.15359 best=0.13368

- [2026-10-21 18:03:19 UTC+8] residual seed=11 step=5300/15000 val_RMSE=0.14629 best=0.13368

- [2026-10-21 18:03:19 UTC+8] residual seed=11 step=5400/15000 val_RMSE=0.14759 best=0.13368

- [2026-10-21 18:03:19 UTC+8] residual seed=11 step=5500/15000 val_RMSE=0.14799 best=0.13368

- [2026-10-21 18:03:19 UTC+8] residual seed=11 step=5600/15000 val_RMSE=0.14608 best=0.13368

- [2026-10-21 18:03:19 UTC+8] residual seed=11 step=5700/15000 val_RMSE=0.14268 best=0.13368

- [2026-10-21 18:03:20 UTC+8] residual seed=11 step=5800/15000 val_RMSE=0.17218 best=0.13368

- [2026-10-21 18:03:20 UTC+8] residual seed=11 step=5900/15000 val_RMSE=0.15126 best=0.13368

- [2026-10-21 18:03:20 UTC+8] residual seed=11 step=6000/15000 val_RMSE=0.13271 best=0.13271

- [2026-10-21 18:03:20 UTC+8] residual seed=11 step=6100/15000 val_RMSE=0.14032 best=0.13271

- [2026-10-21 18:03:20 UTC+8] residual seed=11 step=6200/15000 val_RMSE=0.15418 best=0.13271

- [2026-10-21 18:03:20 UTC+8] residual seed=11 step=6300/15000 val_RMSE=0.15111 best=0.13271

- [2026-10-21 18:03:20 UTC+8] residual seed=11 step=6400/15000 val_RMSE=0.15479 best=0.13271

- [2026-10-21 18:03:21 UTC+8] residual seed=11 step=6500/15000 val_RMSE=0.14752 best=0.13271

- [2026-10-21 18:03:21 UTC+8] residual seed=11 step=6600/15000 val_RMSE=0.14642 best=0.13271

- [2026-10-21 18:03:21 UTC+8] residual seed=11 step=6700/15000 val_RMSE=0.14617 best=0.13271

- [2026-10-21 18:03:21 UTC+8] residual seed=11 step=6800/15000 val_RMSE=0.13759 best=0.13271

- [2026-10-21 18:03:21 UTC+8] residual seed=11 step=6900/15000 val_RMSE=0.15097 best=0.13271

- [2026-10-21 18:03:21 UTC+8] residual seed=11 step=7000/15000 val_RMSE=0.13107 best=0.13107

- [2026-10-21 18:03:22 UTC+8] residual seed=11 step=7100/15000 val_RMSE=0.12346 best=0.12346

- [2026-10-21 18:03:22 UTC+8] residual seed=11 step=7200/15000 val_RMSE=0.12732 best=0.12346

- [2026-10-21 18:03:22 UTC+8] residual seed=11 step=7300/15000 val_RMSE=0.13988 best=0.12346

- [2026-10-21 18:03:22 UTC+8] residual seed=11 step=7400/15000 val_RMSE=0.15029 best=0.12346

- [2026-10-21 18:03:22 UTC+8] residual seed=11 step=7500/15000 val_RMSE=0.13719 best=0.12346

- [2026-10-21 18:03:22 UTC+8] residual seed=11 step=7600/15000 val_RMSE=0.14649 best=0.12346

- [2026-10-21 18:03:23 UTC+8] residual seed=11 step=7700/15000 val_RMSE=0.13563 best=0.12346

- [2026-10-21 18:03:23 UTC+8] residual seed=11 step=7800/15000 val_RMSE=0.13697 best=0.12346

- [2026-10-21 18:03:23 UTC+8] residual seed=11 step=7900/15000 val_RMSE=0.15051 best=0.12346

- [2026-10-21 18:03:23 UTC+8] residual seed=11 step=8000/15000 val_RMSE=0.13339 best=0.12346

- [2026-10-21 18:03:23 UTC+8] residual seed=11 step=8100/15000 val_RMSE=0.14234 best=0.12346

- [2026-10-21 18:03:23 UTC+8] residual seed=11 step=8200/15000 val_RMSE=0.16033 best=0.12346

- [2026-10-21 18:03:24 UTC+8] residual seed=11 step=8300/15000 val_RMSE=0.13566 best=0.12346

- [2026-10-21 18:03:24 UTC+8] residual seed=11 step=8400/15000 val_RMSE=0.12575 best=0.12346

- [2026-10-21 18:03:24 UTC+8] residual seed=11 step=8500/15000 val_RMSE=0.12595 best=0.12346

- [2026-10-21 18:03:24 UTC+8] residual seed=11 step=8600/15000 val_RMSE=0.12747 best=0.12346

- [2026-10-21 18:03:24 UTC+8] residual seed=11 step=8700/15000 val_RMSE=0.12994 best=0.12346

- [2026-10-21 18:03:24 UTC+8] residual seed=11 step=8800/15000 val_RMSE=0.13919 best=0.12346

- [2026-10-21 18:03:24 UTC+8] residual seed=11 step=8900/15000 val_RMSE=0.13250 best=0.12346

- [2026-10-21 18:03:25 UTC+8] residual seed=11 step=9000/15000 val_RMSE=0.16006 best=0.12346

- [2026-10-21 18:03:25 UTC+8] residual seed=11 step=9100/15000 val_RMSE=0.14982 best=0.12346

- [2026-10-21 18:03:25 UTC+8] residual seed=11 step=9200/15000 val_RMSE=0.14140 best=0.12346

- [2026-10-21 18:03:25 UTC+8] residual seed=11 step=9300/15000 val_RMSE=0.14011 best=0.12346

- [2026-10-21 18:03:25 UTC+8] residual seed=11 step=9400/15000 val_RMSE=0.14325 best=0.12346

- [2026-10-21 18:03:25 UTC+8] residual seed=11 step=9500/15000 val_RMSE=0.12439 best=0.12346

- [2026-10-21 18:03:26 UTC+8] residual seed=11 step=9600/15000 val_RMSE=0.13087 best=0.12346

- [2026-10-21 18:03:26 UTC+8] residual seed=11 step=9700/15000 val_RMSE=0.13242 best=0.12346

- [2026-10-21 18:03:26 UTC+8] residual seed=11 step=9800/15000 val_RMSE=0.14255 best=0.12346

- [2026-10-21 18:03:26 UTC+8] residual seed=11 step=9900/15000 val_RMSE=0.16130 best=0.12346

- [2026-10-21 18:03:26 UTC+8] residual seed=11 step=10000/15000 val_RMSE=0.13342 best=0.12346

- [2026-10-21 18:03:26 UTC+8] residual seed=11 step=10100/15000 val_RMSE=0.14072 best=0.12346

- [2026-10-21 18:03:26 UTC+8] residual seed=11 step=10200/15000 val_RMSE=0.13623 best=0.12346

- [2026-10-21 18:03:27 UTC+8] residual seed=11 step=10300/15000 val_RMSE=0.12261 best=0.12261

- [2026-10-21 18:03:27 UTC+8] residual seed=11 step=10400/15000 val_RMSE=0.12402 best=0.12261

- [2026-10-21 18:03:27 UTC+8] residual seed=11 step=10500/15000 val_RMSE=0.13717 best=0.12261

- [2026-10-21 18:03:27 UTC+8] residual seed=11 step=10600/15000 val_RMSE=0.13879 best=0.12261

- [2026-10-21 18:03:27 UTC+8] residual seed=11 step=10700/15000 val_RMSE=0.13768 best=0.12261

- [2026-10-21 18:03:27 UTC+8] residual seed=11 step=10800/15000 val_RMSE=0.13307 best=0.12261

- [2026-10-21 18:03:28 UTC+8] residual seed=11 step=10900/15000 val_RMSE=0.12043 best=0.12043

- [2026-10-21 18:03:28 UTC+8] residual seed=11 step=11000/15000 val_RMSE=0.14722 best=0.12043

- [2026-10-21 18:03:28 UTC+8] residual seed=11 step=11100/15000 val_RMSE=0.13976 best=0.12043

- [2026-10-21 18:03:28 UTC+8] residual seed=11 step=11200/15000 val_RMSE=0.13403 best=0.12043

- [2026-10-21 18:03:28 UTC+8] residual seed=11 step=11300/15000 val_RMSE=0.13691 best=0.12043

- [2026-10-21 18:03:28 UTC+8] residual seed=11 step=11400/15000 val_RMSE=0.12977 best=0.12043

- [2026-10-21 18:03:29 UTC+8] residual seed=11 step=11500/15000 val_RMSE=0.14684 best=0.12043

- [2026-10-21 18:03:29 UTC+8] residual seed=11 step=11600/15000 val_RMSE=0.12500 best=0.12043

- [2026-10-21 18:03:29 UTC+8] residual seed=11 step=11700/15000 val_RMSE=0.13756 best=0.12043

- [2026-10-21 18:03:29 UTC+8] residual seed=11 step=11800/15000 val_RMSE=0.12120 best=0.12043

- [2026-10-21 18:03:29 UTC+8] residual seed=11 step=11900/15000 val_RMSE=0.13154 best=0.12043

- [2026-10-21 18:03:29 UTC+8] residual seed=11 step=12000/15000 val_RMSE=0.13440 best=0.12043

- [2026-10-21 18:03:29 UTC+8] residual seed=11 step=12100/15000 val_RMSE=0.12783 best=0.12043

- [2026-10-21 18:03:30 UTC+8] residual seed=11 step=12200/15000 val_RMSE=0.12584 best=0.12043

- [2026-10-21 18:03:30 UTC+8] residual seed=11 step=12300/15000 val_RMSE=0.12993 best=0.12043

- [2026-10-21 18:03:30 UTC+8] residual seed=11 step=12400/15000 val_RMSE=0.12655 best=0.12043

- [2026-10-21 18:03:30 UTC+8] residual seed=11 step=12500/15000 val_RMSE=0.12089 best=0.12043

- [2026-10-21 18:03:30 UTC+8] residual seed=11 step=12600/15000 val_RMSE=0.12691 best=0.12043

- [2026-10-21 18:03:30 UTC+8] residual seed=11 step=12700/15000 val_RMSE=0.11811 best=0.11811

- [2026-10-21 18:03:31 UTC+8] residual seed=11 step=12800/15000 val_RMSE=0.11862 best=0.11811

- [2026-10-21 18:03:31 UTC+8] residual seed=11 step=12900/15000 val_RMSE=0.11764 best=0.11764

- [2026-10-21 18:03:31 UTC+8] residual seed=11 step=13000/15000 val_RMSE=0.12293 best=0.11764

- [2026-10-21 18:03:31 UTC+8] residual seed=11 step=13100/15000 val_RMSE=0.12696 best=0.11764

- [2026-10-21 18:03:31 UTC+8] residual seed=11 step=13200/15000 val_RMSE=0.12288 best=0.11764

- [2026-10-21 18:03:31 UTC+8] residual seed=11 step=13300/15000 val_RMSE=0.13478 best=0.11764

- [2026-10-21 18:03:31 UTC+8] residual seed=11 step=13400/15000 val_RMSE=0.13446 best=0.11764

- [2026-10-21 18:03:32 UTC+8] residual seed=11 step=13500/15000 val_RMSE=0.13041 best=0.11764

- [2026-10-21 18:03:32 UTC+8] residual seed=11 step=13600/15000 val_RMSE=0.12008 best=0.11764

- [2026-10-21 18:03:32 UTC+8] residual seed=11 step=13700/15000 val_RMSE=0.11855 best=0.11764

- [2026-10-21 18:03:32 UTC+8] residual seed=11 step=13800/15000 val_RMSE=0.12273 best=0.11764

- [2026-10-21 18:03:32 UTC+8] residual seed=11 step=13900/15000 val_RMSE=0.12900 best=0.11764

- [2026-10-21 18:03:32 UTC+8] residual seed=11 step=14000/15000 val_RMSE=0.12978 best=0.11764

- [2026-10-21 18:03:33 UTC+8] residual seed=11 step=14100/15000 val_RMSE=0.14413 best=0.11764

- [2026-10-21 18:03:33 UTC+8] residual seed=11 step=14200/15000 val_RMSE=0.12450 best=0.11764

- [2026-10-21 18:03:33 UTC+8] residual seed=11 step=14300/15000 val_RMSE=0.12385 best=0.11764

- [2026-10-21 18:03:33 UTC+8] residual seed=11 step=14400/15000 val_RMSE=0.13108 best=0.11764

- [2026-10-21 18:03:33 UTC+8] residual seed=11 step=14500/15000 val_RMSE=0.12231 best=0.11764

- [2026-10-21 18:03:33 UTC+8] residual seed=11 step=14600/15000 val_RMSE=0.14039 best=0.11764

- [2026-10-21 18:03:33 UTC+8] residual seed=11 step=14700/15000 val_RMSE=0.14238 best=0.11764

- [2026-10-21 18:03:34 UTC+8] residual seed=11 step=14800/15000 val_RMSE=0.14605 best=0.11764

- [2026-10-21 18:03:34 UTC+8] residual seed=11 step=14900/15000 val_RMSE=0.14054 best=0.11764

- [2026-10-21 18:03:34 UTC+8] residual seed=11 step=15000/15000 val_RMSE=0.12662 best=0.11764

- [2026-10-21 18:03:34 UTC+8] 完成 residual seed=11，本轮耗时 23.4 s，选择验证最优 step=12900

- [2026-10-21 18:03:34 UTC+8] residual seed=22 step=100/15000 val_RMSE=0.26683 best=0.26683

- [2026-10-21 18:03:34 UTC+8] residual seed=22 step=200/15000 val_RMSE=0.26116 best=0.26116

- [2026-10-21 18:03:34 UTC+8] residual seed=22 step=300/15000 val_RMSE=0.24421 best=0.24421

- [2026-10-21 18:03:35 UTC+8] residual seed=22 step=400/15000 val_RMSE=0.25084 best=0.24421

- [2026-10-21 18:03:35 UTC+8] residual seed=22 step=500/15000 val_RMSE=0.23809 best=0.23809

- [2026-10-21 18:03:35 UTC+8] residual seed=22 step=600/15000 val_RMSE=0.24302 best=0.23809

- [2026-10-21 18:03:35 UTC+8] residual seed=22 step=700/15000 val_RMSE=0.28283 best=0.23809

- [2026-10-21 18:03:35 UTC+8] residual seed=22 step=800/15000 val_RMSE=0.23535 best=0.23535

- [2026-10-21 18:03:35 UTC+8] residual seed=22 step=900/15000 val_RMSE=0.21941 best=0.21941

- [2026-10-21 18:03:36 UTC+8] residual seed=22 step=1000/15000 val_RMSE=0.22424 best=0.21941

- [2026-10-21 18:03:36 UTC+8] residual seed=22 step=1100/15000 val_RMSE=0.22089 best=0.21941

- [2026-10-21 18:03:36 UTC+8] residual seed=22 step=1200/15000 val_RMSE=0.20297 best=0.20297

- [2026-10-21 18:03:36 UTC+8] residual seed=22 step=1300/15000 val_RMSE=0.20986 best=0.20297

- [2026-10-21 18:03:36 UTC+8] residual seed=22 step=1400/15000 val_RMSE=0.19149 best=0.19149

- [2026-10-21 18:03:36 UTC+8] residual seed=22 step=1500/15000 val_RMSE=0.20413 best=0.19149

- [2026-10-21 18:03:36 UTC+8] residual seed=22 step=1600/15000 val_RMSE=0.18652 best=0.18652

- [2026-10-21 18:03:37 UTC+8] residual seed=22 step=1700/15000 val_RMSE=0.20054 best=0.18652

- [2026-10-21 18:03:37 UTC+8] residual seed=22 step=1800/15000 val_RMSE=0.17879 best=0.17879

- [2026-10-21 18:03:37 UTC+8] residual seed=22 step=1900/15000 val_RMSE=0.18806 best=0.17879

- [2026-10-21 18:03:37 UTC+8] residual seed=22 step=2000/15000 val_RMSE=0.19222 best=0.17879

- [2026-10-21 18:03:37 UTC+8] residual seed=22 step=2100/15000 val_RMSE=0.20436 best=0.17879

- [2026-10-21 18:03:37 UTC+8] residual seed=22 step=2200/15000 val_RMSE=0.18091 best=0.17879

- [2026-10-21 18:03:38 UTC+8] residual seed=22 step=2300/15000 val_RMSE=0.17778 best=0.17778

- [2026-10-21 18:03:38 UTC+8] residual seed=22 step=2400/15000 val_RMSE=0.16921 best=0.16921

- [2026-10-21 18:03:38 UTC+8] residual seed=22 step=2500/15000 val_RMSE=0.18241 best=0.16921

- [2026-10-21 18:03:38 UTC+8] residual seed=22 step=2600/15000 val_RMSE=0.16139 best=0.16139

- [2026-10-21 18:03:38 UTC+8] residual seed=22 step=2700/15000 val_RMSE=0.16422 best=0.16139

- [2026-10-21 18:03:38 UTC+8] residual seed=22 step=2800/15000 val_RMSE=0.16415 best=0.16139

- [2026-10-21 18:03:38 UTC+8] residual seed=22 step=2900/15000 val_RMSE=0.19084 best=0.16139

- [2026-10-21 18:03:39 UTC+8] residual seed=22 step=3000/15000 val_RMSE=0.15954 best=0.15954

- [2026-10-21 18:03:39 UTC+8] residual seed=22 step=3100/15000 val_RMSE=0.16416 best=0.15954

- [2026-10-21 18:03:39 UTC+8] residual seed=22 step=3200/15000 val_RMSE=0.19771 best=0.15954

- [2026-10-21 18:03:39 UTC+8] residual seed=22 step=3300/15000 val_RMSE=0.16988 best=0.15954

- [2026-10-21 18:03:39 UTC+8] residual seed=22 step=3400/15000 val_RMSE=0.17536 best=0.15954

- [2026-10-21 18:03:39 UTC+8] residual seed=22 step=3500/15000 val_RMSE=0.17800 best=0.15954

- [2026-10-21 18:03:40 UTC+8] residual seed=22 step=3600/15000 val_RMSE=0.15607 best=0.15607

- [2026-10-21 18:08:55 UTC+8] 单步混合实验开始：CPU，训练轨迹=360，每模型更新=15000

- [2026-10-21 18:09:42 UTC+8] 混合数据完成：训练窗口=136080，验证窗口=17010

- [2026-10-21 18:09:42 UTC+8] 恢复 residual seed=22，训练步数 3700

- [2026-10-21 18:09:43 UTC+8] residual seed=22 step=3800/15000 val_RMSE=0.16334 best=0.15607

- [2026-10-21 18:09:43 UTC+8] residual seed=22 step=3900/15000 val_RMSE=0.15125 best=0.15125

- [2026-10-21 18:09:43 UTC+8] residual seed=22 step=4000/15000 val_RMSE=0.16063 best=0.15125

- [2026-10-21 18:09:43 UTC+8] residual seed=22 step=4100/15000 val_RMSE=0.15554 best=0.15125

- [2026-10-21 18:09:43 UTC+8] residual seed=22 step=4200/15000 val_RMSE=0.16534 best=0.15125

- [2026-10-21 18:09:44 UTC+8] residual seed=22 step=4300/15000 val_RMSE=0.14962 best=0.14962

- [2026-10-21 18:09:44 UTC+8] residual seed=22 step=4400/15000 val_RMSE=0.13697 best=0.13697

- [2026-10-21 18:09:44 UTC+8] residual seed=22 step=4500/15000 val_RMSE=0.16148 best=0.13697

- [2026-10-21 18:09:44 UTC+8] residual seed=22 step=4600/15000 val_RMSE=0.15133 best=0.13697

- [2026-10-21 18:09:45 UTC+8] residual seed=22 step=4700/15000 val_RMSE=0.16037 best=0.13697

- [2026-10-21 18:09:45 UTC+8] residual seed=22 step=4800/15000 val_RMSE=0.16775 best=0.13697

- [2026-10-21 18:09:45 UTC+8] residual seed=22 step=4900/15000 val_RMSE=0.15194 best=0.13697

- [2026-10-21 18:09:45 UTC+8] residual seed=22 step=5000/15000 val_RMSE=0.13970 best=0.13697

- [2026-10-21 18:09:45 UTC+8] residual seed=22 step=5100/15000 val_RMSE=0.14220 best=0.13697

- [2026-10-21 18:09:46 UTC+8] residual seed=22 step=5200/15000 val_RMSE=0.14525 best=0.13697

- [2026-10-21 18:09:46 UTC+8] residual seed=22 step=5300/15000 val_RMSE=0.14850 best=0.13697

- [2026-10-21 18:09:46 UTC+8] residual seed=22 step=5400/15000 val_RMSE=0.13719 best=0.13697

- [2026-10-21 18:09:46 UTC+8] residual seed=22 step=5500/15000 val_RMSE=0.14504 best=0.13697

- [2026-10-21 18:09:47 UTC+8] residual seed=22 step=5600/15000 val_RMSE=0.15050 best=0.13697

- [2026-10-21 18:09:47 UTC+8] residual seed=22 step=5700/15000 val_RMSE=0.14165 best=0.13697

- [2026-10-21 18:09:47 UTC+8] residual seed=22 step=5800/15000 val_RMSE=0.17305 best=0.13697

- [2026-10-21 18:09:47 UTC+8] residual seed=22 step=5900/15000 val_RMSE=0.13502 best=0.13502

- [2026-10-21 18:09:47 UTC+8] residual seed=22 step=6000/15000 val_RMSE=0.14219 best=0.13502

- [2026-10-21 18:09:48 UTC+8] residual seed=22 step=6100/15000 val_RMSE=0.14328 best=0.13502

- [2026-10-21 18:09:48 UTC+8] residual seed=22 step=6200/15000 val_RMSE=0.15037 best=0.13502

- [2026-10-21 18:09:48 UTC+8] residual seed=22 step=6300/15000 val_RMSE=0.14126 best=0.13502

- [2026-10-21 18:09:48 UTC+8] residual seed=22 step=6400/15000 val_RMSE=0.17027 best=0.13502

- [2026-10-21 18:09:48 UTC+8] residual seed=22 step=6500/15000 val_RMSE=0.15641 best=0.13502

- [2026-10-21 18:09:49 UTC+8] residual seed=22 step=6600/15000 val_RMSE=0.13116 best=0.13116

- [2026-10-21 18:09:49 UTC+8] residual seed=22 step=6700/15000 val_RMSE=0.15261 best=0.13116

- [2026-10-21 18:09:49 UTC+8] residual seed=22 step=6800/15000 val_RMSE=0.13139 best=0.13116

- [2026-10-21 18:09:49 UTC+8] residual seed=22 step=6900/15000 val_RMSE=0.16619 best=0.13116

- [2026-10-21 18:09:50 UTC+8] residual seed=22 step=7000/15000 val_RMSE=0.13868 best=0.13116

- [2026-10-21 18:09:50 UTC+8] residual seed=22 step=7100/15000 val_RMSE=0.14334 best=0.13116

- [2026-10-21 18:09:50 UTC+8] residual seed=22 step=7200/15000 val_RMSE=0.13544 best=0.13116

- [2026-10-21 18:09:50 UTC+8] residual seed=22 step=7300/15000 val_RMSE=0.12576 best=0.12576

- [2026-10-21 18:09:50 UTC+8] residual seed=22 step=7400/15000 val_RMSE=0.14396 best=0.12576

- [2026-10-21 18:09:51 UTC+8] residual seed=22 step=7500/15000 val_RMSE=0.12866 best=0.12576

- [2026-10-21 18:09:51 UTC+8] residual seed=22 step=7600/15000 val_RMSE=0.12814 best=0.12576

- [2026-10-21 18:09:51 UTC+8] residual seed=22 step=7700/15000 val_RMSE=0.14391 best=0.12576

- [2026-10-21 18:09:51 UTC+8] residual seed=22 step=7800/15000 val_RMSE=0.13185 best=0.12576

- [2026-10-21 18:09:51 UTC+8] residual seed=22 step=7900/15000 val_RMSE=0.13381 best=0.12576

- [2026-10-21 18:09:52 UTC+8] residual seed=22 step=8000/15000 val_RMSE=0.14111 best=0.12576

- [2026-10-21 18:09:52 UTC+8] residual seed=22 step=8100/15000 val_RMSE=0.13463 best=0.12576

- [2026-10-21 18:09:52 UTC+8] residual seed=22 step=8200/15000 val_RMSE=0.13662 best=0.12576

- [2026-10-21 18:09:52 UTC+8] residual seed=22 step=8300/15000 val_RMSE=0.13270 best=0.12576

- [2026-10-21 18:09:53 UTC+8] residual seed=22 step=8400/15000 val_RMSE=0.13480 best=0.12576

- [2026-10-21 18:09:53 UTC+8] residual seed=22 step=8500/15000 val_RMSE=0.14861 best=0.12576

- [2026-10-21 18:09:53 UTC+8] residual seed=22 step=8600/15000 val_RMSE=0.14354 best=0.12576

- [2026-10-21 18:09:53 UTC+8] residual seed=22 step=8700/15000 val_RMSE=0.13827 best=0.12576

- [2026-10-21 18:09:53 UTC+8] residual seed=22 step=8800/15000 val_RMSE=0.13245 best=0.12576

- [2026-10-21 18:09:54 UTC+8] residual seed=22 step=8900/15000 val_RMSE=0.13903 best=0.12576

- [2026-10-21 18:09:54 UTC+8] residual seed=22 step=9000/15000 val_RMSE=0.13733 best=0.12576

- [2026-10-21 18:09:54 UTC+8] residual seed=22 step=9100/15000 val_RMSE=0.13113 best=0.12576

- [2026-10-21 18:09:54 UTC+8] residual seed=22 step=9200/15000 val_RMSE=0.12972 best=0.12576

- [2026-10-21 18:09:55 UTC+8] residual seed=22 step=9300/15000 val_RMSE=0.12700 best=0.12576

- [2026-10-21 18:09:55 UTC+8] residual seed=22 step=9400/15000 val_RMSE=0.13408 best=0.12576

- [2026-10-21 18:09:55 UTC+8] residual seed=22 step=9500/15000 val_RMSE=0.12977 best=0.12576

- [2026-10-21 18:09:55 UTC+8] residual seed=22 step=9600/15000 val_RMSE=0.13709 best=0.12576

- [2026-10-21 18:09:55 UTC+8] residual seed=22 step=9700/15000 val_RMSE=0.15272 best=0.12576

- [2026-10-21 18:09:56 UTC+8] residual seed=22 step=9800/15000 val_RMSE=0.14965 best=0.12576

- [2026-10-21 18:09:56 UTC+8] residual seed=22 step=9900/15000 val_RMSE=0.13162 best=0.12576

- [2026-10-21 18:09:56 UTC+8] residual seed=22 step=10000/15000 val_RMSE=0.13808 best=0.12576

- [2026-10-21 18:09:56 UTC+8] residual seed=22 step=10100/15000 val_RMSE=0.13961 best=0.12576

- [2026-10-21 18:09:57 UTC+8] residual seed=22 step=10200/15000 val_RMSE=0.14048 best=0.12576

- [2026-10-21 18:09:57 UTC+8] residual seed=22 step=10300/15000 val_RMSE=0.13009 best=0.12576

- [2026-10-21 18:09:57 UTC+8] residual seed=22 step=10400/15000 val_RMSE=0.12449 best=0.12449

- [2026-10-21 18:09:57 UTC+8] residual seed=22 step=10500/15000 val_RMSE=0.12679 best=0.12449

- [2026-10-21 18:09:57 UTC+8] residual seed=22 step=10600/15000 val_RMSE=0.13367 best=0.12449

- [2026-10-21 18:09:58 UTC+8] residual seed=22 step=10700/15000 val_RMSE=0.12859 best=0.12449

- [2026-10-21 18:09:58 UTC+8] residual seed=22 step=10800/15000 val_RMSE=0.13276 best=0.12449

- [2026-10-21 18:09:58 UTC+8] residual seed=22 step=10900/15000 val_RMSE=0.13629 best=0.12449

- [2026-10-21 18:09:58 UTC+8] residual seed=22 step=11000/15000 val_RMSE=0.13477 best=0.12449

- [2026-10-21 18:09:59 UTC+8] residual seed=22 step=11100/15000 val_RMSE=0.12763 best=0.12449

- [2026-10-21 18:09:59 UTC+8] residual seed=22 step=11200/15000 val_RMSE=0.14297 best=0.12449

- [2026-10-21 18:09:59 UTC+8] residual seed=22 step=11300/15000 val_RMSE=0.13320 best=0.12449

- [2026-10-21 18:09:59 UTC+8] residual seed=22 step=11400/15000 val_RMSE=0.12581 best=0.12449

- [2026-10-21 18:09:59 UTC+8] residual seed=22 step=11500/15000 val_RMSE=0.12556 best=0.12449

- [2026-10-21 18:10:00 UTC+8] residual seed=22 step=11600/15000 val_RMSE=0.13767 best=0.12449

- [2026-10-21 18:10:00 UTC+8] residual seed=22 step=11700/15000 val_RMSE=0.12685 best=0.12449

- [2026-10-21 18:10:00 UTC+8] residual seed=22 step=11800/15000 val_RMSE=0.12503 best=0.12449

- [2026-10-21 18:10:00 UTC+8] residual seed=22 step=11900/15000 val_RMSE=0.12412 best=0.12412

- [2026-10-21 18:10:00 UTC+8] residual seed=22 step=12000/15000 val_RMSE=0.13402 best=0.12412

- [2026-10-21 18:10:01 UTC+8] residual seed=22 step=12100/15000 val_RMSE=0.12617 best=0.12412

- [2026-10-21 18:10:01 UTC+8] residual seed=22 step=12200/15000 val_RMSE=0.13597 best=0.12412

- [2026-10-21 18:10:01 UTC+8] residual seed=22 step=12300/15000 val_RMSE=0.13479 best=0.12412

- [2026-10-21 18:10:01 UTC+8] residual seed=22 step=12400/15000 val_RMSE=0.13064 best=0.12412

- [2026-10-21 18:10:02 UTC+8] residual seed=22 step=12500/15000 val_RMSE=0.13006 best=0.12412

- [2026-10-21 18:10:02 UTC+8] residual seed=22 step=12600/15000 val_RMSE=0.15175 best=0.12412

- [2026-10-21 18:10:02 UTC+8] residual seed=22 step=12700/15000 val_RMSE=0.12646 best=0.12412

- [2026-10-21 18:10:02 UTC+8] residual seed=22 step=12800/15000 val_RMSE=0.12438 best=0.12412

- [2026-10-21 18:10:02 UTC+8] residual seed=22 step=12900/15000 val_RMSE=0.13092 best=0.12412

- [2026-10-21 18:10:03 UTC+8] residual seed=22 step=13000/15000 val_RMSE=0.12197 best=0.12197

- [2026-10-21 18:10:03 UTC+8] residual seed=22 step=13100/15000 val_RMSE=0.12551 best=0.12197

- [2026-10-21 18:10:03 UTC+8] residual seed=22 step=13200/15000 val_RMSE=0.11670 best=0.11670

- [2026-10-21 18:10:03 UTC+8] residual seed=22 step=13300/15000 val_RMSE=0.12169 best=0.11670

- [2026-10-21 18:10:04 UTC+8] residual seed=22 step=13400/15000 val_RMSE=0.12314 best=0.11670

- [2026-10-21 18:10:04 UTC+8] residual seed=22 step=13500/15000 val_RMSE=0.14922 best=0.11670

- [2026-10-21 18:10:04 UTC+8] residual seed=22 step=13600/15000 val_RMSE=0.11830 best=0.11670

- [2026-10-21 18:10:04 UTC+8] residual seed=22 step=13700/15000 val_RMSE=0.13117 best=0.11670

- [2026-10-21 18:10:04 UTC+8] residual seed=22 step=13800/15000 val_RMSE=0.13182 best=0.11670

- [2026-10-21 18:10:05 UTC+8] residual seed=22 step=13900/15000 val_RMSE=0.11721 best=0.11670

- [2026-10-21 18:10:05 UTC+8] residual seed=22 step=14000/15000 val_RMSE=0.11834 best=0.11670

- [2026-10-21 18:10:05 UTC+8] residual seed=22 step=14100/15000 val_RMSE=0.12651 best=0.11670

- [2026-10-21 18:10:05 UTC+8] residual seed=22 step=14200/15000 val_RMSE=0.12962 best=0.11670

- [2026-10-21 18:10:06 UTC+8] residual seed=22 step=14300/15000 val_RMSE=0.13222 best=0.11670

- [2026-10-21 18:10:06 UTC+8] residual seed=22 step=14400/15000 val_RMSE=0.12525 best=0.11670

- [2026-10-21 18:10:06 UTC+8] residual seed=22 step=14500/15000 val_RMSE=0.12308 best=0.11670

- [2026-10-21 18:10:06 UTC+8] residual seed=22 step=14600/15000 val_RMSE=0.11635 best=0.11635

- [2026-10-21 18:10:06 UTC+8] residual seed=22 step=14700/15000 val_RMSE=0.12010 best=0.11635

- [2026-10-21 18:10:07 UTC+8] residual seed=22 step=14800/15000 val_RMSE=0.12141 best=0.11635

- [2026-10-21 18:10:07 UTC+8] residual seed=22 step=14900/15000 val_RMSE=0.13626 best=0.11635

- [2026-10-21 18:10:07 UTC+8] residual seed=22 step=15000/15000 val_RMSE=0.12957 best=0.11635

- [2026-10-21 18:10:07 UTC+8] 完成 residual seed=22，本轮耗时 24.6 s，选择验证最优 step=14600

- [2026-10-21 18:10:07 UTC+8] residual seed=33 step=100/15000 val_RMSE=0.27310 best=0.27310

- [2026-10-21 18:10:07 UTC+8] residual seed=33 step=200/15000 val_RMSE=0.27403 best=0.27310

- [2026-10-21 18:10:08 UTC+8] residual seed=33 step=300/15000 val_RMSE=0.25850 best=0.25850

- [2026-10-21 18:10:08 UTC+8] residual seed=33 step=400/15000 val_RMSE=0.25168 best=0.25168

- [2026-10-21 18:10:08 UTC+8] residual seed=33 step=500/15000 val_RMSE=0.24188 best=0.24188

- [2026-10-21 18:10:08 UTC+8] residual seed=33 step=600/15000 val_RMSE=0.24290 best=0.24188

- [2026-10-21 18:10:09 UTC+8] residual seed=33 step=700/15000 val_RMSE=0.24867 best=0.24188

- [2026-10-21 18:10:09 UTC+8] residual seed=33 step=800/15000 val_RMSE=0.23086 best=0.23086

- [2026-10-21 18:10:09 UTC+8] residual seed=33 step=900/15000 val_RMSE=0.22633 best=0.22633

- [2026-10-21 18:10:09 UTC+8] residual seed=33 step=1000/15000 val_RMSE=0.23471 best=0.22633

- [2026-10-21 18:10:09 UTC+8] residual seed=33 step=1100/15000 val_RMSE=0.21975 best=0.21975

- [2026-10-21 18:10:09 UTC+8] residual seed=33 step=1200/15000 val_RMSE=0.23479 best=0.21975

- [2026-10-21 18:10:10 UTC+8] residual seed=33 step=1300/15000 val_RMSE=0.19540 best=0.19540

- [2026-10-21 18:10:10 UTC+8] residual seed=33 step=1400/15000 val_RMSE=0.19216 best=0.19216

- [2026-10-21 18:10:10 UTC+8] residual seed=33 step=1500/15000 val_RMSE=0.19904 best=0.19216

- [2026-10-21 18:10:10 UTC+8] residual seed=33 step=1600/15000 val_RMSE=0.18752 best=0.18752

- [2026-10-21 18:10:10 UTC+8] residual seed=33 step=1700/15000 val_RMSE=0.17829 best=0.17829

- [2026-10-21 18:10:10 UTC+8] residual seed=33 step=1800/15000 val_RMSE=0.18395 best=0.17829

- [2026-10-21 18:10:11 UTC+8] residual seed=33 step=1900/15000 val_RMSE=0.17467 best=0.17467

- [2026-10-21 18:10:11 UTC+8] residual seed=33 step=2000/15000 val_RMSE=0.19013 best=0.17467

- [2026-10-21 18:10:11 UTC+8] residual seed=33 step=2100/15000 val_RMSE=0.17092 best=0.17092

- [2026-10-21 18:10:11 UTC+8] residual seed=33 step=2200/15000 val_RMSE=0.17940 best=0.17092

- [2026-10-21 18:10:11 UTC+8] residual seed=33 step=2300/15000 val_RMSE=0.18248 best=0.17092

- [2026-10-21 18:10:11 UTC+8] residual seed=33 step=2400/15000 val_RMSE=0.16459 best=0.16459

- [2026-10-21 18:10:11 UTC+8] residual seed=33 step=2500/15000 val_RMSE=0.19341 best=0.16459

- [2026-10-21 18:10:12 UTC+8] residual seed=33 step=2600/15000 val_RMSE=0.17443 best=0.16459

- [2026-10-21 18:10:12 UTC+8] residual seed=33 step=2700/15000 val_RMSE=0.17121 best=0.16459

- [2026-10-21 18:10:12 UTC+8] residual seed=33 step=2800/15000 val_RMSE=0.18920 best=0.16459

- [2026-10-21 18:10:12 UTC+8] residual seed=33 step=2900/15000 val_RMSE=0.16951 best=0.16459

- [2026-10-21 18:10:12 UTC+8] residual seed=33 step=3000/15000 val_RMSE=0.15539 best=0.15539

- [2026-10-21 18:10:12 UTC+8] residual seed=33 step=3100/15000 val_RMSE=0.15977 best=0.15539

- [2026-10-21 18:10:13 UTC+8] residual seed=33 step=3200/15000 val_RMSE=0.16537 best=0.15539

- [2026-10-21 18:10:13 UTC+8] residual seed=33 step=3300/15000 val_RMSE=0.15835 best=0.15539

- [2026-10-21 18:10:13 UTC+8] residual seed=33 step=3400/15000 val_RMSE=0.15412 best=0.15412

- [2026-10-21 18:10:13 UTC+8] residual seed=33 step=3500/15000 val_RMSE=0.15547 best=0.15412

- [2026-10-21 18:10:13 UTC+8] residual seed=33 step=3600/15000 val_RMSE=0.17498 best=0.15412

- [2026-10-21 18:10:13 UTC+8] residual seed=33 step=3700/15000 val_RMSE=0.16458 best=0.15412

- [2026-10-21 18:10:13 UTC+8] residual seed=33 step=3800/15000 val_RMSE=0.19243 best=0.15412

- [2026-10-21 18:10:14 UTC+8] residual seed=33 step=3900/15000 val_RMSE=0.15761 best=0.15412

- [2026-10-21 18:10:14 UTC+8] residual seed=33 step=4000/15000 val_RMSE=0.14527 best=0.14527

- [2026-10-21 18:10:14 UTC+8] residual seed=33 step=4100/15000 val_RMSE=0.16192 best=0.14527

- [2026-10-21 18:10:14 UTC+8] residual seed=33 step=4200/15000 val_RMSE=0.16045 best=0.14527

- [2026-10-21 18:10:14 UTC+8] residual seed=33 step=4300/15000 val_RMSE=0.14546 best=0.14527

- [2026-10-21 18:10:14 UTC+8] residual seed=33 step=4400/15000 val_RMSE=0.15711 best=0.14527

- [2026-10-21 18:10:15 UTC+8] residual seed=33 step=4500/15000 val_RMSE=0.16654 best=0.14527

- [2026-10-21 18:10:15 UTC+8] residual seed=33 step=4600/15000 val_RMSE=0.14692 best=0.14527

- [2026-10-21 18:10:15 UTC+8] residual seed=33 step=4700/15000 val_RMSE=0.16545 best=0.14527

- [2026-10-21 18:10:15 UTC+8] residual seed=33 step=4800/15000 val_RMSE=0.15091 best=0.14527

- [2026-10-21 18:10:15 UTC+8] residual seed=33 step=4900/15000 val_RMSE=0.17622 best=0.14527

- [2026-10-21 18:10:15 UTC+8] residual seed=33 step=5000/15000 val_RMSE=0.14739 best=0.14527

- [2026-10-21 18:10:16 UTC+8] residual seed=33 step=5100/15000 val_RMSE=0.15067 best=0.14527

- [2026-10-21 18:10:16 UTC+8] residual seed=33 step=5200/15000 val_RMSE=0.13949 best=0.13949

- [2026-10-21 18:10:16 UTC+8] residual seed=33 step=5300/15000 val_RMSE=0.15426 best=0.13949

- [2026-10-21 18:10:16 UTC+8] residual seed=33 step=5400/15000 val_RMSE=0.14752 best=0.13949

- [2026-10-21 18:10:16 UTC+8] residual seed=33 step=5500/15000 val_RMSE=0.14043 best=0.13949

- [2026-10-21 18:10:16 UTC+8] residual seed=33 step=5600/15000 val_RMSE=0.15987 best=0.13949

- [2026-10-21 18:10:16 UTC+8] residual seed=33 step=5700/15000 val_RMSE=0.15102 best=0.13949

- [2026-10-21 18:10:17 UTC+8] residual seed=33 step=5800/15000 val_RMSE=0.14955 best=0.13949

- [2026-10-21 18:10:17 UTC+8] residual seed=33 step=5900/15000 val_RMSE=0.16167 best=0.13949

- [2026-10-21 18:10:17 UTC+8] residual seed=33 step=6000/15000 val_RMSE=0.13872 best=0.13872

- [2026-10-21 18:10:17 UTC+8] residual seed=33 step=6100/15000 val_RMSE=0.16132 best=0.13872

- [2026-10-21 18:10:17 UTC+8] residual seed=33 step=6200/15000 val_RMSE=0.16049 best=0.13872

- [2026-10-21 18:10:17 UTC+8] residual seed=33 step=6300/15000 val_RMSE=0.16017 best=0.13872

- [2026-10-21 18:10:18 UTC+8] residual seed=33 step=6400/15000 val_RMSE=0.15516 best=0.13872

- [2026-10-21 18:10:18 UTC+8] residual seed=33 step=6500/15000 val_RMSE=0.16753 best=0.13872

- [2026-10-21 18:10:18 UTC+8] residual seed=33 step=6600/15000 val_RMSE=0.16253 best=0.13872

- [2026-10-21 18:10:18 UTC+8] residual seed=33 step=6700/15000 val_RMSE=0.13507 best=0.13507

- [2026-10-21 18:10:18 UTC+8] residual seed=33 step=6800/15000 val_RMSE=0.14632 best=0.13507

- [2026-10-21 18:10:18 UTC+8] residual seed=33 step=6900/15000 val_RMSE=0.12144 best=0.12144

- [2026-10-21 18:10:19 UTC+8] residual seed=33 step=7000/15000 val_RMSE=0.13716 best=0.12144

- [2026-10-21 18:10:19 UTC+8] residual seed=33 step=7100/15000 val_RMSE=0.13650 best=0.12144

- [2026-10-21 18:10:19 UTC+8] residual seed=33 step=7200/15000 val_RMSE=0.13851 best=0.12144

- [2026-10-21 18:10:19 UTC+8] residual seed=33 step=7300/15000 val_RMSE=0.13904 best=0.12144

- [2026-10-21 18:10:19 UTC+8] residual seed=33 step=7400/15000 val_RMSE=0.13463 best=0.12144

- [2026-10-21 18:10:19 UTC+8] residual seed=33 step=7500/15000 val_RMSE=0.14123 best=0.12144

- [2026-10-21 18:10:19 UTC+8] residual seed=33 step=7600/15000 val_RMSE=0.12900 best=0.12144

- [2026-10-21 18:10:20 UTC+8] residual seed=33 step=7700/15000 val_RMSE=0.16106 best=0.12144

- [2026-10-21 18:10:20 UTC+8] residual seed=33 step=7800/15000 val_RMSE=0.15020 best=0.12144

- [2026-10-21 18:10:20 UTC+8] residual seed=33 step=7900/15000 val_RMSE=0.14878 best=0.12144

- [2026-10-21 18:10:20 UTC+8] residual seed=33 step=8000/15000 val_RMSE=0.13050 best=0.12144

- [2026-10-21 18:10:20 UTC+8] residual seed=33 step=8100/15000 val_RMSE=0.13380 best=0.12144

- [2026-10-21 18:10:20 UTC+8] residual seed=33 step=8200/15000 val_RMSE=0.12894 best=0.12144

- [2026-10-21 18:10:21 UTC+8] residual seed=33 step=8300/15000 val_RMSE=0.14145 best=0.12144

- [2026-10-21 18:10:21 UTC+8] residual seed=33 step=8400/15000 val_RMSE=0.13272 best=0.12144

- [2026-10-21 18:10:21 UTC+8] residual seed=33 step=8500/15000 val_RMSE=0.13540 best=0.12144

- [2026-10-21 18:10:21 UTC+8] residual seed=33 step=8600/15000 val_RMSE=0.13557 best=0.12144

- [2026-10-21 18:10:21 UTC+8] residual seed=33 step=8700/15000 val_RMSE=0.14362 best=0.12144

- [2026-10-21 18:10:21 UTC+8] residual seed=33 step=8800/15000 val_RMSE=0.14010 best=0.12144

- [2026-10-21 18:10:22 UTC+8] residual seed=33 step=8900/15000 val_RMSE=0.13208 best=0.12144

- [2026-10-21 18:10:22 UTC+8] residual seed=33 step=9000/15000 val_RMSE=0.16036 best=0.12144

- [2026-10-21 18:10:22 UTC+8] residual seed=33 step=9100/15000 val_RMSE=0.12556 best=0.12144

- [2026-10-21 18:10:22 UTC+8] residual seed=33 step=9200/15000 val_RMSE=0.12734 best=0.12144

- [2026-10-21 18:10:22 UTC+8] residual seed=33 step=9300/15000 val_RMSE=0.13502 best=0.12144

- [2026-10-21 18:10:22 UTC+8] residual seed=33 step=9400/15000 val_RMSE=0.12557 best=0.12144

- [2026-10-21 18:10:22 UTC+8] residual seed=33 step=9500/15000 val_RMSE=0.14832 best=0.12144

- [2026-10-21 18:10:23 UTC+8] residual seed=33 step=9600/15000 val_RMSE=0.14216 best=0.12144

- [2026-10-21 18:10:23 UTC+8] residual seed=33 step=9700/15000 val_RMSE=0.12902 best=0.12144

- [2026-10-21 18:10:23 UTC+8] residual seed=33 step=9800/15000 val_RMSE=0.17443 best=0.12144

- [2026-10-21 18:10:23 UTC+8] residual seed=33 step=9900/15000 val_RMSE=0.12981 best=0.12144

- [2026-10-21 18:10:23 UTC+8] residual seed=33 step=10000/15000 val_RMSE=0.13887 best=0.12144

- [2026-10-21 18:10:23 UTC+8] residual seed=33 step=10100/15000 val_RMSE=0.14927 best=0.12144

- [2026-10-21 18:10:24 UTC+8] residual seed=33 step=10200/15000 val_RMSE=0.13676 best=0.12144

- [2026-10-21 18:10:24 UTC+8] residual seed=33 step=10300/15000 val_RMSE=0.13404 best=0.12144

- [2026-10-21 18:10:24 UTC+8] residual seed=33 step=10400/15000 val_RMSE=0.14356 best=0.12144

- [2026-10-21 18:10:24 UTC+8] residual seed=33 step=10500/15000 val_RMSE=0.12260 best=0.12144

- [2026-10-21 18:10:24 UTC+8] residual seed=33 step=10600/15000 val_RMSE=0.12732 best=0.12144

- [2026-10-21 18:10:24 UTC+8] residual seed=33 step=10700/15000 val_RMSE=0.13389 best=0.12144

- [2026-10-21 18:10:25 UTC+8] residual seed=33 step=10800/15000 val_RMSE=0.13252 best=0.12144

- [2026-10-21 18:10:25 UTC+8] residual seed=33 step=10900/15000 val_RMSE=0.13238 best=0.12144

- [2026-10-21 18:10:25 UTC+8] residual seed=33 step=11000/15000 val_RMSE=0.13759 best=0.12144

- [2026-10-21 18:10:25 UTC+8] residual seed=33 step=11100/15000 val_RMSE=0.15845 best=0.12144

- [2026-10-21 18:10:25 UTC+8] residual seed=33 step=11200/15000 val_RMSE=0.12183 best=0.12144

- [2026-10-21 18:10:25 UTC+8] residual seed=33 step=11300/15000 val_RMSE=0.13438 best=0.12144

- [2026-10-21 18:10:25 UTC+8] residual seed=33 step=11400/15000 val_RMSE=0.13560 best=0.12144

- [2026-10-21 18:10:26 UTC+8] residual seed=33 step=11500/15000 val_RMSE=0.13802 best=0.12144

- [2026-10-21 18:10:26 UTC+8] residual seed=33 step=11600/15000 val_RMSE=0.13747 best=0.12144

- [2026-10-21 18:10:26 UTC+8] residual seed=33 step=11700/15000 val_RMSE=0.14527 best=0.12144

- [2026-10-21 18:10:26 UTC+8] residual seed=33 step=11800/15000 val_RMSE=0.13774 best=0.12144

- [2026-10-21 18:10:26 UTC+8] residual seed=33 step=11900/15000 val_RMSE=0.13437 best=0.12144

- [2026-10-21 18:10:26 UTC+8] residual seed=33 step=12000/15000 val_RMSE=0.14314 best=0.12144

- [2026-10-21 18:10:27 UTC+8] residual seed=33 step=12100/15000 val_RMSE=0.13060 best=0.12144

- [2026-10-21 18:10:27 UTC+8] residual seed=33 step=12200/15000 val_RMSE=0.12428 best=0.12144

- [2026-10-21 18:10:27 UTC+8] residual seed=33 step=12300/15000 val_RMSE=0.12262 best=0.12144

- [2026-10-21 18:10:27 UTC+8] residual seed=33 step=12400/15000 val_RMSE=0.14206 best=0.12144

- [2026-10-21 18:10:27 UTC+8] residual seed=33 step=12500/15000 val_RMSE=0.13660 best=0.12144

- [2026-10-21 18:10:27 UTC+8] residual seed=33 step=12600/15000 val_RMSE=0.11724 best=0.11724

- [2026-10-21 18:10:27 UTC+8] residual seed=33 step=12700/15000 val_RMSE=0.12308 best=0.11724

- [2026-10-21 18:10:28 UTC+8] residual seed=33 step=12800/15000 val_RMSE=0.12523 best=0.11724

- [2026-10-21 18:10:28 UTC+8] residual seed=33 step=12900/15000 val_RMSE=0.13761 best=0.11724

- [2026-10-21 18:10:28 UTC+8] residual seed=33 step=13000/15000 val_RMSE=0.12224 best=0.11724

- [2026-10-21 18:10:28 UTC+8] residual seed=33 step=13100/15000 val_RMSE=0.13893 best=0.11724

- [2026-10-21 18:10:28 UTC+8] residual seed=33 step=13200/15000 val_RMSE=0.13181 best=0.11724

- [2026-10-21 18:10:28 UTC+8] residual seed=33 step=13300/15000 val_RMSE=0.11836 best=0.11724

- [2026-10-21 18:10:29 UTC+8] residual seed=33 step=13400/15000 val_RMSE=0.14421 best=0.11724

- [2026-10-21 18:10:29 UTC+8] residual seed=33 step=13500/15000 val_RMSE=0.12320 best=0.11724

- [2026-10-21 18:10:29 UTC+8] residual seed=33 step=13600/15000 val_RMSE=0.13005 best=0.11724

- [2026-10-21 18:10:29 UTC+8] residual seed=33 step=13700/15000 val_RMSE=0.13318 best=0.11724

- [2026-10-21 18:10:29 UTC+8] residual seed=33 step=13800/15000 val_RMSE=0.13529 best=0.11724

- [2026-10-21 18:10:29 UTC+8] residual seed=33 step=13900/15000 val_RMSE=0.11927 best=0.11724

- [2026-10-21 18:10:29 UTC+8] residual seed=33 step=14000/15000 val_RMSE=0.13110 best=0.11724

- [2026-10-21 18:10:30 UTC+8] residual seed=33 step=14100/15000 val_RMSE=0.12001 best=0.11724

- [2026-10-21 18:10:30 UTC+8] residual seed=33 step=14200/15000 val_RMSE=0.12352 best=0.11724

- [2026-10-21 18:10:30 UTC+8] residual seed=33 step=14300/15000 val_RMSE=0.15771 best=0.11724

- [2026-10-21 18:10:30 UTC+8] residual seed=33 step=14400/15000 val_RMSE=0.13151 best=0.11724

- [2026-10-21 18:10:30 UTC+8] residual seed=33 step=14500/15000 val_RMSE=0.12430 best=0.11724

- [2026-10-21 18:10:30 UTC+8] residual seed=33 step=14600/15000 val_RMSE=0.13039 best=0.11724

- [2026-10-21 18:10:31 UTC+8] residual seed=33 step=14700/15000 val_RMSE=0.12148 best=0.11724

- [2026-10-21 18:10:31 UTC+8] residual seed=33 step=14800/15000 val_RMSE=0.12615 best=0.11724

- [2026-10-21 18:10:31 UTC+8] residual seed=33 step=14900/15000 val_RMSE=0.14215 best=0.11724

- [2026-10-21 18:10:31 UTC+8] residual seed=33 step=15000/15000 val_RMSE=0.13039 best=0.11724

- [2026-10-21 18:10:31 UTC+8] 完成 residual seed=33，本轮耗时 24.0 s，选择验证最优 step=12600

- [2026-10-21 18:10:31 UTC+8] 单步实验评估 gaussian_low

- [2026-10-21 18:10:38 UTC+8] 单步实验评估 gaussian_mid

- [2026-10-21 18:10:44 UTC+8] 单步实验评估 gaussian_high

- [2026-10-21 18:10:50 UTC+8] 单步实验评估 student_ood

- [2026-10-21 18:10:57 UTC+8] 冻结权重闭环冲击测试完成 none

- [2026-10-21 18:10:57 UTC+8] 冻结权重闭环冲击测试完成 dob

- [2026-10-21 18:10:57 UTC+8] 冻结权重闭环冲击测试完成 kalman

- [2026-10-21 18:10:58 UTC+8] 冻结权重闭环冲击测试完成 single_fm

- [2026-10-21 18:10:59 UTC+8] 冻结权重闭环冲击测试完成 midpoint_fm

- [2026-10-21 18:10:59 UTC+8] 冻结权重闭环冲击测试完成 regression

- [2026-10-21 18:11:00 UTC+8] 冻结权重闭环冲击测试完成 residual

- [2026-10-21 18:11:00 UTC+8] 单步混合实验完成：E:\Desktop\MyCode\A2AFM\results\single_step_mixed\REPORT.md

- 2026-10-21: 单步混合实验完成：360条训练轨迹、136080窗口；4种网络各3种子、每模型15000次CPU更新。17项测试通过；12个检查点审计通过，公开接口778次估计/778次前向；报告与图表已核对。单步相对多步预测路径加速8.62倍，中噪声RMSE增大1.16%，直接回归更准确；闭环冲击跟踪性能仍需改进。文件锁恢复及训练计时缺失已记录。
