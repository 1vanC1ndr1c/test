import * as R from "ramda";

async function main3a(): Promise<void> {

    let data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    let gammaStr: string = R.pipe(
        R.map(R.split('')),
        R.transpose,
        R.map(R.countBy(R.toLower)),
        R.map(R.toPairs),
        R.map(R.reduce(R.maxBy(((a: (any)[]) => a[1])), ['_', -1])),
        R.map(x => x[0]),
        R.join('')
    )(data);

    const epsilonInt: number = parseInt(
        R.join('',
            R.map(x => x == '1' ? '0' : '1',
                R.split('', gammaStr)
            )
        ), 2
    );
    const gammaInt: number = parseInt(gammaStr, 2)
    console.log("Solution = ", epsilonInt * gammaInt);

}

main3a()