'''input
1
7
2 4 5 8 -4 3 -6 
'''
INT_MIN = -2**32
class Node: 
	def __init__(self, data): 
		self.data = data 
		self.left = None
		self.right = None
def maxPathSumUtil(root, res): 
	if root is None: 
		return 0
	
	if root.left is None and root.right is None: 
		return root.data 
	ls = maxPathSumUtil(root.left, res) 
	rs = maxPathSumUtil(root.right, res) 

	if root.left is not None and root.right is not None: 
		res[0] = max(res[0], ls + rs + root.data) 
		return max(ls, rs) + root.data 
	if root.left is None: 
		return rs + root.data 
	else: 
		return ls + root.data 
def maxPathSum(root): 
		res = [INT_MIN] 
		maxPathSumUtil(root, res) 
		return res[0] 


T = int(input())
for t in range(T):
	N = int(input())
	arr = list(map(int,input().split()))
	l = [0]*N
	for i in range(N):
		l[i] = Node(arr[i])
	for i in range(1,N):
		if (i%2==0):
			l[(i//2)-1].right = l[i]
		else:
			l[i//2].left = l[i]
	print(maxPathSum(l[0]))
