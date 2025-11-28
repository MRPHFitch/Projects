import {KaryTree} from '../models/karyTree';

export class BadgeService {
  private trees: KaryTree[] = [];
  private rng: () => number;

  constructor(
    private numTrees: number = 10,
    private k: number = 10,
    private maxEntriesPerNode: number = 100
  ) {
    // Use crypto-secure RNG if available
    this.rng = () => Math.random();
    for (let i = 0; i < numTrees; i++) {
      this.trees.push(new KaryTree(i, k, maxEntriesPerNode));
    }
  }

  // Insert value, return badge ID as string
  insertAndGetBadge(value: string): string {
    const treeIdx = Math.floor(this.rng() * this.numTrees);
    const tree = this.trees[treeIdx];
    const [nodeNumber, pos] = tree.insert(value, this.rng);
    // Format: TNNNPP
    return `${treeIdx}${nodeNumber.toString().padStart(3, '0')}${pos.toString().padStart(2, '0')}`;
  }
}