import * as R from "ramda";

async function main3a(): Promise<void> {
    const data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    const numberField: Array<Array<number>> = R.pipe<[string[]], string[][], number[][]>(
        R.map<string[], string[][]>(R.split('')),
        R.map<string[][], number[][]>(
            R.map<string[], number[]>(
                (x: string) => parseInt(x)))
    )(data as string[]);


    const numberFieldEnumerated: Array<[number, number[]]> = R.addIndex<Array<number>, [number, Array<number>]>(R.map)(
        (value: number[], index: number) => [index, value], numberField);

    let mins: { [index: string]: number } = {};
    for (const [y, row] of numberFieldEnumerated) {

        const neighborElementsY: number[] = R.filter<number, number[]>(
            (el: number) => el >= 0 && el < numberField.length,
            R.range(y - 1, y + 2)
        ) as number[];
        const rowEnumerated: Array<[number, number]> = R.addIndex<number, number[]>(R.map)(
            (value: number, index: number) => [index, value], row);

        for (const [x, elVal] of rowEnumerated) {

            const neighborElementsX: number[] = R.filter<number, number[]>(
                (el: number) => el >= 0 && el < row.length,
                R.range(x - 1, x + 2)
            );

            const neighborElementsCoords: Array<[number, number]> = R.xprod<number, number>(neighborElementsX, neighborElementsY);

            const neighborElements: { [index: string]: number } = R.fromPairs<number>(
                R.map<[number, number], [string, number]>(
                    (coord: [number, number]) => [coord.toString(), numberField[coord[1]][coord[0]]],
                    neighborElementsCoords
                )
            );

            const minNeighborVal: number = R.reduce<number, number>(R.min, Infinity, R.values<{ [index: string]: number }, string>(neighborElements));

            if (minNeighborVal != elVal) continue;

            mins[[x, y].toString()] = elVal;

            const oldMinsCoords: string[] = R.intersection<string>(
                R.map<[number, number], string>(x => x.toString(), neighborElementsCoords),
                R.keys<{ [index: string]: number }>(mins) as string[],
            );

            let smallerMins: { [index: string]: number } = R.pipe<string[][], Array<[string, number]>, Array<[string, number]>, { [index: string]: number }>(
                R.map((coord: string) => [coord, mins[coord]]),
                R.reject((x: any) => mins[x[0]] > elVal),
                R.fromPairs
            )(oldMinsCoords as string[]);

            mins = R.mergeRight<{ [index: string]: number }, { [index: string]: number }>(
                smallerMins,
                R.omit<{ [index: string]: number }, string>(oldMinsCoords, mins),
            )

        }
    }
    console.log(R.sum(R.map(x => x + 1, R.values(mins))));

}

main3a()

