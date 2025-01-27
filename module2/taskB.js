// Copyright Boris Ermolovich ermolovich.boris@gmail.com
// двоичное дерево поиска
class Node {
    constructor(key, value, parent = null, left = null, right = null) {
        this.key = key;
        this.value = value;
        this.left = left;
        this.right = right;
        this.parent = parent;
    }

    hasBothChildren() {
        return this.left !== null && this.right !== null;
    }

    hasLeftChild() {
        return this.left !== null;
    }

    hasRightChild() {
        return this.right !== null;
    }

    isLeftChild() {
        return this.parent && this.parent.left === this;
    }

    isRightChild() {
        return this.parent && this.parent.right === this;
    }

    clear() {
        this.left = null;
        this.right = null;
        this.parent = null;
    }
}

class SplayTree {
    constructor() {
        this.root = null;
    }

    #toInt(line) {
    const bigIntValue = BigInt(line);
    return bigIntValue < Number.MAX_SAFE_INTEGER && bigIntValue > Number.MIN_SAFE_INTEGER
        ? parseInt(line)
        : bigIntValue;
}

    #rotateLeft(node) {
        let rightChild = node.right;
        if (rightChild) {
            node.right = rightChild.left;
            if (rightChild.left) rightChild.left.parent = node;
            rightChild.parent = node.parent;
            if (!node.parent) this.root = rightChild;
            else if (node.isLeftChild()) node.parent.left = rightChild;
            else node.parent.right = rightChild;
            rightChild.left = node;
            node.parent = rightChild;
        }
    }

    #rotateRight(node) {
        let leftChild = node.left;
        if (leftChild) {
            node.left = leftChild.right;
            if (leftChild.right) leftChild.right.parent = node;
            leftChild.parent = node.parent;
            if (!node.parent) this.root = leftChild;
            else if (node.isLeftChild()) node.parent.left = leftChild;
            else node.parent.right = leftChild;
            leftChild.right = node;
            node.parent = leftChild;
        }
    }

    #splay(node) {
        while (node.parent) {
            if (!node.parent.parent) {
                if (node.isLeftChild()) {
                    this.#rotateRight(node.parent);
                } else {
                    this.#rotateLeft(node.parent);
                }
            } else if (node.isLeftChild() && node.parent.isLeftChild()) {
                this.#rotateRight(node.parent.parent);
                this.#rotateRight(node.parent);
            } else if (node.isRightChild() && node.parent.isRightChild()) {
                this.#rotateLeft(node.parent.parent);
                this.#rotateLeft(node.parent);
            } else if (node.isLeftChild() && node.parent.isRightChild()) {
                this.#rotateRight(node.parent);
                this.#rotateLeft(node.parent);
            } else if (node.isRightChild() && node.parent.isLeftChild()) {
                this.#rotateLeft(node.parent);
                this.#rotateRight(node.parent);
            }
        }
    }

    #put(key, value) {
        const bKey = this.#toInt(key);
        if (!this.root) {
            this.root = new Node(bKey, value);
            return;
        }

        let currentNode = this.root;
        let parent = null;
        while (currentNode) {
            parent = currentNode;
            const bCurrentKey = this.#toInt(currentNode.key);

            if (bKey < bCurrentKey) {
                currentNode = currentNode.left;
            } else if (bKey > bCurrentKey) {
                currentNode = currentNode.right;
            } else {
                currentNode.value = value;
                this.#splay(currentNode);
                return;
            }
        }

        const newNode = new Node(bKey, value, parent);
        if (bKey < this.#toInt(parent.key)) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }
        this.#splay(newNode);
    }

    #find(key) {
        let bKey = this.#toInt(key);
        let currentNode = this.root;
        while (currentNode) {
            let bCurrentKey = this.#toInt(currentNode.key);
            if (bKey < bCurrentKey) {
                currentNode = currentNode.left;
            } else if (bKey > bCurrentKey) {
                currentNode = currentNode.right;
            } else {
                bKey = null;
                bCurrentKey = null;
                return currentNode;
            }
        }
        bKey = null;
        return null;
    }

    #findLastVisited(key) {
        let bKey = this.#toInt(key);
        let lastVisited = null;
        let current = this.root;
        while (current) {
            lastVisited = current;
            if (bKey < this.#toInt(current.key)) current = current.left;
            else current = current.right;
        }
        bKey = null;
        return lastVisited;
    }

    #min(currentNode=null) {
        while (currentNode && currentNode.hasLeftChild()) {
            currentNode = currentNode.left;
        }
        return currentNode;
    }

    #max(currentNode=null) {
        while (currentNode && currentNode.hasRightChild()) {
            currentNode = currentNode.right;
        }
        return currentNode;
    }

    add(key, value) {
        let node = this.#find(key);
        if (node) {
            this.#splay(node);
            throw new Error("error");
        }
        this.#put(key, value);
    }


    set(key, value) {
        const node = this.#find(key);
        if (!node) {
            this.#splay(this.#findLastVisited(key));
            throw new Error("error");
        }
        node.value = value;
        this.#splay(node);
    }

    search(key) {
        if (!this.root) return null;
        let node = this.#find(key);
        if (!node) {
            this.#splay(this.#findLastVisited(key));
            return node;
        }
        this.#splay(node);
        return node;
    }

    findMin() {
        if (!this.root) {
            throw new Error("error");
        }
        let minNode = this.#min(this.root);
        this.#splay(minNode);
        return minNode;
    }

    findMax() {
        if (!this.root) {
            throw new Error("error");
        }
        let maxNode = this.#max(this.root);
        this.#splay(maxNode);
        return maxNode;
    }

    delete(key) {
        const node = this.#find(key);
        if (!node) {
            this.#splay(this.#findLastVisited(key));
            throw new Error("error");
        }
        this.#splay(node);
        if (node.hasBothChildren()) {
            const leftSubtree = node.left;
            const rightSubtree = node.right;
            leftSubtree.parent = null;
            rightSubtree.parent = null;
            const maxLeft = this.#max(leftSubtree);
            this.#splay(maxLeft);
            maxLeft.right = rightSubtree;
            rightSubtree.parent = maxLeft;
            this.root = maxLeft;
        } else if (node.hasLeftChild()) {
            this.root = node.left;
            this.root.parent = null;
        } else if (node.hasRightChild()) {
            this.root = node.right;
            this.root.parent = null;
        } else {
            this.root = null;
        }
        node.clear();
    }

    print() {
        if (!this.root) {
            console.log("_");
            return;
        }

        let currentLayer = { 0: this.root };
        let levelSize = 1;

        while (Object.keys(currentLayer).length > 0) {
            let nextLayer = {};
            let outputLine = "";
            let hasNonEmptyNode = false;

            for (let i = 0; i < levelSize; i++) {
                if (currentLayer[i]) {
                    const node = currentLayer[i];
                    const parentKey = node.parent ? node.parent.key : "";
                    if (node.parent) outputLine += `[${node.key} ${node.value} ${parentKey}] `;
                    else outputLine += `[${node.key} ${node.value}]`;

                    if (node.left) {
                        nextLayer[i * 2] = node.left;
                        hasNonEmptyNode = true;
                    } else {
                        nextLayer[i * 2] = null;
                    }

                    if (node.right) {
                        nextLayer[i * 2 + 1] = node.right;
                        hasNonEmptyNode = true;
                    } else {
                        nextLayer[i * 2 + 1] = null;
                    }
                } else {
                    outputLine += "_ ";
                    nextLayer[i * 2] = null;
                    nextLayer[i * 2 + 1] = null;
                }
            }

            console.log(outputLine.trim());
            currentLayer = hasNonEmptyNode ? nextLayer : {};
            levelSize *= 2;
        }
    }

}

