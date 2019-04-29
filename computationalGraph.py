import operator
import numpy as np

global rootNodes 
rootNodes = set()

class BatchProcess():

	def __init__(self):
		self.opToBeBatched = {operator.mul}
		self.computed = set()

	def processNode(self, node):
		#leafNode
		if len(node.child) == 0:
			return node.val
		#Only single child
		elif len(node.child) == 1:
			return node.val(node.child.res)
		#Multiple Child
		else:
			childern = node.child
			initalVal = node.val(childern[0].res, childern[1].res)
			ans = initalVal
			for i in range(2, len(childern)):
				ans = node.val(res, childern[i].res)
			return ans

	#Assuming all child nodes are of same size, dimesion, etc.
	def process(self, batchGraph):
		for key in batchGraph:

			node0 = batchGraph[key][0]
			#merge all nodes child into two lists
			child0 = node0.child[0].res
			child1 = node0.child[1].res

			for i in range(1, len(batchGraph[key])):
				node = batchGraph[key][i]
				print (child0,  node.child[0].res)
				print (child1,  node.child[1].res)
				child0 = np.concatenate([child0, node.child[0].res])
				child1 = np.concatenate([child1, node.child[1].res])

			newNode = NumpyBatchNode(key)
			newNode.child = [NumpyBatchNode(child0),NumpyBatchNode(child1)]
			newNode.res = self.processNode(newNode)

			start = 0
			for node in batchGraph[key]:
				node.res = newNode.res[start:start+len(node.child[0].res)]
				self.computed.add(node)

			#break the result

	def allChildProcessed(self, node):
		for child in node.child:
			if child not in self.computed:
				return False
		return True
	
	def addToGraph(self, batchGraph, node):
		if node.val in batchGraph:
			batchGraph[node.val].append(node)
		else:
			batchGraph[node.val] = [node]

	def batchProcess(self, stack):
		batchGraph = {}
		for (i,elem) in enumerate(stack):
			if not elem.op:
				continue
			elif self.allChildProcessed(elem):
				self.addToGraph(batchGraph, elem)
			elif (elem.val not in self.opToBeBatched) or (not self.allChildProcessed(elem)):
				self.process(batchGraph)
				batchGraph = {}
				self.addToGraph(batchGraph, elem)
		#reached end of sort. Final process
		self.process(batchGraph)

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
		rootNodes = set()

class NumpyBatchNode():

	def __init__(self, val, res=None):
		self.val = val
		if isinstance(val,np.ndarray):
			self.res = val
			self.op = False
		else:
			self.res = None
			self.op = True
		self.child = [] #can

	def __mul__(self, other):
		assert isinstance(other, NumpyBatchNode) or isinstance(other, int) or isinstance(other, float)
		if isinstance(other,NumpyBatchNode):
			return self.createComputationalTree(other, operator.mul)
		else:
			return self.createComputationalTree(NumpyBatchNode(np.array([other])), operator.mul)

	__rmul__ = __mul__

	def createComputationalTree(self, node2, parent):

		result = NumpyBatchNode(parent)

		global rootNodes

		if self in rootNodes:
			rootNodes.remove(self)

		if node2 in rootNodes:
			rootNodes.remove(node2)

		result.child.append(self)
		result.child.append(node2)
		rootNodes.add(result)
		return result

a = NumpyBatchNode(np.array([2, 4]))
b = NumpyBatchNode(np.array([4, 6]))
c = NumpyBatchNode(np.array([3, 4]))
d = NumpyBatchNode(np.array([5, 6]))

k = a*b
t = c*d

u = k*t

f = a*d

bp = BatchProcess()
bp.evaluate()

print (k.res)
print (t.res)
print (u.res)
print (f.res)


# a = NumpyBatchNode(np.array([[2, 4],[9,8]]))

# t = 4*a
# bp = BatchProcess()
# bp.evaluate()

# print (t.res)