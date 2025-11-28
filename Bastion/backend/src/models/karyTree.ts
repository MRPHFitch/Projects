export class KaryTreeEntry {
  constructor(public value: string) {} // Encoded username
}

//Set up the Nodes of the tree
export class KaryTreeNode {
  public entries: (KaryTreeEntry | null)[];
  public children: (KaryTreeNode | null)[];
  constructor(
    public nodeNumber: number,
    maxEntries: number,
    k: number
  ) {
    this.entries = Array(maxEntries).fill(null);
    this.children = Array(k).fill(null);
  }
}

export class KaryTree {
  private nextNodeNumber = 0;
  public root: KaryTreeNode;

  constructor(
    public treeNumber: number,
    public k: number = 10,
    public maxEntriesPerNode: number = 100
  ) {
    this.root = new KaryTreeNode(0, maxEntriesPerNode, k);
    // Fill first slot with dummy data
    this.root.entries[0] = new KaryTreeEntry('DUMMY');
  }

  // Insert value, return [nodeNumber, position]
  insert(value: string, rng: () => number): [number, number] {
    let node = this.root;
    while (true) {
      // Find all available positions
      const available: number[] = [];
      for (let i = 0; i < this.maxEntriesPerNode; i++) {
        if (node.entries[i] === null) available.push(i);
      }
      if (available.length > 0) {
        const pos = available[Math.floor(rng() * available.length)];
        node.entries[pos] = new KaryTreeEntry(value);
        return [node.nodeNumber, pos];
      }
      // Node full, descend randomly
      const childIdx = Math.floor(rng() * this.k);
      if (!node.children[childIdx]) {
        node.children[childIdx] = new KaryTreeNode(++this.nextNodeNumber, this.maxEntriesPerNode, this.k);
      }
      node = node.children[childIdx]!;
    }
  }
}