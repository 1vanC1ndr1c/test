async function main1b(): Promise<void> {
    let numberArray: number[] = (await fetch('input.txt')
        .then(response => { return response.text() })
    ).split("\n").map(Number)

    let previousSum: number = numberArray.slice(0, 3).reduce((a, b) => a + b, 0);
    let biggerCounter: number = 0;
    numberArray = numberArray.slice(1);
    for (let index = 0; index < numberArray.length; index++) {
        let currentSum: number = numberArray.slice(index, index + 3).reduce((a, b) => a + b, 0);
        if (currentSum > previousSum) biggerCounter++;
        previousSum = currentSum;
    }
    console.log(biggerCounter);
}
main1b()