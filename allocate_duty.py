import numpy as np
np.random.seed(826)

"""
evenly allocate duty to a team size of m

consideration:
member allocated to a weekday duty will not be allocated to a weekend duty for that weekday
max weekday duty per week = 3
max weekend duty per week = 1
weekday slot per week = 5 (Mo, Tu, We, Th, Fr)
cost per each weekday slot = 12
weekday slot per week = 6 (Sa1, Sa2, Sa3, Su1, Su2, Su3)
cost per each weekend slot = 4

track: member allocation to weekend and weekday duties and the associated cost

minimize = total costs

"""

# SETTINGS

# Team size
m = 8

# Number of Weekly Schedule
# n = 4 for a 1-month schedule
n = 12

# Weekday slots
wkday_slot = 5
wkend_slot = 6

# Duty costs
c_wkday = 12
c_wkend = 4

# Costs array
def cost_array(wkday_slot = 5, wkend_slot = 6, c_wkday = 12, c_wkend = 4):
	"""
	Create a (1 by wkday_slot+wkend+slot) array, with allocated costs.
	"""
	wkday = np.zeros(wkday_slot) + c_wkday
	wkend = np.zeros(wkend_slot) + c_wkend
	return wkday, wkend
	
# RMSE

def rmse(arry):
	# error
	e = arry - np.mean(arry)
	# square-error
	s = e**2
	# mean
	m = np.mean(s)
	return np.sqrt(m)
		
# Generating schedule
def generate_schedule(m=8, wkday_slot=5, wkend_slot=6):
	"""
	Create a (m X wkday_slot) and a (m X wkend_slot) array
	"""
	wkday_schd = np.zeros((m, wkday_slot))
	wkend_schd = np.zeros((m, wkend_slot))
	return wkday_schd, wkend_schd
	
def join_array(a, b, axis=0):
	# General tool to join arrays by rows by default
	return np.concatenate((a, b), axis=axis)

# Choose weekday and weekend personnel
def choose_duty_p(m=8, wkday_slot=5, wkend_slot=6):
	# Genereate indices
	m_idx = np.arange(m)
	
	# Choose weekend duty personnel
	wkend_duty_p = list(np.random.choice(m_idx, wkend_slot, replace=False))
	
	# Weekday personnel duty pool
	# Remaning m_idx not in wkend_duty_p. Weekday duty personnel will be chosen here.
	wkday_duty_idx = [i for i in m_idx if i not in wkend_duty_p]
	
	wkday_duty_p = list(np.random.choice(wkday_duty_idx, wkday_slot, replace=True))
	
	return wkday_duty_p, wkend_duty_p
	
def check_duty_p(wkday_duty_p, wkend_duty_p, prev_wkday_p):
	"""
	Require that weekday duty personnel be only selected once a week. 
	If selected, replace it with weekend personnel
	*Should not be required if optimization works
	"""
	return None
	
# Allocate duty
def allocate_duty(wkday_duty_p, wkend_duty_p, wkday_schd, wkend_schd):
	
	# Allocate weekday duty
	row1, col1 = wkday_schd.shape
	for c,p in zip(range(col1) , wkday_duty_p):
		wkday_schd[p][c] = 1
	
	# Allocate weekend duty
	row2, col2 = wkend_schd.shape
	for c, p in zip(range(col2), wkend_duty_p):
			wkend_schd[p][c] = 1
	
	prev_wkday_p = wkday_duty_p
	
	# Return allocated schedules
	return wkday_schd, wkend_schd, prev_wkday_p

def optimize_schd(m = 8, wkday_slot = 5, wkend_slot = 6, numtrials=500, prev_opt_cost = np.zeros(m)):
	cost_wkday, cost_wkend = cost_array(wkday_slot = wkday_slot, wkend_slot = wkend_slot, c_wkday = c_wkday, c_wkend = c_wkend)
	
	# Join the cost arrays
	cost = np.concatenate((cost_wkday, cost_wkend), axis=0)
	# print(cost)
	
	# For tracking
	# min_rmse = 100 + rmse(prev_opt_cost)
	min_rmse = 100

	# For iteration
	for trial in range(numtrials):
		if min_rmse == 0:
			break
		
		# Generate fresh schedule
		wkday_schd, wkend_schd = generate_schedule(m=m, wkday_slot=wkday_slot, wkend_slot=wkend_slot)
		
		wkday_duty_p, wkend_duty_p = choose_duty_p(m=m, wkday_slot=wkday_slot, wkend_slot=wkend_slot)
		wkday_schd_a, wkend_schd_a, prev_wkday_p = allocate_duty(wkday_duty_p, wkend_duty_p, wkday_schd, wkend_schd)
		
		# # Join the schedule, then calculate the cost
		
		schd_t = np.concatenate((wkday_schd_a, wkend_schd_a), axis=1)
		m_cost = np.dot(schd_t, cost)
		m_cost += prev_opt_cost
		rmse_t = rmse(m_cost)
		
		# print(trial, rmse_t)
		
		if rmse_t < min_rmse:
			min_rmse = rmse_t
			opt_m_cost = m_cost
			opt_schd = schd_t
	
	# Debug: Print minimum RMSE
	print(min_rmse)
	
	# return opt_wkday_schd, opt_wkend_schd
	return opt_schd, opt_m_cost
	
def generate_n_schedule(n=2, m=8, wkday_slot=5, wkend_slot=6, numtrials=1000, prev_opt_cost = np.zeros(m)):
	"""
	Generates n weeks of schedule
	"""
	# initialize
	m_cost = np.zeros(m)
	m_schd = np.zeros(wkday_slot + wkend_slot)
	n_opt_schd = []
	for i in range(n):
		np.random.seed(i)
		opt_schd, m_cost = optimize_schd(m, wkday_slot, wkend_slot, numtrials, prev_opt_cost = m_cost)
		n_opt_schd.append(opt_schd)

		# Overall Allocation
		m_schd = np.add(m_schd, opt_schd)
	
	
	return np.concatenate(n_opt_schd, axis=0), m_cost, m_schd

# TESTING

opt_sch, m_cost, m_schedule = generate_n_schedule(m=m, n=n)

print(m_schedule)
print(m_cost)
print(opt_sch)


# PLOTTING

# import matplotlib.pyplot as plt
# y, x = opt_sch.shape
# fig, ax = plt.subplots()
# im = ax.imshow(opt_sch, cmap='gray_r')
# ax.set_xticks(np.arange(x))
# ax.set_xticklabels('Mo,Tu,We,Th,Fr,Sa1,Sa2,Sa3,Su1,Su2,Su3'.split(','))
# ax.set_yticks(np.arange(y))
# plt.setp(ax.get_xticklabels(), rotation=45, ha='center', rotation_mode="anchor")
# plt.setp(ax.get_yticklabels(), ha='center', rotation_mode="anchor")
# fig.tight_layout()
# plt.show()