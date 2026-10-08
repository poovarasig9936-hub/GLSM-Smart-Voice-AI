def generate_dsa(command):

    command = command.lower()


    if "bfs" in command:
        return '''from collections import deque

graph = {
    "A": ["B","C"],
    "B": ["D","E"],
    "C": ["F"],
    "D": [],
    "E": [],
    "F": []
}

visited = []
queue = deque(["A"])

while queue:
    node = queue.popleft()

    if node not in visited:
        print(node)
        visited.append(node)

        for neighbour in graph[node]:
            queue.append(neighbour)
'''


    elif "dfs" in command:
        return '''graph = {
    "A":["B","C"],
    "B":["D","E"],
    "C":["F"],
    "D":[],
    "E":[],
    "F":[]
}

visited=[]

def dfs(node):

    if node not in visited:
        print(node)
        visited.append(node)

        for neighbour in graph[node]:
            dfs(neighbour)

dfs("A")
'''


    elif "stack" in command:
        return '''stack=[]

stack.append(10)
stack.append(20)
stack.append(30)

print("Stack:",stack)

print("Pop:",stack.pop())

print("After Pop:",stack)
'''


    elif "queue" in command:
        return '''from collections import deque

queue=deque()

queue.append(10)
queue.append(20)
queue.append(30)

print("Queue:",queue)

print("Remove:",queue.popleft())

print("After Remove:",queue)
'''


    elif "bubble" in command:
        return '''arr=[5,3,8,1,2]

n=len(arr)

for i in range(n):

    for j in range(0,n-i-1):

        if arr[j]>arr[j+1]:

            arr[j],arr[j+1]=arr[j+1],arr[j]


print("Sorted Array:",arr)
'''


    elif "selection" in command:
        return '''arr=[64,25,12,22,11]

n=len(arr)

for i in range(n):

    min_index=i

    for j in range(i+1,n):

        if arr[j]<arr[min_index]:
            min_index=j

    arr[i],arr[min_index]=arr[min_index],arr[i]


print("Sorted Array:",arr)
'''


    elif "insertion" in command:
        return '''arr=[12,11,13,5,6]

for i in range(1,len(arr)):

    key=arr[i]
    j=i-1

    while j>=0 and key<arr[j]:
        arr[j+1]=arr[j]
        j=j-1

    arr[j+1]=key


print("Sorted Array:",arr)
'''


    else:
        return None

