# COVID-19 SIR Forecasting Model

Python으로 구현한 **SIR 전염병 예측 모델**입니다.  
전염병 확산 과정을 시뮬레이션하여 시간에 따른 **취약자(S), 감염자(I), 회복자(R)**의 변화를 시각화합니다.

---

## Overview

SIR 모델은 인구를 세 집단으로 나누어 감염 확산을 수학적으로 표현합니다.

- **S (Susceptible)** : 취약자
- **I (Infective)** : 감염자
- **R (Recovered)** : 회복자

### Differential Equations

dS/dt = -βSI
dI/dt = βSI - γI
dR/dt = γI


- **β** : 감염 효과율  
- **γ** : 회복률 (감염 기간의 역수)

### Basic Reproduction Number

R₀ = (βS) / γ


- R₀ > 1 → 감염자 수 증가  
- COVID-19 (Korea): R₀ ≈ 2 ~ 2.5

---

## Implementation

- 미분 방정식을 수치해석으로 계산
- 시간에 따른 S, I, R 변화를 그래프로 시각화

---

## Tech Stack

- Python
- numpy
- scipy
- matplotlib
- selenium
- beautifulsoup
- PyQt5

---

## Code

[https://github.com/lamiro3/covid_19_forecasting_model/blob/master/COVID_19_forecasting_model_SIR_003.py](https://github.com/lamiro3/Python/blob/main/covid_19_forecasting_model/COVID_19_forecasting_model_SIR_003.py)

---

## Future Work

- SEIR 모델로 확장
- 국가별 데이터 기반 예측 모델 구현
