import * as R from "ramda";

async function main3a(): Promise<void> {
    const data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    const openBrackets: string[] = ['(', '{', '[', '<'];
    const closedBrackets: string[] = [')', '}', ']', '>'];
    const scoreLookup: { [index: string]: number } = { ')': 1, ']': 2, '}': 3, '>': 4 };
    let scores: number[] = [];

    for (const line of data) {

        let lineOpen: string[] = [];
        let lineCorrupted: boolean = false;

        for (let i = 0; i < line.length; i++) {
            const c: string = line.charAt(i);

            if (openBrackets.includes(c)) {
                lineOpen.push(c);
                continue;
            }

            const lastOpen = lineOpen.pop();
            const expectedClosed = closedBrackets[openBrackets.indexOf(lastOpen)];

            if (expectedClosed != c) {
                lineCorrupted = true;
                break;
            }
        }

        if (lineCorrupted) continue;

        scores.push(R.pipe<[string[]], string, string, string[], string[], Array<[number, string]>, number[], number>(
            R.join(''),
            R.reverse,
            R.split(''),
            R.map<string, string>((c: string) => closedBrackets[R.indexOf(c, openBrackets)]),
            R.addIndex<string, [number, string]>(R.map)((closer: string, index: number) => [index, closer]),
            (neededClosers: Array<[number, string]>) => R.map(
                ([i, el]: [number, string]) => Math.pow(5, neededClosers.length - i - 1) * scoreLookup[el],
                neededClosers
            ),
            R.sum
        )(lineOpen));
    }
    console.log(R.sort<number>((a: number, b: number) => a - b, scores)[Math.floor(scores.length / 2)]);
}

main3a()

