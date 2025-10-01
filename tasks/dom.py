"""dominance utilities with print functionalities
"""

def edges_to_preds(edges):
  """Returns {v -> list_of_preds} mapping.
  """
  from collections import defaultdict #AIGEN whole body
  preds = defaultdict(list)
  for _from, _to in edges:
    preds[_to].append(_from)
  return dict(preds)


def map_to_dom(preds):
  """Returns {v: DOM(v) for all vertices}
  """
  n_v = len(preds)
  if 0 not in preds.keys():
    n_v = n_v + 1
  map_to_dom = {v_i: set(range(n_v)) for v_i in range(n_v)}
  map_to_dom[0] = {0}
  old_map_to_dom = {}
  while old_map_to_dom != map_to_dom:
    old_map_to_dom = map_to_dom
    for v_i in range(1, n_v):
      new_doms = map_to_dom[preds[v_i][0]]
      for v_p in preds[v_i][1:]:
        new_doms = new_doms & map_to_dom[v_p]
      map_to_dom[v_i] = new_doms | {v_i}
  return map_to_dom


def map_to_dominatees(map_to_dom):
  from collections import defaultdict #AIGEN whole body
  map_to_dominatees = defaultdict(set)
  n_v = len(map_to_dom)
  for dominator in range(n_v):
    for v_j in range(n_v):
      if dominator in map_to_dom[v_j]:
        map_to_dominatees[dominator].add(v_j)
  return dict(map_to_dominatees)


def map_to_fronts(dom, domee, pred):
  from collections import defaultdict
  fronts = defaultdict(list)
  fronts[0] = []
  n_v = len(dom)
  for v in range(1, n_v):
    notdom = set(range(1, n_v)) - domee[v]
    fronts[v] = [u for u in notdom if any(w in dom[v] for w in pred[u])]
  return dict(fronts)


def make_dom_tree(map_to_dom):
  """Returns {all edges of the dominance tree}
  """  
  edges = []
  for v_from in range(len(map_to_dom)):
    for v_to in range(v_from + 1, len(map_to_dom)):
      if v_from in map_to_dom[v_to]:
        map_to_dom[v_to].remove(v_from)
        if len(map_to_dom[v_to]) == 1:
          edges.append((v_from, v_to))
  return edges


if __name__ == '__main__':
  import json
  import sys
  from cfg import form_blocks, form_cfg
  prog = json.load(sys.stdin)
  for func in prog['functions']:
    blocks = list(form_blocks(func['instrs']))
    cfg = list(form_cfg(blocks))
    preds = edges_to_preds(cfg)
    print("preds:")
    print(preds)
    doms = map_to_dom(preds)
    print("doms:")
    print(doms)
    dominatees = map_to_dominatees(doms)
    print("dominatees:")
    print(dominatees)
    print("len(doms):")
    print(len(doms))
    dom_tree = make_dom_tree(doms)
    print("dom_tree:")
    print(dom_tree)
    dominance_frontiers = map_to_fronts(doms, dominatees, preds)
    print("fronts:")
    print(dominance_frontiers)
