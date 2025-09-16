# Table of Contents
```txt
computation/
├── unix/
│   ├── commands
│   ├── directory
│   ├── path
│   ├── shell
│   ├── user-and-group
│   ├── public-key
│   ├── ssh
│   ├── public-key
│   └── resource
├── hpc/
│   └── intro
│       ├── discovery
│       ├── module
│       ├── custom-module
│       ├── conda
│       ├── slurm
│       ├── jupyter
│       ├── vscode
│       └── vscode-jupyter
```

```txt
math/
├── foundations/                  # 数学的基礎
│   ├── probability-theory/       # 事象・条件付き確率・独立
│   ├── random-variables/         # 確率変数と期待値・変換
│   ├── stochastic-processes/     # マルコフ連鎖, ランダムウォーク, ポアソン過程
│   ├── mathematical-tools/       # 線形代数・微積分・最適化
│   └── index.md

├── distributions/                # 確率分布と標本分布
│   ├── discrete/                 # 二項分布・ポアソン分布など
│   ├── continuous/               # 正規分布・指数分布など
│   ├── multivariate/             # 多変量正規・共分散構造
│   ├── exponential-family/       # 一般化指数型分布族
│   ├── sampling-distributions/   # 標本分布, CLT, 漸近理論
│   └── index.md

├── statistical-inference/                    # 推定と検定
│   ├── estimation/               # 点推定・区間推定・MLE
│   ├── hypothesis-testing/       # 検定の考え方, 適合度検定
│   ├── estimation-vs-testing/    # 検定と推定の対応
│   │   ├── 01_pvalue_and_asa.ipynb
│   │   ├── 02_ci_vs_cri.ipynb
│   │   ├── 03_lrt_wald_score.ipynb
│   │   └── 04_critiques_alt.ipynb
│   ├── model-selection/          # AIC, BIC, WAIC, LOO
│   └── index.md

├── computational-methods/        # 計算統計学
│   ├── sampling/                 # MC, 重要サンプリング, Rejection
│   ├── mcmc/                     # Metropolis, Gibbs, HMC, 診断
│   ├── abc/                      # Approximate Bayesian Computation
│   ├── variational-inference/    # 平均場近似, ELBO
│   ├── em-algorithm/             # EM, mixtureモデル推定
│   ├── bootstrap/                # リサンプリング
│   └── index.md

├── modeling/                     # モデル化の構造
│   ├── principles/               # モデル化の思想, DGP, latent vs observed
│   ├── regression/               # 回帰 = モデル化の基本形
│   │   ├── linear/               # 線形回帰 (頻度論/ベイズ)
│   │   ├── glm/                  # 一般化線形モデル
│   │   └── hierarchical/         # 階層モデル・階層ベイズ
│   ├── latent-variable-models/   # 混合分布, 因子分析, HMM, LDA
│   ├── graphical-models/         # DAG, MRF, Factor Graphs
│   ├── dynamic-models/           # 時系列, 状態空間, ODE, SDE
│   ├── spatial-models/           # 地理空間データ, CAR/SAR, Gaussian Process
│   ├── bayesian-nonparametrics/  # DP, GP, IBP
│   ├── survival-and-event-history/ # 生存時間モデル, Cox, ハザード
│   ├── point-processes/          # 点過程 (Hawkes, Cox)
│   ├── robust-modeling/          # 外れ値, Heavy-tailed
│   └── mechanistic-and-agent-based/ # SIR, ABM

└── applications/                 # 応用ノート（ドメイン例）
    ├── regression/               # 実データでの回帰・GLM・階層ベイズ
    ├── multilevel-models/        # 集団データ・教育/医療
    ├── causal-inference/         # DAG, 交絡, 感度分析
    ├── missing-data/             # 欠測と測定誤差
    ├── survival/                 # 疫学・臨床データ
    ├── spatial/                  # 空間疫学
    └── index.md
```