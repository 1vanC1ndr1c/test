async function main2b(): Promise<void> {
    let rows: string[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n")

    let hPos: number = 0;
    let vPos: number = 0;
    let aim: number = 0;

    for (let row of rows) {
        const [direction, valueStr] = row.split(' ');
        const value: number = parseInt(valueStr);

        if (direction == 'forward') {
            hPos += value;
            vPos += aim * value;
        } else if (direction == 'down') {
            aim += value;
        } else if (direction == 'up') {
            aim -= value;
        }
    }
    console.log(hPos, vPos);
    console.log(hPos * vPos);
}

main2b()