import * as R from "ramda";

async function main3a(): Promise<void> {
    let data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    R.pipe(
        (x: string[]) => x[0],
        R.split(','),
        R.map(parseInt),
        (x: number[]) => {
            return {
                'input': x,
                'cnt': 0,
                'max': R.reduce(R.max, -Infinity, x),
                'fuel': []
            }
        },
        R.until(
            (x: any) => x['cnt'] > x['max'],
            x => {
                x['fuel'].push(R.sum(R.map(el => Math.abs(el - x['cnt']), x['input'])));
                x['cnt']++;
                return x;}
        ),
        (x: any) => R.reduce(R.min, Infinity, x['fuel']),
        console.log
        

    )(data)

}

main3a()