# Codex 云环境运行验证（2026-10-16）

本目录记录一次真实执行的 CPU 小规模实验，并用于验证从 Codex 云环境向 GitHub 分支提交结果的流程。

## 实验来源与范围

- 源码提交：`8c25c7a8e09b2eaff8bef7864b90b7ee4b018836`；源码校验值见 `source_hashes.json`。
- 环境：Linux、Python 3.12.14、PyTorch 2.5.1+cpu、NumPy 2.2.6、SciPy 1.14.1、Matplotlib 3.9.2；未使用 GPU。
- 按 `requirements-lock.txt` 安装依赖，PyTorch 使用官方 CPU wheel。
- 随机种子 11；A2AFM、直接回归、FM-only 各训练 100 步；12 条训练轨迹、18 条验证轨迹，每个测试场景 4 条轨迹；2 个计算线程。
- 原始执行目录：`/workspace/a2atest-runs/cloud-validation`。本目录是其结果归档；配置中的相对路径 `results` 指原始执行目录下的输出目录。
- 本提交仅新增实验结果和说明，未修改应用代码、原有结果或依赖声明。

## 验证结果

- 开环与闭环单元测试共 9 项全部通过；提交前复测输出见 `tests.log`。
- 训练、四种噪声场景评估与积分步数检查完成，见 `status.json`、`REPORT.md` 和 `integration_check.json`。
- 中等高斯噪声场景：原始估计 RMSE 为 0.46836，A2AFM 为 0.25782，降低约 44.95%。该场景 EMA 为 0.23425，物理基线为 0.04259，均优于本次 A2AFM。
- 使用本次新训练的 A2AFM 检查点运行 `demo.py`：478 个有效估计点，RMSE 为 0.19447857587671444；前 23 个点为历史窗口预热，估计为 NaN。
- 这是环境与端到端流程验证，不能替代完整的 3000 步、多随机种子实验，也不用于证明模型收敛或方法优势。

## 文件说明

- `REPORT.md`、`metrics.*`、`trajectory_metrics.csv`：实验报告及分类、逐轨迹指标。
- `training.png`、`denoising.png`：训练与去噪图。
- `application.png`、`application.npz`：在线推理曲线与数据（t、truth、raw、estimate）。
- `*_seed11.pt`：按验证集选择的检查点；`*_last.pt`：包含优化器和随机数状态的末次检查点。
- `predictions_*.npz`：各噪声场景预测；`*_history.json`：训练历史。
- `config.json`、`environment.json`、`split_manifest.json`、`source_hashes.json`、`filter_params.json`：参数、环境、数据划分、源码摘要和滤波参数。
- `WORK_LOG.md`：本次训练实际产生的日志；`tests.log`：提交前单元测试输出。

## 在 Linux 中复现

从仓库根目录执行，要求 Python 3.12。使用独立输出目录，因为 `experiment.py` 会在源码旁追加 `WORK_LOG.md`。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu 'torch==2.5.1'
.venv/bin/python -m pip install --no-cache-dir -r requirements-lock.txt
.venv/bin/python -m pip --no-cache-dir check

repo_dir="$PWD"
run_dir=$(mktemp -d "${TMPDIR:-/tmp}/a2atest-validation.XXXXXX")
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2
export XDG_CACHE_HOME="$run_dir/.cache"
export MPLCONFIGDIR="$run_dir/.cache/matplotlib"
mkdir -p "$MPLCONFIGDIR"
.venv/bin/python -m unittest test_core closed_loop.test_core -v
cp -a a2afm experiment.py "$run_dir/"
(
  cd "$run_dir"
  "$repo_dir/.venv/bin/python" experiment.py --out results --steps 100 \
    --seeds 11 --train-trajectories 12 --test-trajectories 4 --threads 2 --ablation
)
.venv/bin/python demo.py --checkpoint "$run_dir/results/a2afm_seed11.pt" \
  --out "$run_dir/application.npz"
```

也可直接用本目录已保存的模型运行推理，将 `--checkpoint` 指向 `results/cloud-validation-20261016/a2afm_seed11.pt`，并将 `--out` 指向新的输出路径。不同硬件或库实现可能产生细微数值差异。
