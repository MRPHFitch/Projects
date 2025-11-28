import 'package:comms/models/karyTree.dart';
import 'dart:math';

class KaryForest{
  final int numTrees;
  final int k;
  final int maxEntriesPerNode;
  final List<KaryTree> trees;
  final Random rng;

  KaryForest({this.numTrees=10, this.k=10, this.maxEntriesPerNode=100})
    : trees=[],
    rng=Random.secure(){
      for(int i=0;i<numTrees;i++){
        trees.add(KaryTree(i, k: k, maxPerNode: maxEntriesPerNode));
      }
    }

    //Insert value, return Badge ID#
    String insertForBadge(String value){
      int treeIdx=rng.nextInt(numTrees);
      var tree=trees[treeIdx];
      var res=tree.insert(value);
      //Give Badge in correct format
      String badge='${treeIdx}${res.item1.toString().padLeft(3,'0')}${res.item2.toString().padLeft(2,'0')}';
      return badge;
    }
}