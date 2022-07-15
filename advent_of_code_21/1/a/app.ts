async function main1a(): Promise<void> {
    let numberArray: number[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n").map(Number)

    let largerCounter: number = 0;
    let previousValue = numberArray[0];

    for (let currentValue of numberArray) {
        if (currentValue > previousValue) largerCounter++;
        previousValue = currentValue;
    }

    console.log(largerCounter);

}

main1a()