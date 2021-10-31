import random

import numpy as np
from collections import defaultdict
from abc import abstractmethod

class QAgent:
	def __init__(self,):
		pass

	@abstractmethod
	def select_action(self, ob):
		pass

class MyAgent(QAgent):
	def __init__(self,args):
		self.action=[0,1,2,3]#上下左右
		self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
		#参数初始化
		self.discount_factor=args.discount_factor
		self.learning_rate= args.learning_rate
		pass
	def learn(self,state,action,reward,next_state):
		state = tuple(state)
		next_state=tuple(next_state)
		old_q=self.q_table[state][action]
		new_q=reward+self.discount_factor*np.max(self.q_table[next_state])
		#update Q'=Q+\alpha*[new_q-old_q]
		self.q_table[state][action]+=self.learning_rate*(new_q-old_q)
	def select_action(self, state):
		state=tuple(state)
		action_value=self.q_table[state] #获取当前状态下的动作-价值对
		max_action_list=[]
		max_value=action_value[0]#初始化
		for action,value in enumerate(action_value):
			if value>max_value:
				max_action_list.clear()
				max_value=value
				max_action_list.append(action)
			elif value==max_value:
				max_action_list.append(action)
		return random.choice(max_action_list)

