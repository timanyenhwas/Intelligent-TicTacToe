class Player45:
	
	def __init__(self):
		self.heuristicValues = {}
		self.boardscore = 0
		self.temp = []
		self.testscr=0
		self.heuristicValues['o']=[[0,-10,-100,-1000,-10000],[10,0,50,5000,0],[100,-50,0,0,0],[1000,-5000,0,0,0],[10000,0,0,0,0]]
		self.oord = 'o'
		self.xord = 'x'
		self.dcrd = 'd'
		self.heuristicValues['x']=[[0,-10,-100,-1000,-10000],[10,0,50,0,0],[100,-50,0,500,0],[1000,0,-500,0,50000],[10000,0,0,-50000,0]]
		self.winCombinations = [[[0,0],[0,1],[0,2],[0,3]],[[1,0],[1,1],[1,2],[1,3]],[[2,0],[2,1],[2,2],[2,3]],[[3,0],[3,1],[3,2],[3,3]],[[0,0],[1,0],[2,0],[3,0]],[[0,1],[1,1],[2,1],[3,1]],[[0,2],[1,2],[2,2],[3,2]],[[0,3],[1,3],[2,3],[3,3]],[[0,0],[1,1],[2,2],[3,3]],[[0,3],[1,2],[2,1],[3,0]]]
		self.blocks = []

	def update(self, board, new_move, ply):
		#updating the game board and block status as per the move that has been passed in the arguements
		board.board_status[new_move[0]][new_move[1]] = ply 
		x = new_move[0]/4
		y = new_move[1]/4
		fl = 0 
		#checking if a block has been won or drawn or not after the current move
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if (board.board_status[4*x+i][4*y] == board.board_status[4*x+i][4*y+1] == board.board_status[4*x+i][4*y+2] == board.board_status[4*x+i][4*y+3]) and (board.board_status[4*x+i][4*y] == ply):
				board.block_status[x][y] = ply 
				return 1
			#checking for vertical pattern(i'th column)
			if (board.board_status[4*x][4*y+i] == board.board_status[4*x+1][4*y+i] == board.board_status[4*x+2][4*y+i] == board.board_status[4*x+3][4*y+i]) and (board.board_status[4*x][4*y+i] == ply):
				board.block_status[x][y] = ply 
				return 1

		#checking for diagnol pattern
		if (board.board_status[4*x][4*y] == board.board_status[4*x+1][4*y+1] == board.board_status[4*x+2][4*y+2] == board.board_status[4*x+3][4*y+3]) and (board.board_status[4*x][4*y] == ply):
			board.block_status[x][y] = ply 
			return 1
		if (board.board_status[4*x+3][4*y] == board.board_status[4*x+2][4*y+1] == board.board_status[4*x+1][4*y+2] == board.board_status[4*x][4*y+3]) and (board.board_status[4*x+3][4*y] == ply):
			board.block_status[x][y] = ply 
			return 1

		#checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if board.board_status[4*x+i][4*y+j] =='-':
					return 0
		board.block_status[x][y] = 'd'
		return 0
	
	def evaluateboard(self, board, flaggy):
		score = 0
		for line in self.winCombinations:
			play = 0
			other = 0
			tie = 0
			for cell in line:
				if board.block_status[cell[0]][cell[1]] == self.oord:
					play = play + 1
				elif board.block_status[cell[0]][cell[1]] == self.dcrd:
					tie = tie + 1
				elif board.block_status[cell[0]][cell[1]] == self.xord:
					other = other + 1
			score += 1000*self.heuristicValues[flaggy][play][other]
		
		return score
	

	def evaluatelinescore(self, board, move, flaggy):
		score = 0
		x = move[0]/4*4
		play = 0
		other = 0
		tie = 0
		for i in range(x, x+4):
			if board.board_status[i][move[1]] == self.oord:
				play = play + 1
			elif board.board_status[i][move[1]] == self.dcrd:
				tie = tie + 1
			elif board.board_status[i][move[1]] == self.xord:
				other = other + 1
		score += self.heuristicValues[flaggy][play][other]
		x = move[1]/4*4
		play = 0
		other = 0
		tie = 0
		for i in range(x, x+4):
			if board.board_status[move[0]][i] == self.oord:
				play = play + 1
			elif board.board_status[move[0]][i] == self.dcrd:
				tie = tie + 1
			elif board.board_status[move[0]][i] == self.xord:
				other = other + 1
		score += self.heuristicValues[flaggy][play][other]

		if move[0] == move[1]:
			x = move[0]/4*4
			y = move[1]/4*4
			play = 0
			other = 0
			tie = 0
			for i in range(4):
				if board.board_status[x+i][y+i] == self.oord:
					play = play + 1
				elif board.board_status[x+i][y+i] == self.dcrd:
					tie = tie + 1
				elif board.board_status[x+i][y+i] == self.xord:
					other = other + 1
			score += self.heuristicValues[flaggy][play][other]
		elif (move[0]+move[1])%4 == 3:
			x = move[0]/4*4
			y = move[1]/4*4+3
			play = 0
			other = 0
			tie = 0 
			for i in range(4):
				if board.board_status[x+i][y-i] == self.oord:
					play = play + 1
				elif board.board_status[x+i][y-i] == self.dcrd:
					tie = tie + 1
				elif board.board_status[x+i][y-i] == self.xord:
					other = other + 1
			score += self.heuristicValues[flaggy][play][other]
		return score
			
	def get_block_number(self,old_move):  # returns the block number of a cell
            return ((old_move[0]/4)*4+old_move[1]/4)


 	def get_cell_list_from_block(self,block_number):  #retruns the 16 cells within a block tested and works fine 
            cell_list = []
            add_j = block_number/4  
            add_k = block_number%4  
            for j in range(4):
                for k in range(4):
                    j_temp = j+add_j*4
                    k_temp = k+add_k*4   
                    cell_list.append([j_temp,k_temp])
            return cell_lis


	def alphabetaPruning(self, node, depth, board, alpha, beta, maximizingPlayer, flaggy,valid):

		if depth == 0: 
			return self.boardscore+sum(self.blocks)
		
		elif maximizingPlayer:
			v = float("-inf")
			cells = board.find_valid_move_cells(node)
			stack = []
			cell_stack = []
			for cell in cells:
				x = [cell[0], cell[1], self.linescorechange(board, cell, self.oord,flaggy)]
				stack.append(x)
 				cell_stack.append(cell)
	#		print cell_stack
			sorted(stack, key=lambda x: x[2])

			for x in stack:
				flag = self.update(board, x, self.oord)
				if flag != 0:
					self.temp.append(self.boardscore)
					self.boardscore = self.evaluateboard(board,flaggy)
					self.testscr += 1
				# 	print testscr
				self.blocks.append(x[2])	
				v = max(v, self.alphabetaPruning(x, depth-1, board, alpha, beta, False, flaggy,1))
				self.blocks.pop()
				if flag != 0:
					self.boardscore = self.temp.pop()
					self.testscr += 1
				# 	print testscr
				board.board_status[x[0]][x[1]] = '-'
				board.block_status[x[0]/4][x[1]/4] = '-'
				alp= max(alpha, v)
				if beta <= alp:
					break
			return v

		else:
			v = float("inf")
			cells = board.find_valid_move_cells(node)
			stack = []
			cell_stack = []
			for cell in cells:
				x = [cell[0], cell[1], self.linescorechange(board, cell, self.xord,flaggy)]
				stack.append(x)
				cell_stack.append(cell)
			sorted(stack, key=lambda x: x[2], reverse = True)

			for x in stack:
				flag = self.update(board, x, self.xord)
				if flag != 0:
					self.temp.append(self.boardscore)
					self.boardscore = self.evaluateboard(board,flaggy)
					self.testscr += 1
				# 	print testscr
				self.blocks.append(x[2])
				v = min(v, self.alphabetaPruning(x, depth-1, board, alpha, beta, True, flaggy,1))
				self.blocks.pop()
				if flag != 0:
					self.boardscore = self.temp.pop()
					self.testscr += 1
				# 	print testscr
				board.board_status[x[0]][x[1]] = '-'
				board.block_status[x[0]/4][x[1]/4] = '-'
				beta = min(beta, v)
				if beta <= alpha:
					break
			return v


	
	def linescorechange(self, board, cell, ply, flaggy):
		board.board_status[cell[0]][cell[1]] = ply
		x = self.evaluatelinescore(board, cell,flaggy)
		board.board_status[cell[0]][cell[1]] = '-'
		x -= self.evaluatelinescore(board, cell,flaggy)
		return x



	def move(self, board, old_move, flag):
		flaggy=flag
		if old_move == (-1,-1):
			self.oord = 'x'
			self.xord = 'o'
		self.boardscore = self.evaluateboard(board,flaggy)
		cells = board.find_valid_move_cells(old_move)
		bestValue = float("-inf")
		stack = []
		cell_stack = []
		for cell in cells:
			x = [cell[0], cell[1], self.linescorechange(board, cell, self.oord,flaggy)]
			stack.append(x)
			cell_stack.append(cell)
		sorted(stack, key=lambda x: x[2])

		for x in stack:
			flag = self.update(board, x, self.oord) #Draw move
			if flag != 0:
				self.temp.append(self.boardscore)
				self.boardscore = self.evaluateboard(board,flaggy)
				self.testscr = self.testscr + 1
			# 	print testscr
			self.blocks.append(x[2])
			Value =	self.alphabetaPruning(x, 2, board, float("-inf"), float("inf"), False,flaggy,1)
			self.blocks.pop()
			if flag != 0:
				self.boardscore = self.temp.pop()
				self.testscr = self.testscr + 1
			# 	print testscr
			board.board_status[x[0]][x[1]] = '-'	#delete move
			board.block_status[x[0]/4][x[1]/4] = '-' 
			
			if Value >= bestValue :
				bestValue = Value
				bestMove = (x[0], x[1])

		return bestMove

