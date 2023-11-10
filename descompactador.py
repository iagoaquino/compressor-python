from PIL import Image
from classes.tree import Node
from classes.tree import Tree
from classes.chain import Chain
from classes.chain import Block
import sys
sys.setrecursionlimit(1000)
chain = Chain()
chain_bytes = Chain()

def get_mesure(file):
    lines =  file.readlines()
    for line in lines:
        for i in range(len(line)):
            if chain_bytes.size == 0:
                block = Block()
                block.value = line[i]
                chain_bytes.head = block
                chain_bytes.tail = block
                chain_bytes.size+=1
            elif chain_bytes.size > 0:
                block = Block()
                block.value = line[i]
                chain_bytes.tail.dir = block
                chain_bytes.tail = block
                chain_bytes.size+=1
    width_image = chain_bytes.head.value + (chain_bytes.head.dir.value << 8)
    chain_bytes.head = chain_bytes.head.dir.dir
    height_image = chain_bytes.head.value + (chain_bytes.head.dir.value << 8)
    chain_bytes.head = chain_bytes.head.dir.dir
    block_width = chain_bytes.head.value + (chain_bytes.head.dir.value << 8)
    chain_bytes.head = chain_bytes.head.dir.dir
    block_height = chain_bytes.head.value + (chain_bytes.head.dir.value << 8)
    chain_bytes.head = chain_bytes.head.dir.dir
    size_copy_queue = chain_bytes.head.value + (chain_bytes.head.dir.value << 8)
    chain_bytes.head = chain_bytes.head.dir.dir
    chain_bytes.size -= 8
    print("width:"+str(width_image))
    print("height:"+str(height_image))
    print("block_width:"+str(block_width))
    print("block_height:"+str(block_height))
    print("size_copy_queue:"+str(size_copy_queue))
    return width_image,height_image, block_width, block_height, size_copy_queue

def reconstruct_queue(block_width, block_height, size_copy_queue):
    queue_base = []
    queue_main = []
    for i in range(size_copy_queue):
        size = chain_bytes.head.value + (chain_bytes.head.dir.value << 8)
        chain_bytes.head = chain_bytes.head.dir.dir
        chain_bytes.size -= 2
        queue_intern_base = []
        for i in range(size):
            node = Node()
            node.r = chain_bytes.head.value
            chain_bytes.head = chain_bytes.head.dir
            node.g = chain_bytes.head.value
            chain_bytes.head = chain_bytes.head.dir
            node.b = chain_bytes.head.value
            chain_bytes.head = chain_bytes.head.dir
            node.quant = chain_bytes.head.value + (chain_bytes.head.dir.value << 8)
            chain_bytes.head = chain_bytes.head.dir.dir
            chain_bytes.size -= 5
            queue_intern_base.append(node)
        queue_base.append(queue_intern_base)
    for i in range(block_width*block_height):
        pos = chain_bytes.head.value + (chain_bytes.head.dir.value << 8)
        chain_bytes.head = chain_bytes.head.dir.dir
        chain_bytes.size -= 2
        queue_intern_main = []
        for j in range(len(queue_base[pos])):
            node = Node()
            node.r = queue_base[pos][j].r
            node.g = queue_base[pos][j].g
            node.b = queue_base[pos][j].b
            node.quant = queue_base[pos][j].quant
            queue_intern_main.append(node)
        queue_main.append(queue_intern_main)
    return queue_main

def add_node_to_queue(node1,node2):
    node_father = Node()
    node_father.esq = node1
    node_father.dir = node2
    node1.father = node_father
    node2.father = node_father
    node_father.quant = node1.quant+node2.quant
    node_father.is_father = True
    return node_father

