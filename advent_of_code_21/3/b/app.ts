import * as R from "ramda";

async function main3a(): Promise<void> {

    let data: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

        ;
    let oxygenData: string[] = [...data];
    let scrubData: string[] = [...data];
    let oxygenInt: number;
    let scrubInt: number;

    for (let pos = 0; pos < data[0].length; pos++) {
        if (!oxygenInt) {
            let res: string = R.pipe(
                R.map((items: string): string => items.charAt(pos)),
                R.countBy(R.toLower),
                R.toPairs,
                pair => pair.length == 1 ? pair[0][0] : pair[0][1] == pair[1][1] ? '1' : pair[0][1] > pair[1][1] ? pair[0][0] : pair[1][0]
            )(oxygenData);

            oxygenData = R.filter(x => x[pos] == res, oxygenData);

            if (oxygenData && oxygenData.length == 1) {
                oxygenInt = parseInt(oxygenData[0], 2);
            }
        }
        if (!scrubInt) {
            let res: string = R.pipe(
                R.map((items: string): string => items.charAt(pos)),
                R.countBy(R.toLower),
                R.toPairs,
                pair => pair.length == 1 ? pair[0][0] : pair[0][1] == pair[1][1] ? '0' : pair[0][1] < pair[1][1] ? pair[0][0] : pair[1][0]
            )(scrubData);

            scrubData = R.filter(x => x[pos] == res, scrubData);

            if (scrubData && scrubData.length == 1) {
                scrubInt = parseInt(scrubData[0], 2);
            }
        }

        if (scrubInt && oxygenInt) break;
    }

    console.log("Solution = ", oxygenInt * scrubInt);
}

main3a()