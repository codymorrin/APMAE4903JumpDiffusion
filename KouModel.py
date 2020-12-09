import numpy as np
import matplotlib.pyplot as plt





# inverse of the CDF of a double exponential random variable,
# takes arguments:
#	parameters of the distribution: p, eta1, eta2
def dExpInvCdf(p, eta1, eta2, s):
	q = 1 - p
	if s < q:
		return np.log(s / q) / eta2
	return -np.log((1 - s) / p) / eta1

rng = np.random.default_rng()




# iterating through the model,
# takes arguments:
#	time: n
#	time of next jump: next_jump
#	continuous (jumpless) part of previous value: sleft
#	previous value: s
# returns:
#	time of next jump,
#	continuous (jumpless) part of value,
#	value
def iter(n, next_jump, sleft, s):
	if s <= 0:
		return (np.Inf, 0, 0)
	random_part = sigma * rng.normal(scale=h)
	jump = 0
	if n >= next_jump:
		next_jump = rng.exponential(1 / nlambda)
		# this while makes r uniformly distributed on (0, 1), rather than [0, 1)
		while (r := rng.uniform()) == 0: pass
		jump += np.expm1(dExpInvCdf(p, eta1, eta2, r))

	determ_part = mu * h

	return (next_jump, s + sleft * (determ_part + random_part), s + sleft * (determ_part + random_part + jump))



# Black-Scholes equivalent of iter
# takes argument:
#	previous value: s
# returns:
#	value
def iterb(s):
	random_part = sigma * rng.normal(scale=h)
	determ_part = mu * h
	return s + s * (determ_part + random_part)





# simulate a process using iter
# takes arguments:
#	initial value: s0
# 	total time: n
# returns:
#	list of simulated values
def simulate(s0=1, n=20):

	sl = s0

	x = np.arange(0, n, h)
	y2 = [(rng.exponential(1 / nlambda), sl, s0)]
	for i in x:
		y2.append(iter(i, *y2[-1]))

	return [c for (a, b, c) in y2]


# Black-Scholes equivalent of simulate
# takes arguments:
#	initial value: s0
#	total time: n
# returns:
#	list of simulated values
def simulateb(s0=1, n=20):
	x = np.arange(0, n, h)
	y2 = [s0]
	for _ in x:
		y2.append(iterb(y2[-1]))

	return y2




# plotting section




fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(16,9))



# calculating returns:

h = 0.14 # discrete time interval

mu = 0.01 # drift term

sigma = 0.9 # Brownian stdev term

nlambda = 0.15 # jump frequency

p = 0.5 # jump 'skewness'
q = 1 - p
eta1 = 1.5 # inverse of mean upward jump
eta2 = 1.5 # inverse of mean downward jump

rets = [] # returns in the Kou model
retsb = [] # returns in the Black-Scholes model
for _ in range(1000):
	s = simulate()
	sb = simulateb()
	if s[-15] != 0:
		rets.append((s[-1] - s[-15]) / s[-15])
	if sb[-15] != 0:
		retsb.append((sb[-1] - sb[-15]) / sb[-15])

ax1.hist([rets, retsb], bins=np.linspace(-2, 2, 20), label=["jump-diffusion", "Black-Scholes"])
ax1.set_title("Returns")
ax1.legend()






# simulating process:

h = 0.01

mu = 0.01

sigma = 0.9

nlambda = 0.17

p = 0.5
q = 1 - p
eta1 = 10
eta2 = 10

sims = [] # list of Kou model simulations
simsb = [] # list of Black-Scholes model simulations
for _ in range(1000):
	sims.append(simulate())
	simsb.append(simulateb())

for i in range(5):
	ax2.plot(sims[i])
	ax3.plot(simsb[i])
ax2.set_title("jump-diffusion trajectory")
ax3.set_title("Black-Scholes trajectory")
plt.show()
