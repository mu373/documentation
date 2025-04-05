---
title: Survival Function and Hazard Function | Survival Analysis
custom_title: Survival Function and Hazard Function
sidebar_label: Survival Function
sidebar_position: 1
---

## Introduction
This section introduces the most foundational element of the survival analysis, which are the **survival function** and the **hazard function**.

Simply put,
- **Survival function** $S(t)$ is the probability that an event occurs at some point after time $t$
- **Hazard function** $\lambda(t)$ is the probability that an event occurs in the next instant, given that it has not occurred up to time $t$

These functions are mathematically related, and knowing one allows us to derive the other. Let's check the definitions of each functions and their deriviations in the following section.

## Definitions

### Probability Density Function
$f(t)$ represents the **probability density of an event (e.g., death) occurring at the exact time $t$**. Note that this is different from the hazard function $\lambda(t)$.

### Distribution Function
The distribution function $F(t)$ represents the **probability that an event occurs before time $t$**. If we consider death as the event, the distribution function represents the probability of dying before time $t$.

$$
F(t) = P(T < t)
$$

### Survival Function
The survival function $S(t)$ is, in contrast to the distribution function, **the probability that an event does not occur by time $t$**. If we consider death as the event, the survival function represents the probability of surviving until time $t$.

$$
S(t) = P(T \geq t) = 1 - F(t)
$$

### Hazard Function
The hazard function $\lambda(t)$ can be thought of as a **conditional probability that an event occurs in a small interval between time $t$ and $t+h$, given survival up to time $t$**.

$$
\lambda(t) = \lim_{h \rightarrow 0} \frac{P(t \leq T < t + h \ | \ T \geq t)}{h}
\tag{1}
$$

When death is the event, the hazard function represents the probability (death rate, mortality) that a person who has survived until time $t$ will die in the next instant after $t$. Similarly, when disease onset is the event, the hazard function represents the incidence rate or morbidity at time $t$.

The reason why this is a conditional probability becomes clear when considering mortality at a specific age (e.g., age 40). For the event "death at age 40" to occur, the condition "being alive until age 40" must obviously be met.

The hazard function $\lambda(t)$ can be transformed using the definition of conditional probability:

$$
P(A|B) = \frac{P(A \cap B)}{P(B)} \tag{a}
$$

Following this definition (a), the hazard function can be expressed using the probability density function $f(t)$ and the survival function $S(t)$ at time $t$ as follows:

$$
\begin{align*}
   \lambda(t)
       &= \lim_{h \rightarrow 0} \frac{P(t \leq T \leq t + h) }{h} \frac{1}{P(T \geq t)} \\
       &= \lim_{h \rightarrow 0} \frac{F(t+h) - F(t)}{h} \frac{1}{S(t)} \\
       &= \frac{dF(t)}{dt} \frac{1}{S(t)} \\
       &= \frac{f(t)}{S(t)}
   \tag{2}
\end{align*}
$$

The hazard function $\lambda(t)$ can also be written in terms of $S(t)$. Since $f(t)$ can be transformed as:

$$
\begin{align*}
   f(t)
       &= \frac{dF(t)}{dt} \\
       &= \frac{d}{dt}\bigr( 1 - S(t) \bigl) \\
       &= -\frac{d}{dt}S(t)
\end{align*}
$$

We get:

