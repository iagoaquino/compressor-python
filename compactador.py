from PIL import Image
from classes.tree import Node
from classes.tree import Tree
import os
import sys
sys.setrecursionlimit(1000)


def ler_file_pt_1(image, lose_rate, queue_main, block_width, block_height):
    cont = 0
    for i in range(block_width):
        for j in range(block_height):
            check_and_count = open("checkup/check_and_count_["+str(i)+"]["+str(j)+"].txt", "w")
            queue_intern = []
            for k in range(int(image.width/block_width)):
                for l in range(int(image.height/block_height)):
                    print(cont)
                    cont+=1
                    if image.mode == "RGB":
                        r,g,b = image.getpixel((k+i*int(image.width/block_width),l+j*int(image.height/block_height)))
                        node = Node()
                        node.r = r
                        node.g = g
                        node.b = b
                        exist = False
                        for value in queue_intern:
                            if not exist:
                                distancia_r = (value.r - node.r) ** 2
                                distancia_g = (value.g - node.g) ** 2
                                distancia_b = (value.b - node.b) ** 2
                                if (distancia_r + distancia_g + distancia_b) < lose_rate**2:
                                    value.quant += 1
                                    exist = True
                                    break
                        if not exist:
                            queue_intern.append(node)
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
            for value in queue_intern:
                check_and_count.write("rgb("+str(+value.r)+", "+str(value.g)+", "+str(value.b)+") repeat:"+str(value.quant)+"\n")
            queue_main.append(queue_intern)
            check_and_count.close()

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

def generate_color_check(queue, check):
    for i in queue:
        check.write("rgb:"+str(i.r)+" , "+str(i.g)+" , "+str(i.b)+" , quant: "+str(i.quant))

def create_node_to_queue(node1,node2):
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
            queue.append(create_node_to_queue(temp1,temp2))
            merge_sort(queue)
    return new_tree

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

def get_codes(tree,queue_backup, cont,  binarys, image, lose_rate, mod_x, mod_y, block_width, block_heigh):
    if len(queue_backup[cont]) > 1:
        for i in range(int(image.width/block_width)):
            for j in range(int(image.height/block_heigh)):
                if image.mode == "RGB":
                    r, g, b = image.getpixel((i+mod_x*int(image.width/block_width),j+mod_y*int(image.height/block_heigh)))
                    binarys.append(tree.return_code(tree.root, r,g,b,lose_rate).code)
                elif image.mode == "RGB":
                    r, g, b, a  = image.getpixel((i,j))
                    binarys.append(tree.return_code(tree.root, r,g,b,lose_rate).code)
    else:
        r, g, b = image.getpixel((0+mod_x*int(image.width/block_width),0+mod_y*int(image.height/block_heigh)))
        node = tree.return_code(tree.root, r,g,b,lose_rate)
        code = node.code
        quant_repeat = format(node.quant + 1, "b")
        quant_repeat_bit = []
        for i in quant_repeat:
            quant_repeat_bit.append(i)
        quant_repeat_bit.reverse()
        for i in range(len(quant_repeat_bit)):
            binarys.append(quant_repeat_bit[i])
        binarys.append(code)


            
def create_queue_backup(queue_main, id):
    check = open("checkup/check_num_"+str(id)+".txt","w")
    queue_backup = []
    for i in queue_main:
        node = Node()
        node.r = i.r
        node.g = i.g
        node.b = i.b
        node.quant = i.quant
        check.write("cores: "+str(node.r) +" "+str(node.g)+" "+str(node.b)+" quantidade: "+str(node.quant)+"\n")
        queue_backup.append(node)
    check.close()
    return queue_backup

