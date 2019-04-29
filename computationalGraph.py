import operator

global rootNodes 
rootNodes = set()

class BatchProcess():

	def __init__(self):
		self.opToBeBatched = {operator.mul}

	def processNode(self, node):
		#leafNode
		if len(node.child) == 0:
			return node.val
		#Only single child
		elif len(node.child) == 1:
			return node.val(node.child.res)
		#Multiple Child
		else:
			childern = list(node.child)
			initalVal = node.val(childern[0].res, childern[1].res)
			ans = initalVal
			for i in range(2, len(childern)):
				ans = node.val(res, childern[i].res)
			return ans

	def process(self, stack ,start, end):
		for k in range(start,end):
			#process the node
			node = stack[k]
			if not node.res:
				node.res = self.processNode(node)

	def batchProcess(self, stack):
		start = 0
		for (i,elem) in enumerate(stack):
			#eval all operations before this elem
			if elem.val in self.opToBeBatched:
				self.process(stack, start, i)
				start = i
			# print (num1.val, num2.val)
		self.process(stack,i,i+1)

	def topologicalSortUtil(self, node, visited, stack):
		visited.add(node)
		for child in node.child:
			self.topologicalSortUtil(child, visited, stack)
		stack.append(node) 
	
	def evaluate(self):
		visited = set()
		stack = []
		global rootNodes
		for node in rootNodes:
			if node not in visited:
				self.topologicalSortUtil(node, visited, stack)
			self.batchProcess(stack)
			stack = []

class NumpyBatchNode():

	def __init__(self, val):
		self.val = val
		self.res = None
		self.child = set() #can

	def __mul__(self, other):
		assert isinstance(other, NumpyBatchNode) or isinstance(other, int) or isinstance(other, float)
		if isinstance(other,NumpyBatchNode):
			return self.createComputationalTree(other, operator.mul)
		else:
			return self.createComputationalTree(NumpyBatchNode(other), operator.mul)

	__rmul__ = __mul__

	def createComputationalTree(self, node2, parent):

		result = NumpyBatchNode(parent)

		global rootNodes

		if self in rootNodes:
			rootNodes.remove(self)

		if node2 in rootNodes:
			rootNodes.remove(node2)

		result.child.add(self)
		result.child.add(node2)
		rootNodes.add(result)
		return result

def printNode(node):
	if node:
		print (node.val)
		for child in node.child:
			printNode (child)

a = NumpyBatchNode(4)
b = NumpyBatchNode(2)

c = 5*b

d = 6*a

k = c*d

r = c*d

j = k*r

t = BatchProcess()
t.evaluate()

print (k.res)
print (r.res)
print (j.res)