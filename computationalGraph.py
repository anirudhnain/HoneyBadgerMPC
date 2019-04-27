global rootNodes 
rootNodes = set()

class TopologicalSort():

	def __init__(self):
		self.graph = {} #using graph for quick jumping #delete values before putting new resuls in graph
		self.op = '*'

	def processNode(self, node):
		if node.val == self.op:
			ans = 1
			for child in node.child:
				ans *= int(child.val)
			return ans

	def process(self, stack ,start, end):
		for k in range(start,end):
			#process the node
			if stack[k].val == self.op: #convert self.op to a list and check self.ops.contains(self[k].val)
				node = stack[k]
				result = self.processNode(node)
				#last parent won't be in graph so check
				if stack[k] in self.graph:
					parent = self.graph[stack[k]]
					parent.child.remove(stack[k])
					parent.child.add(Node(result))
				else:
					return result

	def eval(self, stack):
		start = 0
		for (i,elem) in enumerate(stack):
			#eval all operations before it
			if elem.val == self.op:
				self.process(stack, start, i)
				start = i
			# print (num1.val, num2.val)
		return self.process(stack,i,i+1)

	#check for commands that are connection dependent and eval them
	def topologicalSortUtil(self, node, visited, stack):
		visited[node] = True
		for child in node.child:
			self.topologicalSortUtil(child, visited, stack)
			self.graph[child] = node
		stack.append(node) 
	#call eval when you hit a node with connect op
	
	def topologicalSort(self):
		visited = {}
		stack = []
		global rootNodes
		for node in rootNodes:
			if node not in visited:
				self.topologicalSortUtil(node, visited, stack)
			print ("Print-Tree")
			return self.eval(stack)
			# stack = []

class Node():

	def __init__(self, val):
		self.val = val
		self.child = set() #can

	def __mul__(self, other):
		assert isinstance(other, Node) or isinstance(other, int) or isinstance(other, float)
		if isinstance(other,Node):
			return self.createComputationalTree(other, "*")
		else:
			return self.createComputationalTree(Node(other), "*")

	__rmul__ = __mul__

	def createComputationalTree(self, node2, parent):

		result = Node(parent)

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

a = Node("4")
b = Node("2")

c = 5*b

d = 6*a

k = c*d

# e = 400*b

# print (d.val)
# print ("Child")
# printNode(d)
# for elem in rootNodes:
# 	printNode(elem)

t = TopologicalSort()
print (t.topologicalSort())

# n = Node("2")
# k = n*3.0
# print (k.val)

# print ()