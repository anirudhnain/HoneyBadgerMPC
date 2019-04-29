import operator
import numpy as np
import asyncio

global rootNodes 
rootNodes = set()

async def open(x):
	print ('x:',x)
	return x

class BatchProcess():

	def __init__(self):
		self.opToBeBatched = {operator.mul}
		self.computed = set()

	async def processNode(self, node):
		#leafNode
		if not node.op:
			return node.val
		#Only single child
		elif len(node.child) == 1:
			return await node.val(node.child[0].res)
		#Multiple Child
		else:
			childern = node.child
			initalVal = node.val(childern[0].res, childern[1].res)
			ans = initalVal
			for i in range(2, len(childern)):
				ans = node.val(ans, childern[i].res)
			return ans

	async def process(self, batchGraph):
		for key in batchGraph:
			#merge all child nodes for this operator

			initalNode = batchGraph[key][0]
			numberOfChild = len(initalNode.child)

			childList = []

			#Assuming all child nodes are of same size, dimesion, etc.
			for i in range(numberOfChild):
				childList.append(initalNode.child[i].res)

			for i in range(1, len(batchGraph[key])):
				node = batchGraph[key][i]
				for j in range(len(childList)):
					childList[j] = np.concatenate([childList[j],  node.child[j].res])

			print (childList)
			newNode = NumpyBatchNode(key)
			newNode.child = list(map(lambda x: NumpyBatchNode(x), childList))
			newNode.res = await self.processNode(newNode)

			print (newNode.res)
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

	async def batchProcess(self, stack):
		batchGraph = {}
		for (i,elem) in enumerate(stack):
			if not elem.op:
				continue
			elif self.allChildProcessed(elem):
				self.addToGraph(batchGraph, elem)
			elif (elem.val not in self.opToBeBatched) or (not self.allChildProcessed(elem)):
				await self.process(batchGraph)
				batchGraph = {}
				self.addToGraph(batchGraph, elem)
		#reached end of sort. Final process
		await self.process(batchGraph)

	def topologicalSortUtil(self, node, visited, stack):
		visited.add(node)
		for child in node.child:
			self.topologicalSortUtil(child, visited, stack)
		stack.append(node) 
	
	async def evaluate(self):
		visited = set()
		stack = []
		global rootNodes
		for node in rootNodes:
			if node not in visited:
				self.topologicalSortUtil(node, visited, stack)
			await self.batchProcess(stack)
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
			return self.createComputationalTree(operator.mul, other)
		else:
			return self.createComputationalTree(operator.mul, NumpyBatchNode(np.array([other])))

	__rmul__ = __mul__

	def open(self):
		return self.createComputationalTree(open)

	def createComputationalTree(self, parent, node2=None):

		result = NumpyBatchNode(parent)

		global rootNodes

		if self in rootNodes:
			rootNodes.remove(self)

		result.child.append(self)

		if node2:
			if node2 in rootNodes:
				rootNodes.remove(node2)
			result.child.append(node2)
		rootNodes.add(result)
		return result

asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.get_event_loop()

a = NumpyBatchNode(np.array([1, 2]))
b = NumpyBatchNode(np.array([3, 4]))

c = a.open()
d = b.open()

print (c,d)
z = c*d

# a = NumpyBatchNode(np.array([2, 4]))
# b = NumpyBatchNode(np.array([4, 6]))
# c = NumpyBatchNode(np.array([3, 4]))
# d = NumpyBatchNode(np.array([5, 6]))

# k = a*b
# t = c*d

# u = k*t

# f = a*d

bp = BatchProcess()
loop.run_until_complete(bp.evaluate())

# print (k.res)
# print (t.res)
# print (u.res)
# print (f.res)


# a = NumpyBatchNode(np.array([[2, 4],[9,8]]))

# t = 4*a
# bp = BatchProcess()
# bp.evaluate()

# print (t.res)