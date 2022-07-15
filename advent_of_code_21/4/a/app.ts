import * as R from "ramda";

async function main3a(): Promise<void> {

    let data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    const dataParsed: number[][] = R.pipe(
        R.filter((x: string) => x != ''),
        R.map(R.replace(/,/g, ' ')),
        R.map(R.split(' ')),
        R.map(R.filter((x: string) => x != '')),
        R.map(R.map((x: string) => parseInt(x)))
    )(data)

    const drawnNumbers: number[] = dataParsed[0];
    let tickets: (number | string)[][][] = R.splitEvery(5, (R.slice(1, Infinity, dataParsed)));

    const getWinners = (collection: any[][][]) => R.pipe(
        R.map(R.map(R.all(R.equals('x')))),
        R.map(R.any(R.equals(true))),
        (truthTable: boolean[]) => Array.from(truthTable.entries()),
        R.reject((x: (number | boolean)[]) => x[1] == false),
        R.map((x: [number, boolean]) => x[0])
    )(collection);

    for (let drawnNumber of drawnNumbers) {

        tickets = R.pipe(R.map(R.map(R.map(
            (ticketNumber: (number | string)) => ticketNumber == drawnNumber ? 'x' : ticketNumber)))
        )(tickets);

        let winners: number[] = getWinners(tickets).length != 0 ? getWinners(tickets) : getWinners(R.map(R.transpose, tickets));

        if (winners.length == 0) continue;

        console.log(drawnNumber * R.pipe(
            (tickets) => tickets[winners[0]],
            R.map(R.reject(x => x == 'x')),
            R.map(R.sum),
            R.sum,
        )(tickets));
        break;
    }
}

main3a()