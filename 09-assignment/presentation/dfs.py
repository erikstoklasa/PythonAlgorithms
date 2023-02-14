# Prohledávání do hloubky - depth first search
# Rekurzivní implementace
# Jan Kybic, 2016

def solve(problem,maxdepth=10):
  """ Prohledá stavový prostor z počátečního stavu 'problem' (viz. kozavlkzeli.py)
     do hloubky nanejvýše 'maxdepth'.
      Vrátí posloupnost stavu (states) vedoucí k řešení nebo 'None' """
  visited=set() 
  def solve_internal(state,depth):
    """ vrátí posloupnost stavů ze 'state' do cílového stavu """
    nonlocal visited
    if depth<maxdepth and state not in visited:
      if state.final(): # koncový stav?
         return [state]
      visited|={state}  # označ stav jako navštívený
      for s in state.succ():
          r=solve_internal(s,depth+1)
          if r: # řešení nalezeno
            return [state]+r # méně efektivní
      return None
  return solve_internal(problem,0)

def all_states(problem,maxdepth=10):
  """ Najde všechny možné stavy do dané hloubky """
  visited=set()
  def all_states_internal(state,depth):
    """ vrátí množinu všech stavů """
    nonlocal visited
    if depth<maxdepth and state not in visited:
      visited|={state}  # označ stav jako navštívený
      for s in state.succ():
          all_states_internal(s,depth+1)
  all_states_internal(problem,0)
  return visited
      
def print_all_states(problem,maxdepth=10):
  states=all_states(problem,maxdepth=maxdepth)
  for s in states:
    print(s," -> ",", ".join(map(str,s.succ())))
