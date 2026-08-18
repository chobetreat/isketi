startX = 900
startY = 0
scale = 20
addtostart=False
width = 10
height = 10

points = []
connections = []
draw=[]
# generate points
for y in range(height):
    for x in range(width):
        px = startX + x * scale
        py = startY + y * scale
        points.append([px, py])

# helper to convert (x, y) -> point index
def idx(x, y):
    return y * width + x

# generate connections
for y in range(height):
    for x in range(width):
        if x < width - 1:
            connections.append([idx(x, y), idx(x + 1, y)])
        if y < height - 1:
            connections.append([idx(x, y), idx(x, y + 1)])
        if x < width - 1 and y < height - 1:
            connections.append([idx(x, y), idx(x + 1, y + 1)])
        if x > 0 and y < height - 1:
            connections.append([idx(x, y), idx(x - 1, y + 1)])
# long-range connections (gap of 2, 3, ... up to bounds)
max_gap = 4

for gap in range(2, max_gap + 1):
    for y in range(height):
        for x in range(width):
            # horizontal
            if x + gap < width:
                connections.append([idx(x, y), idx(x + gap, y)])

            # vertical
            if y + gap < height:
                connections.append([idx(x, y), idx(x, y + gap)])

            # diagonal down-right
            if x + gap < width and y + gap < height:
                connections.append([idx(x, y), idx(x + gap, y + gap)])

            # diagonal down-left
            if x - gap >= 0 and y + gap < height:
                connections.append([idx(x, y), idx(x - gap, y + gap)])

for x in range(width):
    draw.append(idx(x, 0))
for y in range(height-1):
    draw.append(idx(width-1, y+1))
for x in range(width-1):
    draw.append(idx(width-(x+2), height-1))
for y in range(height-2):
    draw.append( idx(0,height-(y+2)))
if addtostart:
    print(f"points=[", end="")
    loop=0
    for p in points:
        if loop!=0: print(",", end="")
        print(f"[{p[0]}+startX, {p[1]}+startY]", end="")
        loop+=1
    print("]")
else:
    print(f"points={points}")
print(f"connections={connections}")
print(f"draw={draw}")