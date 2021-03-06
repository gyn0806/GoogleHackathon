import json
import sys
from utils import *
import random
from collections import defaultdict

class Splendor(object):
	def __init__(self, status):

		#####################################################
		self.benefit_weight = 0.7
		self.epoch_threshold = 3




		######################################################
		self.status = json.loads(status)
		self.benefit_sets = set()
		self.AllOperList = defaultdict(list)
		# self.AllOperList = {}
		self.moveOption= ['get_different_color_gems', "get_two_same_color_gems" , "reserve_card" , "purchase_card" ,  "noble", "purchase_reserved_card"]
	
	def checkNobleCardBenefit(self):
		nobel_benefit = {'red': 0, 'gold': 0, 'green': 0, 'blue': 0, 'white': 0, 'black': 0}
		for nobel_card in self.status['table']['nobles']:
			for item in nobel_card['requirements']:
				nobel_benefit[item['color']] += item['count']
		
		return nobel_benefit

	def checkDevCardBenefit(self):
		dev_benefit = {}
		for color in ['red', 'green', 'white', 'blue', 'black']:
			dev_benefit[color] = 0
		for card in self.status['table']['cards']:
			dev_benefit[card['color']]+=1
		return dev_benefit

	def checkDevCardBenefit_fix(self):
		dev_benefit = {}
		for color in ['red', 'green', 'white', 'blue', 'black']:
			dev_benefit[color] = 0
		for card in self.status['table']['cards']:
			dev_benefit[card['color']] += card['level']
		return dev_benefit

	def calc3BenefitType(self):

		nobel_benefit = self.checkNobleCardBenefit()
		# dev_benefit = self.checkDevCardBenefit()
		dev_benefit = self.checkDevCardBenefit_fix()

		benefit_union = {'red': 0, 'gold': 0, 'green': 0, 'blue': 0, 'white': 0, 'black': 0}
		for key in benefit_union:
			benefit_union[key] = nobel_benefit.get(key, 0) + dev_benefit.get(key, 0)

		sorted_benefit_union = sorted(benefit_union.items(), key = lambda c:c[1], reverse = True)
		for item in sorted_benefit_union[:3]:
			self.benefit_sets.add(item[0])

		return


		
	def checkDevCard(self,card_set):
		check_gem_init = {}
		for color in ['red', 'green', 'white', 'blue', 'black']:
			check_gem_init[color] = 0
		check_gem = check_gem_init
		for card in card_set:
		    check_gem[card['color']]+=1
		return check_gem

	def evaluateDevDistance(self, validDevSet, gemState):

		pass

	def checkNobleCard(self, move):
		if 'purchase_card' in move:
			player = self.status['playerName']
			my_table = None
			for i in self.status['players']:
				if i['name'] == player:
					my_table = i
			check_gem_init = {'red': 0, 'gold': 0, 'green': 0, 'blue': 0, 'white': 0, 'black': 0}
			check_gem = check_gem_init
			if 'purchased_cards' in my_table:
				for cards in my_table['purchased_cards']:
					check_gem[cards['color']] += 1

			for noble in self.status['table'].get('nobles'):
				flag=True
				for req in noble['requirements']:
					if req['count']>check_gem[req['color']]:
						flag=False
						break
				if flag:
					return {'noble':noble}
		return {}

	def evalAllOper(self):
		# operations = self.AllOperList
		# print(operations)
		def opr_to_key(opr):

			value = random.choice(range(100))
			
			return (value)
		
		# operations.sort(key = lambda opr:opr_to_key(opr), reverse = True)
		#for k, v in operations.items():
		#	return v[random.choice(range(len(v)))]
		# res = {"get_two_same_color_gems": "blue"}

		# index = random.choice(range(100))
		# return res
		index = self.status['round']
		res = self.chooseBuyDevOper()
		# open(str(index)+"#1.txt", "w").write("2")
		if not res:
			res = self.chooseBuyReservedOper()
			# open(str(index)+"#2.txt", "w").write("3")
		if not res:
			res = self.chooseGetGemsOper()
			# open(str(index)+"#3.txt", "w").write("4")
		# if not res:
		# 	res = self.chooseReservedCardOper()
		# 	open(str(index)+"#4.txt", "w").write("5")
		res_noble = self.checkNobleCard(res)
		if 'noble' in res_noble:
			res["noble"] = res_noble["noble"]
		return res


	def findDifferentColorGems(self):
		trueGems = []
		for gem in self.status["table"]["gems"]:
			if(gem.get("count",0)>=1):
				trueGems.append(gem)
		for i in range(0,len(trueGems)):
			for j in range(i,len(trueGems)):
				for k in range(j,len(trueGems)):
					dict_output_temp = {}
					differentColorGems = []
					differentColorGems.append(trueGems[i]["color"])
					differentColorGems.append(trueGems[j]["color"])
					differentColorGems.append(trueGems[k]["color"])
					dict_output_temp["get_different_color_gems"] = differentColorGems
					self.AllOperList["get_different_color_gems"].append(dict_output_temp)
		for i in range(0,len(trueGems)):
			for j in range(i,len(trueGems)):
				dict_output_temp = {}
				differentColorGems = []
				differentColorGems.append(trueGems[i]["color"])
				differentColorGems.append(trueGems[j]["color"])
				dict_output_temp["get_different_color_gems"] = differentColorGems
				self.AllOperList["get_different_color_gems"].append(dict_output_temp)
		for i in range(0,len(trueGems)):
			dict_output_temp = {}
			differentColorGems = []
			differentColorGems.append(trueGems[i]["color"])
			dict_output_temp["get_different_color_gems"] = differentColorGems
			self.AllOperList["get_different_color_gems"].append(dict_output_temp)
		return

	def findSameColorGems(self):
		trueGems = []
		for gem in self.status["table"]["gems"]:
			# print("gem:", gem)
			if(gem.get("count",0)>=4):
				# print("gems:", gem)
				trueGems.append(gem)
		
		for gem in trueGems:
			dict_output_temp = {}
			dict_output_temp["get_two_same_color_gems"] = gem["color"]
			self.AllOperList["get_two_same_color_gems"].append(dict_output_temp)
		# print(self.AllOperList)
		return

	def findReserveCard(self):
		#reserve card on table
		for card in self.status["table"]["cards"]:
			dict_output_temp = {}
			dict_temp = {}
			dict_temp["card"] = card
			dict_output_temp["reserve_card"] = dict_temp
			self.AllOperList["reserve_card"].append(dict_output_temp)
		#remove card from top
		# for level in range(1,4):
		# 	dict_output_temp = {}
		# 	dict_temp = {}
		# 	dict_temp["level"] = level
		# 	dict_output_temp["reserve_card"] = dict_temp
			# self.AllOperList["reserve_card"].append(dict_output_temp)

		# for gem in self.status["table"]["gems"]:
		# 	if(gem["color"]=="gold"):
		# 		return True
		# 	else:
		# 		return False
		return

	def findPurchaseCard(self):
		for card in self.status["table"]["cards"]:
			dict_output_temp = {}
			dict_output_temp["purchase_card"] = card
			# print(dict_output_temp)
			self.AllOperList["purchase_card"].append(dict_output_temp)
		# print(len(self.AllOperList["purchase_card"]))
		return 

	def findPurchaseReservedCard(self):
		playerName = self.status['playerName']
		my_reserved_cards = []
		for player in self.status['players']:
			if player['name'] == playerName:
				if 'reserved_cards' in player:
					my_reserved_cards = player['reserved_cards']
				break
		for card in my_reserved_cards:
			dic= {}
			dic["purchase_reserved_card"] = card
			self.AllOperList["purchase_reserved_card"].append(dic)
		return

	def findAllOper(self):
		self.calc3BenefitType()
		self.findPurchaseCard()
		self.findReserveCard()
		self.findPurchaseReservedCard()
		self.findDifferentColorGems()
		self.findSameColorGems()

		self.AllOperListFinal = defaultdict(list)
		for key, opers in self.AllOperList.items():
			# print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
			# if key == 'get_two_same_color_gems' or key == 'get_different_color_gems':
			# 	print(key,len(self.AllOperList[key]))
			# if key == 'purchase_card':
				# print(key, len(self.AllOperList[key]))
			# for k,v in self.AllOperList[key]:
				# self.AllOperList[key][k] = set(v)
			for oper in opers:
				# print(oper)
				# if key == 'get_two_same_color_gems' or key == 'get_different_color_gems':
				# 	print(key, checkMoveValid(self.status,oper))
				# print('~~~~~~~~~~~~~~~~~~~')
				if checkMoveValid(self.status,oper):
					# self.AllOperList[key].remove(oper)
					self.AllOperListFinal[key].append(oper)
				# print oper
				# exit(0)
			# if key == 'purchase_card':
				# print(key, len(self.AllOperListFinal[key]))
		self.AllOperList = self.AllOperListFinal
		# print(len(self.AllOperList['purchase_card']))

	# cal_round instead of gems
	def evalGemDistance(self,qualified_cards,dict_after_oper):
		distance = 0.0
		for card in qualified_cards:
			distance_tmp = 0.0
			for color_costs in card["costs"]:
				if color_costs['count']>dict_after_oper[color_costs['color']]:
					distance_tmp += color_costs['count'] - dict_after_oper[color_costs['color']]
			if card['color'] in self.benefit_sets:
				distance += (distance_tmp * self.benefit_weight)
			else:
				distance += (distance_tmp * (1.0 - self.benefit_weight))
		return distance

	# cal_round instead of gems
	def evalGemDistance_fix(self,qualified_cards,dict_after_oper):
		distance = 0.0
		for card in qualified_cards:
			color_distance = {}
			for color_costs in card["costs"]:
				if color_costs['count']>dict_after_oper[color_costs['color']]:
					color_distance[color_costs['color']] = color_costs['count'] - dict_after_oper[color_costs['color']]
			round_cou = 0
			for epoch in range(0,10):
				flag_cou = 0
				for key in color_distance:
					if color_distance[key] >= 1:
						flag_cou += 1
						if flag_cou <= 3 :
							color_distance[key] -= 1
				if flag_cou == 0:
					break
				else:
					round_cou += 1
			if card['color'] in self.benefit_sets:
				distance += (round_cou * self.benefit_weight)
			else:
				distance += (round_cou * (1.0 - self.benefit_weight))
		return distance

	def chooseGetGemsOper(self):
		allGetGemsOper = []
		for oper in self.AllOperList["get_two_same_color_gems"]:
			allGetGemsOper.append(oper)
		for oper in self.AllOperList["get_different_color_gems"]:
			allGetGemsOper.append(oper)
		qualified_cards = []
		for card in self.status["table"]["cards"]:
			card_list = []
			card_list.append(card)
			if self.calDevRound(card_list)[0]<=4 :
				qualified_cards.append(card)
		# open("valid-cards", "a+").write('\n'.join([jsons.dumps(i) for i in qualified_cards]))
		reserved_cards = []
		player_cur = {}
		for player in self.status["players"]:
			if player["name"]==self.status['playerName']:
				if 'reserved_cards' in player:
					reserved_cards = player.get("reserved_cards")
				player_cur = player
				break
		for card in reserved_cards:
			card_list = []
			card_list.append(card)
			if self.calDevRound(card_list)[0]<=4:
				qualified_cards.append(card)
		min_distance = 10000
		# open("debug_gems", "w").write(str(min_distance))
		min_oper = {}
		# open("all_gems", "w").write('\n'.join([json.dumps(i) for i in allGetGemsOper]))
		for oper in allGetGemsOper:
			#getDictAfterOper
			check_gem_init = {'red': 0, 'gold': 0, 'green': 0, 'blue': 0, 'white': 0, 'black': 0}
			dict_after_oper = check_gem_init
			if 'purchased_cards' in player_cur:
				for card in player_cur["purchased_cards"]:
					dict_after_oper[card['color']]+=1
			if 'gems' in player_cur:
				for gem in player_cur["gems"]:
					dict_after_oper[gem['color']] += gem['count']
			if "get_different_color_gems" in oper:
				color_list = oper["get_different_color_gems"]
				for color in color_list:
					dict_after_oper[color] += 1
			if "get_two_same_color_gems" in oper:
				color = oper["get_two_same_color_gems"]
				dict_after_oper[color] += 2
			# distance = self.evalGemDistance(qualified_cards,dict_after_oper)
			distance = self.evalGemDistance_fix(qualified_cards,dict_after_oper)
			if distance<min_distance:
				min_distance = distance
				min_oper = oper
			open("debug_gems", "w").write(json.dumps(min_oper) + '    '+str(distance))
		return min_oper



	def chooseBuyDevOper(self):
		opers = self.AllOperList['purchase_card'] # list
		if len(opers) == 0:
			return {}
		max_score = 0
		best_op = None
		max_score_in_3type = 0
		best_op_in_3type = None
		player_cur = {}
		for player in self.status["players"]:
			if player["name"]==self.status['playerName']:
				player_cur = player
				break
		p_card_len = len(player_cur.get('purchased_cards', []))
		# print(p_card_len)
		new_opers = []
		if p_card_len > 10:
			for oper in opers:
				op = oper['purchase_card']
				if op.get('score',0) > 0:
					new_opers.append(oper)
		else:
			new_opers = opers
		for oper in new_opers:
			op = oper['purchase_card']
			bene = op['color']
			if op.get('score', 0) >= max_score:
				max_score = op.get('score',0)
				best_op = oper
			if bene in self.benefit_sets:
				if op.get('score', 0) >= max_score_in_3type:
					max_score_in_3type = op.get('score', 0)
					best_op_in_3type = oper
		if max_score_in_3type > 0:
			return best_op_in_3type
		return best_op


	def chooseBuyReservedOper(self):
		opers = self.AllOperList['purchase_reserved_card'] # list
		if len(opers) == 0:
			return {}
		max_score = 0
		best_op = None
		max_score_in_3type = 0
		best_op_in_3type = None
		for oper in opers:
			op = oper['purchase_reserved_card']
			bene = op['color']
			if op.get('score', 0) >= max_score:
				max_score = op.get('score',0)
				best_op = oper
			if bene in self.benefit_sets:
				if op.get('score', 0) >= max_score_in_3type:
					max_score_in_3type = op.get('score', 0)
					best_op_in_3type = oper
		if max_score_in_3type > 0:
			return best_op_in_3type
		return best_op

	def calDevRound(self, cards):
		player = self.status['playerName']
		my_table = None
		for i in self.status['players']:
			if i['name'] == player:
				my_table = i
		check_gem_init = {'red': 0, 'gold': 0, 'green': 0, 'blue': 0, 'white': 0, 'black': 0}
		check_gem = check_gem_init
		if 'purchased_cards' in my_table:
			for cards in my_table['purchased_cards']:
				check_gem[cards['color']] += 1
		if 'gems' in my_table:
			for gems in my_table['gems']:
				check_gem[gems['color']] += gems['count']
		ret = []
		for card in cards:
			costs = []
			steps = 0
			for gems in card['costs']:
				if gems['count'] > 0:
					costs.append(max(gems['count'] - check_gem[gems['color']], 0))
			costs = np.array(costs)
			while sum(costs > 0) > 1:
				costs = -np.sort(-costs)
				for i in range(min(3, costs.shape[0])):
					if costs[i] == 0:
						break
					costs[i] -= 1
				steps += 1
			costs = -np.sort(-costs)
			steps += (costs[0] + 1) // 2
			ret.append(steps)
		return ret

	def chooseReservedCardOper(self):
		player = self.status['playerName']
		my_table = None
		for i in self.status['players']:
			if i['name'] == player:
				my_table = i
		check_gem_init = {'red': 0, 'gold': 0, 'green': 0, 'blue': 0, 'white': 0, 'black': 0}
		check_gem = check_gem_init
		if 'purchased_cards' in my_table:
			for cards in my_table['purchased_cards']:
				check_gem[cards['color']] += 1
		if 'gems' in my_table:
			for gems in my_table['gems']:
				check_gem[gems['color']] += gems['count']

		min_dist = 1000
		min_card = -1
		for card in self.AllOperList['reserve_card']:
			distance = 0
			for costs in card['reserve_card']['card']['costs']:
				if costs['count'] > check_gem[costs['color']]:
					distance += costs['count'] - check_gem[costs['color']]
			if distance < min_dist:
				min_dist = distance
				min_card = card
		if min_dist < 1000:
			return min_card
		else :
			return None

