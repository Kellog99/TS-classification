# TS-classification

## Cloud-Point

### Definition (Dynamic Time Warping)
Let $S_1=\{x_i\}_{i\in I}, S_2=\{x'_j\}_{j\in J}$ be two sequences of elements in $\mathbb{R}^d$, and let $\mathcal{A}(S_1,S_2)$ be the set of all path alignments between $I$ and $J$. The DTW of $S_1$ and $S_2$ is defined as:
\[DTW_q(S_1,S_2) = \min_{\pi \in \mathcal{A}(S_1,S_2)} \left(\sum_{(i,j)\in \pi}\|x_i-x'_j\|_{l^q}^q\right)^{\frac{1}{q}}\]

It is possible to dynamically program $\mathcal{A}(S_1, S_2)$ using the recursion:
\[D(n,m) = \begin{cases}
    0 & m < 0 \vee n < 0\\
    1 & m = 0 \vee n = 0\\
    D(n-1,m) + D(n-1,m-1) + D(n,m-1) & \text{otherwise}
\end{cases}\]

### Takens' Embedding Theorem
Let $M$ be an $m$-dimensional manifold, $\phi \in Diff(C^2(M))$, and $y \in C^2(M,\mathbb{R})$. Then the map $\Phi_{(\phi,y)}: M \to \mathbb{R}^{2m+1}$ defined by:
\[\Phi_{(\phi,y)}(x) = \left(y(x),y(\phi(x)),\ldots,y\left(\phi^{2m}\right)\right)\]
is an embedding.

### Definition (Embedding)
An injective continuous map $f: X\to Y$ between topological spaces $X$ and $Y$ is a topological embedding if $f$ yields a homeomorphism between $X$ and $f(X)$.

### Definition (Diffeomorphism)
$f: M \rightarrow N$ is a diffeomorphism ($f\in Diff(C^0(M))$) if:
- $f$ is a differentiable bijection.
- $M,N$ are two manifolds.
- $f^{-1}$ is smooth.

### Definition (Manifold)
$M \subset R^d$ is a $d$-dimensional manifold if there exist $\{(W_i , h_i )\}_{i\in I}$ such that:
- $\{W_i\}_{i\in I}$ is a cover of $M$, i.e., $M = \bigcup_i W_i$.
- $\forall i\in I, h_i : W_i \to U_i \subset R^d$ is a diffeomorphism (coordinate map).
- $\forall j,i\in I, h_j \circ h^{-1}_i : U_i \to U_j$ is smooth.

From the previous definition, it is possible to see that:
- $M=(0,1)$ is a 1-dimensional manifold.
- Without loss of generality, consider every time series $y:(0,1)\to\mathbb{R}$.
- The function $\phi(t)=t-\tau,\ \tau\in \mathbb{R}$ is such that $\phi\in Diff(C^\infty(\mathbb{R}))$, so $\phi\in Diff(C^2((0,1)))$.
  - This implies that \[\left\{(y(t),y(t-\tau),y(t-2\tau))\mid t\in (2\tau, 1),\ \tau \in (0,0.5)\right\}\] is an embedding of the time series $y(t)$.

## Simplicial Complex

### Definition (Simplex)
A point $x \in \mathbb{R}^d$ is a convex combination of the points in $S$ if it is an affine combination with non-negative coefficients. The convex hull of $S$ is the set of all convex combinations of $S$:
\[conv(S) = \left\{\sum_{i=0}^k\lambda_iu_i \mid \sum_{i=0}^k\lambda_i=1,\ \lambda\geq 0\right\}\]
A $k$-simplex is the convex hull of $k + 1$ linearly independent points in $\mathbb{R}^d$, and it has dimension $k$.

### Definition (Simplicial Complex)
A simplicial complex $K$ is a finite collection of simplices such that:
- If $\sigma\in K$ and $\tau\leq\sigma$, then $\tau\in K$.
- If $\sigma_1,\sigma_2\in K$, then $\sigma_1\cap\sigma_2\in K$.

### Definition (Vietoris-Rips (VR) Complexes)
Let $S$ be a set of points in $R^d$. The Vietoris-Rips complex of $S$ with radius $r$ is the collection of subsets of $S$ of diameter at most $2r$:
\[VR_r (S) = \{\sigma\subset S \mid \text{diam}(\sigma) \leq 2r\}\]

![VR Complex](immagini/vr_complex.jpg)

### Definition (Witness Complex)
Let $L,Z$ be two cloud points such that $L\subset Z$ and $n=|L|, N=|Z|$. Let $D$ be an $n\times N$ matrix of non-negative entries regarded as the matrix of distances between the points in $L$ and $Z$. The (strict) witness complex $W_\infty(D)$ with vertices $\{1,\cdots,n\}$ is defined as:
\[\sigma:=[a_0,\cdots,a_p]\in W_\infty(D) \iff \exists i\in \{1,\cdots,N\}|D(a_j,i)\leq D(b,i), \forall b\in \{1,\cdots,N\}\setminus\{a_1,\cdots,a_n\}\]

![Witness Complex](immagini/wc.png)

### Definition (p-chain)
Let $K$ be a simplicial complex and $A$ an abelian group. A $p$-chain is a formal sum of $p$-dimensional faces of $K$, i.e.,
\[C_p(K) = \left\{\sum_{\sigma\in F_p(K)}a_\sigma\sigma \mid a_\sigma \in A\right\}\]

### Definitions (p-cycle, p-boundary, p-th homology group)
Let $K$ be a simplex. A $p$-cycle $Z_p(K)$ is a chain with an empty boundary:
\[Z_p(K) = \left\{\sigma\in Ker(\partial_p(C_p(K)))\right\}\]
A $p$-boundary $B_p(K)$ is a chain that is a boundary of a $(p+1)$-chain:
\[B_p(K) = \left\{\sigma\in C_p(K) \mid \exists\sigma'\in C_{p+1}(K), \partial_{p+1}\sigma'=\sigma\right\}\]

Since $Z_p(K)\supset B_p(K)$, the following definition has meaning.

### Definition (p-th Homology Group)
Let $K$ be a simplicial complex. The $p$-th homology group is:
\[H_p(K) = \frac{Z_p(K)}{B_p(K)}\]
and $\beta_p(K) = \text{rank}\left(H_p(K)\right)$ is the $p$-th Betti number.

![Homology Groups](immagini/bn.png)

### Definition (Filtration)
A filtration $\mathcal {F}$ is an indexed family $\{S_{i}\}_{i\in I}$ of sub-objects of a given algebraic structure $S$ such that $S_{i}\subseteq S_{j}$ for all $i,j\in I, i\leq j$.

Let $K$ be a simplicial complex, and let $f: K\to \mathbb{R}$ be a monotonic function. The induced filtration of $K$ is $\{K_i\}_{i=0}^n$ where $K_0=\phi, K_n= K$, and:
\[a_i = \min\left\{r\mid K_i=f^{-1}((-\infty,r])\right.\}\]

By construction, $\forall i\leq j, K_i\subset K_j$, so it is possible to define $f_p^{i,j}:H_p(K_i)\to H_p(K_j)$ where $f_p^{i,j}$ is the induced map.

### Definition (p-th Persistent Homology)
The $p$-th persistent homology groups are the images of the homomorphism induced by inclusion, so:
\[H^{i,j}_p(K) = \text{imm } f_p^{i,j}\]

The ranks of these groups are the $p$-th persistence Betti numbers:
\[\beta_p^{i,j} = \text{rank}\left(H_p^{i,j}(K)\right)\]

### Definition (Life-and-Death)
Given the $p$-th homology group $H_p(K_i)$ and $\gamma\in H_p(K_i)$:
- $\gamma$ is born at $K_i$ if $\gamma\notin H_p^{i-1,i}$.
- $\gamma$ dies in $K_j$ if it merges with an older class as we go from $K_{j-1}$ to $K_j$.

Moreover, consider $a_i, a_j$, previously defined. Then the persistence of $\gamma$ is:
\[pers(\gamma) = a_j - a_i\]
and $(a_j,a_i)$ is called the persistent pair.

## Features
1. The number of elements in each dimension.
2. Maximum holes lifetime in each dimension.
3. Average lifetime in dimension.
4. Sum of all lifetime (represents the integral on the PD graph).
5. Betti numbers.

## Classifier

### Definition (Neural Network (NN))
A neural network $\mathcal{N}$ is a sequence $(D_0,D_1,\cdots, D_L, W^1, \theta^1, W^2, \theta^2, \cdots, W^L, \theta^L)$ where:
- $L\in \mathbb{N}\setminus\{0\}$ represents the depth of $\mathcal{N}$.
- $(D^0,\cdots,D^L)\in\mathbb{N}^{L+1}$ is the layout of the network, where $D_0$ is the number of features of the input and $D_L$ is the number of features of the output.
- $W^l=\left(W^l_{j,k}\right)\in\mathbb{R}^{D_l\times D_{l-1}}$ are matrices whose entries are the network's weights, and $j$ is referred to the $j$-th node in the $D^l$ layer while $k$ to the $k$-th node of the $D^{l-1}$ layer.
- $(\theta^l)=\left(\theta^l_j\right)\in \mathbb{R}^{D_l}$, where $l\in \{1,\cdots,L\}$, is called the bias.

### Definition (Forward Propagation)
Given a neural network $\mathcal{N}$ and $\rho=\{\rho_i\}_{i=1}^L$ (the set of activation functions associated with each level of $\mathcal{N}$. The function defined by $\mathcal{N}$ equipped with $\rho$ is defined as 
\begin{align*}
<\mathcal{N}>^\rho:\mathbb{R}^{D_0}&\to\mathbb{R}^{D_L}\\
x&\mapsto<\mathcal{N}>^\rho(x)=y^{[L]}
\end{align*}
where
$$
\begin{cases}
y^{[0]}(x)=0\\
y^{[l]}(x)=\rho^l\left(W^l y^{[l-1]}(x)+\theta^l\right) & l\in \{1,\cdots,L\}
\end{cases}
$$
and this system defines forward propagation.

