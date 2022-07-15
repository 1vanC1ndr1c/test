import * as R from "ramda";

async function main3a(): Promise<void> {
    let data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    console.log(
        R.pipe(
            R.map(R.split('->')),
            R.map(R.map(R.split(','))),
            R.map(R.map(R.map(R.pipe(R.trim, parseInt)))),
            R.map(doubleArray => {
                const x0 = doubleArray[0][0];
                const x1 = doubleArray[1][0];
                const y0 = doubleArray[0][1];
                const y1 = doubleArray[1][1];
                let xRange = x0 < x1 ? R.range(x0, x1 + 1) : R.reverse(R.range(x1, x0 + 1));
                let yRange = y0 < y1 ? R.range(y0, y1 + 1) : R.reverse(R.range(y1, y0 + 1));
                if (xRange.length > yRange.length) yRange = new Array(xRange.length).fill(yRange[0]);
                else if (xRange.length < yRange.length) xRange = new Array(yRange.length).fill(xRange[0]);
                return [xRange, yRange];
            }),
            //For now, only consider horizontal and vertical lines
            R.filter((el: any[][]) => R.all(R.equals(el[0][0]), el[0]) || R.all(R.equals(el[1][0]), el[1])),
            (ranges: any) => Array.from(ranges.entries()),
            R.map((rangeIndexed: any) => [R.zip(rangeIndexed[1][0], rangeIndexed[1][1]), rangeIndexed[0]]),
            R.map((range: any) => [
                R.map(coords => coords[0].toString() + '-' + coords[1].toString(), range[0]),
                new Array(range[0].length).fill(range[1])
            ]),
            R.map((x: any) => R.zip(x[0], x[1])),
            R.unnest,
            R.countBy((x: any) => x[0]),
            R.filter(x => x > 1),
            R.keys,
            R.length
        )(data)
    );
}

main3a()