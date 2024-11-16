class Deque {
    constructor(size) {
        if (size >= 0) {
            this.n = size;
        } else {
            this.n = 0;
            console.log('error');
        }
        this.deque = new Array(this.n).fill(null);
        this.front = 0;
        this.back = 0;
        this.size = 0;
    }

    printDeque() {
        if (this.size === 0) {
            console.log('empty');
        } else {
            let ind = this.front;
            const data = [];
            for (let i = 0; i < this.size; i++) {
                data.push(this.deque[ind]);
                ind = (ind + 1) % this.n;
            }
            console.log(data.join(' '));
        }
    }

    pushBack(toAdd) {
        if (this.size === this.n) {
            console.log('overflow');
        } else {
            this.deque[this.back] = toAdd;
            this.back = (this.back + 1) % this.n;
            this.size += 1;
        }
    }

    pushFront(toAdd) {
        if (this.size === this.n) {
            console.log('overflow');
        } else {
            this.front = (this.front - 1 + this.n) % this.n;
            this.deque[this.front] = toAdd;
            this.size += 1;
        }
    }

    popBack() {
        if (this.size === 0) {
            console.log('underflow');
        } else {
            const value = this.deque[(this.back - 1 + this.n) % this.n];
            this.back = (this.back - 1 + this.n) % this.n;
            this.size -= 1;
            console.log(value);
        }
    }

    popFront() {
        if (this.size === 0) {
            console.log('underflow');
        } else {
            const value = this.deque[this.front];
            this.front = (this.front + 1) % this.n;
            this.size -= 1;
            console.log(value);
        }
    }
}

function main() {
    const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout,
    });
    let deq = null;
    let allocated = false;

    readline.on('line', (command => {
        if (!command.trim()) return;

        const content = command.match(/\S+|\s+/g);

        if (content[0] === 'set_size' && !allocated && parseInt(content[2], 10) >= 0) {
            try {
                const size = parseInt(content[2], 10);
                deq = new Deque(size);
                allocated = true;
            } catch (error) {
                console.log('error');
            }
        } else if (!allocated) {
            console.log('error');
        } else if (content.length === 1) {
            const head = content[0];
            switch (head) {
                case 'print':
                    deq.printDeque();
                case 'popb':
                    deq.popBack();
                case 'popf':
                    deq.popFront();
                default:
                    console.log('error');
            }
        } else if (content.length === 3 && content[1] === ' ') {
            const head = content[0];
            const value = content[2];

            switch (head) {
                case 'pushb':
                    deq.pushBack(value);
                case 'pushf':
                    deq.pushFront(value);
                default:
                    console.log('error');
            }
        } else {
            console.log('error');
        }
    }));
}

main();