function main() {
    const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    let tree = new SplayTree();

    readline.on('line', (command) => {
        const addMatch = command.match(/^add\s+((-\d+)|(\d+))\s+(.+)$/);
        const setMatch = command.match(/^set\s+((-\d+)|(\d+))\s+(.+)$/);
        const searchMatch = command.match(/^search\s+((-\d+)|(\d+))$/);
        const findMinMatch = command.match(/^min$/);
        const findMaxMatch = command.match(/^max$/);
        const deleteMatch = command.match(/^delete\s+((-\d+)|(\d+))$/);
        const printMatch = command.match(/^print$/);

        try {
            if (addMatch) {
                const key = addMatch[1];
                const value = addMatch[4];
                tree.add(key, value);
            } else if (setMatch) {
                const key = setMatch[1];
                const value = setMatch[4];
                tree.set(key, value);
            } else if (searchMatch) {
                const key = searchMatch[1];
                const node = tree.search(key);
                console.log(node ? `1 ${node.value}` : "0");
            } else if (findMinMatch) {
                const node = tree.findMin();
                console.log(`${node.key} ${node.value}`);
            } else if (findMaxMatch) {
                const node = tree.findMax();
                console.log(`${node.key} ${node.value}`);
            } else if (deleteMatch) {
                const key = deleteMatch[1];
                tree.delete(key);
            } else if (printMatch) {
                tree.print();
            } else {
                console.log("error");
            }
        } catch (error) {
            console.log("error");
        }
    });
}

main();