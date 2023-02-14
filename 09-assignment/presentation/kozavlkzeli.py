# Problem koza, vlk, zeli
# Jan Kybic

import dfs
import dfs2
import bfs

class KozaVlkZeli:
  """ stav problemu Koza, Vlk, Zeli.
      stav = (levý_břeh,pravý_břeh), kde levý/pravý_břeh je množina ze znaků "MKVZ"
      akce = co je převáženo, tedy např. set("KZ")
  """

  actions=list(map(frozenset,["KM","ZM","VM","M"]))
  
  def __init__(self,state=(frozenset("KVZM"),frozenset())):
    """ nastaví počáteční stav """
    self.state=state

  def final(self):
    """ je toto konečný stav? """
    return len(self.state[0])==0

  def succ(self):
    """ vrátí přípustné akce v daném stavu """
    def safe(aset): 
      """ Zkontroluj, zda množina 'aset' neobsahuje nepovolené dvojice, i.e koza+vlk nebo koza+zeli """
      return not ( frozenset("KZ") <= aset  or frozenset("KV") <= aset )
    i=0 if "M" in self.state[0] else 1  # odkud jedeme
    successors=[]                  # následnící současného stavu 
    for aset in self.actions: # možné akce
      if aset <= self.state[i]: # ano, lze odvézt
        newstate=[None,None] 
        newstate[i]=self.state[i] - aset
        newstate[1-i]=self.state[1-i] | aset 
        if safe(newstate[i]):  # bezpečná situace?
           successors+=[KozaVlkZeli(tuple(newstate))]
    return successors

  # následující metody umožní zamezit duplikacím při vkládání objektu do množiny
  def __eq__(self,a):
    return self.state==a.state

  def __hash__(self):
    return hash(self.state)
           
  def __str__(self):
    """ vrátí reprezentaci stavu jako řetězec """
    return "".join(self.state[0])+"|"+"".join(self.state[1])

# ------------------------------------------------------------------------------  
    
def solve_kozavlkzeli(maxdepth=10):
  sol=dfs.solve(KozaVlkZeli(),maxdepth)
  if sol:
    print(" -> ".join(map(str,sol)))
  else:
    print("Řešení nenalezeno.")

def solve_kozavlkzeli_dfs(maxdepth=10):
  sol=dfs2.solve(KozaVlkZeli(),maxdepth)
  if sol:
    print(" -> ".join(map(str,sol)))
  else:
    print("Řešení nenalezeno.")

def solve_kozavlkzeli_bfs(maxdepth=10):
  sol=bfs.solve(KozaVlkZeli(),maxdepth)
  if sol:
    print(" -> ".join(map(str,sol)))
  else:
    print("Řešení nenalezeno.")

        
def print_states():
  dfs.print_all_states(KozaVlkZeli())

def print_states2():
  dfs2.print_all_states(KozaVlkZeli())

def print_states3():
  bfs.print_all_states(KozaVlkZeli())
    
if __name__=="__main__":
  solve_kozavlkzeli()  
