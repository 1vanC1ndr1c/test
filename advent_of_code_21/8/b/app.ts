import * as R from "ramda";

async function main3a(): Promise<void> {
    let data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    const getOneFourSevenEight = (nmb: number, input: string[]) => R.sort(
        (a: string, b: string) => a.localeCompare(b),
        R.split('', R.join('', R.filter((x: any) => x.length == nmb, input)))
    )
    const getRest = (comparator: any, input: string[]) => R.sort(
        (a: string, b: string) => a.localeCompare(b),
        R.split('', R.join('', R.filter(comparator, input)))
    )

    R.pipe(
        R.map(R.split('|')),
        R.map(R.map(R.split(' '))),
        R.map(R.map(R.filter((x: any) => x != ''))),
        R.map((input: any) => ({ 'input': input[0], 'output': input[1] })),
        R.map((obj: any) => R.mergeRight(obj, {
            1: getOneFourSevenEight(2, obj['input']),
            4: getOneFourSevenEight(4, obj['input']),
            7: getOneFourSevenEight(3, obj['input']),
            8: getOneFourSevenEight(7, obj['input']),
        }
        )),
        R.map((obj: any) => R.mergeRight(obj, {
            9: getRest(
                (x: string) =>
                    x.length == 6
                    && R.difference(obj[4], R.split('', x)).length == 0,
                obj['input']),
            0: getRest(
                (x: string) =>
                    x.length == 6
                    && R.difference(obj[7], R.split('', x)).length == 0
                    && R.difference(obj[4], R.split('', x)).length != 0,
                obj['input']),
            6: getRest(
                (x: string) =>
                    x.length == 6
                    && R.difference(obj[7], R.split('', x)).length != 0
                    && R.difference(obj[4], R.split('', x)).length != 0,
                obj['input'])
        })),
        R.map((obj: any) => R.mergeRight(obj, {
            5: getRest(
                (x: string) =>
                    x.length == 5
                    && R.difference(R.split('', x), obj[6]).length == 0,
                obj['input']),
            3: getRest(
                (x: string) =>
                    x.length == 5
                    && R.difference(R.split('', x), obj[9]).length == 0
                    && R.difference(R.split('', x), obj[6]).length != 0,
                obj['input']),
            2: getRest(
                (x: any) =>
                    x.length == 5
                    && R.difference(R.split('', x), obj[9]).length != 0
                    && R.difference(R.split('', x), obj[6]).length != 0,
                obj['input'])
        })),
        R.map(R.omit(['input'])),
        R.map((obj: any) => R.mergeRight(
            R.pick(['output'], obj),
            R.invertObj(R.omit(['output'], obj))
        )),
        R.map((obj: any) => R.mergeRight(
            obj,
            {
                'output': R.map(
                    el => R.sort((a: string, b: string) => a.localeCompare(b), R.split('', el)),
                    obj['output'])
            }
        )),
        R.map((obj: any) => R.map(el => obj[el], obj['output'])),
        R.map(R.join('')),
        R.sum,
        console.log
    )(data)

}

main3a()