def write_bytes(file, tamanho, image, binarys, copy_queue,queue_order, block_width, block_height):
    size_bin = int(image.width).to_bytes(2, byteorder="little",signed=False)
    file.write(size_bin)
    size_bin = int(image.height).to_bytes(2, byteorder="little",signed=False)
    file.write(size_bin)
    size_bin = int(block_width).to_bytes(2, byteorder="little",signed=False)
    file.write(size_bin)
    size_bin = int(block_height).to_bytes(2, byteorder="little",signed=False)
    file.write(size_bin)
    size_bin = int(len(copy_queue)).to_bytes(2, byteorder="little",signed=False)
    file.write(size_bin)
    for i in range(len(copy_queue)):
        size_bin = tamanho[i].to_bytes(2,byteorder="little", signed=False)
        file.write(size_bin)
        for j in range(len(copy_queue[i])):
            node = copy_queue[i][j]
            size_bin = node.r.to_bytes(1,byteorder="little", signed=False)
            file.write(size_bin)
            size_bin = node.g.to_bytes(1,byteorder="little", signed=False)
            file.write(size_bin)
            size_bin = node.b.to_bytes(1,byteorder="little", signed=False)
            file.write(size_bin)
            size_bin = node.quant.to_bytes(3,byteorder="little", signed=False)
            file.write(size_bin)
    for i in queue_order:
        pos = i.to_bytes(2,byteorder="little", signed=False)
        file.write(pos)
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
    if cont > 0:
        binary_made = bin.to_bytes(1,byteorder="little", signed=False)
        binary_made = format(int.from_bytes(binary_made,byteorder="little", signed=False),"b")
        fault_data = 8-len(binary_made)
        for i in range(fault_data):
            bin = bin << 1
        file.write(bin.to_bytes(1,byteorder="little", signed=False))
        binary_made = bin.to_bytes(1,byteorder="little", signed=False)
        binary_made = format(int.from_bytes(binary_made,byteorder="little", signed=False),"b")
    file.close()

def show_divisor(number):
    divisor = ""
    for i in range(number//2 + 1):
        if number % (i+1) == 0:
            divisor += str(i+1) + " "
    print(divisor)

def comparar_listas(lista_1, lista_2):
    if len(lista_1) != len(lista_2):
        return False
    else:
        achou_diferença = False
        for i in range(len(lista_1)):
            if lista_1[i].r != lista_2[i].r or lista_1[i].g != lista_2[i].g or lista_1[i].b != lista_2[i].b or lista_1[i].quant != lista_2[i].quant:
                achou_diferença = True
        if achou_diferença:
            return False
        else:
            return True
        
def main():
    file = open("output.wi", "wb")
    image = Image.open("benchmark.bmp")
    tree = []
    queue_main = []
    copy_queue = []
    queue_backup = []
    binarys = []
    queue_order = []
    lose_rate = int(input("entre com a taxa de perda"))
    show_divisor(image.width)
    block_width = int(input("digite a largura do bloco"))
    show_divisor(image.height)
    block_heigh = int(input("digite a altura do bloco"))
    ler_file_pt_1(image, lose_rate, queue_main, block_width, block_heigh)
    cont = 0
    for i in range(len(queue_main)):
        sort_queue(queue_main[i])
        queue_backup.append(create_queue_backup(queue_main[i], cont))
        tree.append(create_tree(queue_main[i]))
        cont+=1
    cont_teste = 0
    for i in queue_backup:
        cont_teste+=1
        if len(copy_queue) == 0:
            copy_queue.append(i)
        else:
            exist = False
            for j in copy_queue:
                already_exist = comparar_listas(i, j)
                if already_exist:
                    exist = True
                    break
            if not exist:
                copy_queue.append(i)
        print(cont_teste)
    
    checkup_copy_tree = open("checkup/checkup_copy_queue.txt", "w")

    for i in range(len(copy_queue)):
        checkup_copy_tree.write(str(i)+"\n")
        for j in range(len(copy_queue[i])):
            checkup_copy_tree.write("rgb("+str(copy_queue[i][j].r)+", "+str(copy_queue[i][j].g) + ", "+ str(copy_queue[i][j].b) + ", "+str(copy_queue[i][j].quant)+")\n")

    checkup_copy_tree.close()
    for i in range(len(queue_backup)):
        for j in range(len(copy_queue)):
            found = comparar_listas(queue_backup[i], copy_queue[j])
            if found:
                queue_order.append(j)
                break
    print(queue_order)
    print(len(queue_order))

    for i in range(len(tree)):
        tree[i].criar_caminho(tree[i].root)
    cont = 0

    for j in range(block_width):
        for k in range(block_heigh):
            get_codes(tree[cont],queue_backup, cont, binarys, image, lose_rate, j, k, block_width, block_heigh)
            cont+=1
    tamanho = []
    for value in copy_queue:
        tamanho.append(len(value))
    write_bytes(file, tamanho, image,binarys, copy_queue, queue_order, block_width, block_heigh)
main()

#143 776









