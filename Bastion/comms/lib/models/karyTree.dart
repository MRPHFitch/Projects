// ignore_for_file: file_names

import 'dart:math';

class KaryTreeEntry {
  final String value;   //encoded username
  KaryTreeEntry(this.value);
}

class KaryTreeNode{
  final int nodeNumber;
  final List<KaryTreeEntry?> entries;
  final List<KaryTreeNode?> children;
  KaryTreeNode(this.nodeNumber, int maxEntries, int k)
  : entries=List<KaryTreeEntry?>.filled(maxEntries, null),
    children=List<KaryTreeNode?>.filled(k, null);
}

class KaryTree {
  final int treeNumber;
  final int k;    // branching factor
  final int maxPerNode;
  int _nextNodeNumber = 0;
  final KaryTreeNode root;
  final Random rng;

  KaryTree(this.treeNumber, {this.k = 10, this.maxPerNode = 100})
      : root = KaryTreeNode(0, maxPerNode, k),
      rng=Random.secure() {
    root.entries[0] = KaryTreeEntry('Brutus');
    
  }

  //Keep public API clean by using two inserts
  Tuple2<int,int> insert(String value){
    return insertRecursive(root, value);
  }
  
  Tuple2<int, int> insertRecursive(KaryTreeNode root, String value,) {
    KaryTreeNode node = root;
    int childIdx = rng.nextInt(k);
    //Determine if inserting or descending
    bool insertHere=node.entries.any((e)=>e==null) && (rng.nextBool());
    if(insertHere){
      List<int> available = [];
      for (int i = 0; i < maxPerNode; i++) {
        if (node.entries[i] == null) available.add(i);
      }
      int pos=available[rng.nextInt(available.length)];
      node.entries[pos]=KaryTreeEntry(value);
      return Tuple2(node.nodeNumber, pos);    //Return so you break the recursive loop
    }
    //We are descending, so descend to a random child
    else{
      if (node.children[childIdx] == null) {
        node.children[childIdx] = KaryTreeNode(++_nextNodeNumber, maxPerNode, k);
      }
    }
    return insertRecursive(node.children[childIdx]!, value);
    }
}

class Tuple2<A,B>{
  final A item1;
  final B item2;
  Tuple2(this.item1, this.item2);
}