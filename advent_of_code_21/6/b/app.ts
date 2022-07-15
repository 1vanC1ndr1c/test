import * as R from "ramda";

async function main3a(): Promise<void> {
    let data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    console.log(
        R.pipe(
            (x: string[]) => x[0],
            R.split(','),
            R.map(parseInt),
            R.countBy((x: number) => x),
            R.curry(Object.assign)({ 0: 0, 6: 0, 7: 0, 8: 0, 'cnt': 256 }),
            R.until(
                (x: { [key: (number | string)]: number }) => x['cnt'] == 0,
                (x: { [key: (number | string)]: number }) => {
                    const y: {} = {
                        0: x[1],
                        1: x[2],
                        2: x[3],
                        3: x[4],
                        4: x[5],
                        5: x[6],
                        6: x[7] + x[0],
                        7: x[8],
                        8: x[0],
                        'cnt': x['cnt'] - 1
                    };
                    return y;
                }),
            R.values,
            R.sum,
        )(data));

}

main3a()