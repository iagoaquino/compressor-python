from PIL import Image
from classes.tree import Node
from classes.tree import Tree
from bitstring import BitArray
from bitstring import Bits
import sys
file = open("saida.txt","wb")
comparacao = open("saida_teste.txt","w")
sys.setrecursionlimit(1000)
image = Image.open("baldursgate_front.png")
tree = Tree()
queue_main = []
queue_backup = []
def ler_file():
    for i in range(image.width):
        for j in range(image.height):
            if image.mode == "RGB":
                r,g,b = image.getpixel((i,j))
                node = Node()
                node.r = r
                node.g = g
                node.b = b
                exist = False
                for value in queue_main:
                    if value.r == node.r and value.g == node.g and value.b == node.b:
                        value.quant += 1
                        exist = True
                if not exist:
                    queue_main.append(node)

            elif image.mode == "RGBA":
                r,g,b,a = image.getpixel((i,j))
                node = Node()
                node.r = r
                node.g = g
                node.b = b
                exist = False
                for value in queue_main:
                    if value.r == node.r and value.g == node.g and value.b == value.b:
                        value.quant += 1
                        exist = True
                if not exist:
                    queue_main.append(node)
def sort_queue(queue):
    for i in range(len(queue)):
        j = 0
        maior = True
        while maior:
            if j+1 >= len(queue):
                maior = False
            elif queue[j].quant > queue[j+1].quant:
                tmp = queue[j+1]
                queue[j+1] = queue[j]
                queue[j] = tmp
                j+=1
            else:
                j+=1
def add_node_to_queue(node1,node2):
    node_father = Node()
    node_father.esq = node1
    node_father.dir = node2
    node1.father = node_father
    node2.father = node_father
    node_father.quant = node1.quant+node2.quant
    node_father.is_father = True
    return node_father

def create_tree():
    while len(queue_main) >= 2:
        if len(queue_main) == 2:
            temp1 = queue_main[0]
            temp2 = queue_main[1]
            queue_main.remove(queue_main[0])
            queue_main.remove(queue_main[0])
            node = Node()
            node.is_father = True
            node.esq = temp1
            node.dir = temp2
            temp1.father = node
            temp2.father = node
            node.quant = temp1.quant+temp2.quant
            tree.root = node
            break
        else:
            temp1 = queue_main[0]
            temp2 = queue_main[1]
            queue_main.remove(queue_main[0])
            queue_main.remove(queue_main[0])
            queue_main.append(add_node_to_queue(temp1,temp2))
            sort_queue(queue_main)


ler_file()
sort_queue(queue_main)
for i in queue_main:
    queue_backup.append(i)
create_tree()
tree.criar_caminho(tree.root)
tamanho = len(queue_backup)
comparacao.write(str(tamanho))
bin = tamanho.to_bytes(1, byteorder="little", signed=False)
file.write(bin)
for node in queue_backup:
    valor = node.r 
    comparacao.write(str(valor))
    bin = valor.to_bytes(1, byteorder="little", signed=False)
    file.write(bin)
    valor = node.g 
    comparacao.write(str(valor))
    bin = valor.to_bytes(1, byteorder="little", signed=False)
    file.write(bin)
    valor = node.b 
    comparacao.write(str(valor))
    bin = valor.to_bytes(1, byteorder="little", signed=False)
    file.write(bin)
for valor in queue_backup:
    print("r:"+str(valor.r))
    print("g:"+str(valor.g))
    print("b:"+str(valor.b))
file.close()
comparacao.close()
file = open("saida.txt", "rb")
linhas = file.readlines()
valores = []
for linha in linhas:
   for i in range(len(linha)):
       valores.append(linha[i])
print(valores)







