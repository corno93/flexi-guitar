const instruments = {
    'guitar-electric': {
        'D#3': 'Ds3.[mp3|ogg]',
        'D#4': 'Ds4.[mp3|ogg]',
        'D#5': 'Ds5.[mp3|ogg]',
        'E2': 'E2.[mp3|ogg]',
        'F#2': 'Fs2.[mp3|ogg]',
        'F#3': 'Fs3.[mp3|ogg]',
        'F#4': 'Fs4.[mp3|ogg]',
        'F#5': 'Fs5.[mp3|ogg]',
        'A2': 'A2.[mp3|ogg]',
        'A3': 'A3.[mp3|ogg]',
        'A4': 'A4.[mp3|ogg]',
        'A5': 'A5.[mp3|ogg]',
        'C3': 'C3.[mp3|ogg]',
        'C4': 'C4.[mp3|ogg]',
        'C5': 'C5.[mp3|ogg]',
        'C6': 'C6.[mp3|ogg]',
        'C#2': 'Cs2.[mp3|ogg]'
    }
};

const Instruments = {
    handle: () => {
        const sampler = new Tone.Sampler({
            urls:{
                'D#3': 'Ds3.[mp3|ogg]',
                'D#4': 'Ds4.[mp3|ogg]',
            },
            baseUrl: "https://nbrosowsky.github.io/tonejs-instruments/samples/guitar-electric/",
            onload: () => {
                // sampler.triggerAttackRelease(["C1", "E1", "G1", "B1"], 0.5);
                sampler.release = 0.5;
                sampler.toMaster();
            }
        });
        return sampler;
    }
}

