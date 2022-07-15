import * as R from "ramda";

async function main3a(): Promise<void> {
    let data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    R.pipe(
        R.map(R.split('|')),
        R.map(R.map(R.split(' '))),
        R.map(x => x[1]),
        R.map(R.map(x => R.length(x))),
        R.map(R.filter((x: number) => [2, 3, 4, 7].includes(x))),
        R.map(R.length),
        R.sum,
        console.log
    )(data)

}

main3a()