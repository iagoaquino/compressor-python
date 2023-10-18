from PIL import Image
from classes.tree import Node
from classes.tree import Tree
import sys
file = open("saida.bin","wb")
comparacao = open("saida_teste.txt","w")
sys.setrecursionlimit(1000)
image = Image.open("baldursgate_front.png")
tree = Tree()
queue_main = []
queue_backup = []
binarys = []
def ler_file():
    cont = 0
    for i in range(image.width):
        for j in range(image.height):
            print(image.width* image.height)
            print(cont)
            cont+=1
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
                print("entrei aqui: RGBA")
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
            merge_sort(queue_main)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Encontrar o ponto médio do array
        left_half = arr[:mid]  # Dividir o array em duas metades
        right_half = arr[mid:]

        merge_sort(left_half)  # Chamada recursiva para a metade esquerda
        merge_sort(right_half)  # Chamada recursiva para a metade direita

        # Inicializar índices para percorrer as duas metades e o índice para percorrer o array original
        i = j = k = 0

        # Comparar e mesclar as duas metades
        while i < len(left_half) and j < len(right_half):
            if left_half[i].quant < right_half[j].quant:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Verificar se há elementos restantes em ambas as metades
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def get_codes():
    for i in range(image.width):
        for j in range(image.height):
            if image.mode == "RGB":
                r, g, b = image.getpixel((i,j))
                binarys.append(tree.return_code(tree.root, r,g,b).code)
            elif image.mode == "RGB":
                r, g, b = image.getpixel((i,j))
                binarys.append(tree.return_code(tree.root, r,g,b).code)
print(image.width)
print(image.height)
ler_file()
sort_queue(queue_main)
for i in queue_main:
    queue_backup.append(i)
create_tree()
tree.criar_caminho(tree.root)
tree.show_code_tree(tree.root)
tree.reform_tree(tree.root)
tree.criar_caminho(tree.root)
tree.show_code_tree(tree.root)
get_codes()
        
tamanho = len(queue_backup)


bin = 0
one = 1
cont = 0
for binary in binarys:
    for index in binary:
        if cont == 8:
            file.write(bin.to_bytes(1,byteorder="little", signed=False))
            bin = 0
            cont = 0
        value = int(index)
        if value == 0:
            bin = bin << 1
        elif value == 1:
            bin = bin << 1
            bin = bin | one
        cont+=1
file.close()
comparacao.close()
valores = []
file = open("saida.txt", "rb")
linhas = file.readlines()
for i in range(len(linhas)):
    for j in range(len(linhas[i])):
        valores.append(linhas[i][j])









