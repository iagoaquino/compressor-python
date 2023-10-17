class Node:
    def __init__(self):
        self.quant = 0
        self.is_father = False
        self.father = 0
        self.esq = 0
        self.dir = 0
        self.is_null = True
        self.r = -1
        self.b = -1
        self.g = -1
        self.code = 0

class Tree():
    def __init__(self):
        self.root = Node()
        self.size = 0

    def add_node(self, node_receive, node_put):
        if node_receive.r+node_receive.g+node_receive.b > node_put.r+node_put.g+node_put.b:
            if node_receive.esq.is_null == True:
                node_receive.esq = node_put
                node_put.father = node_receive
                print("entrei aqui esquerda")
                print("filho")
                print("r:"+str(node_put.r))
                print("g:"+str(node_put.g))
                print("b:"+str(node_put.b))
                print("pai")
                print("r:"+str(node_put.father.r))
                print("g:"+str(node_put.father.g))
                print("b:"+str(node_put.father.b))
                self.size += 1
            else:
                self.add_node(node_receive.esq,node_put)
        elif node_receive.r+node_receive.g+node_receive.b < node_put.r+node_put.g+node_put.b:
            if node_receive.dir.is_null == True:
                node_receive.dir = node_put
                node_put.father = node_receive
                print("entrei aqui direita")
                print("filho")
                print("r:"+str(node_put.r))
                print("g:"+str(node_put.g))
                print("b:"+str(node_put.b))
                print("pai")
                print("r:"+str(node_put.father.r))
                print("g:"+str(node_put.father.g))
                print("b:"+str(node_put.father.b))
                self.size += 1
            else:
                self.add_node(node_receive.dir,node_put)
        elif node_receive.r+node_receive.g+node_receive.b == node_put.r+node_put.g+node_put.b:
                node_receive.quant+=1

    def show_tree(self, node):
        if node.esq != 0:
            self.show_tree(node.esq)
        if node.dir != 0:
            self.show_tree(node.dir)
        print("encontrei folha")
        print("r:"+ str(node.r))
        print("g:"+ str(node.g))
        print("b:"+ str(node.b))
        print("size:" + str(node.quant))

    def show_code_tree(self, node):
        if node.esq != 0:
            self.show_code_tree(node.esq)
        if node.dir != 0:
            self.show_code_tree(node.dir)
        if node.dir == 0 and node.esq == 0:
            print("encontrei folha")
            print("codigo:" + str(node.code) + "cor: "+str(node.r)+", "+str(node.g)+", "+str(node.b))

    def criar_caminho(self, node):
        if node.esq != 0:
            self.criar_caminho(node.esq)
        if node.dir != 0:
            self.criar_caminho(node.dir)
        if node.dir == 0 and node.esq == 0:
            codigo = []
            node_atual = node
            node_father = node.father
            while(node_father != 0):
                if node_atual == node_father.esq:
                    codigo.append(0)
                elif node_atual == node_father.dir:
                    codigo.append(1)
                node_atual = node_father
                node_father = node_father.father
            codigo.reverse()
            node.code = codigo
            


            
            
            
            