def create_tree(queue):
    new_tree = Tree()
    while True:
        if len(queue) == 1:
            temp1 = queue[0]
            queue.remove(queue[0])
            node = Node()
            node.is_father = True
            node.esq = temp1
            temp1.father = node
            node.quant = temp1.quant
            new_tree.root = node
            break
        elif len(queue) == 2:
            temp1 = queue[0]
            temp2 = queue[1]
            queue.remove(queue[0])
            queue.remove(queue[0])
            node = Node()
            node.is_father = True
            node.esq = temp1
            node.dir = temp2
            temp1.father = node
            temp2.father = node
            node.quant = temp1.quant+temp2.quant
            new_tree.root = node
            break
        else:
            temp1 = queue[0]
            temp2 = queue[1]
            queue.remove(queue[0])
            queue.remove(queue[0])
            queue.append(add_node_to_queue(temp1,temp2))
            merge_sort(queue)
    return new_tree

def get_bits():
    while chain_bytes.size > 0:
        if chain_bytes.head == 0:
            break
        byte = format(chain_bytes.head.value,"b")
        chain_bytes.head = chain_bytes.head.dir
        chain_bytes.size -= 1
        fault_data = 8 - len(byte)
        for i in range(fault_data):
            byte = "0" + byte
        for i in range(len(byte)):
            if chain.size == 0:
                chain.size += 1
                block = Block()
                block.value = byte[i]
                chain.head = block
                chain.tail = block
            elif chain.size != 0:
                block = Block()
                chain.size += 1
                block.value = byte[i]
                chain.tail.esq = block
                chain.tail = block
            


def show_bits():
    bits = ""
    valor = chain.head
    while True:
        valor = valor.esq
        if valor == 0:
            break
        else:
            bits = bits+str(valor.value)
    print(bits)

        

def get_pixels(pixels, tree, width, heigh, block_width, block_height):
    node = tree.root
    cont = 0
    if tree.root.esq.r > -1 and tree.root.dir == 0:
        chain.head = chain.head.esq
        repeat_complete = int(width/block_width) * int(heigh/block_height)
        for i in range(repeat_complete):
            cores = []
            cores.append(tree.root.esq.r)
            cores.append(tree.root.esq.g)
            cores.append(tree.root.esq.b)
            pixels.append(cores)
    else:
        while True:
            if chain.head.value == "0":
                node = node.esq
                chain.head = chain.head.esq
                chain.size -= 1
            elif chain.head.value == "1":
                node = node.dir
                chain.head = chain.head.esq
                chain.size -= 1
            if node.r > -1:
                cores = []
                cores.append(node.r)
                cores.append(node.g)
                cores.append(node.b)
                pixels.append(cores)
                node = tree.root
                cont+=1
            if cont >= int(width/block_width) * int(heigh/block_height): 
                break

        
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

def reconstruct_image(width, height, block_width, block_height, pixels, saida):
    image = Image.new("RGB",(width,height), (255,255,255))
    cont = 0
    for i in range(block_width):
        for j in range(block_height):
            for k in range(int(width/block_width)):
                for l in range(int(height/block_height)):
                    image.putpixel((k+i*int(width/block_width),l+j*int(height/block_height)), (pixels[cont][0],pixels[cont][1],pixels[cont][2]))
                    if cont < len(pixels)-1:
                        cont+=1
    image.save(saida+".bmp")
def main():
    entrada = input("digite o nome do arquivo de entrada sem a extensão (.wi): ")
    saida = input("digite o nome do arquivo de saida: ")
    file = open(entrada+".wi", "rb")
    width, height, block_width, block_height, size_copy_queue = get_mesure(file)
    trees = []
    queue_main = reconstruct_queue(block_width, block_height, size_copy_queue)
    for queue in queue_main:
        trees.append(create_tree(queue))
    for tree in trees:
        tree.criar_caminho(tree.root)
    get_bits()
    pixels = []
    for i in range(block_width*block_height):
        get_pixels(pixels, trees[i], width, height, block_width, block_height)
    reconstruct_image(width,height, block_width, block_height, pixels, saida)

main()


