import * as R from "ramda";
import { Template } from "webpack";

type dataType = { value: number, flashed: boolean };

async function main3a(): Promise<void> {
    const data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    let numberData: number[][] = R.pipe<[string[]], string[][], number[][]>(
        R.map<string, string[]>(R.split('')),
        R.map<string[], number[]>(R.map<string, number>(parseInt)),
    )(data);

    let flashCounter: number = 0;
    let newFlashes: number;
    let cnt = 0;
    while (true) {
        const allZeroes: boolean = R.pipe(
            R.map(R.all(R.equals(0))),
            R.all(R.equals(true))
        )(numberData);
        
        if (allZeroes) {
            console.log(cnt);
            break;
        }
        let formattedData: dataType[][] = R.map<number[], dataType[]>(
            R.map<number, dataType>(
                (el: number) => ({
                    value: R.add(1, el),
                    flashed: false
                }))
        )(numberData);

        [formattedData, newFlashes] = flashNeighbors(formattedData);

        flashCounter += newFlashes;
        numberData = R.map(R.map((x: dataType) => x.value > 9 ? 0 : x.value))(formattedData);
        cnt++;
    }
}
function flashNeighbors(data: dataType[][]): [dataType[][], number] {
    let needsFlashing: boolean = true;
    let newData: dataType[][] = JSON.parse(JSON.stringify(data));
    let internalCount: number = 0;

    while (needsFlashing) {
        needsFlashing = false;
        data = JSON.parse(JSON.stringify(newData));

        const enumeratedData: [number, dataType[]][] = R.addIndex<dataType[], [number, dataType[]]>(R.map)(
            (val: dataType[], index: number) => [index, val], data);
        for (let [y, row] of enumeratedData) {

            const enumeratedRow: [number, dataType][] = R.addIndex<dataType, [number, dataType]>(R.map)(
                (val: dataType, index: number) => [index, val], row);
            for (let [x, el] of enumeratedRow) {
                if (el.value <= 9 || el.flashed) continue;

                internalCount++;
                newData[y][x].flashed = true;
                needsFlashing = true;

                const neighborCoords: [number, number][] = R.filter<[number, number], [number, number][]>(
                    (el: [number, number]) => (
                        (el[0] > -1 && el[0] < row.length)
                        &&
                        (el[1] > -1 && el[1] < data.length)
                    ),
                    R.xprod<number, number>(R.range(x - 1, x + 2), R.range(y - 1, y + 2)),
                );

                for (let coord of neighborCoords)
                    newData[coord[1]][coord[0]].value++;
            }
        }
    }
    return [data, internalCount]
}

main3a()

