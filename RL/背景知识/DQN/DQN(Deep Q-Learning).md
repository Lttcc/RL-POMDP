# DQN(Deep Q-Learning)

## 动机背景

普通Q-Learning算法中维护(状态，动作)的价值表格(Q-Table)，当状态/动作空间较大时，或处在连续空间时**，表格会非常大，此时针对所有的(S,A)对去计算价值会导致成本非常的高。**

一个直觉上的想法是：**不再针对每个(S,A)计算Q值，而是直接拟合/估计一个完整的Q值函数。**即让相近的状态能得到相近的输出动作，通过更新参数$\theta$的方式，使得Q函数逼近最优$Q^*$函数:
$$
Q(s,a;\theta)\approx Q^*(s,a)
$$
而拟合函数这种问题非常适合使用深度神经网络来做，因此可以结合深度学习DL和强化学习RL来解决这个问题，DQN就是结合了深度神经网络+Q-Learning形成的深度强化学习算法(DRL)。

## 关键问题

我们已经在直觉上提出了深度神经网络+Q-Learning的方式，但这种结合并不是简单的就可以做到，而是会产生一些问题：

1. 深度神经网络的训练往往需要大量的带标签数据，而RL只有一个episode完成后的reward，而且reward往往是稀疏、带噪声的，因此如何给网络提供大量的带标签数据？
2. 据过往研究表明使用非线性网络拟合值函数会产生不稳定的情况，如何解决这种不稳定性？
3. 深度学习往往假设数据样本是独立同分布的，而在强化学习中状态序列具有高度的相关性；不仅如此，深度学习往往假设潜在的数据分布是固定的，而在RL中，数据分布会随着Agent学习新行为而发现变化(例如：Agent玩同个游戏的不同关卡)

## 核心组件

1. ##### Q-Learning+随机梯度下降。(针对问题1)

   DQN使用权重为$\theta$深度神经网络拟合Q函数，损失函数定义如下：
   $$
   L_{i}\left(\theta_{i}\right)=\mathbb{E}_{s, a \sim \rho(\cdot)}\left[\left(y_{i}-Q\left(s, a ; \theta_{i}\right)\right)^{2}\right]
   $$
   其中$i$​为迭代论述，$\theta_i$​为第i轮我们需要更新的权重，$\rho(s,a)$​定义了状态动作分布，其中：
   $$
   y_i=R+\gamma \max_aQ(s',a';\theta_{i-1})
   $$
   与Q-Learning对比：
   $$
   Q(S,A)=Q(S,A)+\alpha(R+\gamma\max_a Q(S',a)-Q(S,A))
   $$
   可以发现，DQN与Q-Learning的思路相同，都是希望Q函数的估计，能够逼近目标Q函数：
   $$
   Q_{target}=R+\gamma \max_aQ_{evaluate}(s',a';\theta)
   $$
   因此可以理解为在DQN中，$Q_{target}$作为样本的标签值，目标是训练网络使得Q函数的估计与$Q_{target}$的平方误差最小。

2. ##### 经验重放：replay memory(针对问题3)

   DQN使用**经验重放**的机制来缓解数据之间的相关性和分布的非静态性，它随机采样先前的转换，从而平滑许多过去行为的训练分布。

   DQN会把每个时间步Agent的经验$e_t=(s_t,a_t,r_t,s_{t+1})$​​​存储到replay memory $D=e_1,...,$$e_N$中。当需要对网络进行更新时，DQN会从D中随机采样一个minibatch的数据集E，并在E上进行随机梯度下降来优化网络参数$\theta$​​，**如果不这么做，Agent产生的序列数据会被按顺序输入到网络中，而这些样本具有很强的前后相关性，因此这样做可以打乱了网络输入样本的相关性，而且由于数据可以被重复采样来进行梯度更新，因此也提高了数据的利用效率。**可以把经验重放机制简单理解为一个数据缓存区，用来打乱数据顺序和对数据进行重复采样。

3. ##### 目标神经网络：Target Network(针对问题2)

   在2013年的DQN版本中，$Q_{target}$​​​的计算由$\eqref{3}$​​​式决定，即$：Q_{target}$​​​和$Q_{evaluate}$​​​共用同一个神经网络，且$Q_{target}$​​​使用的参数为上一时刻参数$\theta_{i-1}$​​​，每一时刻都会对$Q_{target}$​​进行更新。

   值得注意的是：**对$Q$函数的微小更新可能会显著的改变策略，从而改变数据分布，进而影响$Q_{target}$​和$Q_{evaluate}$​的相关性，且两者均由相同的网络拟合，会产生数据之间的耦合性。**

   因此在2015年的版本中，作者分别使用两个CNN来拟合$Q_{target}$和$Q_{evaluate}$​，从而降低它们之间的耦合性，同时为了避免$Q_{target}$网络与$Q_{evaluate}$网络参数相同带来的关联性，$Q_{target}$​网络参数只有在执行$C$步之后才会与$Q_{evaluate}$网络参数同步，进而再次对数据解耦，$Q_{target}$表示如下：
   $$
   Q_{target}=R+\gamma \max_aQ(s',a';\theta^-_i)
   $$

## 伪代码

<h3><center>2013年版本</center>

![image-20211102170500632](DQN(Deep Q-Learning).assets/image-20211102170500632.png)

<h3><center>2015年版本</center>

![image-20211102170551889](DQN(Deep Q-Learning).assets/image-20211102170551889.png)

## 参考：

1.[深度强化学习-DQN](https://blog.csdn.net/u013236946/article/details/72871858)

2.[DQN2015版本论文](http://www.kreimanlab.com/academia/classes/BAI/pdfs/MnihEtAlHassibis15NatureControlDeepRL.pdf)

3.[DQN2013版本论文](https://arxiv.org/pdf/1312.5602.pdf)