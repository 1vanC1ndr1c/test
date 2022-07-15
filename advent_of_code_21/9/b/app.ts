import * as R from "ramda";


type coordsValues = { [index: string]: number };

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

    let mins: coordsValues = {};
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

            const neighborElements: coordsValues = R.fromPairs<number>(
                R.map<[number, number], [string, number]>(
                    (coord: [number, number]) => [coord.toString(), numberField[coord[1]][coord[0]]],
                    neighborElementsCoords
                )
            );

            const minNeighborVal: number = R.reduce<number, number>(R.min, Infinity, R.values<coordsValues, string>(neighborElements));

            if (minNeighborVal != elVal) continue;

            mins[[x, y].toString()] = elVal;

            const oldMinsCoords: string[] = R.intersection<string>(
                R.map<[number, number], string>(x => x.toString(), neighborElementsCoords),
                R.keys<coordsValues>(mins) as string[],
            );

            let smallerMins: coordsValues = R.pipe<string[][], Array<[string, number]>, Array<[string, number]>, coordsValues>(
                R.map((coord: string) => [coord, mins[coord]]),
                R.reject((x: any) => mins[x[0]] > elVal),
                R.fromPairs
            )(oldMinsCoords as string[]);

            mins = R.mergeRight<coordsValues, coordsValues>(
                smallerMins,
                R.omit<coordsValues, string>(oldMinsCoords, mins),
            )

        }
    }
    console.log(
        R.pipe<[coordsValues], string[], coordsValues[], number[], number[], number[], number>(
            R.keys,
            R.map<string, coordsValues>((key: string) => _getNeighbors(key, numberField, {})),
            R.map<coordsValues, number>((coll: coordsValues) => R.keys(coll).length),
            R.sort<number>((a: number, b: number) => b - a),
            R.slice(0, 3),
            R.product
        )(mins)
    );
}

function _getNeighbors(key: string, coll: number[][], neighborVals: coordsValues): coordsValues {
    const coords: string[] = key.split(',');
    const x: number = parseInt(coords[0]);
    const y: number = parseInt(coords[1]);

    if (!(0 <= y && y < coll.length) || !(0 <= x && x < coll[0].length))
        return neighborVals;

    if (R.keys(neighborVals).includes(key) || coll[y][x] == 9)
        return neighborVals;

    neighborVals[key] = coll[y][x];

    neighborVals = R.mergeRight<coordsValues, coordsValues>(_getNeighbors([x - 1, y].toString(), coll, neighborVals), neighborVals);
    neighborVals = R.mergeRight<coordsValues, coordsValues>(_getNeighbors([x + 1, y].toString(), coll, neighborVals), neighborVals);
    neighborVals = R.mergeRight<coordsValues, coordsValues>(_getNeighbors([x, y - 1].toString(), coll, neighborVals), neighborVals);
    neighborVals = R.mergeRight<coordsValues, coordsValues>(_getNeighbors([x, y + 1].toString(), coll, neighborVals), neighborVals);

    return neighborVals;
}

main3a()