$$
\begin{align}
   \lambda(t)
       &= \frac{f(t)}{S(t)} \\
       &= -\frac{dS(t)}{dt} \frac{1}{S(t)} \\
       &= -\frac{S'(t)}{S(t)} \\
       &= -\frac{d}{dt} \log {S(t)}
   \tag{3}
\end{align}
$$

By integrating equation (3) from time 0 to $t$, we can write it the other way around, expressing the survival function $S(t)$ in terms of the hazard function $\lambda(t)$.

$$
\begin{align*}
\int_0^t \bigg( -\frac{d}{du} \log {S(u)} \bigg) du &= \int_0^t \lambda(u) du \\
\bigg[- \log S(u) \bigg]_0^t &= \int_0^t \lambda(u) du \\
-\log S(t) + \log S(0) &= \int_0^t \lambda(u) du
\end{align*}
$$

Since the survival probability at time $t=0$ is 1, i.e., $S(0)=1$:

$$
\begin{align*}
-\log S(t) + \log 1 &= \int_0^t \lambda(u) du \\
\log S(t) &= - \int_0^t \lambda(u) du
\end{align*}
$$

Taking the exponential of both sides, we get:

$$
S(t) = \exp \bigg( - \int_0^t \lambda(u) du \bigg) \tag{4}
$$

### Cumulative Hazard Function
The cumulative hazard function $\Lambda(t)$ at time $t$ is the definite integral of the hazard function $\lambda(t)$ from time 0 to $t$, yielding the following relationship:

$$
\begin{align*}
\Lambda(t)
   &= \int_0^t \lambda(u) du \\
   &= - \log S(t)
\end{align*}
$$

Taking the exponential of both sides, the survival function $S(t)$ can also be expressed as follows, which is also derived from equation (4) of the hazard function:

$$
S(t) = \exp \big( - \Lambda(t) \big)
$$

<!-- 
## はじめに
生存関数とハザード関数を扱う。
- 生存関数$S(t)$: ある時点$t$以降のどこかでイベントが生じる確率
- ハザード関数$\lambda(t)$: ある時点$t$まではイベントが生じておらず、$t$のすぐ次の瞬間イベントが起こる確率

## 関係性
これらの関数は数学的に等価であり、一方ががわかれば他方も導くことができる。

## 定義

### 確率密度関数 $f(t)$
時点 $t$ の瞬時に、あるイベント(e.g. 死亡)が発生する確率密度を $f(t)$ として示す。後述するように、確率密度関数はハザード関数とは異なることに留意したい。

### 分布関数 $F(t)$
分布関数 $F(t)$ は、 $t$ 時点より前にイベントが発生する確率を示す。死亡をイベントとして考えるとすると、分布関数は時点 $t$ 以前に死亡する確率を表す。

$$
F(t) = P(T < t)
$$

### 生存関数
生存関数 survival function $S(t)$ は分布関数とは対照的に、時点 $t$ までイベントが起こらない確率を示す。死亡をイベントとして考えると、生存関数は時点 $t$ まで生き残る確率を示す。

$$
S(t) = P(T \geq t) = 1 - F(t)
$$

### ハザード関数
ハザード関数 hazard function $\lambda(t)$ は、時点 $t$ まで生存するという条件のもとで、イベントが時点 $t$ と $t+h$ の間の微小な期間に生じる[条件付き確率](#)として考えることができる。

$$
\lambda(t) = \lim_{h \rightarrow 0} \frac{P(t \leq T < t + h \ | \ T \geq t)}{h}
\tag{1}
$$

死亡をイベントとしたとき、ハザード関数は時点 $t$ まで生存していた人が $t$ を過ぎた次の瞬間に死亡する確率（時点 $t$ での死亡率 death rate, mortality）を示す。また疾患の発症をイベントとしたときには、ハザード関数は時点 $t$ での罹患率 incidence rate, morbidity を示す。


なぜ条件付き確率なのかについては、特定の年齢における死亡率（40歳死亡率など）を例に取って考えるとわかりやすい。「40歳で死亡する」というイベントが発生するためには、「40歳まで生きている」ことが条件となるのは明らかだろう。

ハザード関数 $\lambda(t)$ は、[条件付き確率の定義](#)によって変形することが可能である。

$$
P(A|B) = \frac{P(A \cap B)}{P(B)}
\tag{a}
$$

上記の定義(a)に従って変形すると、ハザード関数は、時点 $t$ における確率密度関数 $f(t)$ と生存関数 $S(t)$ を用いて、次のように表される。

$$
\begin{align*}
    \lambda(t)
        &= \lim_{h \rightarrow 0} \frac{P(t \leq T \leq t + h) }{h} \frac{1}{P(T \geq t)} \\
        &= \lim_{h \rightarrow 0} \frac{F(t+h) - F(t)}{h} \frac{1}{S(t)} \\
        &= \frac{dF(t)}{dt} \frac{1}{S(t)} \\
        &= \frac{f(t)}{S(t)}
    \tag{2}
\end{align*}
$$

また、ハザード関数は $S(t)$ の式としても書くことができる。 $f(t)$ は

$$
\begin{align*}
    f(t)
        &= \frac{dF(t)}{dt} \\
        &= \frac{d}{dt}\bigr( 1 - S(t) \bigl) \\
        &= -\frac{d}{dt}S(t)
\end{align*}
$$

のように変形できるので、

$$
\begin{align*}
    \lambda(t)
        &= \frac{f(t)}{S(t)} \\
        &= -\frac{dS(t)}{dt} \frac{1}{S(t)} \\
        &= -\frac{S'(t)}{S(t)} \\
        &= -\frac{d}{dt} \log {S(t)}
    \tag{3}
\end{align*}
$$

となる。

なお、式(3)を時点0から $t$ までの範囲で積分することによって、生存関数 $S(t)$ をハザード関数 $\lambda(t)$ を用いて示すことができる。

$$
\begin{align*}
\int_0^t \bigg( -\frac{d}{du} \log {S(u)} \bigg) du &= \int_0^t \lambda(u) du \\
\bigg[- \log S(u) \bigg]_0^t &= \int_0^t \lambda(u) du \\
-\log S(t) + \log S(0) &= \int_0^t \lambda(u) du
\end{align*}
$$

時点 $t=0$ において生存確率は1、つまり $S(0)=1$ であるから、

$$
\begin{align*}
-\log S(t) + \log 1 &= \int_0^t \lambda(u) du \\
\log S(t) &= - \int_0^t \lambda(u) du
\end{align*}
$$

両辺の指数を取ると

$$
\begin{align*}
S(t)
    & = \exp \bigg( - \int_0^t \lambda(u) du \bigg) \tag{4}
\end{align*}
$$

となる。



### 累積ハザード関数
時点 $t$ での累積ハザード関数は、ハザード関数を時点0から $t$ までの間の定積分であるので次の関係性が成り立つ。

$$
\begin{align*}
\Lambda(t)
    &= \int_0^t \lambda(u) du \\
    &= - \log S(t)
\end{align*}
$$

両辺について指数を取ると、生存関数 $S(t)$ は次のようにも表される。これはハザード関数の式(4)からも導かれる。

$$
\begin{align*}
S(t)
    &= \exp \big( - \Lambda(t) \big)
\end{align*}
$$ -->

## References
1. 大橋靖雄, 浜田知久馬, 魚住龍史. [生存時間解析](https://www.hanmoto.com/bd/isbn/9784130623223). 第2版, 東京大学出版会, 2022, 320p.
1. Germán Rodríguez. "7. Survival Models | Generalized Linear Models". Statistics and Population. https://grodri.github.io/glms/notes/c7s1, Retrieved 2022-12-01.
1. quossy. "生存時間解析にまつわる関数のおさらい". ねこすたっと. 2022-07-06. https://necostat.hatenablog.jp/entry/2022/07/06/080239, Retrieved 2022-12-01.
