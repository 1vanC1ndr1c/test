import * as R from "ramda";

async function main3a(): Promise<void> {
    const data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    const openBrackets: string[] = ['(', '{', '[', '<'];
    const closedBrackets: string[] = [')', '}', ']', '>'];
    const scoreLookup: { [index: string]: number } = { ')': 3, ']': 57, '}': 1197, '>': 25137 };
    let highScore: number = 0;

    for (const line of data) {

        let lineOpen: string[] = [];

        for (let i = 0; i < line.length; i++) {
            const c: string = line.charAt(i);

            if (openBrackets.includes(c)) {
                lineOpen.push(c);
                continue;
            }

            const lastOpen = lineOpen.pop();
            const expectedClosed = closedBrackets[openBrackets.indexOf(lastOpen)];

            if (expectedClosed != c)
                highScore += scoreLookup[c];
        }
    }
    type initObj = { row: Array<[number, string]>, lineOpen: Array<string> };
    type openedClosed = { opened: Array<[number, string]>, closed: Array<[number, string]> };
    type fullObj = initObj & openedClosed;
    type elType = [number, string];
    const magicFun = (obj: any) => {console.log('TAKE WHILE', obj); return true;};

   console.log(highScore);
}

main3a()

